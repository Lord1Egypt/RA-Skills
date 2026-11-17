#!/usr/bin/env python3
"""
scripts/capability_compensator.py — 外部依赖能力代偿编排器（M0.2.5）

解决"能力间代偿"缺口：当某能力族整体失效时，沿注册表 degrade_to 链
做**语义替代**（而非仅能力内引擎轮换）。

与 engine_lifecycle 协同：
  - lifecycle 管"单引擎健康"（record_success/record_failure/classify）
  - compensator 管"能力族替代"（沿 degrade_to 选下一个可用能力）
  - 每个被尝试的能力仍经 lifecycle 记录健康，保证自愈闭环

API：
  compensate(cap_name, handlers, *args, **kwargs)
      handlers: {cap_name: callable(*args, **kwargs) -> result}
      返回 CompensateResult(result, used, trail, exhausted)
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Tuple

try:  # G1：统一包路径优先；scripts/ 直接注入 core/ 时回退顶层（同一模块对象）
    from core.capability_registry import (
        degrade_chain, get_capability, is_effective_enabled,
    )
except Exception:  # pragma: no cover - 部署形态差异
    from capability_registry import (
        degrade_chain, get_capability, is_effective_enabled,
    )

log = logging.getLogger("infoseek.capability_compensator")

# 延迟导入避免循环；运行时再取生命周期单例
def _get_lifecycle():
    try:
        from engine_lifecycle import get_lifecycle
        return get_lifecycle()
    except Exception:
        return None


def _boundary_preflight(cap_name: str):
    """GA12：边界门控预检。门控关闭 / 模块异常 / 导入失败 → None（调用方按放行处理）。"""
    try:
        import os
        if os.environ.get("INFOSEEK_BOUNDARY_GATE", "").lower() not in \
                ("1", "true", "on", "yes"):
            return None
        from boundary_gate import preflight
        return preflight(cap_name)
    except Exception:
        return None  # fail-open：边界治理自身故障不得阻断主调研链


@dataclass
class CompensateResult:
    result: object = None
    used: Optional[str] = None           # 实际生效的能力
    trail: List[Tuple[str, str]] = field(default_factory=list)  # [(cap, status), ...]
    exhausted: bool = False              # 整条链均失败/不可用
    gap_flag: bool = False               # 是否标记为"能力缺口"（需人工核实）
    boundary_restricted: bool = False    # GA12：是否有能力因网络边界被门控降级


def compensate(cap_name: str,
               handlers: Dict[str, Callable],
               *args,
               **kwargs) -> CompensateResult:
    """沿 degrade_to 链选第一个有效可用且能成功返回的能力。

    - 跳过未启用（含未授权 consent）的能力
    - 跳过无 handler 的能力（声明存在但代码未实现）
    - 每个尝试经 lifecycle 记录健康；异常视为该能力失败，继续链
    - 末端 manual_review（graceful_fallback）始终"成功"返回缺口标记
    """
    lc = _get_lifecycle()
    chain = degrade_chain(cap_name)
    out = CompensateResult()
    attempted = []

    for name in chain:
        cap = get_capability(name)
        kind = cap.get("kind") if cap else None

        # 1) 启用判定（含 consent）
        if not is_effective_enabled(name):
            out.trail.append((name, "skipped_disabled"))
            attempted.append(name)
            continue
        # 2) handler 存在判定
        fn = handlers.get(name)
        if fn is None:
            # G6：末端 graceful_fallback 无 handler 时内置默认，
            # 保证「缺口必被显式标记」（而非静默丢失 gap_flag）。
            if kind == "graceful_fallback":
                out.trail.append((name, "ok"))
                out.result = [{
                    "platform": "(需人工核实)", "url": "",
                    "username": str(args[0]) if args else "",
                    "confidence": 0.0, "source": name, "_gap": True,
                }]
                out.used = name
                out.gap_flag = True
                return out
            out.trail.append((name, "no_handler"))
            attempted.append(name)
            continue

        # 2.5) GA12 网络边界预检（门控默认 OFF ⇒ 恒跳过，零行为变更）
        #   开启后（INFOSEEK_BOUNDARY_GATE=1）：必需 host 不可达 → 显式降级，
        #   不静默长超时；预检自身异常 fail-open（不阻断主链）。
        pre = _boundary_preflight(name)
        if pre is not None and not pre.get("allowed", True):
            out.boundary_restricted = True
            unreach = ",".join(pre.get("unreachable", [])[:3])
            out.trail.append((name, f"boundary_restricted:{unreach}" if unreach
                              else "boundary_restricted"))
            attempted.append(name)
            log.info(f"[代偿] 能力 '{name}' 网络边界受限（{unreach}），显式降级")
            continue

        attempted.append(name)
        try:
            res = fn(*args, **kwargs)
            if lc:
                lc.record_success(name, res)
            out.trail.append((name, "ok"))
            out.result = res
            out.used = name
            # graceful_fallback 末端：标记为能力缺口（非真实数据）
            if kind == "graceful_fallback":
                out.gap_flag = True
            return out
        except Exception as e:
            if lc:
                lc.record_failure(name, e)
            log.warning(f"[代偿] 能力 '{name}' 失败，尝试下一替代: {e}")
            out.trail.append((name, f"fail:{type(e).__name__}"))

    out.exhausted = bool(attempted)  # 至少尝试过即视为已耗尽链
    if not attempted:
        out.exhausted = True
    return out


def audit_trail(result: CompensateResult) -> str:
    """生成代偿审计串（写入 audit.log）。"""
    parts = " → ".join(f"{c}[{s}]" for c, s in result.trail)
    return (f"capability_compensate used={result.used} "
            f"exhausted={result.exhausted} gap={result.gap_flag} "
            f"trail=({parts})")
