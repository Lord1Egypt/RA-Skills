#!/usr/bin/env python3
"""
Self-Improving Skill — Observation Layer

通用的 original → final 记录器。适用于任何 "AI 生成 → 人类修改" 的循环。

用法:
    python3 observe.py record-original article.md [--text "..."] [--account X] [--content-type article]
    python3 observe.py record-final article.md [--match <hash>] [--text "..."]
    python3 observe.py pending
    python3 observe.py stats

环境变量:
    SKILL_LOG_DIR  — 日志目录（默认 ~/clawd/memory/skill-runs/default/）
"""

import sys
import json
import os
import argparse
from pathlib import Path
from datetime import datetime, timedelta
import hashlib

# 日志目录 — 自动检测 OpenClaw / Claude Code / standalone
def _detect_base():
    if os.environ.get("SKILL_BASE_DIR"):
        return Path(os.environ["SKILL_BASE_DIR"])
    candidates = [
        Path.home() / "clawd" / "memory",
        Path.home() / ".openclaw" / "memory",
        Path.home() / ".claude" / "memory",
    ]
    for c in candidates:
        if c.parent.exists():
            return c
    return Path.home() / ".self-improving" / "memory"

DEFAULT_LOG_DIR = _detect_base() / "skill-runs" / "default"


def get_log_dir(args=None):
    """按优先级决定日志目录：--log-dir > SKILL_LOG_DIR > default"""
    if args and hasattr(args, 'log_dir') and args.log_dir:
        d = Path(args.log_dir)
    elif os.environ.get("SKILL_LOG_DIR"):
        d = Path(os.environ["SKILL_LOG_DIR"])
    elif args and hasattr(args, 'skill') and args.skill:
        skill_name = Path(args.skill).name
        d = Path.home() / "clawd" / "memory" / "skill-runs" / skill_name
    else:
        d = DEFAULT_LOG_DIR
    d.mkdir(parents=True, exist_ok=True)
    return d


def get_log_file(log_dir, date_str=None):
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    return log_dir / f"{date_str}.jsonl"


def compute_hash(content):
    return hashlib.md5(content.encode()).hexdigest()[:8]


def get_content(args):
    if hasattr(args, 'text') and args.text:
        return args.text
    if hasattr(args, 'stdin') and args.stdin:
        return sys.stdin.read()
    if hasattr(args, 'file') and args.file:
        p = Path(args.file)
        if not p.exists():
            print(f"❌ 文件不存在: {args.file}")
            sys.exit(1)
        return p.read_text()
    return None


def read_log_entries(log_file):
    if not log_file.exists():
        return []
    entries = []
    with log_file.open("r") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return entries


def find_unmatched(log_dir, days=14):
    """找到有 original 但没有 final 的记录（兼容旧 edited/no-change type）"""
    all_originals = {}
    all_matched = set()

    for i in range(days):
        date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        entries = read_log_entries(get_log_file(log_dir, date))
        for e in entries:
            if e["type"] == "original":
                e["_date"] = date
                all_originals[e["content_hash"]] = e
            elif e["type"] in ("final", "edited", "no-change"):
                all_matched.add(e["content_hash"])

    return {h: o for h, o in all_originals.items() if h not in all_matched}


def record_original(args):
    content = get_content(args)
    if not content:
        print("❌ 需要提供内容（文件路径、--text 或 --stdin）")
        sys.exit(1)

    log_dir = get_log_dir(args)
    content_hash = compute_hash(content)

    context = {}
    if hasattr(args, 'account') and args.account:
        context["account"] = args.account
    if hasattr(args, 'content_type') and args.content_type:
        context["content_type"] = args.content_type

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "type": "original",
        "content_hash": content_hash,
        "file": str(args.file) if hasattr(args, 'file') and args.file else None,
        "content": content,
        "context": context,
        "char_count": len(content),
    }

    log_file = get_log_file(log_dir)
    with log_file.open("a") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    print(f"✅ 记录原稿: {content_hash}")
    print(f"📝 字数: {len(content)}")
    print(f"📁 日志: {log_file}")
    return content_hash


def record_final(args):
    content = get_content(args)
    if not content:
        print("❌ 需要提供最终版内容")
        sys.exit(1)

    log_dir = get_log_dir(args)
    target_hash = getattr(args, 'match', None)

    if target_hash:
        # 指定 hash，跨天查找
        original = None
        for i in range(14):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            entries = read_log_entries(get_log_file(log_dir, date))
            for e in entries:
                if e["type"] == "original" and e["content_hash"] == target_hash:
                    original = e
                    break
            if original:
                break
        if not original:
            print(f"❌ 找不到 hash {target_hash} 的原稿")
            sys.exit(1)
    else:
        # 自动匹配最近的未配对 original
        unmatched = find_unmatched(log_dir, 14)
        if not unmatched:
            print("❌ 没有待配对的原稿")
            sys.exit(1)
        target_hash = list(unmatched.keys())[-1]
        original = unmatched[target_hash]

    is_same = content.strip() == original["content"].strip()

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "type": "final",
        "content_hash": target_hash,
        "original_content": original["content"],
        "final_content": content,
        "original_char_count": len(original["content"]),
        "final_char_count": len(content),
        "context": original.get("context", {}),
        "no_change": is_same,
    }

    log_file = get_log_file(log_dir)
    with log_file.open("a") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    if is_same:
        print(f"✅ 记录最终版: {target_hash} (无修改 — 正反馈)")
    else:
        diff_pct = ((len(content) - len(original["content"])) / max(len(original["content"]), 1)) * 100
        print(f"✅ 记录最终版: {target_hash}")
        print(f"📝 原稿: {len(original['content'])} 字 → 最终: {len(content)} 字 ({diff_pct:+.1f}%)")
    print(f"📁 日志: {log_file}")


def show_pending(args):
    log_dir = get_log_dir(args)
    unmatched = find_unmatched(log_dir, 14)

    if not unmatched:
        print("✅ 全部已配对")
        return

    print(f"\n⏳ {len(unmatched)} 条待配对:\n")
    for h, entry in unmatched.items():
        preview = entry["content"][:80].replace("\n", " ")
        ctx = entry.get("context", {})
        account = ctx.get("account", "?")
        date = entry.get("_date", "?")
        print(f"  📄 {h} | {date} | {account}")
        print(f"     {preview}...")
        print()


def show_stats(args):
    log_dir = get_log_dir(args)
    all_files = sorted(log_dir.glob("*.jsonl"))

    total_originals = 0
    total_finals = 0
    total_no_change = 0
    total_changed = 0

    for log_file in all_files:
        entries = read_log_entries(log_file)
        total_originals += sum(1 for e in entries if e["type"] == "original")
        finals = [e for e in entries if e["type"] in ("final", "edited")]
        total_finals += len(finals)
        total_no_change += sum(1 for e in finals if e.get("no_change"))
        total_changed += sum(1 for e in finals if not e.get("no_change"))

    pending = find_unmatched(log_dir, 14)

    print(f"\n📊 Self-Improving Skill 观察统计")
    print(f"{'='*40}")
    print(f"📁 日志天数: {len(all_files)}")
    print(f"📝 原稿: {total_originals}")
    print(f"✅ 已配对: {total_finals}")
    print(f"   ├ 有修改: {total_changed}")
    print(f"   └ 无修改: {total_no_change}")
    print(f"⏳ 待配对: {len(pending)}")
    if total_finals > 0:
        print(f"📈 修改率: {total_changed}/{total_finals} = {total_changed/total_finals*100:.0f}%")


def add_common_args(parser):
    """添加通用参数"""
    parser.add_argument("--skill", help="目标 skill 目录名（用于定位日志目录）")
    parser.add_argument("--log-dir", help="自定义日志目录")


def main():
    parser = argparse.ArgumentParser(description="Self-Improving Skill — Observation Layer")
    subparsers = parser.add_subparsers(dest="action")

    # record-original
    p_orig = subparsers.add_parser("record-original", help="记录 AI 原稿")
    p_orig.add_argument("file", nargs="?", help="文件路径")
    p_orig.add_argument("--text", help="直接传入文本")
    p_orig.add_argument("--stdin", action="store_true", help="从 stdin 读取")
    p_orig.add_argument("--account", help="发布账号")
    p_orig.add_argument("--content-type", help="内容类型")
    add_common_args(p_orig)

    # record-final
    p_final = subparsers.add_parser("record-final", help="记录最终版")
    p_final.add_argument("file", nargs="?", help="文件路径")
    p_final.add_argument("--text", help="直接传入文本")
    p_final.add_argument("--stdin", action="store_true", help="从 stdin 读取")
    p_final.add_argument("--match", help="匹配的原稿 hash")
    add_common_args(p_final)

    # pending
    p_pending = subparsers.add_parser("pending", help="查看待配对原稿")
    add_common_args(p_pending)

    # stats
    p_stats = subparsers.add_parser("stats", help="总体统计")
    add_common_args(p_stats)

    args = parser.parse_args()
    if not args.action:
        parser.print_help()
        sys.exit(1)

    actions = {
        "record-original": record_original,
        "record-final": record_final,
        "pending": show_pending,
        "stats": show_stats,
    }
    actions[args.action](args)


if __name__ == "__main__":
    main()
