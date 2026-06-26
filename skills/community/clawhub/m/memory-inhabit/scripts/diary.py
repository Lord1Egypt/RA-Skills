#!/usr/bin/env python3
"""
Memory-Inhabit Secret Diary — 私密日记（本地存储，不进 Git）

用法：
  python3 diary.py check <persona> [--date YYYY-MM-DD]
  python3 diary.py prepare-write <persona> [--date YYYY-MM-DD]
  python3 diary.py save <persona> [--date YYYY-MM-DD]   # 从 stdin 读 JSON: {"full":"...","traces":["..."]}
  python3 diary.py list-traces <persona> [--date YYYY-MM-DD] [--days N] [--limit N]
  python3 diary.py detect-intent "<用户原话>"
  python3 diary.py paths <persona>
"""

import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from memory import (
    get_persona_dirs,
    get_today_history,
    resolve_persona_dir,
    sanitize_path_name,
)

# 自然话术意图（非死板匹配，供 detect-intent 与 Agent 参考）
INTENT_PATTERNS_HIGH = [
    r"昨晚.{0,8}想",
    r"昨夜.{0,8}想",
    r"没说完",
    r"憋着没说",
    r"还有.{0,6}没告诉",
    r"没告诉你",
    r"偷看.{0,6}日记",
    r"日记.{0,6}写了什么",
    r"漏出来",
    r"漏给你的",
    r"心里话",
    r"私下想",
    r"背着我.{0,6}想",
]

INTENT_PATTERNS_LOW = [
    r"你在想什么",
    r"心里想",
    r"是不是想说什么",
]


def get_diary_dir(persona_name):
    """@brief 私密日记目录 memories/diary/"""
    return get_persona_dirs(persona_name)["base"] / "diary"


def diary_paths(persona_name, date_str=None):
    """@brief 某日日记文件路径"""
    date_str = date_str or datetime.now().strftime("%Y-%m-%d")
    base = get_diary_dir(persona_name)
    return {
        "dir": base,
        "date": date_str,
        "full": base / f"{date_str}.full.md",
        "traces": base / f"{date_str}.traces.json",
    }


def count_history_messages(history_text):
    """@brief 估算当日对话条数（按时间戳行）"""
    if not history_text:
        return 0
    return len(re.findall(r"^\*\*\[\d", history_text, re.MULTILINE))


def load_story_baseline(persona_dir):
    """@brief 读取故事基线"""
    path = Path(persona_dir) / "prompt" / "story_baseline.txt"
    if path.exists():
        return path.read_text(encoding="utf-8").strip()
    return ""


def load_config(persona_dir):
    """@brief 读取 config.json"""
    path = Path(persona_dir) / "config.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def diary_settings(config):
    """@brief 私密日记配置项"""
    diary = config.get("secret_diary", {})
    return {
        "enabled": diary.get("enabled", True),
        "min_messages_today": int(diary.get("min_messages_today", 2)),
    }


def cmd_check(persona_name, date_str):
    """@brief 是否宜生成当日日记"""
    persona_dir = resolve_persona_dir(persona_name)
    if not persona_dir.exists():
        print(json.dumps({"ok": False, "error": "persona_not_found"}, ensure_ascii=False))
        return

    paths = diary_paths(persona_name, date_str)
    config = load_config(persona_dir)
    settings = diary_settings(config)

    history_file = get_persona_dirs(persona_name)["history"] / f"{date_str}.md"
    history_text = ""
    if history_file.exists():
        history_text = history_file.read_text(encoding="utf-8")

    msg_count = count_history_messages(history_text)
    baseline = load_story_baseline(persona_dir)

    result = {
        "ok": True,
        "persona": persona_name,
        "date": date_str,
        "enabled": settings["enabled"],
        "should_write": False,
        "reason": "",
        "message_count": msg_count,
        "min_messages": settings["min_messages_today"],
        "has_baseline": bool(baseline),
        "has_history": bool(history_text.strip()),
        "already_exists": paths["full"].exists(),
        "diary_dir": str(paths["dir"]),
    }

    if not settings["enabled"]:
        result["reason"] = "disabled_in_config"
    elif paths["full"].exists():
        result["reason"] = "already_written"
    elif msg_count < settings["min_messages_today"]:
        result["reason"] = "not_enough_messages"
    elif not baseline:
        result["reason"] = "missing_story_baseline"
        result["should_write"] = False
    elif not history_text.strip():
        result["reason"] = "no_history_today"
    else:
        result["should_write"] = True
        result["reason"] = "ready"

    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_prepare_write(persona_name, date_str):
    """@brief 输出供 Agent 撰写日记的上下文（不含历史 full 日记）"""
    persona_dir = resolve_persona_dir(persona_name)
    if not persona_dir.exists():
        print("❌ 人格包不存在", file=sys.stderr)
        sys.exit(1)

    profile_path = persona_dir / "profile.json"
    profile = json.loads(profile_path.read_text(encoding="utf-8")) if profile_path.exists() else {}
    name = profile.get("name", persona_name)

    history_file = get_persona_dirs(persona_name)["history"] / f"{date_str}.md"
    history_text = ""
    if history_file.exists():
        history_text = history_file.read_text(encoding="utf-8")

    baseline = load_story_baseline(persona_dir)

    print(f"# 私密日记撰写任务 — {name} — {date_str}\n")
    print("## 要求")
    print("- 第一人称内心独白，贴合 story_baseline 的当前主线与阶段目标")
    print("- 基于下方「今日对话」事实，写未当面对玩家说出口的心思")
    print("- 产出 full 正文（400～800 字为宜）与 1～2 条 traces（每条 15～40 字，像漏出的半句话）")
    print("- traces 禁止剧透 full 全文；禁止打破第四面墙")
    print("- 完成后：python3 diary.py save <persona> --date {date_str}  （stdin 传 JSON）\n")

    print("## 故事基线 (story_baseline.txt)\n")
    print(baseline if baseline else "（缺失，请先补充 prompt/story_baseline.txt）")
    print("\n## 今日对话 (memories/history)\n")
    print(history_text.strip() if history_text else "（无）")
    print("\n## save JSON 格式示例")
    print(json.dumps(
        {"full": "# 私密日记 ...", "traces": ["……片段一。", "……片段二。"]},
        ensure_ascii=False,
        indent=2,
    ))


def cmd_save(persona_name, date_str):
    """@brief 保存 full + traces（stdin JSON）"""
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"❌ stdin 不是合法 JSON: {e}", file=sys.stderr)
        sys.exit(1)

    full_text = (payload.get("full") or "").strip()
    traces = payload.get("traces") or []
    if not full_text:
        print("❌ 缺少 full 字段", file=sys.stderr)
        sys.exit(1)
    if not traces:
        print("❌ 至少 1 条 traces", file=sys.stderr)
        sys.exit(1)

    paths = diary_paths(persona_name, date_str)
    paths["dir"].mkdir(parents=True, exist_ok=True)

    if not full_text.startswith("#"):
        full_text = f"# 私密日记 — {persona_name} — {date_str}\n\n{full_text}"

    paths["full"].write_text(full_text, encoding="utf-8")

    trace_items = []
    now = datetime.now().isoformat(timespec="seconds")
    for t in traces[:3]:
        text = str(t).strip()
        if text:
            trace_items.append({"text": text, "created_at": now})

    traces_doc = {
        "persona": persona_name,
        "date": date_str,
        "generated_at": now,
        "traces": trace_items,
    }
    paths["traces"].write_text(
        json.dumps(traces_doc, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(json.dumps({
        "ok": True,
        "full_path": str(paths["full"]),
        "traces_path": str(paths["traces"]),
        "trace_count": len(trace_items),
    }, ensure_ascii=False, indent=2))


def load_traces_file(traces_path):
    """@brief 读取 traces.json"""
    if not traces_path.exists():
        return None
    return json.loads(traces_path.read_text(encoding="utf-8"))


def cmd_list_traces(persona_name, date_str=None, days=7, limit=3):
    """@brief 列出可展示给玩家的碎片（JSON）"""
    diary_dir = get_diary_dir(persona_name)
    if not diary_dir.exists():
        print(json.dumps({"ok": True, "traces": [], "message": "no_diary_dir"}, ensure_ascii=False))
        return

    collected = []
    if date_str:
        dates = [date_str]
    else:
        dates = [
            (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            for i in range(days)
        ]

    for d in dates:
        p = diary_dir / f"{d}.traces.json"
        doc = load_traces_file(p)
        if not doc:
            continue
        for item in doc.get("traces", []):
            collected.append({
                "date": d,
                "text": item.get("text", ""),
                "created_at": item.get("created_at", ""),
            })

    collected.sort(key=lambda x: (x["date"], x.get("created_at", "")), reverse=True)
    collected = collected[:limit]

    print(json.dumps({
        "ok": True,
        "persona": persona_name,
        "traces": collected,
        "count": len(collected),
    }, ensure_ascii=False, indent=2))


def cmd_detect_intent(text):
    """@brief 检测用户是否在追问「未说出口的心思」"""
    text = text.strip()
    confidence = "none"
    for pat in INTENT_PATTERNS_HIGH:
        if re.search(pat, text, re.IGNORECASE):
            confidence = "high"
            break
    if confidence == "none":
        for pat in INTENT_PATTERNS_LOW:
            if re.search(pat, text, re.IGNORECASE):
                confidence = "low"
                break

    print(json.dumps({
        "ok": True,
        "text": text,
        "should_offer_traces": confidence in ("high", "low"),
        "confidence": confidence,
        "hint": "high 时调用 diary.py list-traces 并以角色口吻只念 traces，禁止输出 *.full.md",
    }, ensure_ascii=False, indent=2))


def cmd_paths(persona_name):
    """@brief 打印日记目录路径"""
    p = get_diary_dir(persona_name)
    print(json.dumps({
        "ok": True,
        "diary_dir": str(p),
        "gitignored": True,
        "note": "私密日记仅存本地，不提交 Git",
    }, ensure_ascii=False, indent=2))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    cmd = sys.argv[1]
    args = sys.argv[2:]

    persona = None
    date_str = datetime.now().strftime("%Y-%m-%d")
    days = 7
    limit = 3
    intent_text = None

    i = 0
    while i < len(args):
        if args[i] == "--date" and i + 1 < len(args):
            date_str = args[i + 1]
            i += 2
        elif args[i] == "--days" and i + 1 < len(args):
            days = int(args[i + 1])
            i += 2
        elif args[i] == "--limit" and i + 1 < len(args):
            limit = int(args[i + 1])
            i += 2
        elif not args[i].startswith("-"):
            if cmd == "detect-intent" and intent_text is None:
                intent_text = args[i]
            elif persona is None:
                persona = sanitize_path_name(args[i])
            i += 1
        else:
            i += 1

    if cmd == "detect-intent":
        if not intent_text and len(args) > 0:
            intent_text = " ".join(a for a in args if not a.startswith("--"))
        if not intent_text:
            print("用法: python3 diary.py detect-intent \"你昨晚想了什么\"", file=sys.stderr)
            sys.exit(1)
        cmd_detect_intent(intent_text)
    elif cmd == "paths":
        if not persona:
            print("用法: python3 diary.py paths <persona>", file=sys.stderr)
            sys.exit(1)
        cmd_paths(persona)
    elif cmd == "check":
        if not persona:
            print("用法: python3 diary.py check <persona>", file=sys.stderr)
            sys.exit(1)
        cmd_check(persona, date_str)
    elif cmd == "prepare-write":
        if not persona:
            print("用法: python3 diary.py prepare-write <persona>", file=sys.stderr)
            sys.exit(1)
        cmd_prepare_write(persona, date_str)
    elif cmd == "save":
        if not persona:
            print("用法: python3 diary.py save <persona> [--date YYYY-MM-DD] < payload.json", file=sys.stderr)
            sys.exit(1)
        cmd_save(persona, date_str)
    elif cmd == "list-traces":
        if not persona:
            print("用法: python3 diary.py list-traces <persona>", file=sys.stderr)
            sys.exit(1)
        cmd_list_traces(persona, date_str if "--date" in sys.argv else None, days, limit)
    else:
        print(f"❌ 未知命令: {cmd}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
