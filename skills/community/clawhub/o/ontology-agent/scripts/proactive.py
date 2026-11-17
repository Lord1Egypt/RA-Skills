#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
proactive.py — 自发行为引擎（Phase 10 新增，零侵入）

职责：
  - grade()：对 monitor.py 写入的每一条信号套用分级（L0 静默 / L1 轻提醒 /
    L2 草拟待确认[默认] / L3 授权内执行），并对照 decision.yaml 红线与 人设D 授权边界
  - compose_brief()：聚合近 N 天的 L1/L2 信号，生成「企业情报简报」，落到 company-memory.md
  - 提供 CLI：--slug --grade (--domain --title ...) / --brief [--days]

复用 decision.yaml 的 PII/合规红线与 人设D 授权边界；不修改核心文件。
"""
import os
import re
import sqlite3
import argparse
from datetime import datetime, timedelta

try:
    import yaml
except ImportError:
    yaml = None

HERE = os.path.dirname(os.path.abspath(__file__))
REFERENCES = os.path.join(os.path.dirname(HERE), "references")
sys_path = HERE
import sys
sys.path.insert(0, sys_path)
from monitor import load_instance, db_path, ensure_signals  # noqa: E402


def slugify(text):
    s = re.sub(r"[^0-9a-zA-Z]+", "-", text or "").strip("-").lower()
    return s or "company"


def load_proactive():
    if not yaml:
        raise RuntimeError("需要 PyYAML：pip install pyyaml")
    p = os.path.join(REFERENCES, "proactive.yaml")
    with open(p, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _block_list():
    cfg = load_proactive().get("authorization", {})
    raw = cfg.get("block_to_owner_confirm", [])
    # 每个条目可能含 " / " 分隔的多个短语，拆开后逐个匹配
    out = []
    for item in raw:
        for phrase in str(item).split(" / "):
            phrase = phrase.strip()
            if phrase:
                out.append(phrase)
    return out


def grade(sig, instance):
    """返回 (level, reason)。越权必降级 L2。"""
    auth = ((instance.get("owner") or {}) or {}).get("authorization", "关键确认")
    relevance = sig.get("relevance", "relevant")
    value = sig.get("value", "mid")
    urgency = sig.get("urgency", "low")
    text = ((sig.get("title") or "") + " " + (sig.get("detail") or ""))
    blocked = any(k in text for k in _block_list())

    if relevance == "irrelevant":
        return "L0", "不相关，静默观察"
    if value == "low" and urgency == "low":
        return "L0", "低价值低紧急，静默观察"

    level, reason = "L1", "相关但非紧急，汇入选报"
    if urgency != "low" or value == "high":
        level, reason = "L2", "高价值/需决策，草拟待确认（默认档）"

    if blocked:
        return "L2", "命中 decision 红线（报税/开票/重大合同/资金转出），降级 L2 草拟+等确认"
    if level == "L2" and auth == "全委托" and value != "high" and urgency == "mid":
        level, reason = "L3", "低风险常规动作 + 授权=全委托，授权内自动执行"
    return level, reason


def compose_brief(slug, days=3):
    instance = load_instance(slug)
    p = db_path(slug)
    if not os.path.exists(p):
        print(f"[proactive] 无数据库：{p}")
        return ""
    db = sqlite3.connect(p)
    ensure_signals(db)
    cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    rows = db.execute(
        "SELECT * FROM signals WHERE created_at >= ? ORDER BY created_at DESC", (cutoff,)
    ).fetchall()
    db.close()

    graded = []
    cols = ["id", "domain", "title", "detail", "relevance", "value",
            "urgency", "dept", "created_at", "level"]
    for r in rows:
        sig = dict(zip(cols, r))
        lvl, reason = grade(sig, instance)
        sig["level"] = lvl
        sig["reason"] = reason
        graded.append(sig)

    # 回写分级
    db = sqlite3.connect(p)
    for s in graded:
        db.execute("UPDATE signals SET level=? WHERE id=?", (s["level"], s["id"]))
    db.commit()
    db.close()

    # 聚合 L1/L2（排除 L0）
    picks = [s for s in graded if s["level"] in ("L1", "L2")]
    today = datetime.now().strftime("%Y-%m-%d")
    lines = [f"# 企业情报简报（{today}）", ""]
    if not picks:
        lines.append("_近 %d 天无需要推送的情报信号（静默观察中）。_" % days)
    else:
        for s in picks:
            lines.append(f"- **[{s['level']}] {s['domain']}** {s['title']}")
            lines.append(f"  - 价值:{s['value']} 紧急:{s['urgency']} 部门:{s['dept']} | {s['reason']}")
            if s["detail"]:
                lines.append(f"  - {s['detail']}")
    brief = "\n".join(lines) + "\n"

    # 落到 company-memory.md
    mp = os.path.join(os.path.expanduser("~"), ".workbuddy", "company-data",
                      slugify(slug), "company-memory.md")
    header = "\n## 情报简报（自主监测聚合）\n"
    if os.path.exists(mp):
        with open(mp, "r", encoding="utf-8") as f:
            text = f.read()
        text = text.rstrip() + "\n" + header + brief
        with open(mp, "w", encoding="utf-8") as f:
            f.write(text)
    print(brief)
    return brief


# ── CLI ─────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(description="本体论智能体 · 自发行为引擎")
    ap.add_argument("--slug", required=True, help="公司简称 slug")
    ap.add_argument("--grade", action="store_true", help="对一条信号分级（配合参数）")
    ap.add_argument("--domain", help="信号域 id")
    ap.add_argument("--title", help="信号标题")
    ap.add_argument("--detail", default="", help="信号详情")
    ap.add_argument("--relevance", default="relevant")
    ap.add_argument("--value", default="mid")
    ap.add_argument("--urgency", default="low")
    ap.add_argument("--brief", action="store_true", help="生成情报简报")
    ap.add_argument("--days", type=int, default=3, help="简报聚合天数")
    args = ap.parse_args()

    if args.grade:
        inst = load_instance(args.slug)
        sig = dict(domain=args.domain, title=args.title, detail=args.detail,
                  relevance=args.relevance, value=args.value, urgency=args.urgency)
        lvl, reason = grade(sig, inst)
        print(f"[proactive] 分级：{lvl} —— {reason}")
    if args.brief:
        compose_brief(args.slug, days=args.days)
    if not (args.grade or args.brief):
        print("[proactive] 无操作。可用 --grade / --brief。")


if __name__ == "__main__":
    main()
