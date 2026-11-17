#!/usr/bin/env python3
"""麻将报牌解析：把「123万 56万 东东东」这类写法解析成结构化牌。

只做结构判断，不判胡、不算番、不给最优解。
"""
from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, asdict
from typing import List

# ---------- 牌面定义 ----------

SUITED = {"万": "m", "条": "s", "筒": "p"}
WINDS = ["东", "南", "西", "北"]
DRAGONS = ["中", "发", "白"]
FLOWERS = ["春", "夏", "秋", "冬", "梅", "兰", "竹", "菊"]

CN_NUM = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}
# 其他常见写法别名
ALIASES = {
    "东风": "东", "南风": "南", "西风": "西", "北风": "北",
    "红中": "中", "发财": "发", "白板": "白", "白皮": "白",
    "幺鸡": "1条", "一条": "1条", "幺万": "1万", "幺筒": "1筒",
    "饼": "筒", "索": "条", "万子": "万", "条子": "条", "筒子": "筒",
}

TILE_ORDER = (
    [f"{n}{s}" for s in SUITED for n in range(1, 10)]
    + WINDS
    + DRAGONS
    + FLOWERS
)


@dataclass
class Tile:
    code: str          # 规范码：1-9 + 万/条/筒，或 东/南/西/北/中/发/白/春...
    kind: str          # suited | wind | dragon | flower
    suit: str = ""     # 万/条/筒（仅 suited）
    rank: int = 0      # 1-9（仅 suited）


def classify(code: str) -> Tile:
    if code in WINDS:
        return Tile(code, "wind")
    if code in DRAGONS:
        return Tile(code, "dragon")
    if code in FLOWERS:
        return Tile(code, "flower")
    m = re.fullmatch(r"([1-9])([万条筒])", code)
    if m:
        return Tile(code, "suited", m.group(2), int(m.group(1)))
    raise ValueError(f"无法识别的牌：{code}")


# ---------- 解析 ----------

def normalize(text: str) -> str:
    """把各种口语写法归一成可解析的形式。"""
    t = text
    # 全角数字转半角
    t = t.translate(str.maketrans("０１２３４５６７８９", "0123456789"))
    # ① 先做花色别名：「饼」->筒、「索」->条（必须在数字替换前，否则「二饼」里没有花色可匹配）
    for k in ("饼", "索", "万子", "条子", "筒子"):
        if k in ALIASES:
            t = t.replace(k, ALIASES[k])
    # ② 再整体别名（长词优先）
    for k in sorted(ALIASES, key=len, reverse=True):
        t = t.replace(k, ALIASES[k])
    # ③ 中文数字连着写 + 花色：「一二三万」-> 123万
    cn_chars = "".join(CN_NUM.keys())
    t = re.sub(rf"([{cn_chars}]{{2,}})(?=[万条筒])",
               lambda m: "".join(str(CN_NUM[c]) for c in m.group(1)), t)
    # ④ 单个中文数字 + 花色：「五万」-> 5万
    for cn, n in CN_NUM.items():
        t = re.sub(rf"{cn}(?=[万条筒])", str(n), t)
    return t


def parse(text: str) -> List[Tile]:
    """解析报牌文本。支持：123万 / 1万2万3万 / 东东东 / 123万 56万 / 一万二万三万"""
    t = normalize(text)
    tiles: List[Tile] = []

    # 先处理「数字串 + 花色」紧凑写法：123万 -> 1万 2万 3万
    def expand(match: re.Match) -> str:
        digits, suit = match.group(1), match.group(2)
        return " ".join(f"{d}{suit}" for d in digits)

    t = re.sub(r"([1-9]{2,})([万条筒])", expand, t)

    # 再逐个抓 token
    for tok in re.findall(r"[1-9][万条筒]|[东南西北中发白春夏秋冬梅兰竹菊]", t):
        tiles.append(classify(tok))

    if not tiles:
        raise ValueError(f"没能从这段文字里认出任何牌：{text!r}")
    return tiles


# ---------- 结构分组（不判胡） ----------

SUIT_ORDER = {"万": 0, "条": 1, "筒": 2}


def sort_key(t: Tile):
    """排序：万 → 条 → 筒 → 风（东南西北）→ 箭（中发白）→ 花。返回长度固定为 2 的数值元组。"""
    if t.kind == "suited":
        return (SUIT_ORDER[t.suit], t.rank)
    if t.kind == "wind":
        return (3, WINDS.index(t.code) if t.code in WINDS else 0)
    if t.kind == "dragon":
        return (4, DRAGONS.index(t.code) if t.code in DRAGONS else 0)
    return (5, FLOWERS.index(t.code) if t.code in FLOWERS else 0)


def find_melds(tiles: List[Tile]) -> dict:
    """找出成型的顺子/刻子，以及差一张的搭子。

    说明：这是「描述结构」而不是「判定胡牌」。顺序是 刻子 → 顺子 → 对子 → 搭子，
    目的是把手上现成的东西尽量认出来，让新手看到「我已经有几组了」。
    """
    counts: dict = {}
    for t in tiles:
        counts[t.code] = counts.get(t.code, 0) + 1

    triplets: List[str] = []
    melds: List[List[str]] = []
    pairs: List[str] = []

    # --- 1. 刻子（三张一样） ---
    for code in list(counts):
        while counts[code] >= 3:
            triplets.append(code)
            counts[code] -= 3

    # --- 2. 顺子（同花色三张连号），从低到高扫 ---
    for suit in ("万", "条", "筒"):
        for start in range(1, 8):          # 只可能是 1~7 开头
            while all(counts.get(f"{start + i}{suit}", 0) > 0 for i in range(3)):
                melds.append([f"{start}{suit}", f"{start+1}{suit}", f"{start+2}{suit}"])
                for i in range(3):
                    counts[f"{start + i}{suit}"] -= 1

    # --- 3. 对子 ---
    for code in list(counts):
        while counts[code] >= 2 and classify(code).kind != "flower":
            pairs.append(code)
            counts[code] -= 2

    # --- 4. 剩下的单张 ---
    singles = [c for c in counts if counts[c] > 0]
    singles.sort(key=lambda c: sort_key(classify(c)))

    # --- 5. 差一张的搭子（两张同花色、差 1 或差 2），从单张里配 ---
    by_suit: dict = {}
    for code in singles:
        t = classify(code)
        if t.kind == "suited":
            by_suit.setdefault(t.suit, []).append(t.rank)
    partials = []
    leftover = set(singles)
    for suit, ranks in by_suit.items():
        ranks = sorted(set(ranks))
        i = 0
        while i < len(ranks) - 1:
            a, b = ranks[i], ranks[i + 1]
            d = b - a
            if d in (1, 2):
                ca, cb = f"{a}{suit}", f"{b}{suit}"
                if d == 1:
                    # 连着的两张（如 56）：两头都能补（4 或 7）
                    waiting = ([f"{a-1}{suit}"] if a > 1 else []) + \
                              ([f"{b+1}{suit}"] if b < 9 else [])
                else:
                    # 隔一张（如 57）：只有中间那张（6）
                    waiting = [f"{a+1}{suit}"]
                partials.append({"tiles": [ca, cb], "waiting": waiting})
                leftover.discard(ca)
                leftover.discard(cb)
                i += 2
            else:
                i += 1

    return {
        "count": len(tiles),
        "melds_formed": melds,
        "triplets_formed": triplets,
        "pairs": pairs,
        "partials": partials,
        "singles": sorted(leftover, key=lambda c: sort_key(classify(c))),
    }


def analyze(text: str) -> dict:
    tiles = parse(text)
    tiles_sorted = sorted(tiles, key=sort_key)
    return {
        "input": text,
        "normalized": [t.code for t in tiles_sorted],
        "tiles": [asdict(t) for t in tiles_sorted],
        "structure": find_melds(tiles_sorted),
        "note": "仅描述手牌结构，不判断能否胡牌、不计算番数、不推荐出牌。",
    }


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        print("用法：python3 parse_hand.py \"123万 56万 东东东 白白白 8条\"")
        sys.exit(0)
    raw = " ".join(sys.argv[1:])
    try:
        print(json.dumps(analyze(raw), ensure_ascii=False, indent=2))
    except ValueError as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
