#!/usr/bin/env python3
"""
formation_diagram.py — 把"知识阵容"渲染成足球场 SVG 阵型图

用法:
    python3 formation_diagram.py team.json output.svg [--strict]

退出码:
    0  成功（SVG 已生成；stderr 可能仍有警告，交付前必须逐条处理）
    2  参数错误 / 输入文件不存在 / JSON 解析失败 / 阵型不支持
    3  --strict 模式下存在任何警告（SVG 仍会生成，便于排查）

输入 JSON 结构:
{
  "topic": "主题名",
  "formation": "4-3-3",
  "coach":  {"name": "主教练(核心思想)名", "desc": "一句话说明"},
  "players": [
    {"pos": "CB", "name": "知识点A", "desc": "一句话"},
    {"pos": "LW", "name": "知识点B", "desc": "一句话"}
  ],
  "bench":  [{"name": "替补知识点1", "desc": "一句话"}],
  "flow":   ["GK","CB","CDM","AMD","CF"],
  "b_team": {
     "formation": "3-5-2",
     "coach": {"name": "B队教练(次级核心)", "desc": "一句话"},
     "players": [{"pos": "CM", "name": "扩展知识点", "desc": "一句话"}]
  }
}

- "players" 按场上位置代码摆放；同名位置（如两个 CB）按出现顺序填入。
- 同位置人数超过阵型槽位时（如 3 个 CB 塞进只有 2 个 CB 槽的阵型），多出的球员
  不会消失：一律转入替补席，并在 stderr 给出明确警告（绝不静默丢内容）。
- 位置代码不在阵型中时，同样放上替补席并在 stderr 警告。
- 场上位置未填满时，空位画成虚线圈，代表"还可以继续深挖的位置"。
- "flow" 可选：按位置代码顺序画学习路径箭头（球路）。
  * 含阵型外的位置代码会在 stderr 逐条警告（该点被跳过），有效点不足 2 个时不画箭头并警告；
  * 同名多槽位置（如两个 CB）默认连接第一个槽。
- 知识点的 "desc" 只用于输出警告/统计，不画进 SVG（长文由 Agent 写进正文球员卡）。

支持的阵型: 4-3-3, 4-2-3-1, 4-3-2-1, 4-4-2, 4-5-1, 4-1-4-1, 3-5-2, 3-4-3
位置代码: GK RB CB LB CDM CM CAM AMD LAM RAM RM LM LW RW CF SS
"""

import argparse
import json
import sys
import html
import math
from collections import Counter

FORMATIONS = {
    # 位置, x%, y% (虚拟球场坐标，左上角为原点，向右进攻)
    "4-3-3": [
        ("GK", 8, 50), ("LB", 24, 14), ("CB", 24, 36), ("CB", 24, 64),
        ("RB", 24, 86), ("CM", 52, 30), ("CDM", 52, 50), ("CM", 52, 70),
        ("LW", 80, 18), ("CF", 80, 50), ("RW", 80, 82),
    ],
    "4-2-3-1": [
        ("GK", 8, 50), ("LB", 24, 14), ("CB", 24, 36), ("CB", 24, 64),
        ("RB", 24, 86), ("CDM", 46, 33), ("CDM", 46, 67),
        ("LAM", 72, 22), ("AMD", 72, 50), ("RAM", 72, 78), ("CF", 90, 50),
    ],
    "4-3-2-1": [
        ("GK", 8, 50), ("LB", 24, 14), ("CB", 24, 36), ("CB", 24, 64),
        ("RB", 24, 86), ("CM", 48, 62), ("CDM", 48, 50), ("CM", 48, 38),
        ("SS", 74, 35), ("SS", 74, 65), ("CF", 90, 50),
    ],
    "4-4-2": [
        ("GK", 8, 50), ("LB", 24, 14), ("CB", 24, 36), ("CB", 24, 64),
        ("RB", 24, 86), ("LM", 52, 20), ("CM", 52, 40), ("CM", 52, 60),
        ("RM", 52, 80), ("CF", 78, 35), ("CF", 78, 65),
    ],
    "4-5-1": [
        ("GK", 8, 50), ("LB", 24, 14), ("CB", 24, 36), ("CB", 24, 64),
        ("RB", 24, 86), ("LM", 52, 18), ("CM", 52, 38), ("CDM", 52, 50),
        ("CM", 52, 62), ("RM", 52, 82), ("CF", 82, 50),
    ],
    "4-1-4-1": [
        ("GK", 8, 50), ("LB", 24, 14), ("CB", 24, 36), ("CB", 24, 64),
        ("RB", 24, 86), ("CDM", 44, 50),
        ("LM", 54, 22), ("CM", 54, 42), ("CM", 54, 58), ("RM", 54, 78),
        ("CF", 80, 50),
    ],
    "3-5-2": [
        ("GK", 8, 50), ("CB", 22, 30), ("CB", 22, 50), ("CB", 22, 70),
        ("LM", 50, 14), ("CM", 50, 35), ("CDM", 50, 50), ("CM", 50, 65),
        ("RM", 50, 86), ("CF", 78, 35), ("CF", 78, 65),
    ],
    "3-4-3": [
        ("GK", 8, 50), ("CB", 22, 30), ("CB", 22, 50), ("CB", 22, 70),
        ("LM", 50, 14), ("CM", 50, 35), ("CM", 50, 65), ("RM", 50, 86),
        ("LW", 80, 18), ("CF", 80, 50), ("RW", 80, 82),
    ],
}

POS_GROUP = {
    "GK": ("门将", "#FFC107"),
    "RB": ("后卫", "#64B5F6"), "CB": ("后卫", "#64B5F6"),
    "LB": ("后卫", "#64B5F6"), "WB": ("后卫", "#64B5F6"),
    "CDM": ("中场", "#4CAF50"), "CM": ("中场", "#4CAF50"),
    "CAM": ("中场", "#4CAF50"), "AMD": ("中场", "#4CAF50"),
    "LAM": ("中场", "#4CAF50"), "RAM": ("中场", "#4CAF50"),
    "LM": ("中场", "#4CAF50"), "RM": ("中场", "#4CAF50"),
    "LW": ("前锋", "#E53935"), "RW": ("前锋", "#E53935"),
    "CF": ("前锋", "#E53935"), "SS": ("前锋", "#E53935"),
}
BENCH_COLOR = "#90A4AE"
COACH_COLOR = "#9C27B0"
TEXT_COLOR = "#12321C"

POS_ALIAS = {
    "GK": "GK", "RB": "RB", "CB": "CB", "LB": "LB", "WB": "WB",
    "CDM": "CDM", "CM": "CM", "CAM": "AMD", "AMD": "AMD",
    "LAM": "LAM", "RAM": "RAM", "LM": "LM", "RM": "RM",
    "LW": "LW", "RW": "RW", "CF": "CF", "SS": "SS",
}


def esc(s):
    return html.escape(str(s), quote=True)


def pitch_lines(box, clip_id):
    """生成一个球场的 SVG 线条（含草地条纹与标线），box=(x0,y0,x1,y1)。"""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    cx, cy = x0 + w / 2, y0 + h / 2
    L = []
    L.append(f'<defs><clipPath id="{clip_id}">'
             f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="10"/></clipPath></defs>')
    # 草地底色
    L.append(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="10" '
             f'fill="#2E9E44" stroke="#F5F5F5" stroke-width="3"/>')
    # 草皮条纹
    stripes = []
    stripe_w = w / 10
    for i in range(10):
        if i % 2 == 0:
            sx = x0 + i * stripe_w
            stripes.append(f'<rect x="{sx:.1f}" y="{y0}" width="{stripe_w:.1f}" '
                          f'height="{h}" fill="#2A9340"/>')
    L.append(f'<g clip-path="url(#{clip_id})">{"".join(stripes)}</g>')
    # 标线
    L.append(f'<g stroke="#F5F5F5" stroke-width="2" fill="none">')
    L.append(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="10"/>')
    L.append(f'<line x1="{cx}" y1="{y0}" x2="{cx}" y2="{y1}"/>')
    L.append(f'<circle cx="{cx}" cy="{cy}" r="{min(w,h)*0.09:.1f}"/>')
    L.append(f'<circle cx="{cx}" cy="{cy}" r="2.5" fill="#F5F5F5"/>')
    # 禁区
    pw, ph = w * 0.16, h * 0.55
    L.append(f'<rect x="{x0}" y="{cy-ph/2:.1f}" width="{pw:.1f}" height="{ph:.1f}"/>')
    L.append(f'<rect x="{x1-pw:.1f}" y="{cy-ph/2:.1f}" width="{pw:.1f}" height="{ph:.1f}"/>')
    # 小禁区
    gw, gh = w * 0.05, h * 0.22
    L.append(f'<rect x="{x0}" y="{cy-gh/2:.1f}" width="{gw:.1f}" height="{gh:.1f}"/>')
    L.append(f'<rect x="{x1-gw:.1f}" y="{cy-gh/2:.1f}" width="{gw:.1f}" height="{gh:.1f}"/>')
    # 球门
    L.append(f'<rect x="{x0-4}" y="{cy-gh/2+2:.1f}" width="5" height="{gh-4:.1f}" fill="#F5F5F5"/>')
    L.append(f'<rect x="{x1-1}" y="{cy-gh/2+2:.1f}" width="5" height="{gh-4:.1f}" fill="#F5F5F5"/>')
    L.append('</g>')
    return L


def wrap_name(name, max_chars=14):
    """把名字完整换行（绝不丢字）：英文按单词，中文按字符。

    返回全部行；超长的单个英文 token 整体保留为一行，
    由 fit_font_size() 缩小字号保证不溢出、不截断。
    """
    name = str(name).strip()
    if not name:
        return [""]

    if ' ' in name:
        # 英文/混合：按单词换行
        words = name.split(' ')
        lines = []
        cur = ""
        for w in words:
            if cur and len(cur) + 1 + len(w) > max_chars:
                lines.append(cur)
                cur = w
            else:
                cur = (cur + " " + w).strip()
        if cur:
            lines.append(cur)
    else:
        # 无空格：中文按字符换行；超长英文 token 整体保留（交给缩字号）
        lines = []
        cur = ""
        for ch in name:
            is_cjk = ord(ch) > 0x2E7F
            if is_cjk and len(cur) >= max_chars:
                lines.append(cur)
                cur = ch
            else:
                cur += ch
        if cur:
            lines.append(cur)

    return lines


def fit_font_size(text, max_width, base_size, min_size=6):
    """按内容估算文本宽度，返回不超过 max_width 的字号。

    中文/全角约 1.0em，拉丁约 0.6em，预留 10% 余量。
    长名字自动缩小但完整显示，绝不静默截断丢字。
    """
    units = 0.0
    for ch in str(text):
        units += 1.0 if ord(ch) > 0x2E7F else 0.6
    size = float(base_size)
    while size > min_size and units * size * 1.1 > max_width:
        size -= 0.5
    return round(size, 1)


def draw_team(svg, box, formation, coach, players, bench, flow, topic_label,
              team_label="", b_team=False, clip_id="pitch", flip=False):
    """在 box 内画一套阵容。返回渲染过程中的警告列表（绝不静默丢内容）。"""
    warnings = []
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    r = 50  # 球员圈半径

    def pt(slot):
        px = slot[1]
        if flip:
            px = 100 - px  # 水平翻转：B队从右向左攻
        return (x0 + px / 100.0 * w, y0 + slot[2] / 100.0 * h)

    slots = FORMATIONS.get(formation, [])
    if not slots:
        raise ValueError(
            f"不支持的阵型: {formation}，可选: {', '.join(FORMATIONS)}")

    # 把 players 按位置代码归位
    pos_queue = {}
    for p in players:
        key = POS_ALIAS.get(p.get("pos", ""), p.get("pos", ""))
        pos_queue.setdefault(key, []).append(p)

    # === 画足球场地 ===
    svg.extend(pitch_lines(box, clip_id))

    # === 标题（最上方，分两行：主题 + 阵型） ===
    title1 = topic_label
    title2 = formation
    if team_label:
        title1 = f"{team_label} | {title1}"
    # 第一行：主题
    svg.append(f'<text x="{(x0+x1)/2:.0f}" y="{y0-210}" text-anchor="middle" '
               f'font-size="40" font-weight="bold" fill="{TEXT_COLOR}">{esc(title1)}</text>')
    # 第二行：阵型
    svg.append(f'<text x="{(x0+x1)/2:.0f}" y="{y0-145}" text-anchor="middle" '
               f'font-size="28" font-weight="bold" fill="#666">{esc(title2)}</text>')

    # === 主教练（标题下方，左侧） ===
    if coach:
        cx, cy = x0 + 20, y0 - 90
        svg.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="20" fill="{COACH_COLOR}"/>')
        svg.append(f'<text x="{cx:.0f}" y="{cy+4:.0f}" text-anchor="middle" '
                   f'font-size="12" font-weight="bold" fill="#fff">HC</text>')
        coach_text = f"主教练·{coach.get('name','')}"
        svg.append(f'<text x="{cx+50:.0f}" y="{cy+8:.0f}" font-size="24" '
                   f'font-weight="bold" fill="{TEXT_COLOR}">{esc(coach_text)}</text>')

    # === 学习路径箭头（球路） ===
    if flow:
        idx = {}
        for s in slots:
            idx.setdefault(s[0], []).append(s)
        pts = []
        unknown_flow = []
        for code in flow:
            k = POS_ALIAS.get(code, code)
            if k in idx and idx[k]:
                pts.append(pt(idx[k][0]))
            elif code not in unknown_flow:
                unknown_flow.append(code)
        if unknown_flow:
            warnings.append(
                f"球路包含阵型 {formation} 中不存在的位置："
                f"{'、'.join(unknown_flow)}（已跳过，请检查 flow 与阵型是否匹配）")
        if len(pts) < 2:
            warnings.append(
                f"球路有效节点不足 2 个，未画出学习路径箭头（flow={flow}，请对照阵型检查）")
        if len(pts) >= 2:
            marker_id = f"arrow_{clip_id}"
            svg.append(f'<defs><marker id="{marker_id}" viewBox="0 0 10 10" refX="26" refY="5" '
                       f'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
                       f'<path d="M0,0 L10,5 L0,10 z" fill="#FFF59D" stroke="#F9A825" stroke-width="1"/>'
                       f'</marker></defs>')
            for i in range(len(pts) - 1):
                ax, ay = pts[i]
                bx, by = pts[i + 1]
                svg.append(f'<line x1="{ax:.1f}" y1="{ay:.1f}" x2="{bx:.1f}" y2="{by:.1f}" '
                           f'stroke="#FFF59D" stroke-width="4" stroke-dasharray="8,6" '
                           f'marker-end="url(#{marker_id})" opacity="0.9"/>')

    # === 球员 ===
    used_slots = set()
    for i, (code, px, py) in enumerate(slots):
        key = POS_ALIAS.get(code, code)
        queue = pos_queue.get(key, [])
        if queue:
            p = queue.pop(0)
            used_slots.add(i)
            cx, cy = pt((code, px, py))
            color = POS_GROUP.get(key, (None, BENCH_COLOR))[1]
            gname = POS_GROUP.get(key, ("?", ""))[0]
            svg.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{color}" '
                       f'stroke="#fff" stroke-width="2.5"/>')
            svg.append(f'<text x="{cx:.1f}" y="{cy-3:.1f}" text-anchor="middle" font-size="10" '
                       f'font-weight="bold" fill="#fff">{esc(code)}</text>')
            svg.append(f'<text x="{cx:.1f}" y="{cy+9:.1f}" text-anchor="middle" font-size="8" '
                       f'fill="#fff">{esc(gname)}</text>')
            # 球员名字（在圆圈下方）：完整显示，长名自动缩字号，不截断
            lines = wrap_name(p.get("name", ""), max_chars=14)
            name_max_w = 2.9 * r  # 名字可用宽度
            fs = min((fit_font_size(ln, name_max_w, 10, min_size=6) for ln in lines),
                     default=10)
            line_h = fs * 1.35
            ty = cy + r + 12 + fs
            for ln in lines:
                svg.append(f'<text x="{cx:.1f}" y="{ty:.1f}" text-anchor="middle" '
                           f'font-size="{fs}" font-weight="bold" fill="{TEXT_COLOR}">'
                           f'{esc(ln)}</text>')
                ty += line_h
    # === 空位（可继续深挖） ===
    for i, (code, px, py) in enumerate(slots):
        if i in used_slots:
            continue
        cx, cy = pt((code, px, py))
        svg.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="none" '
                   f'stroke="#E0E0E0" stroke-width="2" stroke-dasharray="5,5"/>')
        svg.append(f'<text x="{cx:.1f}" y="{cy-3:.1f}" text-anchor="middle" font-size="10" '
                   f'fill="#9E9E9E">{esc(code)}</text>')
        svg.append(f'<text x="{cx:.1f}" y="{cy+9:.1f}" text-anchor="middle" font-size="8" '
                   f'fill="#BDBDBD">空位</text>')

    # === 替补席（位置不在阵型 / 同位置超额，一律收进来，绝不静默丢球员）===
    slot_counts = Counter(POS_ALIAS.get(s[0], s[0]) for s in slots)
    leftovers = []
    for key, queue in pos_queue.items():
        if not queue:
            continue
        names = "、".join(str(p.get("name", "")) for p in queue)
        raw_pos = queue[0].get("pos", key)
        if key in slot_counts:
            warnings.append(
                f"位置 {raw_pos} 在 {formation} 阵型中只有 {slot_counts[key]} 个槽，"
                f"多出 {len(queue)} 人：{names}（已转入替补席；请更换阵型，"
                f"或把多余球员放进 bench / 改打其他位置）")
        else:
            warnings.append(
                f"位置 {raw_pos} 不存在于 {formation} 阵型：「{names}」已放入替补席")
        leftovers.extend(queue)
    bench_all = leftovers + bench
    if bench_all:
        by = y1 + 120
        # 替补席标题
        svg.append(f'<text x="{x0+5}" y="{by}" font-size="13" font-weight="bold" '
                   f'fill="{TEXT_COLOR}">替补席（{len(bench_all)}人）</text>')
        # 替补内容（标题下方开始）：完整显示，长名缩字号，不截断
        by += 40
        bx = x0 + 15
        for p in bench_all:
            if bx > x1 - 40:
                bx = x0 + 15
                by += 80
            svg.append(f'<circle cx="{bx}" cy="{by}" r="24" fill="{BENCH_COLOR}" '
                       f'stroke="#fff" stroke-width="2"/>')
            svg.append(f'<text x="{bx}" y="{by+3}" text-anchor="middle" font-size="7" '
                       f'fill="#fff">SUB</text>')
            lines = wrap_name(p.get("name", ""), max_chars=9)
            bench_max_w = 66
            fs = min((fit_font_size(ln, bench_max_w, 9, min_size=6) for ln in lines),
                     default=9)
            line_h = fs * 1.3
            ty = by + 38 + fs
            for ln in lines:
                svg.append(f'<text x="{bx}" y="{ty:.1f}" text-anchor="middle" '
                           f'font-size="{fs}" font-weight="bold" fill="{TEXT_COLOR}">'
                           f'{esc(ln)}</text>')
                ty += line_h
            bx += 74

    return warnings


def _bench_rows(team_data, formation, box_w):
    """估算某一队替补席占用的行数。

    含两类落单球员：位置代码不在阵型中的、同位置超额（槽位用完仍多出）的，
    与 draw_team() 实际收进替补席的口径保持一致，保证画布高度足够、不裁切。
    """
    players = team_data.get("players", [])
    slot_counts = Counter(POS_ALIAS.get(s[0], s[0])
                          for s in FORMATIONS.get(formation, []))
    pos_count = Counter(POS_ALIAS.get(p.get("pos", ""), p.get("pos", ""))
                        for p in players)
    leftovers = 0
    for key, cnt in pos_count.items():
        leftovers += cnt - slot_counts[key] if key in slot_counts else cnt
    n = leftovers + len(team_data.get("bench", []))
    if n == 0:
        return 0
    per_row = max(1, int((box_w - 55) / 74))
    return math.ceil(n / per_row)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="把知识阵容 JSON 渲染成足球场 SVG 阵型图")
    parser.add_argument("input", help="输入阵容 JSON 路径")
    parser.add_argument("output", help="输出 SVG 路径")
    parser.add_argument("--strict", action="store_true",
                        help="存在任何警告时以退出码 3 结束（交付前自检用）")
    args = parser.parse_args(argv)

    try:
        with open(args.input, "r", encoding="utf-8") as f:
            team = json.load(f)
    except FileNotFoundError:
        print(f"❌ 找不到输入文件：{args.input}", file=sys.stderr)
        sys.exit(2)
    except json.JSONDecodeError as e:
        print(f"❌ 输入 JSON 解析失败（第 {e.lineno} 行第 {e.colno} 列）：{e.msg}",
              file=sys.stderr)
        sys.exit(2)

    topic = team.get("topic", "未命名主题")
    formation = team.get("formation", "4-3-3")
    b_team = team.get("b_team")

    # 画布高度随替补席行数自适应，保证多替补/长名字不被裁切
    if b_team:
        rows_a = _bench_rows(team, formation, 700)
        rows_b = _bench_rows(b_team, b_team.get("formation", "4-3-3"), 700)
        rows = max(rows_a, rows_b)
    else:
        rows = _bench_rows(team, formation, 1500)
    # 球场底 1100，替补标题 +120，每行 80，底部留白
    canvas_height = max(1570, 1300 + rows * 80 + 60)

    svg = []
    warnings_all = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="{canvas_height}" '
               f'viewBox="0 0 1600 {canvas_height}" '
               f'font-family="\'PingFang SC\',\'Microsoft YaHei\','
               f'\'Noto Sans CJK SC\',sans-serif">')
    svg.append(f'<rect width="1600" height="{canvas_height}" fill="#F4F7F2"/>')

    try:
        if b_team:
            main_box = (50, 280, 750, 1100)
            b_box = (850, 280, 1550, 1100)
            warnings_all += [f"[主队] {w}" for w in draw_team(
                svg, main_box, formation, team.get("coach"), team.get("players", []),
                team.get("bench", []), team.get("flow"), topic, clip_id="pitch_main")]
            bt = b_team.get("topic", topic + "·进阶")
            warnings_all += [f"[B队] {w}" for w in draw_team(
                svg, b_box, b_team.get("formation", "4-3-3"),
                b_team.get("coach"), b_team.get("players", []),
                b_team.get("bench", []), b_team.get("flow"), bt,
                team_label="B 队", b_team=True, clip_id="pitch_b", flip=True)]
        else:
            main_box = (50, 280, 1550, 1100)
            warnings_all += [f"[主队] {w}" for w in draw_team(
                svg, main_box, formation, team.get("coach"), team.get("players", []),
                team.get("bench", []), team.get("flow"), topic, clip_id="pitch_main")]
    except ValueError as e:
        # 不支持的阵型等用户输入错误：给中文友好提示，不抛裸 Traceback
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:  # noqa: BLE001 兜底：任何意外都不得静默或裸 Traceback
        print(f"❌ 阵型图生成失败：{type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(2)

    svg.append('</svg>')
    with open(args.output, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"✅ 已生成阵型图: {args.output}")

    if warnings_all:
        for w in warnings_all:
            print(f"⚠️  {w}", file=sys.stderr)
        if args.strict:
            print("❌ --strict 模式下存在警告，以退出码 3 结束；请修正 JSON 后重新渲染",
                  file=sys.stderr)
            sys.exit(3)


if __name__ == "__main__":
    main()