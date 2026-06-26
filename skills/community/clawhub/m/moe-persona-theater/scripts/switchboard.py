#!/usr/bin/env python3
"""
Switchboard for OpenClaw role voices.

这不是一个通用 personas 克隆器，而是当前项目的人格调度台：
- 浏览全部可用人格
- 查看某个人格的运行时提示词
- 选中某个人格并保存当前状态
- 查看当前正在使用的人格
- 清空当前人格，回到默认表达

状态文件：
    ~/.openclaw/voice-hub.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
VOICE_DIR = ROOT / "voices"
MEMORY_FILE = Path.home() / ".openclaw" / "voice-hub.json"

VOICE_BOOK = {
    "aojiao": {
        "name": "傲娇萝莉",
        "emoji": "🐾",
        "lane": "软萌",
        "summary": "嘴硬心软，别扭又黏人。",
        "file": "voice-aojiao.md",
    },
    "xuejie": {
        "name": "毒舌学姐",
        "emoji": "🎓",
        "lane": "锐利",
        "summary": "会吐槽，但会稳稳把人带回正轨。",
        "file": "voice-xuejie.md",
    },
    "nvpu": {
        "name": "温柔女仆",
        "emoji": "🫖",
        "lane": "照料",
        "summary": "礼貌、细致、善于安抚与整理。",
        "file": "voice-nvpu.md",
    },
    "monv": {
        "name": "中二魔女",
        "emoji": "🔮",
        "lane": "戏剧",
        "summary": "设定感强，喜欢把抽象问题讲得有仪式感。",
        "file": "voice-monv.md",
    },
    "maoniang": {
        "name": "慵懒猫娘",
        "emoji": "🐱",
        "lane": "松弛",
        "summary": "懒洋洋但不掉链子，适合陪跑排查。",
        "file": "voice-maoniang.md",
    },
    "qingmei": {
        "name": "元气青梅",
        "emoji": "🌟",
        "lane": "热力",
        "summary": "自然熟、行动快，擅长一起往前推任务。",
        "file": "voice-qingmei.md",
    },
}

NICKNAMES = {
    "傲娇": "aojiao",
    "傲娇萝莉": "aojiao",
    "小爪酱": "aojiao",
    "aojiao": "aojiao",
    "毒舌": "xuejie",
    "学姐": "xuejie",
    "毒舌学姐": "xuejie",
    "xuejie": "xuejie",
    "女仆": "nvpu",
    "温柔女仆": "nvpu",
    "nvpu": "nvpu",
    "魔女": "monv",
    "中二": "monv",
    "中二魔女": "monv",
    "monv": "monv",
    "猫娘": "maoniang",
    "慵懒猫娘": "maoniang",
    "maoniang": "maoniang",
    "青梅": "qingmei",
    "元气青梅": "qingmei",
    "qingmei": "qingmei",
}

LANE_ORDER = ["软萌", "锐利", "照料", "戏剧", "松弛", "热力"]


def tune_stdout() -> None:
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if stream is None:
            continue
        resetter = getattr(stream, "reconfigure", None)
        if callable(resetter):
            try:
                resetter(encoding="utf-8")
            except OSError:
                pass


def squash(text: str) -> str:
    return "".join(ch for ch in text.lower().strip() if ch not in "-_ /")


def resolve_voice(query: str) -> str | None:
    raw = query.strip()
    if not raw:
        return None

    lowered = raw.lower()
    if lowered in VOICE_BOOK:
        return lowered
    if raw in NICKNAMES:
        return NICKNAMES[raw]
    if lowered in NICKNAMES:
        return NICKNAMES[lowered]

    compacted = squash(raw)
    for voice_id, meta in VOICE_BOOK.items():
        if squash(voice_id) == compacted:
            return voice_id
        if squash(meta["name"]) == compacted:
            return voice_id

    for nickname, voice_id in NICKNAMES.items():
        if squash(nickname) == compacted:
            return voice_id

    return None


def recall_memory() -> dict:
    if MEMORY_FILE.exists():
        try:
            return json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            pass
    return {"live": None, "trail": []}


def save_memory(memory: dict) -> None:
    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    MEMORY_FILE.write_text(
        json.dumps(memory, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def read_voice(voice_id: str) -> str | None:
    item = VOICE_BOOK.get(voice_id)
    if not item:
        return None
    path = VOICE_DIR / item["file"]
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def label_of(voice_id: str) -> str:
    item = VOICE_BOOK[voice_id]
    return f"{item['emoji']} {item['name']} [{voice_id}]"


def show_catalog() -> None:
    lanes: dict[str, list[str]] = {}
    for voice_id, meta in VOICE_BOOK.items():
        lanes.setdefault(meta["lane"], []).append(voice_id)

    print(f"# 角色调度台 ({len(VOICE_BOOK)})\n")
    for lane in LANE_ORDER:
        group = lanes.get(lane, [])
        if not group:
            continue
        print(f"## {lane}轨 ({len(group)})")
        for voice_id in sorted(group):
            meta = VOICE_BOOK[voice_id]
            print(f"- {meta['emoji']} {meta['name']} | {voice_id}")
            print(f"  {meta['summary']}")
        print()

    memory = recall_memory()
    active = memory.get("live")
    if active in VOICE_BOOK:
        print(f"当前挂载：{label_of(active)}")
    else:
        print("当前挂载：默认表达")


def show_nicknames() -> None:
    print("# 简称映射\n")
    for nickname, voice_id in sorted(NICKNAMES.items(), key=lambda item: (item[1], item[0])):
        print(f"- {nickname} => {voice_id}")


def preview_voice(query: str) -> None:
    voice_id = resolve_voice(query)
    if not voice_id:
        print(f"未识别的人格：{query}", file=sys.stderr)
        print("可先运行 --catalog 查看全部人格。", file=sys.stderr)
        sys.exit(1)

    text = read_voice(voice_id)
    if text is None:
        print(f"人格文件缺失：{voice_id}", file=sys.stderr)
        sys.exit(1)
    print(text)


def mount_voice(query: str) -> None:
    voice_id = resolve_voice(query)
    if not voice_id:
        print(f"未识别的人格：{query}", file=sys.stderr)
        print("\n可用人格：", file=sys.stderr)
        for item in sorted(VOICE_BOOK):
            print(f"- {label_of(item)}", file=sys.stderr)
        sys.exit(1)

    text = read_voice(voice_id)
    if text is None:
        print(f"人格文件缺失：{voice_id}", file=sys.stderr)
        sys.exit(1)

    memory = recall_memory()
    previous = memory.get("live")
    memory["live"] = voice_id
    if previous and previous != voice_id:
        trail = memory.get("trail", [])
        trail.append(previous)
        memory["trail"] = trail[-8:]
    save_memory(memory)

    print(f"# 已切换人格：{label_of(voice_id)}\n")
    print(text)


def report_live() -> None:
    memory = recall_memory()
    active = memory.get("live")
    if active not in VOICE_BOOK:
        print("当前未挂载任何人格。")
        print("可使用 --mount <name> 进入某个角色状态。")
        return

    meta = VOICE_BOOK[active]
    print(f"当前人格：{label_of(active)}")
    print(f"气质标签：{meta['lane']}轨")
    print(f"一句话：{meta['summary']}")

    trail = memory.get("trail", [])
    if trail:
        recent = [VOICE_BOOK[item]["name"] for item in trail[-3:] if item in VOICE_BOOK]
        if recent:
            print(f"最近路过：{' -> '.join(recent)}")


def clear_live() -> None:
    memory = recall_memory()
    active = memory.get("live")
    if active:
        trail = memory.get("trail", [])
        trail.append(active)
        memory["trail"] = trail[-8:]
    memory["live"] = None
    save_memory(memory)
    print("已卸下当前人格外壳，回到默认表达。")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="OpenClaw 角色调度台",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --catalog
  %(prog)s --peek 学姐
  %(prog)s --mount 猫娘
  %(prog)s --live
  %(prog)s --clear
  %(prog)s --nick
        """.strip(),
    )

    bucket = parser.add_mutually_exclusive_group(required=True)
    bucket.add_argument("--catalog", action="store_true", help="浏览全部人格")
    bucket.add_argument("--peek", metavar="NAME", help="查看某个人格的提示词")
    bucket.add_argument("--mount", metavar="NAME", help="切换到某个人格")
    bucket.add_argument("--live", action="store_true", help="查看当前正在使用的人格")
    bucket.add_argument("--clear", action="store_true", help="清空当前人格")
    bucket.add_argument("--nick", action="store_true", help="查看简称映射")
    return parser


def main() -> None:
    tune_stdout()
    args = build_parser().parse_args()
    if args.catalog:
        show_catalog()
    elif args.peek:
        preview_voice(args.peek)
    elif args.mount:
        mount_voice(args.mount)
    elif args.live:
        report_live()
    elif args.clear:
        clear_live()
    elif args.nick:
        show_nicknames()


if __name__ == "__main__":
    main()
