#!/usr/bin/env python3
"""创作热身 — 写文案前 2 分钟的创意唤醒仪式。

运动员上场前要拉伸，写文案前也需要把脑子从「分析模式」切到「感受模式」。
这个脚本帮你：切换感官 → 调取记忆 → 找到情绪 → 然后动笔。

用法:
    python3 scripts/warmup.py              # 完整 3 步热身
    python3 scripts/warmup.py --quick      # 只看一个场景+情绪，直接动笔
    python3 scripts/warmup.py --freewrite  # 场景 → 60 秒自由书写
"""

from __future__ import annotations

import argparse
import random
import sys
from pathlib import Path

_DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _load_scene_library() -> list[dict]:
    """解析 scene_library.md，提取所有画面 + 分类。"""
    path = _DATA_DIR / "scene_library.md"
    if not path.exists():
        return []
    text = path.read_text()
    scenes: list[dict] = []
    current_category = ""
    for line in text.split("\n"):
        line = line.strip()
        if line.startswith("## "):
            current_category = line.lstrip("# ").strip()
        elif line.startswith("- ") and current_category:
            scene_text = line[2:].strip()
            if scene_text and len(scene_text) > 5:
                scenes.append({"category": current_category, "scene": scene_text})
    return scenes


def _load_seasonal() -> list[str]:
    """从 seasonal_themes.md 提取情绪词。"""
    path = _DATA_DIR / "seasonal_themes.md"
    if not path.exists():
        return []
    text = path.read_text()
    emotions: list[str] = []
    for line in text.split("\n"):
        line = line.strip()
        if line.startswith("- **情绪**：") or line.startswith("- **情绪**:"):
            em = line.replace("- **情绪**：", "").replace("- **情绪**:", "").strip()
            emotions.extend([e.strip() for e in em.split("、") if e.strip()])
    return list(set(emotions))


# 情绪触发器 —— 当场景画面不够时，用这些词激活感受
EMOTIONAL_TRIGGERS = [
    "上一次你觉得「时间刚好停在这一刻就好了」是什么时候？",
    "最近一次你为自己做了一件很小但很对的事是什么？",
    "有没有一个瞬间，你突然理解了某个很久以前的事？",
    "你最近一次觉得「被看见了」是什么时候？",
    "什么东西你用完了会立刻去买？不是因为好用，是因为习惯。",
    "最近有什么东西让你觉得「这钱花得值」？",
    "你最近删掉的一个 APP 是什么？为什么？",
    "有没有一句话，你第一次听没感觉，后来才懂？",
    "你最近一次因为天气改变了计划是什么时候？",
    "有没有一个味道，能让你一秒回到某个年纪？",
    "你最近一次主动联系一个很久没联系的人，是因为什么？",
    "什么东西你一直在等，但不知道为什么在等？",
    "你最近一次「想多了」是什么事？后来证明想多了吗？",
    "你有没有一件「每次用都觉得心情好一点」的东西？",
]


def show_quick():
    """快速模式：一个画面 + 一个情绪问题。"""
    scenes = _load_scene_library()
    if not scenes:
        print("场景库未找到，直接看情绪问题。\n")
    else:
        s = random.choice(scenes)
        print(f"\n  画面：{s['scene']}")
        print(f"  （来自：{s['category']}）\n")

    trigger = random.choice(EMOTIONAL_TRIGGERS)
    print(f"  想一下：{trigger}")
    print(f"\n  → 现在可以动笔了。记住：你在分享感受，不是在写教程。")
    print(f"  → 写完跑 python3 scripts/philosophy.py 自检。\n")


def show_freewrite():
    """自由书写模式：给一个画面，60 秒不限主题写。"""
    scenes = _load_scene_library()
    s = random.choice(scenes) if scenes else {"scene": "此刻窗外", "category": "当下"}
    emotions = _load_seasonal()
    em = random.choice(emotions) if emotions else "安静"

    print(f"""
  ╔══════════════════════════════════════════════════════════╗
  ║           ✍️  60 秒自由书写 — 不要停、不要改              ║
  ╚══════════════════════════════════════════════════════════╝

  画面：{s['scene']}
  情绪：{em}

  规则：
  - 从这个画面开始写
  - 60 秒内不要停笔
  - 不要改错别字
  - 不要判断好坏
  - 写到哪儿算哪儿

  这不是文案，是矿石。好的文案从矿石里提炼。
  写完之后，再打开 philosophy.py 看 8 问。
""")
    # 给一个具体的开头句，降低空白页焦虑
    starters = [
        f"那天{s['scene']}，我突然觉得……",
        f"我后来才意识到，{s['scene']}的那个时候……",
        f"其实{s['scene']}，是一种很小的幸福。",
        f"你有没有过这样的时刻：{s['scene']}。",
    ]
    print(f"  实在不知道写什么，从这里开始：")
    print(f"  「{random.choice(starters)}」\n")


def show_full():
    """完整热身：三步。"""
    scenes = _load_scene_library()
    emotions = _load_seasonal()

    # Step 1: 切换感官
    print("""
  ┌─ Step 1/3: 切换感官 ─────────────────────────────────┐
  │  放下分析脑。你不是在写论文，你是在和朋友聊天。        │
  │  深呼吸一次，然后读下面这个画面：                      │
  └──────────────────────────────────────────────────────┘""")

    if scenes:
        s1 = random.choice(scenes)
        print(f"\n  「{s1['scene']}」\n")
        print(f"  你能感觉到它吗？温度、声音、光线？花 10 秒真正感受一下。\n")

    # Step 2: 找到情绪
    em = random.choice(emotions) if emotions else "珍惜"
    print(f"""  ┌─ Step 2/3: 找到情绪 ─────────────────────────────────┐
  │  今天的情绪锚点：{em}                                  │
  │                                                        │
  │  不是去「写{em}」，是去想「上一次我感到{em}是什么时候？」│
  │  场景不是编的，是从记忆里捞的。                          │
  └──────────────────────────────────────────────────────┘""")

    trigger = random.choice(EMOTIONAL_TRIGGERS)
    print(f"\n  {trigger}\n")

    # Step 3: 对齐哲学
    print(f"""  ┌─ Step 3/3: 对齐哲学 ─────────────────────────────────┐
  │  默念四句，然后动笔：                                  │
  │                                                        │
  │  1. 好文案是留出来的，不是写出来的。                    │
  │  2. 卖的是身份认同，不是商品。                          │
  │  3. 站文案里面读，不是站外面分析。                      │
  │  4. 一流的糖衣本身就是炮弹。                            │
  │                                                        │
  │  记住：你是在邀请读者进入一个感受，不是在教她做一件事。  │
  └──────────────────────────────────────────────────────┘

  → 现在动笔。写完跑 python3 scripts/philosophy.py 自检。
""")


def main():
    parser = argparse.ArgumentParser(
        description="创作热身 — 写文案前 2 分钟的创意唤醒仪式"
    )
    parser.add_argument(
        "--quick", action="store_true",
        help="只看一个场景+情绪问题，直接动笔"
    )
    parser.add_argument(
        "--freewrite", action="store_true",
        help="给一个场景，60 秒自由书写"
    )
    args = parser.parse_args()

    if args.quick:
        show_quick()
    elif args.freewrite:
        show_freewrite()
    else:
        show_full()


if __name__ == "__main__":
    main()
