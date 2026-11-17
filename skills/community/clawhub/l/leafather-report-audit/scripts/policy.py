#!/usr/bin/env python3
"""policy.py — 审计策略（配置化，可版本化，拼错就报错）。

为什么要有它：
    容差、舍入、locale 这些东西一旦硬编码在代码里，就变成了隐式假设。
    v3.0 就栽在这：0.5% 相对容差让"30 万改错 32"判通过。
    现在把它们写成一份你能看见、能版本化、能 diff 的文件。

设计原则（抄自 groundlens）：
    * 未知键 = 错误，不静默忽略（拼错的规则不能悄悄不生效）
    * 策略哈希进审计结论（每个判决能追到"当时用的是哪套规则"）
"""
from __future__ import annotations

import hashlib
import json
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

try:
    import yaml
except ImportError as e:  # pragma: no cover
    raise SystemExit("❌ 缺 pyyaml（pip install pyyaml）") from e

POLICY_NAME = "policy.yaml"

DEFAULTS = {
    "version": "1.0",
    "numeric": {
        "rounding": "within_last_digit",   # half_up | half_even | within_last_digit
        "tol_abbrev": 500,                 # 报告写「1.5万」这类缩写时的容差（绝对值）
        "tol_abs": 0.5,                    # 无法判断精度时的兜底绝对容差
    },
    "verdict": {
        "fail": ["ledger_mismatch", "unmatched_number", "precision_mismatch"],
        "review": ["not_recomputed", "unverifiable_entry", "unscanned_image",
                   "ambiguous_number", "weak_anchor", "cross_file_mismatch",
                   "must_missing", "leak",
                   # 2026-10-26（方案 A）：没有可查的东西 ≠ 全都查过了
                   "no_metric", "low_coverage"],
    },
    # 2026-10-26（方案 A）：覆盖率闸门
    # 背景：判"这数字要不要追"靠词表，词表外的说法会被判杂项豁免。
    # 实测：同一份报告只把"总行数"改成"样本池规模"，4 个数字全部被豁免，结论照样 ✅ 通过。
    # 所以结论必须报"实际审了多少"，审得太少就不许说通过。
    "coverage": {
        "min_ratio": 0.9,      # 追溯到的 / 应审的，低于此 → 至少「需人工复核」
        "min_metric": 1,       # 判定为指标的数字少于这个数（而报告里明明有像数据的数字）→ 至少「需人工复核」
    },
    "checks": {
        "must": [],                        # 必现指标 metric_id（每个交付件都得有）
        "leak_patterns": ["*客户版*", "*客户*", "*client*"],   # 视为客户版的文件
        # 默认带 3 条"几乎对所有行业都成立、误报率低"的规则；
        # 行业特有的敏感词请自己加。15 位以上才算 ID，避免把金额当成 ID。
        "leak_rules": [
            {"name": "长数字ID", "regex": r"\b\d{15,}\b"},
            {"name": "内部字样", "regex": r"内部|内部稿|内部备注|严禁外传|机密|勿外传"},
            {"name": "邮箱", "regex": r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"},
        ],
    },
    "strict": "error",                     # error | warn（未知键怎么处理）
}

# 允许的键（任何不在这里的键 → 报错）
ALLOWED = {
    "version": set(),
    "numeric": {"rounding", "tol_abbrev", "tol_abs"},
    "verdict": {"fail", "review"},
    "coverage": {"min_ratio", "min_metric"},
    "checks": {"must", "leak_patterns", "leak_rules"},
    "strict": set(),
}

ROUNDINGS = {"half_up", "half_even", "within_last_digit"}

# 拼错时的提示用
_HINTS = {
    "round": "rounding", "roundings": "rounding", "tolerance": "tol_abs",
    "tol": "tol_abs", "tolerence": "tol_abs", "locales": None,
    "fails": "fail", "reviews": "review", "strict_mode": "strict",
}


class PolicyError(Exception):
    """策略文件有问题。对应退出码 2（未就绪）—— 不算通过。"""


def _check_keys(cfg: dict, path: Path) -> None:
    for k in cfg:
        if k not in ALLOWED:
            hint = _HINTS.get(k)
            msg = f"{path.name}：未知键 {k!r}"
            if hint:
                msg += f"（是不是想写 {hint!r}？）"
            raise PolicyError(msg + f"。允许的键：{', '.join(sorted(ALLOWED))}")
    for section, allowed in ALLOWED.items():
        if section in cfg and isinstance(cfg[section], dict):
            for k in cfg[section]:
                if k not in allowed:
                    raise PolicyError(
                        f"{path.name}：{section}.{k!r} 不是有效键。"
                        f"允许的：{', '.join(sorted(allowed))}")


def _merge(base: dict, over: dict) -> dict:
    out = json.loads(json.dumps(base))
    for k, v in over.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _merge(out[k], v)
        else:
            out[k] = v
    return out


def load(path: str | Path | None = None) -> dict:
    """加载策略：默认值 + 文件覆盖。返回 dict（含 _hash）。"""
    cfg = json.loads(json.dumps(DEFAULTS))
    src = None
    if path:
        p = Path(path)
        if not p.exists():
            raise PolicyError(f"策略文件不存在：{p}")
        try:
            raw = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError as e:
            raise PolicyError(f"{p.name} YAML 解析失败：{e}") from e
        if not isinstance(raw, dict):
            raise PolicyError(f"{p.name} 顶层必须是映射（key: value）")
        _check_keys(raw, p)
        cfg = _merge(cfg, raw)
        src = str(p)
    # 取值校验
    r = cfg["numeric"]["rounding"]
    if r not in ROUNDINGS:
        raise PolicyError(f"numeric.rounding 只能是 {sorted(ROUNDINGS)}，当前 {r!r}")
    if cfg["strict"] not in ("error", "warn"):
        raise PolicyError(f"strict 只能是 error / warn，当前 {cfg['strict']!r}")
    cfg["_source"] = src
    cfg["_hash"] = hashlib.sha256(
        json.dumps({k: v for k, v in cfg.items() if not k.startswith("_")},
                   sort_keys=True, ensure_ascii=False).encode()
    ).hexdigest()[:12]
    return cfg


# ------------------------------------------------------------------ 数字比较
def decimals(raw: str) -> int:
    """报告里这个数字写了几位小数。/ -1 表示用了 万/亿/千 缩写（精度损失大）。"""
    s = (raw or "").replace(",", "").replace("，", "").rstrip("%％")
    if any(u in s for u in ("万", "亿", "千")):
        return -1
    return len(s.split(".")[1]) if "." in s else 0


def _round(x: float, d: int, mode: str) -> float:
    if mode == "half_even":
        return round(x, d)
    q = Decimal(1).scaleb(-d)
    return float(Decimal(str(x)).quantize(q, rounding=ROUND_HALF_UP))


def close(raw: str, a: float, b: float, pol: dict) -> bool:
    """报告里的数 a 与账本里的数 b 是否一致。

    容差由**报告怎么写**决定：写 301,600 就必须等于 301600；
    写 73.9% 才允许在最后一位上舍入。绝不按数值大小放宽。
    """
    num = pol["numeric"]
    d = decimals(raw)
    if d < 0:
        return abs(a - b) <= float(num["tol_abbrev"])
    mode = num["rounding"]
    if mode == "within_last_digit":
        # d=0 是"明确的整数"，不是"无法判断精度" → 必须精确比，不能用兜底容差。
        # （2026-10-25 修：原来 d=0 时用 tol_abs=0.5，导致 28 和 27.8 判相等、
        #   84% 和 84 场景数判相等 —— 又一处"兜底宽容"变成误配来源。）
        tol = 0.5 * (10 ** (-d)) if d > 0 else 0.0
        return abs(a - b) <= tol + 1e-9
    return abs(_round(a, d, mode) - _round(b, d, mode)) < 1e-9


def close_ledger(actual: float, expect: float, pol: dict) -> bool:
    """复算值 vs 账本值：按账本值自身精度比（账本可能被四舍五入过）。"""
    e = float(expect)
    s = repr(e)
    d = len(s.split(".")[1]) if ("." in s and "e" not in s) else 0
    if d <= 0:
        return abs(float(actual) - e) < 1e-9
    tol = 0.5 * (10 ** (-d))
    return abs(float(actual) - e) <= tol + 1e-9


# ------------------------------------------------------------------ 判决
def decide(fail_items: list, review_items: list, pol: dict) -> tuple[str, int]:
    """把证据转成判决。返回 (verdict, exit_code)。"""
    if fail_items:
        return "❌ 不通过", 1
    if review_items:
        return "⚠️ 需人工复核", 3
    return "✅ 通过", 0
