#!/usr/bin/env python3
"""metrics.py — 指标定义（可选增强层 L2）。

为什么是"可选"：
    录像已经能保证"每个数字都有 SQL 可查"（L1 保底）。
    但账本里只有「合计 n17」这种流水账，客户看不懂、跨报告也对不上。
    写一份 metrics.yaml，就是给这些数字一个**稳定身份**（L2）。

怎么用：
    # metrics.yaml 放项目根
    metrics:
      - id: ship.amt_net
        label: 净发货额
        unit: 元
        caliber: 含税金额，扣退货
        match_sql: "sum(amt_tax)"        # 用来认领录像里的 SQL（子串匹配）

认领规则：SQL 归一化后包含 match_sql 就算命中。
**它不定义 SQL，只给已经跑过的 SQL 贴标签** —— 所以不写也能跑。
"""
from __future__ import annotations

import re
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

METRICS_NAME = "metrics.yaml"
ALLOWED_KEYS = {"id", "label", "unit", "caliber", "match_sql", "role", "note"}


class MetricsError(Exception):
    pass


def _norm(sql: str) -> str:
    return re.sub(r"\s+", " ", str(sql or "")).strip().lower()


def load(path: str | Path | None = None) -> dict:
    """加载 metrics.yaml。找不到就返回空定义（不影响主流程）。"""
    if not path:
        return {"metrics": [], "_source": None}
    p = Path(path)
    if not p.exists():
        raise MetricsError(f"metrics 文件不存在：{p}")
    if yaml is None:
        raise MetricsError("缺 pyyaml")
    try:
        raw = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as e:
        raise MetricsError(f"{p.name} YAML 解析失败：{e}") from e
    items = raw.get("metrics")
    if not isinstance(items, list):
        raise MetricsError(f"{p.name} 里应该有 metrics: [ ... ] 列表")

    seen = set()
    for i, m in enumerate(items):
        if not isinstance(m, dict):
            raise MetricsError(f"{p.name} 第 {i+1} 条不是映射")
        unknown = set(m) - ALLOWED_KEYS
        if unknown:
            raise MetricsError(
                f"{p.name} 第 {i+1} 条有未知键 {sorted(unknown)}；"
                f"允许的：{sorted(ALLOWED_KEYS)}")
        for k in ("id", "label", "match_sql"):
            if not m.get(k):
                raise MetricsError(f"{p.name} 第 {i+1} 条缺 {k}")
        if m["id"] in seen:
            raise MetricsError(f"{p.name}：id 重复 {m['id']}")
        seen.add(m["id"])
    return {"metrics": items, "_source": str(p)}


def claim(sql: str, defs: dict) -> dict | None:
    """给一条 SQL 认领一个指标定义。命中多条时取 match_sql 最长的（最具体）。"""
    s = _norm(sql)
    hits = [m for m in defs.get("metrics", []) if _norm(m["match_sql"]) in s]
    if not hits:
        return None
    return max(hits, key=lambda m: len(_norm(m["match_sql"])))


def apply_claim(numbers: list[dict], defs: dict) -> int:
    """给账本条目打上 metric_id / label / unit / caliber。返回命中条数。"""
    n = 0
    for num in numbers:
        sql = num.get("sql")
        if not sql:
            continue
        m = claim(sql, defs)
        if not m:
            continue
        num["metric_id"] = m["id"]
        num["label"] = m.get("label") or num.get("label")
        if m.get("unit"):
            num["unit"] = m["unit"]
        if m.get("caliber"):
            num["caliber"] = m["caliber"]
        if m.get("role"):
            num["role"] = m["role"]
        n += 1
    return n
