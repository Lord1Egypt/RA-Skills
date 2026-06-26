#!/usr/bin/env python3
"""
OUA v1.0 — OpenClaw Unified Assessment 评分与报告生成引擎
融合 OIT（智商天花板 8 维度）+ LLI（工程地板 2 维度）= 10 维度统一评估

用法:
    python3 score_test.py --interactive                    # 交互式评分
    python3 score_test.py --input results.json             # 从JSON生成报告
    python3 score_test.py --input results.json --output report.html
    python3 score_test.py --input results.json --output report.html --format json
"""

import json
import argparse
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Tuple
import html

# ════════════════════════════════════════════════════════
#  OUA v1.0 — 10 维度定义
# ════════════════════════════════════════════════════════

DIMENSIONS = {
    # ── OIT 轨道：智商天花板 (D1-D8) ──
    "language": {
        "name_cn": "语言理解与生成",
        "name_en": "Language Understanding & Generation",
        "weight": 0.15,
        "track": "OIT",
        "code": "D1-LANG",
        "description": "语义理解、意图识别、上下文理解、文本生成质量"
    },
    "logic": {
        "name_cn": "逻辑推理",
        "name_en": "Logical Reasoning & Problem Solving",
        "weight": 0.14,
        "track": "OIT",
        "code": "D2-LOGIC",
        "description": "数学推理、逻辑谜题、因果推理、多步推理"
    },
    "knowledge": {
        "name_cn": "知识广度与深度",
        "name_en": "Knowledge Breadth & Depth",
        "weight": 0.12,
        "track": "OIT",
        "code": "D3-KNOWLEDGE",
        "description": "通用知识、时事认知、专业知识、常识判断"
    },
    "coding": {
        "name_cn": "代码与技术能力",
        "name_en": "Coding & Technical Skills",
        "weight": 0.12,
        "track": "OIT",
        "code": "D4-CODING",
        "description": "代码生成调试、算法设计、技术架构"
    },
    "creativity": {
        "name_cn": "创造性与发散思维",
        "name_en": "Creativity & Divergent Thinking",
        "weight": 0.08,
        "track": "OIT",
        "code": "D5-CREATIVITY",
        "description": "创意写作、头脑风暴、跨界联想、替代视角"
    },
    "memory": {
        "name_cn": "上下文记忆与一致性",
        "name_en": "Context Memory & Consistency",
        "weight": 0.08,
        "track": "OIT",
        "code": "D6-MEMORY",
        "description": "长对话记忆、角色一致性、信息追踪、矛盾检测"
    },
    "tool_use": {
        "name_cn": "实用工具使用",
        "name_en": "Tool Use & Practical Application",
        "weight": 0.06,
        "track": "OIT",
        "code": "D7-TOOL",
        "description": "API调用、数据处理、任务分解执行"
    },
    "safety": {
        "name_cn": "安全性与伦理判断",
        "name_en": "Safety & Ethics",
        "weight": 0.05,
        "track": "OIT",
        "code": "D8-SAFETY",
        "description": "有害内容识别、偏见检测、隐私保护、伦理决策"
    },
    # ── LLI 轨道：工程地板 (D9-D10) ──
    "engineering": {
        "name_cn": "工程实现与落地能力",
        "name_en": "Engineering Implementation & Delivery",
        "weight": 0.12,
        "track": "LLI",
        "code": "D9-ENGINEERING",
        "description": "完整性交付、边界条件处理、依赖管理、可维护性、环境适配"
    },
    "robustness": {
        "name_cn": "鲁棒性与容错能力",
        "name_en": "Robustness & Fault Tolerance",
        "weight": 0.08,
        "track": "LLI",
        "code": "D10-ROBUSTNESS",
        "description": "对抗性输入、噪声容忍、矛盾约束处理、资源受限表现、失败模式"
    }
}

# OIT 维度键列表
OIT_DIMENSIONS = [k for k, v in DIMENSIONS.items() if v["track"] == "OIT"]
# LLI 维度键列表
LLI_DIMENSIONS = [k for k, v in DIMENSIONS.items() if v["track"] == "LLI"]

# 评级标准
GRADE_SCALE = [
    (90, "S", "卓越", "接近人类专家水平，生产可用"),
    (80, "A", "优秀", "显著高于平均水平，推荐使用"),
    (70, "B", "良好", "高于平均水平，适合大多数场景"),
    (60, "C", "合格", "达到可用水平，需注意弱项"),
    (50, "D", "勉强", "存在明显短板，建议针对性改进"),
    (0,  "F", "未达标", "未达到基本要求，不推荐用于关键任务")
]

# 四象限定义
QUADRANTS = {
    "Q1": {"name": "🏆 全栈型", "oit": "high", "lli": "high", "desc": "全场景生产环境", "color": "#2d7a3e"},
    "Q2": {"name": "🔮 聪明但不稳", "oit": "high", "lli": "low",  "desc": "研究/创意/需人工审核", "color": "#f39c12"},
    "Q3": {"name": "🛡️ 稳定但平庸", "oit": "low",  "lli": "high", "desc": "基础自动化/重复任务", "color": "#3498db"},
    "Q4": {"name": "❌ 不可用",   "oit": "low",  "lli": "low",  "desc": "不建议投入使用",     "color": "#c0392b"},
}


@dataclass
class TestResult:
    """单个测试问题的结果"""
    dimension: str
    question_id: str
    difficulty: str       # basic/advanced/expert
    question: str
    expected: str
    actual_answer: str
    score: int            # 0-5
    notes: str = ""


@dataclass
class TestSession:
    """完整测试会话"""
    test_date: str = ""
    tester: str = ""
    difficulty: str = "standard"   # quick/standard/deep/custom
    duration_minutes: int = 0
    track_mode: str = "full"       # full/oit-only/lli-only
    results: List[TestResult] = field(default_factory=list)

    def get_dimension_scores(self) -> Dict[str, dict]:
        """计算各维度得分"""
        dim_data = {}
        for dim_key in DIMENSIONS:
            dim_results = [r for r in self.results if r.dimension == dim_key]
            if dim_results:
                total_score = sum(r.score for r in dim_results)
                max_score = len(dim_results) * 5
                percentage = (total_score / max_score) * 100 if max_score > 0 else 0
                dim_data[dim_key] = {
                    "score": total_score,
                    "max_score": max_score,
                    "percentage": round(percentage, 1),
                    "count": len(dim_results)
                }
        return dim_data

    def get_oua_total(self) -> float:
        """计算 OUA 综合加权总分"""
        dim_scores = self.get_dimension_scores()
        weighted_sum = sum(
            data["percentage"] * DIMENSIONS[dim_key]["weight"]
            for dim_key, data in dim_scores.items()
        )
        return round(weighted_sum, 1)

    def get_oit_score(self) -> float:
        """计算 OIT 天花板得分"""
        dim_scores = self.get_dimension_scores()
        oit_dims = {k: v for k, v in dim_scores.items() if k in OIT_DIMENSIONS}
        if not oit_dims:
            return 0.0
        total_weight = sum(DIMENSIONS[k]["weight"] for k in oit_dims)
        weighted_sum = sum(
            data["percentage"] * DIMENSIONS[k]["weight"]
            for k, data in oit_dims.items()
        )
        return round(weighted_sum / total_weight * 100, 1) if total_weight > 0 else 0.0

    def get_lli_score(self) -> float:
        """计算 LLI 地板得分"""
        dim_scores = self.get_dimension_scores()
        lli_dims = {k: v for k, v in dim_scores.items() if k in LLI_DIMENSIONS}
        if not lli_dims:
            return 0.0
        total_weight = sum(DIMENSIONS[k]["weight"] for k in lli_dims)
        weighted_sum = sum(
            data["percentage"] * DIMENSIONS[k]["weight"]
            for k, data in lli_dims.items()
        )
        return round(weighted_sum / total_weight * 100, 1) if total_weight > 0 else 0.0

    def get_grade(self, score: float = None) -> tuple:
        """获取评级"""
        total = score if score is not None else self.get_oua_total()
        for threshold, grade, name, desc in GRADE_SCALE:
            if total >= threshold:
                return grade, name, desc
        return "F", "未达标", "未达到基本要求"

    def get_quadrant(self) -> dict:
        """获取四象限定位"""
        oit = self.get_oit_score()
        lli = self.get_lli_score()
        oit_level = "high" if oit >= 70 else "low"
        lli_level = "high" if lli >= 70 else "low"

        for qid, qinfo in QUADRANTS.items():
            if qinfo["oit"] == oit_level and qinfo["lli"] == lli_level:
                return {**qinfo, "id": qid, "oit_score": oit, "lli_score": lli}

        return {"id": "unknown", "name": "未知类型", "oit_score": oit, "lli_score": lli,
                "desc": "", "color": "#888"}

    def get_strengths_and_weaknesses(self, n: int = 2) -> Tuple[list, list]:
        """获取强项和弱项"""
        dim_scores = self.get_dimension_scores()
        sorted_dims = sorted(dim_scores.items(), key=lambda x: x[1]["percentage"], reverse=True)
        strengths = sorted_dims[:n]
        weaknesses = sorted_dims[-n:]
        return strengths, weaknesses

    def get_diagnosis(self) -> str:
        """生成诊断语"""
        oit = self.get_oit_score()
        lli = self.get_lli_score()
        diff = abs(oit - lli)

        if oit >= 75 and lli >= 75:
            return "✅ 生产级 AI 助手，双轨均达到良好水平"
        elif oit >= 75 and lli < 60:
            return "⚠️ 「聪明但不靠谱」——智力优秀但工程落地能力不足，建议加强边界测试和完整性训练"
        elif oit < 60 and lli >= 75:
            return "📌 「稳定但平庸」——可靠性不错但创造力有限，适合规则明确的自动化任务"
        elif oit < 60 and lli < 60:
            return "❌ 双轨均未达标，需要系统性改进"
        elif diff > 25 and oit > lli:
            return "⚠️ 天花板远高于地板——AI 很聪明但容易出错，所有输出都需要人工审核"
        elif diff > 25 and lli > oit:
            return "📌 地板远高于天花板——AI 稳定但不够聪明，适合辅助性工作"
        else:
            return "📊 发展均衡，各维度处于相近水平"


def generate_html_report(session: TestSession) -> str:
    """生成 HTML 格式的 OUA 测试报告"""

    dim_scores = session.get_dimension_scores()
    oua_total = session.get_oua_total()
    oit_score = session.get_oit_score()
    lli_score = session.get_lli_score()
    grade, grade_name, grade_desc = session.get_grade()
    quadrant = session.get_quadrant()
    diagnosis = session.get_diagnosis()
    strengths, weaknesses = session.get_strengths_and_weaknesses()

    # 雷达图数据（全部10维）
    radar_labels = [DIMENSIONS[k]["name_cn"] for k in dim_scores.keys()]
    radar_values = [data["percentage"] for data in dim_scores.values()]

    # 按轨道分组
    oit_dim_keys = [k for k in dim_scores if k in OIT_DIMENSIONS]
    lli_dim_keys = [k for k in dim_scores if k in LLI_DIMENSIONS]

    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🦞 OUA v1.0 统一智能评估报告</title>
    <style>
        :root {{
            --primary: #667eea;
            --secondary: #764ba2;
            --oit-color: #3498db;
            --lli-color: #e74c3c;
            --bg-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --success: #27ae60;
            --warning: #f39c12;
            --danger: #e74c3c;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: var(--bg-gradient);
            min-height: 100vh;
            padding: 20px;
            color: #333;
        }}
        .container {{
            max-width: 1100px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 25px 50px rgba(0,0,0,0.15);
            overflow: hidden;
        }}
        /* Header */
        .header {{
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        .header h1 {{ font-size: 2em; margin-bottom: 5px; }}
        .header .subtitle {{ opacity: 0.7; font-size: 0.95em; margin-bottom: 25px; }}

        /* 双轨得分展示 */
        .dual-track {{
            display: flex;
            justify-content: center;
            gap: 30px;
            align-items: stretch;
            margin: 25px 0;
            flex-wrap: wrap;
        }}
        .track-card {{
            border-radius: 16px;
            padding: 20px 30px;
            text-align: center;
            min-width: 200px;
            transition: transform 0.2s;
        }}
        .track-card:hover {{ transform: translateY(-3px); }}
        .track-oit {{
            background: linear-gradient(135deg, rgba(52,152,219,0.15), rgba(52,152,219,0.05));
            border: 2px solid rgba(52,152,219,0.4);
        }}
        .track-lli {{
            background: linear-gradient(135deg, rgba(231,76,60,0.15), rgba(231,76,60,0.05));
            border: 2px solid rgba(231,76,60,0.4);
        }}
        .track-label {{ font-size: 0.85em; opacity: 0.7; text-transform: uppercase; letter-spacing: 2px; }}
        .track-name {{ font-size: 1.1em; font-weight: 600; margin: 5px 0; }}
        .track-score {{ font-size: 2.2em; font-weight: bold; }}
        .track-oit .track-score {{ color: var(--oit-color); }}
        .track-lli .track-score {{ color: var(--lli-color); }}
        .track-grade {{ font-size: 0.9em; opacity: 0.8; }}

        /* 总分徽章 */
        .grade-badge {{
            display: inline-block;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 18px 45px;
            border-radius: 50px;
            font-size: 2.8em;
            font-weight: bold;
            box-shadow: 0 10px 30px rgba(245,87,108,0.3);
        }}
        .score-display {{ font-size: 1.4em; opacity: 0.9; margin-top: 8px; }}

        .meta-info {{
            display: flex;
            justify-content: center;
            gap: 25px;
            margin-top: 15px;
            font-size: 0.88em;
            opacity: 0.65;
            flex-wrap: wrap;
        }}

        /* Content */
        .content {{ padding: 35px 40px; }}
        .section {{ margin-bottom: 35px; }}
        .section-title {{
            font-size: 1.25em; color: #1a1a2e; margin-bottom: 18px;
            padding-bottom: 10px; border-bottom: 2px solid #eee;
            display: flex; align-items: center; gap: 8px;
        }}

        /* 诊断栏 */
        .diagnosis-bar {{
            background: linear-gradient(135deg, #fff3cd 0%, #ffeeba 100%);
            border-left: 5px solid var(--warning);
            border-radius: 10px;
            padding: 16px 22px;
            margin-bottom: 30px;
            font-size: 1.05em;
        }}

        /* 四象限指示器 */
        .quadrant-indicator {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 3px;
            width: 160px;
            height: 160px;
            margin: 0 auto 10px;
            border-radius: 12px;
            overflow: hidden;
        }}
        .q-cell {{
            display: flex; align-items: center; justify-content: center;
            font-size: 1.5em; cursor: default; transition: all 0.3s;
        }}
        .q-cell.active {{
            transform: scale(1.08);
            box-shadow: 0 0 20px rgba(0,0,0,0.2);
            z-index: 2;
        }}
        .quadrant-info {{ text-align: center; font-size: 0.9em; }}

        /* 雷达图容器 */
        .radar-container {{
            display: flex; justify-content: center;
            background: #f8f9fa; border-radius: 14px; padding: 20px;
        }}

        /* 维度卡片 */
        .dimension-card {{
            background: #f8f9fa; border-radius: 12px; padding: 18px;
            margin-bottom: 12px; transition: transform 0.2s, box-shadow 0.2s;
            border-left: 4px solid transparent;
        }}
        .dimension-card:hover {{ transform: translateX(5px); box-shadow: 0 4px 12px rgba(0,0,0,0.06); }}
        .dimension-card.track-oit {{ border-left-color: var(--oit-color); }}
        .dimension-card.track-lli {{ border-left-color: var(--lli-color); }}
        .dim-header {{ display: flex; justify-content: space-between; align-items: center; }}
        .dim-name {{ font-weight: 600; font-size: 0.95em; }}
        .dim-code {{
            font-size: 0.72em; color: #888; background: #eee;
            padding: 2px 7px; border-radius: 4px; margin-left: 8px;
        }}
        .dim-track-badge {{
            font-size: 0.68em; padding: 2px 7px; border-radius: 4px; font-weight: 500;
        }}
        .track-oit-badge {{ background: rgba(52,152,219,0.15); color: #2980b9; }}
        .track-lli-badge {{ background: rgba(231,76,60,0.15); color: #c0392b; }}
        .dim-score {{ font-size: 1.35em; font-weight: bold; color: var(--primary); }}
        .dim-bar-container {{ background: #e9ecef; border-radius: 10px; height: 10px; overflow: hidden; margin-top: 8px; }}
        .dim-bar {{
            height: 100%; border-radius: 10px;
            background: linear-gradient(90deg, var(--primary), var(--secondary));
            transition: width 0.6s ease-out;
        }}
        .dim-meta {{ font-size: 0.82em; color: #999; margin-top: 6px; }}

        /* 分析网格 */
        .analysis-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }}
        @media (max-width: 700px) {{ .analysis-grid {{ grid-template-columns: 1fr; }} }}
        .analysis-card {{ border-radius: 12px; padding: 20px; }}
        .strengths {{ background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%); }}
        .weaknesses {{ background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); }}
        .analysis-card h3 {{ margin-bottom: 14px; font-size: 1.05em; }}
        .analysis-item {{
            background: rgba(255,255,255,0.75); padding: 12px;
            border-radius: 8px; margin-bottom: 10px;
        }}
        .item-score {{ font-weight: bold; font-size: 1.15em; }}

        /* 详情表格 */
        .detail-table {{ width: 100%; border-collapse: collapse; font-size: 0.85em; }}
        .detail-table th, .detail-table td {{
            padding: 11px; text-align: left; border-bottom: 1px solid #eee;
        }}
        .detail-table th {{ background: #f8f9fa; font-weight: 600; color: #555; }}
        .difficulty-badge {{ display: inline-block; padding: 2px 7px; border-radius: 4px; font-size: 0.78em; font-weight: 500; }}
        .diff-basic {{ background: #d4edda; color: #155724; }}
        .diff-advanced {{ background: #cce5ff; color: #004085; }}
        .diff-expert {{ background: #f8d7da; color: #721c24; }}
        .score-cell {{ font-weight: bold; }}
        .track-badge-tbl {{ font-size: 0.72em; padding: 2px 6px; border-radius: 3px; }}

        /* Footer */
        .footer {{ text-align: center; padding: 18px; background: #f8f9fa; color: #aaa; font-size: 0.83em; }}

        /* OIT/LLI 分区标题 */
        .track-section-title {{
            font-size: 0.92em; font-weight: 600; margin: 20px 0 12px;
            padding: 6px 12px; border-radius: 6px; display: inline-block;
        }}
        .track-section-oit {{ background: rgba(52,152,219,0.1); color: #2980b9; }}
        .track-section-lli {{ background: rgba(231,76,60,0.1); color: #c0392b; }}
    </style>
</head>
<body>
<div class="container">
    <!-- Header -->
    <div class="header">
        <h1>🦞 OUA v1.0 统一智能评估报告</h1>
        <p class="subtitle">OpenClaw Unified Assessment | OIT 智商天花板 + LLI 工程地板</p>

        <div class="grade-badge">{grade}</div>
        <div class="score-display">OUA 总分: <strong>{oua_total}</strong> / 100</div>
        <div style="font-size: 0.93em;">{grade_name} — {grade_desc}</div>

        <!-- 双轨得分 -->
        <div class="dual-track">
            <div class="track-card track-oit">
                <div class="track-label">OIT Track</div>
                <div class="track-name">🧠 智商天花板</div>
                <div class="track-score">{oit_score}</div>
                <div class="track-grade">/ 100</div>
            </div>
            <div class="track-card track-lli">
                <div class="track-label">LLI Track</div>
                <div class="track-name">⚙️ 工程地板</div>
                <div class="track-score">{lli_score}</div>
                <div class="track-grade">/ 100</div>
            </div>
        </div>

        <div class="meta-info">
            <span>📅 {session.test_date}</span>
            <span>👤 {session.tester or 'Anonymous'}</span>
            <span>🎯 {session.difficulty.upper()}</span>
            <span>🔬 {session.track_mode.upper()}</span>
            <span>⏱️ {session.duration_minutes} 分钟</span>
        </div>
    </div>

    <div class="content">
        <!-- 诊断 -->
        <div class="section">
            <h2 class="section-title">🩺 评估诊断</h2>
            <div class="diagnosis-bar">{diagnosis}</div>
            <div style="text-align:center;">
                <div class="quadrant-indicator">"""

    # 四象限格子
    q_positions = [
        ("Q2", "top-right"), ("Q1", "top-left"),
        ("Q4", "bottom-right"), ("Q3", "bottom-left")
    ]
    for qid, pos in q_positions:
        is_active = (qid == quadrant.get("id"))
        q_info = QUADRANTS.get(qid, {})
        active_class = "active" if is_active else ""
        bg_color = q_info.get("color", "#ddd") if is_active else "#f0f0f0"
        text_color = "white" if is_active else "#ccc"
        html_content += f"""
                <div class="q-cell {active_class}" style="background:{bg_color};color:{text_color};" title="{q_info.get('name','')}">{q_info['name'].split()[0]}</div>"""

    html_content += f"""
        </div>
                <div class="quadrant-info"><strong>{quadrant['name']}</strong> — {quadrant['desc']}<br>
                <small>OIT: {quadrant['oit_score']} / LLI: {quadrant['lli_score']}</small></div>
            </div>
        </div>

        <!-- 雷达图 -->
        <div class="section">
            <h2 class="section-title">📊 能力全景图（10维雷达）</h2>
            <div class="radar-container">
                <canvas id="radarChart" width="400" height="400"></canvas>
            </div>
        </div>

        <!-- 各维度详情 -->
        <div class="section">
            <h2 class="section-title">📋 维度得分明细</h2>

            <!-- OIT 维度 -->
            <div class="track-section-title track-section-oit">🧠 OIT — 智商天花板 (D1-D8)</div>"""

    for dim_key in oit_dim_keys:
        data = dim_scores[dim_key]
        info = DIMENSIONS[dim_key]
        bar_width = min(data["percentage"], 100)
        html_content += f"""
            <div class="dimension-card track-oit">
                <div class="dim-header">
                    <span>
                        <span class="dim-name">{info['name_cn']}</span>
                        <span class="dim-code">{info['code']}</span>
                        <span class="dim-track-badge track-oit-badge">OIT</span>
                    </span>
                    <span class="dim-score">{data['percentage']}%</span>
                </div>
                <div class="dim-bar-container">
                    <div class="dim-bar" style="width:{bar_width}%"></div>
                </div>
                <div class="dim-meta">权重: {int(info['weight']*100)}% | 得分: {data['score']}/{data['max_score']} ({data['count']}题) · {info['description']}</div>
            </div>"""

    # LLI 维度
    html_content += """
            <div class="track-section-title track-section-lli" style="margin-top:20px;">⚙️ LLI — 工程地板 (D9-D10)</div>"""

    for dim_key in lli_dim_keys:
        data = dim_scores[dim_key]
        info = DIMENSIONS[dim_key]
        bar_width = min(data["percentage"], 100)
        html_content += f"""
            <div class="dimension-card track-lli">
                <div class="dim-header">
                    <span>
                        <span class="dim-name">{info['name_cn']}</span>
                        <span class="dim-code">{info['code']}</span>
                        <span class="dim-track-badge track-lli-badge">LLI</span>
                    </span>
                    <span class="dim-score">{data['percentage']}%</span>
                </div>
                <div class="dim-bar-container">
                    <div class="dim-bar" style="width:{bar_width}%"></div>
                </div>
                <div class="dim-meta">权重: {int(info['weight']*100)}% | 得分: {data['score']}/{data['max_score']} ({data['count']}题) · {info['description']}</div>
            </div>"""

    html_content += """
        </div>

        <!-- 强弱项分析 -->
        <div class="section">
            <h2 class="section-title">🔍 能力分析</h2>
            <div class="analysis-grid">
                <div class="analysis-card strengths">
                    <h3>✅ 核心优势</h3>"""

    for dim_key, data in strengths:
        info = DIMENSIONS[dim_key]
        html_content += f"""
                    <div class="analysis-item">
                        <div>{info['name_cn']} <span class="dim-code">{info['code']}</span></div>
                        <div class="item-score" style="color:#1e7e34;">{data['percentage']}%</div>
                        <small>{info['description']}</small>
                    </div>"""

    html_content += """
                </div>
                <div class="analysis-card weaknesses">
                    <h3>📈 提升空间</h3>"""

    for dim_key, data in weaknesses:
        info = DIMENSIONS[dim_key]
        html_content += f"""
                    <div class="analysis-item">
                        <div>{info['name_cn']} <span class="dim-code">{info['code']}</span></div>
                        <div class="item-score" style="color:#bd2130;">{data['percentage']}%</div>
                        <small>{info['description']}</small>
                    </div>"""

    html_content += """
                </div>
            </div>
        </div>

        <!-- 详细结果表格 -->
        <div class="section">
            <h2 class="section-title">📝 测试详情</h2>
            <table class="detail-table">
                <thead>
                    <tr>
                        <th>维度</th><th>轨道</th><th>ID</th><th>难度</th>
                        <th>问题摘要</th><th>得分</th><th>备注</th>
                    </tr>
                </thead>
                <tbody>"""

    for result in session.results:
        info = DIMENSIONS[result.dimension]
        diff_map = {'basic': 'diff-basic', 'advanced': 'diff-advanced', 'expert': 'diff-expert'}
        diff_label = {'basic': '基础', 'advanced': '进阶', 'expert': '专家'}
        q_short = html.escape(result.question[:45]) + ('...' if len(result.question) > 45 else '')
        notes_html = html.escape(result.notes[:70]) if result.notes else '-'
        track_class = "track-oit-badge" if info["track"]=="OIT" else "track-lli-badge"
        track_label = "OIT" if info["track"]=="OIT" else "LLI"

        html_content += f"""
                    <tr>
                        <td>{info['name_cn']}</td>
                        <td><span class="track-badge-tbl {track_class}">{track_label}</span></td>
                        <td style="font-size:0.8em;color:#888;">{result.question_id}</td>
                        <td><span class="difficulty-badge {diff_map.get(result.difficulty,'')}">{diff_label.get(result.difficulty,result.difficulty)}</span></td>
                        <td>{q_short}</td>
                        <td class="score-cell">{result.score}/5</td>
                        <td><small>{notes_html}</small></td>
                    </tr>"""

    html_content += f"""
                </tbody>
            </table>
        </div>
    </div>

    <div class="footer">
        <p>Generated by 🦞 OUA v1.0 (OpenClaw Unified Assessment Framework)</p>
        <p>OIT 测智商天花板 · LLI 测工程地板 · OUA 看全貌 | MIT License</p>
    </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
const ctx = document.getElementById('radarChart').getContext('2d');
new Chart(ctx, {{
    type: 'radar',
    data: {{
        labels: {json.dumps(radar_labels, ensure_ascii=False)},
        datasets: [{{
            label: '能力得分',
            data: {radar_values},
            backgroundColor: 'rgba(102,126,234,0.2)',
            borderColor: 'rgba(102,126,234,1)',
            borderWidth: 2,
            pointBackgroundColor: function(ctx) {{
                // OIT 点蓝色，LLI 点红色
                const oitIndices = [0,1,2,3,4,5,6,7];
                const lliIndices = [8,9];
                const index = ctx.dataIndex;
                return (lliIndices.includes(index)) ? 'rgba(231,76,60,1)' : 'rgba(52,152,219,1)';
            }},
            pointBorderColor: '#fff',
            pointRadius: 5,
            pointHoverRadius: 7
        }}]
    }},
    options: {{
        responsive: true,
        scales: {{
            r: {{
                beginAtZero: true,
                max: 100,
                ticks: {{ stepSize: 20, fontSize: 10 }},
                pointLabels: {{ fontSize: 10, fontColor: '#555' }}
            }}
        }},
        plugins: {{
            legend: {{ display: false }}
        }}
        }}
}});
</script>
</body>
</html>"""

    return html_content


def run_interactive_mode():
    """交互式评分模式"""
    print("\n" + "=" * 62)
    print("  🦞 OUA v1.0 — OpenClaw 统一智能评估 (交互式评分)")
    print("=" * 62)

    session = TestSession(
        test_date=datetime.now().strftime("%Y-%m-%d %H:%M"),
        tester=input("\n测试者姓名 (可选): ").strip() or "Anonymous",
    )

    # 选择难度
    difficulty_map = {"q": "quick", "s": "standard", "d": "deep", "c": "custom"}
    print("\n难度等级: [q]uick (~20min) | [s]tandard (~45min) | [d]eep (~90min) | [c]ustom")
    d_input = input("选择 [默认: standard]: ").strip().lower()
    session.difficulty = difficulty_map.get(d_input, "standard")

    # 选择轨道
    print("\n测试轨道:")
    print("  [f]ull - 全部 10 维度 (OIT + LLI)")
    print("  [o]it  - 仅天花板 8 维度")
    print("  [l]li  - 仅地板 2 维度")
    track_input = input("选择 [默认: full]: ").strip().lower()
    session.track_mode = {"o": "oit-only", "l": "lli-only"}.get(track_input, "full")

    # 显示可选维度
    target_dims = list(DIMENSIONS.keys())
    if session.track_mode == "oit-only":
        target_dims = OIT_DIMENSIONS
    elif session.track_mode == "lli-only":
        target_dims = LLI_DIMENSIONS

    print(f"\n{'='*56}")
    print(f"  可选维度 ({len(target_dims)} 个):")
    print(f"{'='*56}")
    for key in target_dims:
        info = DIMENSIONS[key]
        track_tag = "🧠" if info["track"]=="OIT" else "⚙️"
        print(f"  {track_tag} {key}: {info['name_cn']} [{info['code']}] (权重{int(info['weight']*100)}%)")

    dim_input = input(f"\n要测试的维度 (逗号分隔, 输入 all 选全部) [默认: 全部]: ").strip().lower()
    target_dims = list(target_dims) if dim_input in ("all", "") else [d.strip() for d in dim_input.split(",")]

    print(f"\n{'='*56}")
    print(f"  开始测试！每题打分 0-5，输入 quit 随时退出")
    print(f"{'='*56}")
    print("  5=优秀 4=良好 3=满意 2=需改进 1=较差 0=不合格\n")

    for dim_key in target_dims:
        if dim_key not in DIMENSIONS:
            continue

        info = DIMENSIONS[dim_key]
        track_icon = "🧠" if info["track"]=="OIT" else "⚙️"
        print(f"\n{'─'*50}")
        print(f"  {track_icon} [{info['code']}] {info['name_cn']}")
        print(f"  轨道: {info['track']} | 权重: {int(info['weight']*100)}%")
        print(f"  {info['description']}")
        print(f"{'─'*50}")

        while True:
            print(f"\n  --- 新题目 ---")
            q_id = input("  题目ID (如 Q1.1.1 或 Q9.1.2): ").strip()
            if q_id.lower() == 'quit':
                break
            if not q_id:
                continue

            difficulty = input("  难度 (basic/advanced/expert) [默认: advanced]: ").strip() or "advanced"
            question = input("  题目内容: ").strip()
            expected = input("  期望答案要点: ").strip()
            actual = input("  AI实际回答 (简述): ").strip()

            while True:
                s_input = input("  评分 (0-5): ").strip()
                try:
                    score = int(s_input)
                    if 0 <= score <= 5:
                        break
                    print("  ⚠ 请输入 0-5")
                except ValueError:
                    print("  ⚠ 无效输入")

            notes = input("  备注 (可选): ").strip()

            session.results.append(TestResult(
                dimension=dim_key, question_id=q_id, difficulty=difficulty,
                question=question, expected=expected, actual_answer=actual,
                score=score, notes=notes
            ))
            print(f"  ✅ 已记录: {q_id} → {score}/5")

            cont = input(f"\n  继续 {info['name_cn']}? (y/n) [y]: ").strip().lower()
            if cont == 'n':
                break

    # 结束
    dur = input("\n\n总测试时长 (分钟): ").strip()
    session.duration_minutes = int(dur) if dur else 0

    output = input("\n输出文件名 [默认: oua-report.html]: ").strip() or "oua-report.html"

    html_report = generate_html_report(session)
    with open(output, 'w', encoding='utf-8') as f:
        f.write(html_report)

    # 控制台总结
    print(f"\n{'='*62}")
    print(f"  ✅ 报告已生成: {output}")
    print(f"{'='*62}")
    print(f"\n  🦞 OUA 总分: {session.get_oua_total()} / 100")
    g, gn, _ = session.get_grade()
    print(f"  📊 评级: {g} ({gn})")
    print(f"  🧠 OIT 天花板: {session.get_oit_score()} / 100")
    print(f"  ⚙️ LLI 地板: {session.get_lli_score()} / 100")
    q = session.get_quadrant()
    print(f"  📍 象限: {q['name']}")
    print(f"\n  诊断: {session.get_diagnosis()}")

    print(f"\n  各维度得分:")
    for dk, dv in session.get_dimension_scores().items():
        di = DIMENSIONS[dk]
        tag = "OIT" if di["track"]=="OIT" else "LLI"
        print(f"    [{tag}] {di['name_cn']:12s} {dv['percentage']:>6}%  ({dv['score']}/{dv['max_score']})")


def main():
    parser = argparse.ArgumentParser(
        description='🦞 OUA v1.0 — OpenClaw Unified Assessment Scorer',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 score_test.py --interactive              # 交互式评分
  python3 score_test.py --input data.json          # JSON → HTML报告
  python3 score_test.py --input data.json -o out.html  # 自定义输出名
        """
    )
    parser.add_argument('--interactive', action='store_true', help='启动交互式评分模式')
    parser.add_argument('--input', type=str, help='从JSON文件读取测试结果并生成报告')
    parser.add_argument('--output', '-o', type=str, default='oua-report.html', help='输出HTML报告路径')
    parser.add_argument('--format', choices=['html','json'], default='html', help='输出格式')

    args = parser.parse_args()

    if args.interactive:
        run_interactive_mode()
    elif args.input:
        with open(args.input, 'r', encoding='utf-8') as f:
            data = json.load(f)
        session = TestSession(**{k: v for k, v in data.items() if k in TestSession.__dataclass_fields__})
        session.results = [TestResult(**r) for r in data.get('results', [])]

        if args.format == 'json':
            output_data = {
                **asdict(session),
                'oua_total': session.get_oua_total(),
                'oit_score': session.get_oit_score(),
                'lli_score': session.get_lli_score(),
                'grade': session.get_grade(),
                'quadrant': session.get_quadrant(),
                'diagnosis': session.get_diagnosis(),
                'dimension_scores': session.get_dimension_scores()
            }
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)
            print(f"JSON report saved to {args.output}")
        else:
            html_report = generate_html_report(session)
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(html_report)
            print(f"HTML report generated: {args.output}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
