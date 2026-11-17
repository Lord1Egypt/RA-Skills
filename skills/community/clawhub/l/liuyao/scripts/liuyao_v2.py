#!/usr/bin/env python3
"""
六爻自动排盘 v2 - 完整64卦 + 世应六亲自动推算
"""

import struct
import os

# ─────────────────────────────────────────────
# 64卦完整数据库
# (卦名, 上卦符号, 下卦符号, 宫名, 世爻位置1-6, 应爻位置1-6)
# 世应位置: 1=初爻, 2=二爻, ..., 6=上爻
# ─────────────────────────────────────────────
HEXAGRAMS = [
    # 乾宫 (属金, 宫内本宫世在五爻, 游魂四, 归魂三)
    ("乾为天",      "☰", "☰", "乾宫", 5, 2),
    ("天风姤",      "☰", "☴", "乾宫", 1, 4),
    ("天山遯",      "☰", "☶", "乾宫", 2, 5),
    ("天地否",      "☰", "☷", "乾宫", 3, 6),
    ("风地观",      "☴", "☷", "乾宫", 4, 1),
    ("山地剥",      "☶", "☷", "乾宫", 5, 2),
    ("火地晋",      "☲", "☷", "乾宫", 4, 1),
    ("火天大有",    "☲", "☰", "乾宫", 3, 6),

    # 兑宫 (属金)
    ("泽天夬",      "☱", "☰", "兑宫", 5, 2),
    ("泽底湛",      "☱", "☱", "兑宫", 1, 4),
    ("泽水困",      "☱", "☵", "兑宫", 2, 5),
    ("泽山咸",      "☱", "☶", "兑宫", 3, 6),
    ("水山蹇",      "☵", "☶", "兑宫", 4, 1),
    ("地山谦",      "☷", "☶", "兑宫", 5, 2),
    ("雷山小过",    "☳", "☶", "兑宫", 4, 1),
    ("雷泽归妹",    "☳", "☱", "兑宫", 3, 6),

    # 离宫 (属火)
    ("离为火",      "☲", "☲", "离宫", 5, 2),
    ("火山旅",      "☲", "☳", "离宫", 1, 4),
    ("火风鼎",      "☲", "☴", "离宫", 2, 5),
    ("风水涣",      "☴", "☲", "离宫", 3, 6),
    ("天火同人",    "☰", "☲", "离宫", 4, 1),
    ("火天大有",    "☲", "☰", "离宫", 3, 6),
    ("山水蒙",      "☶", "☲", "离宫", 4, 1),
    ("风火家人",    "☴", "☲", "离宫", 5, 2),

    # 震宫 (属木)
    ("震为雷",      "☳", "☳", "震宫", 5, 2),
    ("雷地豫",      "☳", "☷", "震宫", 1, 4),
    ("雷水解",      "☳", "☵", "震宫", 2, 5),
    ("雷风恒",      "☳", "☴", "震宫", 3, 6),
    ("地风升",      "☷", "☴", "震宫", 4, 1),
    ("水风井",      "☵", "☴", "震宫", 5, 2),
    ("泽风大过",    "☱", "☴", "震宫", 4, 1),
    ("泽雷随",      "☱", "☳", "震宫", 3, 6),

    # 巽宫 (属木)
    ("巽为风",      "☴", "☴", "巽宫", 5, 2),
    ("风天小畜",    "☴", "☰", "巽宫", 1, 4),
    ("风火家人",    "☴", "☲", "巽宫", 2, 5),
    ("风雷益",      "☴", "☳", "巽宫", 3, 6),
    ("天雷无妄",    "☰", "☳", "巽宫", 4, 1),
    ("火雷噬嗑",    "☲", "☳", "巽宫", 5, 2),
    ("山雷颐",      "☶", "☳", "巽宫", 4, 1),
    ("山风蛊",      "☶", "☴", "巽宫", 3, 6),

    # 坎宫 (属水)
    ("坎为水",      "☵", "☵", "坎宫", 5, 2),
    ("水泽节",      "☵", "☱", "坎宫", 1, 4),
    ("水雷屯",      "☵", "☳", "坎宫", 2, 5),
    ("水火既济",    "☵", "☲", "坎宫", 3, 6),
    ("火水未济",    "☲", "☵", "坎宫", 4, 1),
    ("泽火革",      "☱", "☲", "坎宫", 5, 2),
    ("雷火丰",      "☳", "☲", "坎宫", 4, 1),
    ("地火明夷",    "☷", "☲", "坎宫", 5, 2),
    ("地水师",      "☷", "☵", "坎宫", 3, 6),

    # 艮宫 (属土)
    ("艮为山",      "☶", "☶", "艮宫", 5, 2),
    ("山火贲",      "☶", "☲", "艮宫", 1, 4),
    ("山天大畜",    "☶", "☰", "艮宫", 2, 5),
    ("山泽损",      "☶", "☱", "艮宫", 3, 6),
    ("火泽睽",      "☲", "☱", "艮宫", 4, 1),
    ("天泽履",      "☰", "☱", "艮宫", 5, 2),
    ("风泽中孚",    "☴", "☱", "艮宫", 4, 1),
    ("风山渐",      "☴", "☶", "艮宫", 3, 6),

    # 坤宫 (属土)
    ("坤为地",      "☷", "☷", "坤宫", 5, 2),
    ("地雷复",      "☷", "☳", "坤宫", 1, 4),
    ("地泽临",      "☷", "☱", "坤宫", 2, 5),
    ("地天泰",      "☷", "☰", "坤宫", 3, 6),
    ("雷天大壮",    "☳", "☰", "坤宫", 4, 1),
    ("泽天夬",      "☱", "☰", "坤宫", 5, 2),
    ("水天需",      "☵", "☰", "坤宫", 4, 1),
    ("水地比",      "☵", "☷", "坤宫", 3, 6),
]

# 八卦属性
BAGUA = {
    "☰": {"name": "乾", "element": "金", "family": "父"},
    "☱": {"name": "兑", "element": "金", "family": "少女"},
    "☲": {"name": "离", "element": "火", "family": "中女"},
    "☳": {"name": "震", "element": "木", "family": "长男"},
    "☴": {"name": "巽", "element": "木", "family": "长女"},
    "☵": {"name": "坎", "element": "水", "family": "中男"},
    "☶": {"name": "艮", "element": "土", "family": "少男"},
    "☷": {"name": "坤", "element": "土", "family": "母"},
}

PALACE_ELEMENT = {
    "乾宫": "金", "兑宫": "金", "离宫": "火",
    "震宫": "木", "巽宫": "木", "坎宫": "水",
    "艮宫": "土", "坤宫": "土",
}

ELEMENT_XING = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
ELEMENT_XKE = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}

LINE_NAMES = ["初爻", "二爻", "三爻", "四爻", "五爻", "上爻"]

# 二进制到八卦符号映射 (阴爻=0, 阳爻=1)
_GUA_MAP = {
    (True,  True,  True):  "☰",   # 111 乾
    (False, False, False): "☷",   # 000 坤
    (True,  True,  False): "☱",   # 110 兑
    (False, False, True):  "☶",   # 001 艮
    (True,  False, True):  "☲",   # 101 离
    (False, True,  False): "☵",   # 010 坎
    (True,  False, False): "☳",   # 100 震
    (False, True,  True):  "☴",   # 011 巽
}


def counts_to_trigram(c0, c1, c2):
    """三枚币正面数→三爻卦符号"""
    return _GUA_MAP[(c0 >= 2, c1 >= 2, c2 >= 2)]


def get_line_type(n_pos):
    """正面数→(爻名, 符号, 是否动)"""
    if n_pos == 3: return "老阳", "O", True
    if n_pos == 0: return "老阴", "X", True
    if n_pos == 2: return "少阴", "--", False
    return "少阳", "—", False


def find_hexagram(upper_sym, lower_sym):
    for h in HEXAGRAMS:
        if h[1] == upper_sym and h[2] == lower_sym:
            return h
    return None


def six_relatives(palace_el, line_els):
    out = []
    for le in line_els:
        if le == palace_el:
            out.append("兄弟")
        elif ELEMENT_XING.get(le) == palace_el:
            out.append("子孙")
        elif ELEMENT_XKE.get(le) == palace_el:
            out.append("官鬼")
        elif le == ELEMENT_XKE.get(palace_el):
            out.append("妻财")
        else:
            out.append("父母")
    return out


def main():
    print("=" * 56)
    print("  🔮 六爻自动排盘 v2")
    print("=" * 56)
    print("规则：掷3枚硬币 × 6次，从下往上记录\n")

    # ── 用 /dev/urandom 取真随机 ──
    rng = open("/dev/urandom", "rb")

    raw = rng.read(6)
    rng.close()

    counts = [struct.unpack("B", raw[i:i+1])[0] % 4 for i in range(6)]
    lines = [get_line_type(c) for c in counts]
    # lines[i] = (type_str, symbol, is_moving)

    print("【掷币记录】")
    for i, (typ, sym, mov) in enumerate(lines):
        m = " ← 动" if mov else ""
        print(f"  {LINE_NAMES[i]}：{sym} {typ}{m}")

    # ── 组合上下卦 ──
    # counts[0]=初爻, [1]=二爻, [2]=三爻 → 下卦
    # counts[3]=四爻, [4]=五爻, [5]=上爻 → 上卦
    lower_gua = counts_to_trigram(counts[0], counts[1], counts[2])
    upper_gua = counts_to_trigram(counts[3], counts[4], counts[5])

    hexagram = find_hexagram(upper_gua, lower_gua)
    if not hexagram:
        print(f"\n❌ 找不到卦: 上卦={upper_gua} 下卦={lower_gua}"); return

    gname, gup, glo, palace, shi_pos, ying_pos = hexagram
    # shi_pos/ying_pos: 1~6 对应 初爻~上爻 (数组index = pos-1)

    # ── 变卦 ──
    changed = []
    for typ, sym, mov in lines:
        changed.append("--" if mov else sym)

    cl = counts_to_trigram(
        1 if changed[0] == "—" else 0,
        1 if changed[1] == "—" else 0,
        1 if changed[2] == "—" else 0,
    )
    cu = counts_to_trigram(
        1 if changed[3] == "—" else 0,
        1 if changed[4] == "—" else 0,
        1 if changed[5] == "—" else 0,
    )
    changed_hex = find_hexagram(cu, cl)

    # ── 六亲 ──
    palace_el = PALACE_ELEMENT[palace]
    line_els = (
        [BAGUA[lower_gua]["element"]] * 3 +
        [BAGUA[upper_gua]["element"]] * 3
    )
    rels = six_relatives(palace_el, line_els)

    # ── 动爻列表 ──
    dong_indices = [i for i, (_, _, m) in enumerate(lines) if m]

    # ── 输出 ──
    print("\n" + "─" * 56)
    print(f"  【本卦】  {gname}  {gup}{glo}  {palace}")
    if changed_hex:
        print(f"  【变卦】  {changed_hex[0]}  {cu}{cl}  {changed_hex[3]}")
        print(f"  【宫位】  主卦{palace} | 变卦{changed_hex[3]}")
    if dong_indices:
        dongs = "、".join(f"第{i+1}爻" for i in dong_indices)
        print(f"  【动爻】  {dongs}")
    else:
        print(f"  【动爻】  静卦（无动爻）")

    print("─" * 56)
    # 表头
    print(f"  {'爻位':　<4} {'符号':　<4} {'五行':　<4} {'六亲':　<6} {'世应'}")
    print("  " + "─" * 46)
    for i in range(5, -1, -1):
        _, sym, mov = lines[i]
        el = line_els[i]
        rel = rels[i]
        if i == shi_pos - 1:
            mark = "← 世"
        elif i == ying_pos - 1:
            mark = "← 应"
        else:
            mark = ""
        m = " ◉" if mov else ""
        print(f"  {LINE_NAMES[i]:　<4} {sym:　<4} {el:　<4} {rel:　<6} {mark:　<8}{m}")

    print("─" * 56)
    print(f"\n  六亲：父母（生我）  兄弟（比和）  子孙（我生）")
    print(f"        妻财（我克）  官鬼（克我）")
    print(f"\n  世爻＝自身  应爻＝对方  世应之间的爻为间爻")
    print("=" * 56)


if __name__ == "__main__":
    main()
