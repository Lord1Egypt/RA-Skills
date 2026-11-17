#!/usr/bin/env python3
"""
MAGI 风险矩阵生成工具
支持两种输出模式：
1. 终端文本矩阵（默认）
2. HTML可视化矩阵（--html 参数）

风险等级计算：概率(1-5) × 影响(1-5) = 风险值(1-25)
- 20-25: 🔴 红色（极高风险）
- 12-19: 🟠 橙色（高风险）
- 5-11:  🟡 黄色（中等风险）
- 1-4:   🟢 绿色（低风险）
"""

import json
import sys
from typing import Optional


# ─── 风险等级定义 ───────────────────────────────────────────

RISK_LEVELS = {
    "red":    {"range": (20, 25), "label": "极高风险", "emoji": "🔴", "action": "立即升级处理，考虑暂停相关活动"},
    "orange": {"range": (12, 19), "label": "高风险",   "emoji": "🟠", "action": "制定专项缓解计划，密切监控"},
    "yellow": {"range": (5, 11),  "label": "中等风险", "emoji": "🟡", "action": "常规监控，准备应急预案"},
    "green":  {"range": (1, 4),   "label": "低风险",   "emoji": "🟢", "action": "接受风险，定期复查"},
}

PROBABILITY_LABELS = {1: "极低", 2: "低", 3: "中", 4: "高", 5: "极高"}
IMPACT_LABELS = {1: "轻微", 2: "较小", 3: "中等", 4: "严重", 5: "致命"}


def classify_risk(score: int) -> dict:
    """根据风险值返回风险等级信息"""
    for level, info in RISK_LEVELS.items():
        if info["range"][0] <= score <= info["range"][1]:
            return {"level": level, **info}
    return {"level": "unknown", "label": "未知", "emoji": "⚪", "action": "需要人工判断"}


def build_risk_entry(
    name: str,
    probability: int,
    impact: int,
    domain: str = "",
    source: str = "",
    reversibility: str = "",
    detectability: str = "",
    mitigation: str = "",
) -> dict:
    """
    构建单条风险记录。

    参数:
        name: 风险名称
        probability: 发生概率 (1-5)
        impact: 影响程度 (1-5)
        domain: 风险域（财务/执行/合规/声誉/时机/人心）
        source: 判断来源（MELCHIOR/BALTHASAR/CASPER）
        reversibility: 可逆性（可逆/部分可逆/不可逆）
        detectability: 可检测性（可提前预警/事后才发现/无法检测）
        mitigation: 缓解措施
    """
    score = probability * impact
    risk_info = classify_risk(score)

    return {
        "name": name,
        "domain": domain,
        "source": source,
        "probability": probability,
        "probability_label": PROBABILITY_LABELS.get(probability, "未知"),
        "impact": impact,
        "impact_label": IMPACT_LABELS.get(impact, "未知"),
        "score": score,
        "risk_level": risk_info["level"],
        "risk_emoji": risk_info["emoji"],
        "risk_label": risk_info["label"],
        "action": risk_info["action"],
        "reversibility": reversibility,
        "detectability": detectability,
        "mitigation": mitigation,
    }


def generate_text_matrix(risks: list) -> str:
    """生成终端文本格式的风险矩阵"""
    lines = []
    lines.append("=" * 70)
    lines.append("  MAGI 风险矩阵 — 三贤者战略参谋")
    lines.append("=" * 70)

    # 5×5 矩阵网格
    lines.append("")
    lines.append("  影响程度 →")
    lines.append("  概率 ↓   |  轻微(1)  较小(2)  中等(3)  严重(4)  致命(5)")
    lines.append("  " + "-" * 62)

    for p in range(5, 0, -1):
        row = f"  {PROBABILITY_LABELS[p]}({p}) |"
        for i in range(1, 6):
            score = p * i
            info = classify_risk(score)
            cell = f" {info['emoji']}{score:>2} "
            row += cell
        lines.append(row)

    lines.append("  " + "-" * 62)

    # 风险清单
    lines.append("")
    lines.append("  风险清单（按风险值降序）")
    lines.append("  " + "-" * 62)

    sorted_risks = sorted(risks, key=lambda r: r["score"], reverse=True)
    for i, r in enumerate(sorted_risks, 1):
        lines.append(f"  {i}. {r['risk_emoji']} {r['name']}")
        lines.append(f"     风险值: {r['score']} ({r['risk_label']})")
        lines.append(f"     概率: {r['probability_label']}({r['probability']}) × 影响: {r['impact_label']}({r['impact']})")
        if r["domain"]:
            lines.append(f"     风险域: {r['domain']} | 判断来源: {r['source']}")
        if r["reversibility"]:
            lines.append(f"     可逆性: {r['reversibility']} | 可检测性: {r['detectability']}")
        if r["mitigation"]:
            lines.append(f"     缓解措施: {r['mitigation']}")
        lines.append(f"     行动建议: {r['action']}")
        lines.append("")

    # 统计摘要
    level_counts = {"red": 0, "orange": 0, "yellow": 0, "green": 0}
    for r in risks:
        level_counts[r["risk_level"]] = level_counts.get(r["risk_level"], 0) + 1

    lines.append("  " + "-" * 62)
    lines.append("  统计摘要")
    lines.append(f"  🔴 极高风险: {level_counts['red']} 项")
    lines.append(f"  🟠 高风险:   {level_counts['orange']} 项")
    lines.append(f"  🟡 中等风险: {level_counts['yellow']} 项")
    lines.append(f"  🟢 低风险:   {level_counts['green']} 项")
    lines.append(f"  总计:        {len(risks)} 项")

    # 否决判定
    red_count = level_counts["red"]
    if red_count > 0:
        lines.append("")
        lines.append(f"  ⛔ 否决预警: 存在 {red_count} 项极高风险，建议暂停决策直至风险缓解")

    lines.append("=" * 70)
    return "\n".join(lines)


def generate_html_matrix(risks: list, output_path: str = "risk_matrix.html") -> str:
    """生成HTML格式的风险矩阵可视化"""

    COLOR_MAP = {
        "red": "#e74c3c",
        "orange": "#e67e22",
        "yellow": "#f1c40f",
        "green": "#2ecc71",
    }

    # 构建5×5网格数据
    grid = {}
    for r in risks:
        key = (r["probability"], r["impact"])
        if key not in grid:
            grid[key] = []
        grid[key].append(r)

    html = []
    html.append("""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>MAGI 风险矩阵</title>
<style>
  body { font-family: -apple-system, 'Segoe UI', sans-serif; background: #1a1a2e; color: #eee; padding: 40px; }
  h1 { text-align: center; color: #e94560; }
  .matrix-container { display: flex; justify-content: center; margin: 30px 0; }
  table { border-collapse: collapse; }
  th, td { width: 90px; height: 60px; text-align: center; border: 2px solid #333; font-size: 14px; }
  th { background: #16213e; color: #e94560; }
  .axis-label { background: #16213e; color: #0f3460; font-weight: bold; }
  .cell-red { background: rgba(231,76,60,0.3); }
  .cell-orange { background: rgba(230,126,34,0.3); }
  .cell-yellow { background: rgba(241,196,15,0.2); }
  .cell-green { background: rgba(46,204,113,0.2); }
  .risk-list { max-width: 800px; margin: 30px auto; }
  .risk-card { background: #16213e; border-radius: 8px; padding: 16px; margin: 12px 0; border-left: 4px solid #e94560; }
  .risk-card.orange { border-left-color: #e67e22; }
  .risk-card.yellow { border-left-color: #f1c40f; }
  .risk-card.green { border-left-color: #2ecc71; }
  .risk-card h3 { margin: 0 0 8px 0; }
  .risk-card .meta { color: #aaa; font-size: 13px; }
  .summary { text-align: center; margin: 30px 0; font-size: 18px; }
  .summary span { margin: 0 15px; }
</style>
</head>
<body>
<h1>🛡️ MAGI 风险矩阵 — 三贤者战略参谋</h1>
""")

    # 矩阵表格
    html.append('<div class="matrix-container"><table>')
    html.append('<tr><th>概率 ↓ / 影响 →</th>')
    for i in range(1, 6):
        html.append(f'<th>{IMPACT_LABELS[i]}({i})</th>')
    html.append('</tr>')

    for p in range(5, 0, -1):
        html.append(f'<tr><th>{PROBABILITY_LABELS[p]}({p})</th>')
        for i in range(1, 6):
            score = p * i
            info = classify_risk(score)
            cell_class = f"cell-{info['level']}"
            risks_in_cell = grid.get((p, i), [])
            count = len(risks_in_cell)
            cell_content = f"{info['emoji']} {score}"
            if count > 0:
                cell_content += f" ({count})"
            html.append(f'<td class="{cell_class}">{cell_content}</td>')
        html.append('</tr>')

    html.append('</table></div>')

    # 统计摘要
    level_counts = {"red": 0, "orange": 0, "yellow": 0, "green": 0}
    for r in risks:
        level_counts[r["risk_level"]] = level_counts.get(r["risk_level"], 0) + 1

    html.append('<div class="summary">')
    html.append(f'<span>🔴 极高: {level_counts["red"]}</span>')
    html.append(f'<span>🟠 高: {level_counts["orange"]}</span>')
    html.append(f'<span>🟡 中: {level_counts["yellow"]}</span>')
    html.append(f'<span>🟢 低: {level_counts["green"]}</span>')
    html.append('</div>')

    # 风险卡片列表
    html.append('<div class="risk-list">')
    sorted_risks = sorted(risks, key=lambda r: r["score"], reverse=True)
    for r in sorted_risks:
        card_class = r["risk_level"]
        html.append(f'<div class="risk-card {card_class}">')
        html.append(f'<h3>{r["risk_emoji"]} {r["name"]} <small>(风险值: {r["score"]})</small></h3>')
        html.append(f'<div class="meta">')
        html.append(f'概率: {r["probability_label"]} × 影响: {r["impact_label"]} | ')
        if r["domain"]:
            html.append(f'风险域: {r["domain"]} | ')
        if r["source"]:
            html.append(f'来源: {r["source"]} | ')
        if r["reversibility"]:
            html.append(f'可逆性: {r["reversibility"]}')
        html.append('</div>')
        if r["mitigation"]:
            html.append(f'<p>缓解措施: {r["mitigation"]}</p>')
        html.append(f'<p><strong>行动建议:</strong> {r["action"]}</p>')
        html.append('</div>')

    html.append('</div>')
    html.append('</body></html>')

    html_content = "\n".join(html)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    return output_path


# ─── 使用示例 ──────────────────────────────────────────────

if __name__ == "__main__":
    # 示例风险数据
    sample_risks = [
        build_risk_entry(
            name="核心技术人员离职",
            probability=3,
            impact=5,
            domain="执行风险",
            source="BALTHASAR",
            reversibility="部分可逆",
            detectability="可提前预警",
            mitigation="建立知识文档化机制，培养备份人选",
        ),
        build_risk_entry(
            name="监管政策突变",
            probability=2,
            impact=5,
            domain="合规风险",
            source="BALTHASAR",
            reversibility="不可逆",
            detectability="事后才发现",
            mitigation="预留合规缓冲期，建立政策追踪机制",
        ),
        build_risk_entry(
            name="竞品提前发布类似产品",
            probability=4,
            impact=3,
            domain="时机风险",
            source="CASPER",
            reversibility="不可逆",
            detectability="可提前预警",
            mitigation="加速MVP上线，强化差异化定位",
        ),
        build_risk_entry(
            name="预算超支",
            probability=3,
            impact=3,
            domain="财务风险",
            source="MELCHIOR",
            reversibility="部分可逆",
            detectability="可提前预警",
            mitigation="设置阶段性预算审查节点，预留15%应急资金",
        ),
        build_risk_entry(
            name="团队士气下降",
            probability=3,
            impact=2,
            domain="人心风险",
            source="CASPER",
            reversibility="可逆",
            detectability="事后才发现",
            mitigation="定期1-on-1沟通，设置阶段性庆功节点",
        ),
    ]

    # 判断输出模式
    if "--html" in sys.argv:
        output_path = "risk_matrix.html"
        for arg in sys.argv:
            if arg.startswith("--output="):
                output_path = arg.split("=", 1)[1]
        result = generate_html_matrix(sample_risks, output_path)
        print(f"HTML风险矩阵已生成: {result}")
    else:
        print(generate_text_matrix(sample_risks))

    # 同时输出JSON格式（方便其他脚本调用）
    if "--json" in sys.argv:
        print("\n\n--- JSON 格式输出 ---")
        print(json.dumps(sample_risks, ensure_ascii=False, indent=2))