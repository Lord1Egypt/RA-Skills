#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
医疗设备合规评分器 (Medical Device Compliance Grader)
=====================================================
8 大合规维度 0-5 分制评分，生成自包含 HTML 评分卡报告（雷达图 + 明细表 + 改进建议）。

用法:
    python grade_compliance.py --demo                          # 生成示例报告
    python grade_compliance.py --input scores.json --out report.html
    python grade_compliance.py --input scores.json --out report.html --json result.json

无第三方依赖，纯标准库；雷达图用 SVG 绘制，报告为单个自包含 HTML。
作者: 注册老炮 | 用途: 合规自评工具（不构成监管裁定）
"""

import argparse
import json
import os
import sys
import math
from datetime import date

DIMENSIONS = [
    ("D1", "注册路径与分类", "Regulatory Pathway & Classification"),
    ("D2", "技术文件完整性", "Technical Documentation Completeness"),
    ("D3", "风险管理", "Risk Management"),
    ("D4", "临床评价", "Clinical Evaluation"),
    ("D5", "标签与说明书", "Labeling & IFU"),
    ("D6", "软件与网络安全", "Software & Cybersecurity"),
    ("D7", "上市后监管", "Post-Market Surveillance"),
    ("D8", "质量体系", "QMS / GMP"),
]

ANCHORS = {
    0: "缺失", 1: "仅提及", 2: "部分成文",
    3: "基本完整", 4: "完整可查证", 5: "标杆级",
}

ADVICE = {
    "D1": "先做分类界定/路径判定（官方分类目录或分类界定申请），明确产品类别再启动后续工作",
    "D2": "以 STED 六章搭骨架，按目标市场官方模板（MDR Annex II / 121号公告）补全缺失章节",
    "D3": "立即补风险管理报告（ISO 14971 六步流程），与验证/临床文件建立互相引用闭环",
    "D4": "先做临床评价路径判定（免临床/同品种/临床试验），再按官方模板（MDCG 2020-13）撰写 CER",
    "D5": "按标签要素检查表 + IFU 内容框架逐项补全，符号使用 ISO 15223-1，复核版本时效",
    "D6": "先判定软件身份与风险分类（IMDRF N12 / 三级关注 / MDR 规则11），再按 IEC 62304 搭文档并做网络安全评估",
    "D7": "建立 PMS 计划 + 不良事件监测报告流程，明确各市场（美国/欧盟/中国/日本）报告时限",
    "D8": "建立/完善质量体系文件与设计控制记录（DHF），安排内审并闭环 CAPA",
}

COLORS = {
    0: "#c0392b", 1: "#e67e22", 2: "#f1c40f",
    3: "#27ae60", 4: "#16a085", 5: "#0e6655",
}

DEFAULT_SCORES = {
    "product": "示例产品（关节镜用复用外科器械）",
    "market": "中国 II 类 / 欧盟 MDR IIa / 美国 510(k)",
    "date": date.today().isoformat(),
    "scores": {
        "D1": {"score": 4, "note": "分类已按目录确认，路径已定"},
        "D2": {"score": 3, "note": "STED 骨架已搭，验证章节待补"},
        "D3": {"score": 2, "note": "风险管理报告初稿，缺控制措施验证记录"},
        "D4": {"score": 1, "note": "尚未启动临床评价路径判定"},
        "D5": {"score": 3, "note": "标签草稿已有，缺 UDI 与符号核验"},
        "D6": {"score": "N/A", "note": "纯无源器械，无软件"},
        "D7": {"score": 2, "note": "PMS 计划未建，不良事件渠道已接入"},
        "D8": {"score": 3, "note": "ISO 13485 体系运行中，DHF 待完善"},
    },
}


def parse_score(value):
    """解析单个维度分值，返回 (数值或 None, 是否为 N/A)"""
    if isinstance(value, int):
        return value, False
    if isinstance(value, str):
        v = value.strip().upper()
        if v in ("N/A", "NA", "NA/", "不适用", "-"):
            return None, True
        try:
            return int(float(v)), False
        except ValueError:
            raise ValueError(f"无法解析分值: {value!r}")
    if isinstance(value, float) and value == int(value):
        return int(value), False
    raise ValueError(f"无法解析分值: {value!r}")


def load_input(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def grade(data):
    """计算各维分数与总评，返回结构化结果"""
    scores_in = data.get("scores", {})
    items = []
    applicable = []
    for key, zh, en in DIMENSIONS:
        entry = scores_in.get(key, {"score": 0, "note": ""})
        value, is_na = parse_score(entry.get("score", 0))
        note = entry.get("note", "")
        if is_na:
            items.append({"key": key, "zh": zh, "en": en, "na": True,
                          "score": None, "label": "N/A", "color": "#95a5a6", "note": note})
        else:
            if value is None or value < 0 or value > 5:
                raise ValueError(f"{key} 分值必须在 0-5 之间或 N/A，收到: {entry.get('score')!r}")
            items.append({"key": key, "zh": zh, "en": en, "na": False,
                          "score": value, "label": f"{value} · {ANCHORS[value]}",
                          "color": COLORS.get(value, "#333"), "note": note})
            applicable.append(value)

    avg = sum(applicable) / len(applicable) if applicable else 0.0
    if avg >= 4.0:
        grade_label, grade_desc = "A（优）", "可支撑申报/持续合规，短板已可控"
    elif avg >= 3.0:
        grade_label, grade_desc = "B（良）", "基本可申报，存在待补项（建议整改后申报）"
    elif avg >= 2.0:
        grade_label, grade_desc = "C（中）", "缺项较多，须系统补全后再申报"
    else:
        grade_label, grade_desc = "D（差）", "证据严重不足，先建体系再谈申报"

    advice = [ADVICE[it["key"]] for it in items
              if not it["na"] and it["score"] is not None and it["score"] <= 2]

    return {
        "product": data.get("product", "未命名产品"),
        "market": data.get("market", "未填写"),
        "date": data.get("date", date.today().isoformat()),
        "items": items,
        "avg": round(avg, 2),
        "applicable_count": len(applicable),
        "grade": grade_label,
        "grade_desc": grade_desc,
        "advice": advice,
        "low_dimensions": [it["zh"] for it in items
                           if not it["na"] and it["score"] is not None and it["score"] <= 2],
    }


def render_radar_svg(items, size=520):
    """用 SVG 绘制 8 维雷达图（N/A 维度跳过）"""
    na_keys = {it["key"] for it in items if it["na"]}
    active = [it for it in items if not it["na"]]
    n = len(active)
    if n == 0:
        return "<text x='260' y='260' text-anchor='middle'>无适用维度</text>"

    cx = cy = size / 2
    radius = size * 0.36
    start_angle = -90.0  # 12 点方向开始

    def point(angle_deg, r):
        rad = math.radians(angle_deg)
        return cx + r * math.cos(rad), cy + r * math.sin(rad)

    angle_step = 360.0 / n
    label_r = radius + 30

    svg = [f'<svg viewBox="0 0 {size} {size}" width="100%" style="max-width:{size}px;margin:0 auto;display:block">']
    # 网格圆（0-5）
    for level in range(1, 6):
        r = radius * level / 5
        pts = " ".join(f"{point(start_angle + i * angle_step, r)[0]:.1f},{point(start_angle + i * angle_step, r)[1]:.1f}"
                       for i in range(n))
        svg.append(f'<polygon points="{pts}" fill="none" stroke="#d5d8dc" stroke-width="1"/>')
    # 轴线
    for i in range(n):
        x, y = point(start_angle + i * angle_step, radius)
        svg.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="#d5d8dc" stroke-width="1"/>')
    # 数据多边形
    poly = []
    for i, it in enumerate(active):
        r = radius * it["score"] / 5
        x, y = point(start_angle + i * angle_step, r)
        poly.append(f"{x:.1f},{y:.1f}")
    svg.append(f'<polygon points="{" ".join(poly)}" fill="rgba(41,128,185,0.25)" stroke="#2980b9" stroke-width="2.5"/>')
    # 数据点
    for i, it in enumerate(active):
        r = radius * it["score"] / 5
        x, y = point(start_angle + i * angle_step, r)
        svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{it["color"]}" stroke="#fff" stroke-width="1.5"/>')
    # 标签
    for i, it in enumerate(active):
        x, y = point(start_angle + i * angle_step, label_r)
        anchor = "middle"
        if abs(x - cx) > 20:
            anchor = "start" if x > cx else "end"
        svg.append(
            f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-size="14" fill="#2c3e50">'
            f'{it["zh"]}<tspan x="{x:.1f}" dy="16" font-size="11" fill="{it["color"]}" font-weight="bold">'
            f'{it["score"]}分</tspan></text>'
        )
    svg.append("</svg>")
    return "".join(svg)


def render_html(result):
    radar = render_radar_svg(result["items"])

    rows = []
    for it in result["items"]:
        note = (it["note"] or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        rows.append(
            f"<tr>"
            f"<td style='padding:10px;border-bottom:1px solid #ecf0f1'><b>{it['key']}</b></td>"
            f"<td style='padding:10px;border-bottom:1px solid #ecf0f1'>{it['zh']}</td>"
            f"<td style='padding:10px;border-bottom:1px solid #ecf0f1'><span style='display:inline-block;padding:4px 12px;border-radius:20px;color:#fff;background:{it['color']};font-weight:bold'>{it['label']}</span></td>"
            f"<td style='padding:10px;border-bottom:1px solid #ecf0f1;color:#555'>{note or '—'}</td>"
            f"</tr>"
        )

    advice_html = ""
    if result["advice"]:
        advice_html = "<div style='background:#fdf3e7;border-left:4px solid #e67e22;padding:14px 18px;border-radius:6px;margin-top:18px'><h3 style='margin:0 0 8px;color:#b9770e'>⚠️ 短板维度改进建议（≤2 分）</h3><ul style='margin:0;padding-left:20px;line-height:1.8'>" + "".join(
            f"<li>{a}</li>" for a in result["advice"]) + "</ul></div>"
    else:
        advice_html = "<div style='background:#eafaf1;border-left:4px solid #27ae60;padding:14px 18px;border-radius:6px;margin-top:18px'><b style='color:#1e8449'>✓ 无 ≤2 分短板维度，整体合规状态良好</b></div>"

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>医疗器械合规评分卡 · {result["product"]}</title>
<style>
  body {{ font-family: "Microsoft YaHei", "PingFang SC", sans-serif; background:#f4f6f7; margin:0; padding:24px; color:#2c3e50; }}
  .card {{ max-width:1080px; margin:0 auto; background:#fff; border-radius:12px; box-shadow:0 2px 12px rgba(0,0,0,.08); overflow:hidden; }}
  .header {{ background:linear-gradient(135deg,#1a5276,#2980b9); color:#fff; padding:24px 28px; }}
  .header h1 {{ margin:0 0 6px; font-size:22px; }}
  .header p {{ margin:2px 0; opacity:.9; font-size:13px; }}
  .body {{ padding:24px 28px; }}
  .grade-box {{ display:flex; align-items:center; gap:24px; flex-wrap:wrap; background:#f8f9fa; border:1px solid #e5e8ec; border-radius:8px; padding:16px 20px; margin-bottom:20px; }}
  .grade-big {{ font-size:40px; font-weight:bold; color:#1a5276; }}
  .grade-label {{ font-size:18px; font-weight:bold; }}
  .grade-desc {{ color:#666; font-size:13px; margin-top:4px; }}
  table {{ width:100%; border-collapse:collapse; margin-top:8px; }}
  th {{ text-align:left; background:#f0f3f5; padding:10px; border-bottom:2px solid #d5d8dc; font-size:13px; color:#555; }}
  td {{ font-size:13px; }}
  .footer {{ padding:16px 28px; background:#f8f9fa; color:#7f8c8d; font-size:12px; border-top:1px solid #ecf0f1; }}
</style>
</head>
<body>
<div class="card">
  <div class="header">
    <h1>医疗器械合规评分卡</h1>
    <p>产品：{result["product"]}</p>
    <p>目标市场：{result["market"]} ｜ 评估日期：{result["date"]}</p>
    <p>评估工具：medical-device-compliance-grader v1.0.0（自评工具，不构成监管裁定）</p>
  </div>
  <div class="body">
    <div class="grade-box">
      <div>
        <div class="grade-big">{result["avg"]:.2f}</div>
        <div style="color:#999;font-size:12px">适用维度均分（{result["applicable_count"]} 维）</div>
      </div>
      <div>
        <div class="grade-label">等级：{result["grade"]}</div>
        <div class="grade-desc">{result["grade_desc"]}</div>
      </div>
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:24px;flex-wrap:wrap">
      <div>{radar}</div>
      <div>
        <h3 style="margin-top:0">维度评分明细</h3>
        <table>
          <tr><th>维度</th><th>名称</th><th>分值</th><th>证据备注</th></tr>
          {''.join(rows)}
        </table>
      </div>
    </div>
    {advice_html}
  </div>
  <div class="footer">
    生成时间：{date.today().isoformat()} ｜ 评分锚点：0=缺失 · 1=仅提及 · 2=部分成文 · 3=基本完整 · 4=完整可查证 · 5=标杆级 ｜ N/A 维度不计入总分
  </div>
</div>
</body>
</html>"""
    return html


def main():
    parser = argparse.ArgumentParser(description="医疗设备合规评分器")
    parser.add_argument("--demo", action="store_true", help="生成示例评分卡")
    parser.add_argument("--input", help="评分输入 JSON 文件路径")
    parser.add_argument("--out", default="compliance_scorecard.html", help="输出 HTML 报告路径")
    parser.add_argument("--json", help="同时输出 JSON 结果路径")
    args = parser.parse_args()

    if args.demo:
        data = DEFAULT_SCORES
    elif args.input:
        data = load_input(args.input)
    else:
        parser.print_help()
        sys.exit(1)

    try:
        result = grade(data)
    except ValueError as e:
        print(f"[错误] {e}", file=sys.stderr)
        sys.exit(2)

    html = render_html(result)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[OK] 评分卡已生成: {args.out}")
    print(f"     产品: {result['product']} | 均分: {result['avg']:.2f} | 等级: {result['grade']}")

    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"[OK] JSON 结果已生成: {args.json}")


if __name__ == "__main__":
    main()
