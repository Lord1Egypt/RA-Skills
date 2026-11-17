#!/usr/bin/env python3
r"""协作雷达 v0.4.4 雷达图可视化模块。

将 7 模块协作状态卡片转化为一张 SVG 蜘蛛网图（radar / spider chart），
7 个维度分别衡量项目协作信息的健康度和完整度。

    进展透明度  ──── 决策确定度
       \             /
  证据完整度    待办健康度
       /             \
    确认负担  ──── 风险可控度
           协作畅通度

纯 Python 标准库，零依赖。SVG 可直接在浏览器中预览或嵌入文档。

CLI:
  python radar_chart.py generate --card card.json --out radar.svg
  python radar_chart.py scores   --card card.json            # 只看分数
  python radar_chart.py selftest
"""

from __future__ import annotations

import argparse
import html
import json
import math
import sys
from pathlib import Path
from typing import Any

from process import RadarInputError, _load_json, write_output_text

# ---------------------------------------------------------------------------
# SVG 画布常量
# ---------------------------------------------------------------------------
SVG_WIDTH = 600
SVG_HEIGHT = 520
CENTER_X = SVG_WIDTH // 2
CENTER_Y = 230
RADIUS = 180
LEVELS = 5                     # 同心圆层数（每层 20 分）
LABEL_OFFSET = 22              # 轴标签离最外圈的距离
TABLE_Y = 440                  # 分数表起始 y

# 配色：浅色背景（仅 deep green accent）
GRID_COLOR = "#d4d4d8"
AXIS_COLOR = "#a1a1aa"
POLYGON_FILL = "rgba(22,163,74,0.18)"
POLYGON_STROKE = "#16a34a"
DOT_COLOR = "#16a34a"
LABEL_COLOR = "#27272a"
TABLE_BORDER = "#e4e4e7"
TABLE_HEADER_BG = "#f0fdf4"

# ---------------------------------------------------------------------------
# 7 维度定义（顺序决定从顶部顺时针排列）
# ---------------------------------------------------------------------------
DIMENSIONS = [
    ("progress_clarity",   "进展透明度",  "进展项的证据覆盖率"),
    ("decision_certainty", "决策确定度",  "决策有 confirmed_by 的比例"),
    ("task_health",        "待办健康度",  "待办 Owner+DDL 完备率，无冲突"),
    ("risk_control",       "风险可控度",  "风险项有应对措施的比例"),
    ("collab_flow",        "协作畅通度",  "跨部门关系的透明度"),
    ("evidence_coverage",  "证据完整度",  "全卡片五项的证据覆盖率"),
    ("confirmation_debt",  "确认负担",    "待确认积压量，越少越健康"),
]


# ---------------------------------------------------------------------------
# 分数计算引擎
# ---------------------------------------------------------------------------
def compute_scores(card: dict) -> dict[str, float]:
    """从 7 模块卡片中计算各维度健康分（0–100）。

    规则概要：
    - 某模块有内容 → 根据内容完备度打分
    - 某模块为空  → 100（没有内容 = 没��坏信号）
    - 确认负担是反向指标：0 条待确认 = 100 分，4+ 条 = 0 分
    """
    scores: dict[str, float] = {}

    # ── 进展透明度 ──
    items = card.get("progress")
    if isinstance(items, list) and items:
        ok = sum(1 for p in items if isinstance(p, dict)
                 and p.get("evidence") and p["evidence"] != "未提供")
        scores["progress_clarity"] = round(ok / len(items) * 100, 1)
    else:
        scores["progress_clarity"] = 100.0

    # ── 决策确定度 ──
    items = card.get("confirmed_decisions")
    if isinstance(items, list) and items:
        ok = sum(1 for d in items if isinstance(d, dict)
                 and d.get("confirmed_by") and d["confirmed_by"] not in ("未提供", ""))
        scores["decision_certainty"] = round(ok / len(items) * 100, 1)
    else:
        scores["decision_certainty"] = 100.0

    # ── 待办健康度 ──
    items = card.get("action_items")
    if isinstance(items, list) and items:
        healthy = 0
        for a in items:
            if not isinstance(a, dict):
                continue
            has_owner = a.get("owner") and a["owner"] not in ("未提供", "")
            has_ddl = a.get("ddl") and a["ddl"] not in ("未提供", "")
            no_conflict = not a.get("conflict")
            if has_owner and has_ddl and no_conflict:
                healthy += 1
        scores["task_health"] = round(healthy / len(items) * 100, 1)
    else:
        scores["task_health"] = 100.0

    # ── 风险可控度 ──
    items = card.get("risks_dependencies")
    if isinstance(items, list) and items:
        ok = sum(1 for r in items if isinstance(r, dict)
                 and r.get("mitigation") and r["mitigation"] not in ("未提供", ""))
        scores["risk_control"] = round(ok / len(items) * 100, 1)
    else:
        scores["risk_control"] = 100.0

    # ── 协作畅通度 ──
    items = card.get("cross_department_relationships")
    if isinstance(items, list) and items:
        ok = sum(1 for c in items if isinstance(c, dict)
                 and c.get("evidence") and c["evidence"] != "未提供")
        scores["collab_flow"] = round(ok / len(items) * 100, 1)
    else:
        scores["collab_flow"] = 100.0

    # ── 证据完整度 ──
    ev_keys = [
        "progress", "confirmed_decisions", "action_items",
        "risks_dependencies", "cross_department_relationships",
        "needs_human_confirmation",
    ]
    all_items: list[dict] = []
    for k in ev_keys:
        section = card.get(k, [])
        if isinstance(section, list):
            all_items.extend([i for i in section if isinstance(i, dict)])
    if all_items:
        ev_ok = sum(1 for i in all_items
                    if i.get("evidence") and i["evidence"] != "未提供")
        scores["evidence_coverage"] = round(ev_ok / len(all_items) * 100, 1)
    else:
        scores["evidence_coverage"] = 50.0  # 无数据 = 中性

    # ── 确认负担（反向） ──
    nhc = card.get("needs_human_confirmation")
    count = len(nhc) if isinstance(nhc, list) else 0
    scores["confirmation_debt"] = round(max(0, 100 - count * 25), 1)

    return scores


# ---------------------------------------------------------------------------
# SVG 生成
# ---------------------------------------------------------------------------
def _axis_point(angle: float, level: float, radius: float = RADIUS) -> tuple[float, float]:
    """角度 + 层级 → 画布坐标。level 0=圆心, 1=最外圈。"""
    x = CENTER_X + radius * level * math.cos(angle)
    y = CENTER_Y + radius * level * math.sin(angle)
    return x, y


def _path_points(scores: dict[str, float]) -> str:
    """按顺序生成数据多边形路径字符串。"""
    n = len(DIMENSIONS)
    pts = []
    for i, (key, _, _) in enumerate(DIMENSIONS):
        angle = -math.pi / 2 + i * 2 * math.pi / n
        level = min(scores.get(key, 0), 100) / 100
        x, y = _axis_point(angle, level)
        pts.append(f"{x:.1f},{y:.1f}")
    return " ".join(pts)


def generate_svg(scores: dict[str, float], title: str = "协作健康雷达") -> str:
    """生成完整 SVG 蜘蛛网图。"""
    n = len(DIMENSIONS)

    lines: list[str] = []
    lines.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}"'
        f' width="{SVG_WIDTH}" height="{SVG_HEIGHT}"'
        f' font-family="system-ui, -apple-system, sans-serif">'
    )
    lines.append(f'<rect width="{SVG_WIDTH}" height="{SVG_HEIGHT}" fill="#ffffff"/>')

    # ── 标题 ──
    lines.append(
        f'<text x="{CENTER_X}" y="28" text-anchor="middle"'
        f' font-size="18" font-weight="700" fill="{LABEL_COLOR}">{html.escape(title, quote=True)}</text>'
    )

    # ── 背景网格（同心多边形 + 轴线） ──
    for level in range(1, LEVELS + 1):
        lv = level / LEVELS
        pts = []
        for i in range(n):
            angle = -math.pi / 2 + i * 2 * math.pi / n
            x, y = _axis_point(angle, lv)
            pts.append(f"{x:.1f},{y:.1f}")
        poly = " ".join(pts)
        lines.append(
            f'<polygon points="{poly}" fill="none" stroke="{GRID_COLOR}"'
            f' stroke-width="1"/>'
        )
        # 分数标签（左侧第一层）
        lines.append(
            f'<text x="{CENTER_X}" y="{CENTER_Y - RADIUS * lv + 4}"'
            f' text-anchor="middle" font-size="9" fill="#a1a1aa">{level * 20}</text>'
        )

    # 轴线
    for i, (key, _, _) in enumerate(DIMENSIONS):
        angle = -math.pi / 2 + i * 2 * math.pi / n
        x1, y1 = _axis_point(angle, 0)
        x2, y2 = _axis_point(angle, 1)
        lines.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"'
            f' stroke="{AXIS_COLOR}" stroke-width="1"/>'
        )

    # ── 数据多边形 ──
    data_pts = _path_points(scores)
    lines.append(
        f'<polygon points="{data_pts}" fill="{POLYGON_FILL}"'
        f' stroke="{POLYGON_STROKE}" stroke-width="2.2"/>'
    )

    # 顶点圆点
    for i, (key, _, _) in enumerate(DIMENSIONS):
        angle = -math.pi / 2 + i * 2 * math.pi / n
        level = min(scores.get(key, 0), 100) / 100
        x, y = _axis_point(angle, level)
        lines.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="{DOT_COLOR}"/>')
        # 顶上写分数
        score_label_y = y - 10 if y < CENTER_Y else y + 14
        lines.append(
            f'<text x="{x:.1f}" y="{score_label_y:.1f}" text-anchor="middle"'
            f' font-size="10" font-weight="600" fill="{DOT_COLOR}">{scores.get(key, 0):.0f}</text>'
        )

    # ── 轴标签（外圈外侧） ──
    for i, (key, dim_label, _) in enumerate(DIMENSIONS):
        angle = -math.pi / 2 + i * 2 * math.pi / n
        lx, ly = _axis_point(angle, 1 + LABEL_OFFSET / RADIUS)
        lines.append(
            f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="middle"'
            f' font-size="12" fill="{LABEL_COLOR}">{dim_label}</text>'
        )

    # ── 底部分数表 ──
    col_w = 180
    row_h = 22
    table_start_x = CENTER_X - col_w * 1.5
    # 表头
    lines.append(
        f'<rect x="{table_start_x}" y="{TABLE_Y}" width="{col_w * 3}"'
        f' height="{row_h}" fill="{TABLE_HEADER_BG}" stroke="{TABLE_BORDER}" stroke-width="1"/>'
    )
    lines.append(
        f'<text x="{table_start_x + 8}" y="{TABLE_Y + 15}" font-size="11"'
        f' font-weight="600" fill="{LABEL_COLOR}">维度</text>'
    )
    lines.append(
        f'<text x="{table_start_x + col_w + 8}" y="{TABLE_Y + 15}" font-size="11"'
        f' font-weight="600" fill="{LABEL_COLOR}">说明</text>'
    )
    lines.append(
        f'<text x="{table_start_x + col_w * 2 + 8}" y="{TABLE_Y + 15}" font-size="11"'
        f' font-weight="600" fill="{LABEL_COLOR}">分数</text>'
    )

    for j, (key, dim_label, dim_desc) in enumerate(DIMENSIONS):
        y = TABLE_Y + row_h + j * row_h
        bg = "#fafafa" if j % 2 == 0 else "#ffffff"
        lines.append(
            f'<rect x="{table_start_x}" y="{y}" width="{col_w * 3}" height="{row_h}"'
            f' fill="{bg}" stroke="{TABLE_BORDER}" stroke-width="0.5"/>'
        )
        lines.append(
            f'<text x="{table_start_x + 8}" y="{y + 15}" font-size="11"'
            f' fill="{LABEL_COLOR}">{dim_label}</text>'
        )
        lines.append(
            f'<text x="{table_start_x + col_w + 8}" y="{y + 15}" font-size="10"'
            f' fill="#71717a">{dim_desc}</text>'
        )
        val = scores.get(key, 0)
        color = "#16a34a" if val >= 70 else ("#eab308" if val >= 40 else "#ef4444")
        lines.append(
            f'<text x="{table_start_x + col_w * 2 + 8}" y="{y + 15}" font-size="12"'
            f' font-weight="600" fill="{color}">{val:.0f}</text>'
        )

    lines.append("</svg>")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def _load_card_json(path: str) -> dict:
    return _load_json(Path(path))


def _selftest() -> int:
    print("== 协作雷达 v0.4.4 雷达图模块自测 ==")
    fails = 0

    sample = {
        "project_overview": {"project_name": "X", "summary": "正常推进"},
        "progress": [
            {"item": "设计完成", "evidence": "评审通过"},
            {"item": "开发中", "evidence": "未提供"},
        ],
        "confirmed_decisions": [
            {"decision": "用方案A", "result": "已拍板", "confirmed_by": "张三", "evidence": "会议纪要"},
        ],
        "action_items": [
            {"task": "联调", "owner": "李四", "ddl": "下周三", "evidence": "群聊"},
            {"task": "写文档", "owner": "未提供", "ddl": "未提供", "evidence": "未提供", "conflict": "存在冲突，需人工确认"},
        ],
        "risks_dependencies": [
            {"type": "风险", "description": "依赖外部", "mitigation": "预案", "evidence": "复盘"},
        ],
        "cross_department_relationships": [
            {"from": "产品", "to": "研发", "collaboration_item": "需求澄清", "evidence": "会议"},
        ],
        "needs_human_confirmation": [{"item": "预算", "reason": "超支"}],
    }

    # T1: 分数计算
    scores = compute_scores(sample)
    ok = (0 <= scores["task_health"] <= 100
          and scores["decision_certainty"] == 100.0
          and scores["risk_control"] == 100.0
          and scores["confirmation_debt"] == 75.0)
    print(("PASS" if ok else "FAIL"), "T1 分数计算逻辑:", {k: v for k, v in sorted(scores.items())})
    fails += 0 if ok else 1

    # T2: SVG 生成（含 7 维度标签和分数）
    svg = generate_svg(scores, "测试雷达")
    ok = ("<svg" in svg and "</svg>" in svg
          and "进展透明度" in svg and "待办健康度" in svg
          and "测试雷达" in svg)
    print(("PASS" if ok else "FAIL"), "T2 SVG 结构完整:", len(svg), "字节")
    fails += 0 if ok else 1

    # T3: 对抗——空卡片
    empty = {}
    scores_e = compute_scores(empty)
    ok = all(0 <= v <= 100 for v in scores_e.values())
    print(("PASS" if ok else "FAIL"), "T3 空卡片不崩溃:", {k: v for k, v in sorted(scores_e.items())})
    fails += 0 if ok else 1

    # T4: SVG 写出成功
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "test.svg"
        out.write_text(svg, encoding="utf-8")
        ok = out.exists() and out.stat().st_size > 500
        print(("PASS" if ok else "FAIL"), "T4 SVG 落盘成功:", out.stat().st_size, "字节")
        fails += 0 if ok else 1

    # T5: XSS 防护 —— 标题中 & < > " ' 必须被转义，且 <script> 不 应以源码形式出现在 SVG 中
    xss_title = '<script>alert(1)</script>&"x"'
    svg_xss = generate_svg(scores, xss_title)
    ok = (
        "&lt;script&gt;" in svg_xss
        and "&amp;" in svg_xss
        and "&quot;" in svg_xss
        and "<script>" not in svg_xss
    )
    print(("PASS" if ok else "FAIL"), "T5 XSS 标题转义:", "&lt;script&gt;" in svg_xss)
    fails += 0 if ok else 1

    print("=" * 40)
    if fails == 0:
        print("ALL PASS -- v0.4.4 雷达图模块自检通过")
        return 0
    print(f"{fails} 项失败 (FAIL)")
    return 1


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="radar_chart", description="协作雷达 SVG 雷达图生成器")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_gen = sub.add_parser("generate", help="生成 SVG 雷达图")
    p_gen.add_argument("--card", required=True, help="协作状态卡片 JSON 路径")
    p_gen.add_argument("--out", required=True, help="新的输出 SVG 路径")
    p_gen.add_argument("--force", action="store_true", help="明确替换已存在的命名输出文件")
    p_gen.add_argument("--title", default="协作健康雷达", help="图表标题")

    sub.add_parser("scores", help="只输出各维度分数 JSON").add_argument("--card", required=True)

    sub.add_parser("selftest", help="运行雷达图模块自检")

    args = parser.parse_args(argv)

    if args.cmd == "selftest":
        return _selftest()

    if args.cmd == "scores":
        card = _load_card_json(args.card)
        print(json.dumps(compute_scores(card), ensure_ascii=False, indent=2))
        return 0

    if args.cmd == "generate":
        card = _load_card_json(args.card)
        scores = compute_scores(card)
        svg = generate_svg(scores, args.title)
        write_output_text(
            Path(args.out),
            svg,
            protected_paths=[Path(args.card)],
            force=args.force,
        )
        print(f"雷达图已生成 -> {args.out} ({len(svg)} 字节)")
        return 0

    return 1


def _cli_entry(argv: list[str]) -> int:
    try:
        return main(argv)
    except RadarInputError as e:
        print(f"[输入错误] {e}", file=sys.stderr)
        return 2
    except SystemExit as e:
        return int(e.code) if e.code is not None else 1
    except Exception as e:
        print(f"[意外错误] {type(e).__name__}: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(_cli_entry(sys.argv[1:]))
