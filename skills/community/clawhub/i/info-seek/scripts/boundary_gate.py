#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/boundary_gate.py — Infoseek 网络边界门控（GA12 / v2.0.0）

把「能力声明的网络边界」与「实测 host 可达性」对齐：
  - check_declared(cap)   纯静态校验（零网络）：声明完整性/枚举合法/host 非空规则
  - available(cap, ...)   实测：按 requires_hosts 探测（TTL 缓存），任一必需 host 不可达即受限
  - preflight(cap, ...)   执行前门控：默认 OFF（INFOSEEK_BOUNDARY_GATE 未开 → 恒放行），
                          开启后不可达则显式返回 restricted 决定，调用方据此走 degrade_to
  - restricted_report()   汇总所有受限能力/host，渲染 references/network-boundary-report.md

设计铁律（P3 简报 §2.3）：
  - 不绕过网络边界；不把受限能力伪装为可用（显式 restricted + 留痕）；
  - 门控默认 OFF ⇒ 既有行为零变更；
  - fail-open：本模块自身异常时 preflight 恒放行（边界治理不得阻断主调研链）。

零第三方硬依赖（host 探测委托 scripts/net_probe.py）。
"""

from __future__ import annotations

import os
import sys
import time
from typing import Dict, List, Optional

# 脚本直接执行时自举路径（scripts/ 与仓库根）
_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
_ROOT_DIR = os.path.dirname(_SCRIPTS_DIR)
for _p in (_ROOT_DIR, _SCRIPTS_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)

try:  # 统一包路径，避免双模块状态分裂
    from core import capability_registry as _reg
except Exception:  # scripts/ 直接注入路径时
    import capability_registry as _reg  # type: ignore

try:
    from net_probe import check_hosts  # type: ignore
except Exception:
    try:
        from scripts.net_probe import check_hosts  # type: ignore
    except Exception:
        check_hosts = None  # fail-open 兜底


GATE_ENV = "INFOSEEK_BOUNDARY_GATE"
_VALID_BOUNDARIES = ("open", "sandbox_restricted", "local")


def gate_enabled() -> bool:
    """门控总开关，默认 OFF。"""
    return os.environ.get(GATE_ENV, "").lower() in ("1", "true", "on", "yes")


# ═══════════════════════════════════════════════════════════
# ① 静态声明校验（零网络）
# ═══════════════════════════════════════════════════════════

def check_declared(cap_name: str) -> Dict:
    """校验单能力的网络边界声明完整性（不发任何网络请求）。

    返回 {"cap", "ok", "issues": [...], "boundary", "hosts"}。
    """
    issues: List[str] = []
    cap = _reg.get_capability(cap_name)
    if not cap:
        return {"cap": cap_name, "ok": False, "issues": ["capability_not_found"],
                "boundary": None, "hosts": []}
    boundary = cap.get("network_boundary")
    hosts = list(cap.get("requires_hosts") or [])
    if boundary is None:
        issues.append("missing_network_boundary")
    elif boundary not in _VALID_BOUNDARIES:
        issues.append(f"invalid_network_boundary:{boundary}")
    if "requires_hosts" not in cap:
        issues.append("missing_requires_hosts")
    # 声明受限却无 host：无法实测，属声明不完整（local/open 允许空）
    if boundary == "sandbox_restricted" and not hosts:
        issues.append("restricted_without_hosts")
    # 声明 local 却挂了 host：语义矛盾
    if boundary == "local" and hosts:
        issues.append("local_with_hosts")
    return {"cap": cap_name, "ok": not issues, "issues": issues,
            "boundary": boundary, "hosts": hosts}


def check_all_declared() -> List[Dict]:
    """全量声明校验（供测试 / 报告 / CI 用）。"""
    return [check_declared(c["name"]) for c in _reg.list_capabilities()]


# ═══════════════════════════════════════════════════════════
# ② 实测可达性
# ═══════════════════════════════════════════════════════════

def available(cap_name: str, timeout: float = 5.0, *,
              force: bool = False, probe=None) -> Dict:
    """按 requires_hosts 实测能力是否可运行。

    - local：无 host 依赖，恒可用；
    - open / sandbox_restricted 且有 host：所有必需 host 均可达才 available=True；
    - open 且未声明 host：无法实测，保守判 available=True（fail-open）。

    probe 可注入（测试 mock），签名同 net_probe.check_hosts。
    返回 {"cap","available","status","unreachable":[...],"results":{...},"issues":[...]}。
    """
    declared = check_declared(cap_name)
    cap = _reg.get_capability(cap_name)
    boundary = declared["boundary"]
    hosts = declared["hosts"]

    if not cap:
        return {"cap": cap_name, "available": False, "status": "unknown_capability",
                "unreachable": [], "results": {}, "issues": declared["issues"]}
    if boundary == "local":
        return {"cap": cap_name, "available": True, "status": "local",
                "unreachable": [], "results": {}, "issues": declared["issues"]}
    if not hosts:
        # 无 host 可测：不阻断（open 能力的真实端点由其自身健康探测负责）
        return {"cap": cap_name, "available": True, "status": "untested_no_hosts",
                "unreachable": [], "results": {}, "issues": declared["issues"]}

    fn = probe or check_hosts
    if fn is None:
        # 探测设施缺失：fail-open
        return {"cap": cap_name, "available": True, "status": "probe_unavailable",
                "unreachable": [], "results": {}, "issues": declared["issues"]}
    try:
        results = fn(hosts, timeout=timeout, force=force)
    except Exception as e:
        return {"cap": cap_name, "available": True, "status": "probe_error",
                "unreachable": [], "results": {},
                "issues": declared["issues"] + [f"probe_error:{type(e).__name__}"]}

    unreachable = [h for h in hosts if not (results.get(h) or {}).get("ok")]
    status = "available" if not unreachable else "boundary_restricted"
    return {"cap": cap_name, "available": not unreachable, "status": status,
            "unreachable": unreachable, "results": results,
            "issues": declared["issues"]}


# ═══════════════════════════════════════════════════════════
# ③ 执行前门控（默认 OFF / fail-open）
# ═══════════════════════════════════════════════════════════

def preflight(cap_name: str, timeout: float = 5.0, *,
              force: bool = False, probe=None) -> Dict:
    """能力执行前边界门控。

    门控关闭（默认）：{"allowed": True, "gated": False, "status": "gate_off"}，零网络；
    门控开启：实测 host，不可达 → allowed=False / status=boundary_restricted，
              调用方应沿 degrade_to 显式降级；
    任何内部异常：fail-open 放行（status=fail_open），避免边界治理阻断主链。
    """
    if not gate_enabled():
        return {"cap": cap_name, "allowed": True, "gated": False,
                "status": "gate_off", "unreachable": [], "degrade_to":
                list((_reg.get_capability(cap_name) or {}).get("degrade_to") or [])}
    try:
        av = available(cap_name, timeout=timeout, force=force, probe=probe)
        # 探测自身异常（probe_error/probe_unavailable）→ fail-open 归一，
        # 区别于「已确认 host 不可达」的 boundary_restricted
        if av["status"] in ("probe_error", "probe_unavailable"):
            return {"cap": cap_name, "allowed": True, "gated": True,
                    "status": "fail_open", "unreachable": [],
                    "issues": av.get("issues", []),
                    "degrade_to": list((_reg.get_capability(cap_name) or {}).get("degrade_to") or [])}
        allowed = av["available"]
        return {"cap": cap_name, "allowed": allowed, "gated": True,
                "status": av["status"], "unreachable": av["unreachable"],
                "degrade_to": list((_reg.get_capability(cap_name) or {}).get("degrade_to") or [])}
    except Exception as e:  # fail-open
        return {"cap": cap_name, "allowed": True, "gated": True,
                "status": "fail_open", "unreachable": [],
                "error": f"{type(e).__name__}:{e}",
                "degrade_to": list((_reg.get_capability(cap_name) or {}).get("degrade_to") or [])}


# ═══════════════════════════════════════════════════════════
# ④ 受限清单 / 报告
# ═══════════════════════════════════════════════════════════

def restricted_report(timeout: float = 5.0, *, force: bool = False,
                      probe=None) -> Dict:
    """汇总受限能力 + host 台账 + 实测结果（报告生成器消费）。"""
    ledger = _reg.get_network_boundaries()
    caps = []
    for c in _reg.list_capabilities():
        name = c["name"]
        boundary = c.get("network_boundary")
        hosts = list(c.get("requires_hosts") or [])
        caps.append({"cap": name, "boundary": boundary, "hosts": hosts,
                     "declared_restricted": boundary == "sandbox_restricted"})
    # host 实测（仅对声明过的 host 去重探测）
    all_hosts = sorted({h for c in caps for h in c["hosts"]} | set(ledger.keys()))
    fn = probe or check_hosts
    results = {}
    if all_hosts and fn is not None:
        try:
            results = fn(all_hosts, timeout=timeout, force=force)
        except Exception:
            results = {}
    unreachable = sorted(h for h in all_hosts if h in results and not results[h].get("ok"))
    reachable = sorted(h for h in all_hosts if h in results and results[h].get("ok"))
    return {"generated_ts": time.time(), "gate_enabled": gate_enabled(),
            "capabilities": caps, "host_ledger": ledger,
            "probe_results": results, "reachable": reachable,
            "unreachable": unreachable}


def render_report_md(report: Optional[Dict] = None, **kw) -> str:
    """渲染 network-boundary-report.md 文本。"""
    r = report or restricted_report(**kw)
    ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(r.get("generated_ts", time.time())))
    lines = [
        "# Infoseek 网络边界受限清单（GA12）",
        "",
        f"> 生成时间：{ts}｜ 边界门控：{'ON（INFOSEEK_BOUNDARY_GATE=1）' if r['gate_enabled'] else 'OFF（默认，零行为变更）'}",
        "> 定位：声明式网络边界台账 + host 实测证据；**不绕过网络边界，不把受限能力伪装为可用**。",
        "> 用法：目标机重跑 `python scripts/boundary_gate.py --report --force` 刷新，形成「沙箱 vs 目标机」对照。",
        "",
        "## 1. 能力边界声明",
        "",
        "| 能力 | 边界 | 依赖 host |",
        "|---|---|---|",
    ]
    for c in sorted(r["capabilities"], key=lambda x: x["cap"]):
        hosts = ", ".join(c["hosts"]) if c["hosts"] else "—"
        lines.append(f"| {c['cap']} | {c['boundary'] or '（未声明）'} | {hosts} |")

    lines += ["", "## 2. Host 实测台账", "",
              "| Host | 静态边界 | 实测 | 证据 | 消费能力 |",
              "|---|---|---|---|---|"]
    ledger = r["host_ledger"]
    all_hosts = sorted(set(list(ledger.keys())) |
                       {h for c in r["capabilities"] for h in c["hosts"]})
    for h in all_hosts:
        info = ledger.get(h, {})
        pr = r["probe_results"].get(h) or {}
        if pr:
            measured = "❌ 不可达" if not pr.get("ok") else "✅ 可达"
        else:
            measured = "未探测"
        evidence = (info.get("evidence") or "").replace("|", "/")
        used = ", ".join(info.get("used_by") or []) or "—"
        lines.append(f"| {h} | {info.get('boundary', '（未登记）')} | {measured} | {evidence} | {used} |")

    lines += ["",
              f"**实测汇总**：不可达 {len(r['unreachable'])} 个 ｜ 可达 {len(r['reachable'])} 个",
              "",
              "## 3. 受限能力降级路径",
              "",
              "门控开启后，受限能力的执行请求沿注册表 `degrade_to` 链显式降级（默认末端 `manual_review`），",
              "并在代偿 trail 中以 `boundary_restricted` 留痕，绝不静默失败或长超时。",
              "",
              "## 4. 边界原则",
              "",
              "1. 不尝试绕过网络限制（无代理/VPN/反爬对抗）；",
              "2. 不将受限项标记为「通过」（沙箱仅做负向验证，正向可达性由目标机补验）；",
              "3. 不改动既有能力默认开关语义（仅新增声明与门控，门控默认 OFF）。",
              ""]
    return "\n".join(lines)


def write_report(path: Optional[str] = None, *, force: bool = False,
                 timeout: float = 5.0, probe=None) -> str:
    """生成报告并写入 references/network-boundary-report.md，返回路径。"""
    if path is None:
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(root, "references", "network-boundary-report.md")
    md = render_report_md(restricted_report(timeout=timeout, force=force, probe=probe))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(md)
    return path


if __name__ == "__main__":
    import argparse
    import json
    ap = argparse.ArgumentParser(description="infoseek 网络边界门控（GA12）")
    ap.add_argument("--check", action="store_true", help="仅静态声明校验（零网络）")
    ap.add_argument("--available", metavar="CAP", help="实测某能力可达性")
    ap.add_argument("--report", action="store_true", help="生成/刷新受限清单报告")
    ap.add_argument("--force", action="store_true", help="忽略探测缓存")
    ap.add_argument("--timeout", type=float, default=5.0)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.check:
        rows = check_all_declared()
        if args.json:
            print(json.dumps(rows, ensure_ascii=False, indent=2))
        else:
            bad = [r for r in rows if not r["ok"]]
            for r in rows:
                mark = "✅" if r["ok"] else "❌"
                print(f"{mark} {r['cap']:20s} {r['boundary']}  {';'.join(r['issues'])}")
            print(f"\n声明校验：{len(rows)-len(bad)}/{len(rows)} 完整")
    elif args.available:
        print(json.dumps(available(args.available, timeout=args.timeout,
                                   force=args.force), ensure_ascii=False, indent=2))
    elif args.report:
        p = write_report(force=args.force, timeout=args.timeout)
        print(f"报告已写入：{p}")
    else:
        ap.print_help()
