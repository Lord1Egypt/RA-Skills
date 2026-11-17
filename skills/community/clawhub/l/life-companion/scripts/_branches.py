#!/usr/bin/env python3
"""
_branches.py — the traditional 地支 relation tables and the arithmetic over them, in
one place.

合婚 (synastry.py) reads them between two people's charts; the daily card (bazi.py)
reads them between the day and one person's own chart. They used to live inside
synastry.py, so the daily card had nothing day-specific to say to a near-balanced
chart. One copy means the two can never drift apart.
"""

# ---------------------------------------------------------------------------
# Standard 地支 relation tables. These are fixed, disclosed, and checkable — the
# whole point is that a reader can verify them against any 子平 text.
# ---------------------------------------------------------------------------
ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

LIUHE = {  # 六合 — the classic pairings
    frozenset(("子", "丑")): "土", frozenset(("寅", "亥")): "木",
    frozenset(("卯", "戌")): "火", frozenset(("辰", "酉")): "金",
    frozenset(("巳", "申")): "水", frozenset(("午", "未")): "土",
}
SANHE = {  # 三合局 — full triads
    frozenset(("申", "子", "辰")): "水", frozenset(("亥", "卯", "未")): "木",
    frozenset(("寅", "午", "戌")): "火", frozenset(("巳", "酉", "丑")): "金",
}
SANHUI = {  # 三会方 — seasonal assemblies
    frozenset(("寅", "卯", "辰")): "木", frozenset(("巳", "午", "未")): "火",
    frozenset(("申", "酉", "戌")): "金", frozenset(("亥", "子", "丑")): "水",
}
LIUCHONG = [("子", "午"), ("丑", "未"), ("寅", "申"),
            ("卯", "酉"), ("辰", "戌"), ("巳", "亥")]          # 六冲
LIUHAI = [("子", "未"), ("丑", "午"), ("寅", "巳"),
          ("卯", "辰"), ("申", "亥"), ("酉", "戌")]            # 六害(穿)
LIUPO = [("子", "酉"), ("午", "卯"), ("申", "巳"), ("寅", "亥"),
         ("辰", "丑"), ("戌", "未")]                            # 六破
XING = {  # 三刑 / 自刑
    "无恩之刑": ("寅", "巳", "申"),
    "恃势之刑": ("丑", "戌", "未"),
    "无礼之刑": ("子", "卯"),
}
SELF_XING = ("辰", "午", "酉", "亥")


def _pair(a, b):
    return frozenset((a, b))


def relations_between(z1, z2):
    """Every traditional relation between two branches. Two branches can carry more
    than one at once (寅亥 is both 六合 and 六破) — return all of them rather than
    picking the flattering one."""
    out = []
    if z1 == z2 and z1 in SELF_XING:
        out.append({"relation": "自刑", "detail": f"{z1}{z2}"})
    if _pair(z1, z2) in LIUHE:
        out.append({"relation": "六合", "detail": f"{z1}{z2}合化{LIUHE[_pair(z1, z2)]}"})
    for triad, elem in SANHE.items():
        if z1 in triad and z2 in triad and z1 != z2:
            missing = sorted(triad - {z1, z2})
            out.append({"relation": "半合", "detail": f"{z1}{z2}（{elem}局，缺{missing[0]}）"})
    for triad, elem in SANHUI.items():
        if z1 in triad and z2 in triad and z1 != z2:
            out.append({"relation": "三会", "detail": f"{z1}{z2}（会{elem}方）"})
    for x, y in LIUCHONG:
        if {z1, z2} == {x, y}:
            out.append({"relation": "六冲", "detail": f"{z1}{z2}冲"})
    for x, y in LIUHAI:
        if {z1, z2} == {x, y}:
            out.append({"relation": "六害", "detail": f"{z1}{z2}害"})
    for x, y in LIUPO:
        if {z1, z2} == {x, y}:
            out.append({"relation": "六破", "detail": f"{z1}{z2}破"})
    for name, group in XING.items():
        if len(group) == 2:
            if {z1, z2} == set(group):
                out.append({"relation": "相刑", "detail": f"{z1}{z2}刑（{name}）"})
        elif z1 in group and z2 in group and z1 != z2:
            out.append({"relation": "相刑", "detail": f"{z1}{z2}（{name}，全见{''.join(group)}才成三刑）"})
    return out
