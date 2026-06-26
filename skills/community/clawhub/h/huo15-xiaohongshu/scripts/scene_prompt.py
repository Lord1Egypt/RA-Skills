#!/usr/bin/env python3
"""火一五小红书"场景词触发器" — 解 AI 写文案场景库窄。

为什么需要
==========
Allen 教训："AI 写文案最大短板是场景库太窄，反复用同一批词
（西瓜 / 蝉 / 冰棍 / 窗帘 / 傍晚的风）。"

scene_prompt 每天给 5 个**冷门但具象**的画面词，作为"创作触发器"。
写之前先抽 3 个进文，避免"同一个 AI 反复推荐同 5 个画面"的问题。

工作模式
========
1. 解析 data/scene_library.md 提取所有"具体画面"句子（按"-"开头匹配）
2. 按当前节气 + 时间段 + 用户已用过的画面 智能挑选
3. 输出 N 条画面 + 写作提示
4. 历史记录存 ~/.xiaohongshu/profile/scenes_used.jsonl 避免重复

用法
----

    # 抽 5 个今日画面
    python3 scene_prompt.py

    # 指定数量 + 类目
    python3 scene_prompt.py --n 8 --category 厨房

    # 看过去用过哪些
    python3 scene_prompt.py --history

    # 标记某个画面已用
    python3 scene_prompt.py --used "中午办公室落下一束斜阳到键盘上"
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import random
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent))

from xhs_profile import ProfileStore  # noqa: E402

_DATA_DIR = Path(__file__).resolve().parent.parent / "data"


@dataclass
class Scene:
    text: str
    category: str

    def to_dict(self) -> Dict[str, str]:
        return {"text": self.text, "category": self.category}


def load_scenes() -> List[Scene]:
    """从 data/scene_library.md 提取所有画面词。"""
    p = _DATA_DIR / "scene_library.md"
    if not p.exists():
        return []
    text = p.read_text(encoding="utf-8")
    out: List[Scene] = []
    current_cat = ""
    for line in text.splitlines():
        ln = line.strip()
        if ln.startswith("###"):
            current_cat = ln.lstrip("# ").strip()
            continue
        if ln.startswith("## "):
            current_cat = ln.lstrip("# ").strip()
            continue
        if ln.startswith("- ") and len(ln) > 4:
            scene_text = ln[2:].strip()
            # 跳过过短的（< 6 字）和带"❌""✅"的对照例
            if len(scene_text) < 6 or "❌" in scene_text or "✅" in scene_text:
                continue
            # 跳过列表元素（包含 → 或 例 等）
            if any(m in scene_text for m in ["→", "例：", "比喻：", "通用模板"]):
                continue
            out.append(Scene(text=scene_text, category=current_cat or "未分类"))
    return out


def load_history(store: ProfileStore) -> List[Dict[str, Any]]:
    p = store.root / "scenes_used.jsonl"
    if not p.exists():
        return []
    out = []
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return out


def append_history(store: ProfileStore, scenes: List[Scene]) -> None:
    p = store.root / "scenes_used.jsonl"
    p.parent.mkdir(parents=True, exist_ok=True)
    now = dt.datetime.now().isoformat(timespec="seconds")
    with p.open("a", encoding="utf-8") as f:
        for s in scenes:
            f.write(json.dumps({"at": now, "text": s.text, "category": s.category},
                               ensure_ascii=False) + "\n")


def pick_scenes(scenes: List[Scene], used: set, *,
                n: int = 5, category: str = "") -> List[Scene]:
    """挑 n 个：未用过 > 同类不重复 > 跨类目均衡。"""
    available = [s for s in scenes if s.text not in used]
    if not available:
        # 全用过了，重置
        available = list(scenes)
    if category:
        available = [s for s in available if category in s.category]
        if not available:
            print(f"⚠️ 类目 '{category}' 没找到画面，回退到全库", file=sys.stderr)
            available = [s for s in scenes if s.text not in used] or list(scenes)

    # 跨类目均衡：每个类目最多挑 1 个，挑满 n 个为止
    by_cat: Dict[str, List[Scene]] = {}
    for s in available:
        by_cat.setdefault(s.category, []).append(s)
    cats = list(by_cat.keys())
    random.shuffle(cats)

    picked: List[Scene] = []
    while len(picked) < n and cats:
        for c in list(cats):
            if not by_cat[c]:
                cats.remove(c)
                continue
            picked.append(by_cat[c].pop(random.randrange(len(by_cat[c]))))
            if len(picked) >= n:
                break
    return picked


def render_prompt(scenes: List[Scene]) -> str:
    parts = []
    parts.append("✨ 今日场景词触发器（写之前抽 3 个进文）")
    parts.append("=" * 60)
    for i, s in enumerate(scenes, 1):
        parts.append(f"  {i}. [{s.category}] {s.text}")
    parts.append("")
    parts.append("─" * 60)
    parts.append("用法 3 步：")
    parts.append("  1. 挑 3 个最让你 '看见画面' 的（不要同一类目挑 3）")
    parts.append("  2. 一个开场 / 一个中段反差 / 一个结尾余韵")
    parts.append("  3. 自检：你的奶奶 / 同事 / 邻居孩子，他们都有过这画面吗？")
    parts.append("")
    parts.append("跑 `scene_prompt.py --used '<画面文字>'` 标记已用，")
    parts.append("下次刷新会避开重复。")
    return "\n".join(parts)


def cmd_main(args: argparse.Namespace) -> int:
    store = ProfileStore()
    history = load_history(store)
    used = set(h["text"] for h in history)

    if args.history:
        if not history:
            print("（还没用过任何场景词。先跑一次看看）")
            return 0
        recent = history[-20:]
        print(f"📚 最近 {len(recent)} 个用过的画面：\n")
        for h in recent:
            print(f"  {h.get('at', '?')[:10]}  [{h.get('category', '?')[:10]}]  {h['text']}")
        return 0

    if args.used:
        # 加进 history 不输出新的
        scenes_to_log = [Scene(text=t, category="manual") for t in args.used]
        append_history(store, scenes_to_log)
        print(f"✓ 已标记 {len(args.used)} 个画面为已用")
        return 0

    scenes = load_scenes()
    if not scenes:
        print("❌ 找不到 data/scene_library.md 或解析失败", file=sys.stderr)
        return 1

    picked = pick_scenes(scenes, used, n=args.n, category=args.category)
    if args.format == "json":
        print(json.dumps([s.to_dict() for s in picked], ensure_ascii=False, indent=2))
    else:
        print(render_prompt(picked))

    if args.no_log:
        return 0
    # 默认追加到 history（写文案前抽到就当用了 — 用户可以 --no-log 不记）
    append_history(store, picked)
    return 0


def main() -> int:
    p = argparse.ArgumentParser(prog="scene_prompt.py", description="每日场景词触发器")
    p.add_argument("--n", type=int, default=5, help="抽几个（默认 5）")
    p.add_argument("--category", default="", help="限定类目（如 厨房 / 通勤 / 独处）")
    p.add_argument("--format", choices=["text", "json"], default="text")
    p.add_argument("--history", action="store_true", help="看历史用过的")
    p.add_argument("--used", nargs="*", default=[], help="手动标记某些画面已用")
    p.add_argument("--no-log", action="store_true", help="不记进 history")
    args = p.parse_args()
    return cmd_main(args)


if __name__ == "__main__":
    sys.exit(main())
