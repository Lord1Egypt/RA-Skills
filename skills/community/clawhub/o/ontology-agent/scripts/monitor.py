#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
monitor.py — 自主监测引擎（Phase 10 新增，零侵入）

职责：
  - 读 instance.yaml 解析「薄 / 厚」档案 → 决定激活哪些信号域
  - record_signal() 把监测到的信号写入 ops.db 的 signals 表（自建表，不动 ops_db.py 核心）
    + 追加到 company-memory.md 的「情报库」段落
  - 提供 CLI：--list-domains / --profile / --record / --query

不依赖 init.py 核心逻辑，可独立运行；仅复用 yaml 解析与本地路径约定。
"""
import os
import re
import sqlite3
import argparse
from datetime import datetime

try:
    import yaml
except ImportError:
    yaml = None

HERE = os.path.dirname(os.path.abspath(__file__))
REFERENCES = os.path.join(os.path.dirname(HERE), "references")


# ── 路径工具 ────────────────────────────────────────────────────────
def slugify(text):
    s = re.sub(r"[^0-9a-zA-Z]+", "-", text or "").strip("-").lower()
    return s or "company"


def company_dir(slug):
    return os.path.join(os.path.expanduser("~"), ".workbuddy", "company-data", slugify(slug))


def instance_path(slug):
    return os.path.join(company_dir(slug), "instance.yaml")


def memory_path(slug):
    return os.path.join(company_dir(slug), "company-memory.md")


def db_path(slug):
    return os.path.join(company_dir(slug), "ops.db")


# ── 读取 ────────────────────────────────────────────────────────────
def load_instance(slug):
    if not yaml:
        raise RuntimeError("需要 PyYAML：pip install pyyaml")
    p = instance_path(slug)
    if not os.path.exists(p):
        return {}
    with open(p, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_monitoring():
    if not yaml:
        raise RuntimeError("需要 PyYAML：pip install pyyaml")
    p = os.path.join(REFERENCES, "monitoring.yaml")
    with open(p, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def resolve_profile(instance):
    """薄/厚档案判定：rich_fields 命中数 >= rich_threshold 视为厚档案。"""
    cfg = load_monitoring().get("profile_mode", {})
    rich_fields = cfg.get("rich_fields", [])
    threshold = cfg.get("rich_threshold", 2)
    hit = 0
    for f in rich_fields:
        v = instance.get(f)
        if v and (not isinstance(v, (list, dict)) or len(v) > 0):
            hit += 1
    return "thick" if hit >= threshold else "thin"


def active_domains(slug):
    """返回当前档案下应激活的信号域 id 列表。"""
    instance = load_instance(slug)
    profile = resolve_profile(instance)
    domains = load_monitoring().get("signal_domains", [])
    out = []
    for d in domains:
        applicable = d.get("thin_applicable", False) if profile == "thin" else True
        if applicable:
            out.append(d["id"])
    return out


# ── 信号写入 ────────────────────────────────────────────────────────
def ensure_signals(db):
    db.execute("""
        CREATE TABLE IF NOT EXISTS signals (
            id TEXT PRIMARY KEY,
            domain TEXT,
            title TEXT,
            detail TEXT,
            relevance TEXT,
            value TEXT,
            urgency TEXT,
            dept TEXT,
            created_at TEXT,
            level TEXT
        )""")
    db.commit()


def record_signal(slug, domain, title, detail="", relevance="relevant",
                  value="mid", urgency="low", dept="", level="L0"):
    p = db_path(slug)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    db = sqlite3.connect(p)
    ensure_signals(db)
    n = db.execute("SELECT COUNT(*) c FROM signals").fetchone()[0] + 1
    sid = f"S{n:05d}"
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    db.execute(
        "INSERT OR REPLACE INTO signals "
        "(id,domain,title,detail,relevance,value,urgency,dept,created_at,level) "
        "VALUES (?,?,?,?,?,?,?,?,?,?)",
        (sid, domain, title, detail, relevance, value, urgency, dept, now, level))
    db.commit()
    db.close()
    # 同时追加到 company-memory.md 情报库
    append_memory_intel(slug, domain, title, detail, relevance, value, urgency, dept, now, level)
    return sid


def append_memory_intel(slug, domain, title, detail, relevance, value, urgency, dept, now, level):
    mp = memory_path(slug)
    line = (f"- [{now}] [{level}] {domain} | {title} | 价值:{value} 紧急:{urgency} "
            f"部门:{dept}\n  {detail}\n")
    header = "\n## 情报库（自主监测信号）\n"
    if not os.path.exists(mp):
        with open(mp, "w", encoding="utf-8") as f:
            f.write("# 公司记忆日志\n" + header + line)
        return
    with open(mp, "r", encoding="utf-8") as f:
        text = f.read()
    if "## 情报库（自主监测信号）" not in text:
        text = text.rstrip() + "\n" + header + line
    else:
        # 追加到该标题之后最近位置（简单追加到文件末尾该段）
        text = text.rstrip() + "\n" + line
    with open(mp, "w", encoding="utf-8") as f:
        f.write(text)


# ── CLI ─────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(description="本体论智能体 · 自主监测引擎")
    ap.add_argument("--slug", required=True, help="公司简称 slug")
    ap.add_argument("--profile", action="store_true", help="打印薄/厚档案判定")
    ap.add_argument("--list-domains", action="store_true", help="列出当前激活的信号域")
    ap.add_argument("--record", action="store_true", help="写入一条信号（配合下列参数）")
    ap.add_argument("--domain", help="信号域 id")
    ap.add_argument("--title", help="信号标题")
    ap.add_argument("--detail", default="", help="信号详情")
    ap.add_argument("--relevance", default="relevant", help="relevant/irrelevant")
    ap.add_argument("--value", default="mid", help="high/mid/low")
    ap.add_argument("--urgency", default="low", help="high/mid/low")
    ap.add_argument("--dept", default="", help="负责部门 code")
    ap.add_argument("--level", default="L0", help="L0/L1/L2/L3 分级（由 proactive.py 决定）")
    args = ap.parse_args()

    if args.profile:
        inst = load_instance(args.slug)
        print(f"[monitor] 档案类型：{resolve_profile(inst)}")
    if args.list_domains:
        print(f"[monitor] 激活信号域：{active_domains(args.slug)}")
    if args.record:
        if not args.domain or not args.title:
            print("[monitor] --record 需要 --domain 与 --title")
            return
        sid = record_signal(args.slug, args.domain, args.title, args.detail,
                           args.relevance, args.value, args.urgency, args.dept, args.level)
        print(f"[monitor] 已写入信号 {sid}（domain={args.domain}, level={args.level}）")
    if not (args.profile or args.list_domains or args.record):
        print("[monitor] 无操作。可用 --profile / --list-domains / --record。")


if __name__ == "__main__":
    main()
