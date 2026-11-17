#!/usr/bin/env python3
"""workflow_d.py — McKinsey-style PPTX generator (工作流D)

生成原生可编辑的 PPTX（python-pptx 原生形状，无需右键转换）。
支持40个专业业务模板，通过 --templates 参数组合任意模板。

Usage:
  python3 workflow_d.py --templates cover,agenda,kpi_dashboard --output /tmp/out.pptx
  python3 workflow_d.py --list
  python3 workflow_d.py --demo --output /tmp/demo.pptx

禁止硬编码 token/key。所有凭据从环境变量读取。
"""
import argparse
import sys
import os

# ---------------------------------------------------------------------------
# Template registry: 40个模板 → (函数导入路径, 中文名, 适用场景, 默认参数)
# ---------------------------------------------------------------------------
TEMPLATE_CATALOG = {
    # ──── 结构页 (Structure Slides) ────
    "cover": {
        "cn": "封面页",
        "scene": "演讲首页、汇报开场",
        "module": "consulting_pptx.slides.structure_slides",
        "fn": "add_cover_slide",
        "defaults": {"title": "演示标题", "subtitle": "副标题", "date": "2025"},
    },
    "agenda": {
        "cn": "议程页",
        "scene": "目录、会议议程",
        "module": "consulting_pptx.slides.structure_slides",
        "fn": "add_agenda",
        "defaults": {"title": "Agenda", "items": ["第一章", "第二章", "第三章"]},
    },
    "section_divider": {
        "cn": "章节分隔页",
        "scene": "多章节 PPT 的章节过渡",
        "module": "consulting_pptx.slides.structure_slides",
        "fn": "add_section_divider",
        "defaults": {"section_number": "01", "section_title": "章节标题"},
    },
    "stat_hero": {
        "cn": "大数字冲击页",
        "scene": "突出关键指标、数字冲击",
        "module": "consulting_pptx.slides.structure_slides",
        "fn": "add_stat_hero",
        "defaults": {"stat": "87%", "stat_label": "客户满意度", "context": "较去年提升 12 个百分点"},
    },
    "quote": {
        "cn": "引言页",
        "scene": "金句引用、领导讲话摘录",
        "module": "consulting_pptx.slides.structure_slides",
        "fn": "add_quote_slide",
        "defaults": {"quote": "引言内容", "author": "作者姓名", "author_title": "职位"},
    },
    # ──── 摘要页 (Summary Slides) ────
    "dark_navy_summary": {
        "cn": "深蓝摘要页",
        "scene": "章节总结、核心结论",
        "module": "consulting_pptx.slides.summary_slide",
        "fn": "add_dark_navy_summary",
        "defaults": {"body": "[核心结论]: 关键信息摘要，请替换为实际内容"},
    },
    "keytakeaway_summary": {
        "cn": "关键要点摘要",
        "scene": "执行摘要、多要点汇总",
        "module": "consulting_pptx.slides.executive_summary",
        "fn": "add_keytakeaway_summary",
        "defaults": {
            "title": "执行摘要",
            "sections": [
                {"takeaway": "AI将重塑HR工作方式", "bullets": ["效率提升50%", "决策质量更高"]},
                {"takeaway": "转型分三个阶段推进", "bullets": ["试点→推广→深化"]},
            ],
        },
    },
    "paragraph_summary": {
        "cn": "段落摘要页",
        "scene": "叙述性总结、情况说明",
        "module": "consulting_pptx.slides.executive_summary",
        "fn": "add_paragraph_summary",
        "defaults": {"title": "执行摘要", "paragraphs": ["这是正文段落内容。"]},
    },
    # ──── 柱状图 (Column Charts) ────
    "column_simple_growth": {
        "cn": "简单增长柱状图",
        "scene": "同比/环比增长展示",
        "module": "consulting_pptx.slides.column_chart",
        "fn": "add_column_simple_growth",
        "defaults": {
            "title": "增长趋势",
            "categories": ["2022", "2023", "2024"],
            "values": [120, 145, 180],
            "growth_pct": "24%",
        },
    },
    "column_split_growth": {
        "cn": "分段增长柱状图",
        "scene": "有分割点的增长展示",
        "module": "consulting_pptx.slides.column_chart",
        "fn": "add_column_split_growth",
        "defaults": {
            "title": "分段增长",
            "categories": ["2021", "2022", "2023", "2024"],
            "values": [100, 115, 130, 160],
            "split_index": 2,
        },
    },
    "column_historic_forecast": {
        "cn": "历史与预测柱状图",
        "scene": "过去数据 + 未来预测",
        "module": "consulting_pptx.slides.column_chart",
        "fn": "add_column_historic_forecast",
        "defaults": {
            "title": "历史与预测",
            "categories": ["2022", "2023", "2024E", "2025E"],
            "values": [100, 120, 140, 165],
            "forecast_from_index": 2,
        },
    },
    "column_comparison": {
        "cn": "柱状对比图",
        "scene": "多维度数值对比",
        "module": "consulting_pptx.slides.column_chart",
        "fn": "add_column_comparison",
        "defaults": {
            "title": "数值对比",
            "categories": ["A", "B", "C"],
            "values": [75, 90, 65],
        },
    },
    # ──── 气泡图 / 矩阵 (Bubble & Matrix) ────
    "bubble_chart": {
        "cn": "气泡散点图",
        "scene": "三维数据对比、市场地图",
        "module": "consulting_pptx.slides.bubble_chart",
        "fn": "add_bubble_chart",
        "defaults": {
            "title": "市场规模对比",
            "bubbles": [{"label": "产品A", "x": 0.3, "y": 0.7, "size": 0.5}],
        },
    },
    "bubble_chart_with_takeaways": {
        "cn": "气泡图+要点",
        "scene": "气泡图附带分析结论",
        "module": "consulting_pptx.slides.bubble_chart",
        "fn": "add_bubble_chart_with_takeaways",
        "defaults": {
            "title": "市场分析",
            "bubbles": [{"label": "产品A", "x": 0.3, "y": 0.7, "size": 0.5}],
            "takeaways": ["关键洞察1", "关键洞察2"],
        },
    },
    "stacked_column_chart": {
        "cn": "堆叠柱状图",
        "scene": "结构占比随时间变化",
        "module": "consulting_pptx.slides.extra_charts",
        "fn": "add_stacked_column_chart",
        "defaults": {
            "title": "结构变化",
            "categories": ["2022", "2023", "2024"],
            "series": [{"name": "部分A", "values": [40, 45, 50]},
                       {"name": "部分B", "values": [60, 55, 50]}],
        },
    },
    "grouped_column_chart": {
        "cn": "分组柱状图",
        "scene": "多系列并排对比",
        "module": "consulting_pptx.slides.extra_charts",
        "fn": "add_grouped_column_chart",
        "defaults": {
            "title": "分组对比",
            "categories": ["Q1", "Q2", "Q3"],
            "series": [{"name": "去年", "values": [80, 90, 85]},
                       {"name": "今年", "values": [95, 100, 110]}],
        },
    },
    "line_chart": {
        "cn": "折线趋势图",
        "scene": "趋势变化、时间序列",
        "module": "consulting_pptx.slides.extra_charts",
        "fn": "add_line_chart",
        "defaults": {
            "title": "趋势分析",
            "categories": ["1月", "2月", "3月", "4月"],
            "series": [{"name": "指标", "values": [10, 15, 12, 20]}],
        },
    },
    # ──── 对比表格 (Comparison Slides) ────
    "comparison_table": {
        "cn": "对比表格",
        "scene": "多选项多维度评分对比",
        "module": "consulting_pptx.slides.comparison_slides",
        "fn": "add_comparison_table",
        "defaults": {
            "title": "方案对比",
            "options": ["方案A", "方案B"],
            "criteria": [
                {"name": "实施成本", "scores": [3, 4], "notes": ["较低", "较高"]},
                {"name": "效率提升", "scores": [4, 3], "notes": ["显著", "一般"]},
                {"name": "风险程度", "scores": [2, 4], "notes": ["低", "中"]},
            ],
        },
    },
    "pros_cons": {
        "cn": "优劣势对比",
        "scene": "方案利弊分析",
        "module": "consulting_pptx.slides.comparison_slides",
        "fn": "add_pros_cons",
        "defaults": {
            "title": "优劣势分析",
            "pros": ["优势1", "优势2"],
            "cons": ["劣势1", "劣势2"],
        },
    },
    "two_column_compare": {
        "cn": "双列对比",
        "scene": "两方案/前后对比",
        "module": "consulting_pptx.slides.comparison_slides",
        "fn": "add_two_column_compare",
        "defaults": {
            "title": "前后对比",
            "left_label": "现状 As-Is",
            "right_label": "目标 To-Be",
            "left_items": ["HR流程繁琐、依赖人工", "数据分散、决策靠直觉"],
            "right_items": ["AI自动化处理重复任务", "数据驱动、智能决策支持"],
        },
    },
    # ──── 时间线 / 流程 (Timeline Slides) ────
    "gantt_timeline": {
        "cn": "甘特时间线",
        "scene": "项目计划、里程碑排期",
        "module": "consulting_pptx.slides.timeline_slides",
        "fn": "add_gantt_timeline",
        "defaults": {
            "title": "项目计划",
            "weeks": ["W1", "W2", "W3", "W4", "W5", "W6"],
            "workstreams": [
                {"name": "需求分析", "start": 0, "end": 2},
                {"name": "设计开发", "start": 1, "end": 5},
            ],
        },
    },
    "phases_chevron_3": {
        "cn": "三阶段箭头流程",
        "scene": "三段式推进计划",
        "module": "consulting_pptx.slides.timeline_slides",
        "fn": "add_phases_chevron_3",
        "defaults": {
            "title": "三阶段计划",
            "phases": [
                {"label": "第一阶段", "sub": "基础建设"},
                {"label": "第二阶段", "sub": "能力提升"},
                {"label": "第三阶段", "sub": "规模化"},
            ],
        },
    },
    "phases_table_4": {
        "cn": "四阶段表格路线图",
        "scene": "四阶段详细推进路径",
        "module": "consulting_pptx.slides.timeline_slides",
        "fn": "add_phases_table_4",
        "defaults": {
            "title": "四阶段路线图",
            "phases": [
                {"label": "Q1", "outcomes": ["成果1"], "activities": ["活动1"]},
                {"label": "Q2", "outcomes": ["成果2"], "activities": ["活动2"]},
                {"label": "Q3", "outcomes": ["成果3"], "activities": ["活动3"]},
                {"label": "Q4", "outcomes": ["成果4"], "activities": ["活动4"]},
            ],
        },
    },
    "waves_timeline_4": {
        "cn": "四阶段波浪时间线",
        "scene": "战略演进路线图",
        "module": "consulting_pptx.slides.timeline_slides",
        "fn": "add_waves_timeline_4",
        "defaults": {
            "title": "战略路线图",
            "waves": [
                {"label": "Wave 1", "theme": "打基础", "bullets": ["行动A"]},
                {"label": "Wave 2", "theme": "建能力", "bullets": ["行动B"]},
                {"label": "Wave 3", "theme": "扩规模", "bullets": ["行动C"]},
                {"label": "Wave 4", "theme": "领先", "bullets": ["行动D"]},
            ],
        },
    },
    "overview_areas": {
        "cn": "领域概览",
        "scene": "多业务/产品线总览",
        "module": "consulting_pptx.slides.timeline_slides",
        "fn": "add_overview_areas",
        "defaults": {
            "title": "业务领域概览",
            "areas": [
                {"title": "领域A", "bullets": ["要点1", "要点2"]},
                {"title": "领域B", "bullets": ["要点3", "要点4"]},
            ],
        },
    },
    "process_activities": {
        "cn": "流程活动矩阵",
        "scene": "工作流程、职责分工",
        "module": "consulting_pptx.slides.timeline_slides",
        "fn": "add_process_activities",
        "defaults": {
            "title": "流程活动",
            "steps": [
                {"label": "步骤1", "activities": ["活动A", "活动B"]},
                {"label": "步骤2", "activities": ["活动C"]},
            ],
        },
    },
    # ──── 趋势 / 重点 (Trends Slides) ────
    "three_trends_icons": {
        "cn": "三大趋势（图标版）",
        "scene": "三个关键趋势/洞察",
        "module": "consulting_pptx.slides.trends_slides",
        "fn": "add_three_trends_icons",
        "defaults": {
            "title": "三大趋势",
            "trends": [
                {"icon": "📊", "headline": "趋势1", "body": "说明文字"},
                {"icon": "🚀", "headline": "趋势2", "body": "说明文字"},
                {"icon": "🌐", "headline": "趋势3", "body": "说明文字"},
            ],
        },
    },
    "three_trends_numbered": {
        "cn": "三大趋势（编号版）",
        "scene": "三个编号要点",
        "module": "consulting_pptx.slides.trends_slides",
        "fn": "add_three_trends_numbered",
        "defaults": {
            "title": "三大趋势",
            "trends": [
                {"label": "AI重塑招聘", "bullets": ["简历自动筛选", "面试智能辅助"]},
                {"label": "数据驱动决策", "bullets": ["人效分析实时化", "预测性离职预警"]},
                {"label": "员工体验升级", "bullets": ["自助式HR服务", "个性化发展建议"]},
            ],
        },
    },
    "three_trends_table": {
        "cn": "三大趋势（表格版）",
        "scene": "趋势 + 示例 + 影响",
        "module": "consulting_pptx.slides.trends_slides",
        "fn": "add_three_trends_table",
        "defaults": {
            "title": "三大趋势",
            "trends": [
                {"headline": "趋势1", "body": "描述", "examples": ["示例A"]},
                {"headline": "趋势2", "body": "描述", "examples": ["示例B"]},
                {"headline": "趋势3", "body": "描述", "examples": ["示例C"]},
            ],
        },
    },
    "five_key_areas": {
        "cn": "五大重点领域",
        "scene": "五个核心战略方向",
        "module": "consulting_pptx.slides.trends_slides",
        "fn": "add_five_key_areas",
        "defaults": {
            "title": "五大重点",
            "areas": [
                {"title": "重点1", "bullets": ["要点A"]},
                {"title": "重点2", "bullets": ["要点B"]},
                {"title": "重点3", "bullets": ["要点C"]},
                {"title": "重点4", "bullets": ["要点D"]},
                {"title": "重点5", "bullets": ["要点E"]},
            ],
        },
    },
    # ──── 漏斗 / KPI / 流程 (Process & Metrics) ────
    "funnel": {
        "cn": "漏斗图",
        "scene": "转化率、销售漏斗",
        "module": "consulting_pptx.slides.process_extras",
        "fn": "add_funnel",
        "defaults": {
            "title": "销售漏斗",
            "stages": [
                {"label": "潜在客户", "value": 1000},
                {"label": "意向客户", "value": 500},
                {"label": "成交", "value": 100},
            ],
        },
    },
    "kpi_dashboard": {
        "cn": "KPI 仪表盘",
        "scene": "多指标总览、运营日报",
        "module": "consulting_pptx.slides.process_extras",
        "fn": "add_kpi_dashboard",
        "defaults": {
            "title": "KPI 仪表盘",
            "kpis": [
                {"label": "收入", "value": "¥1.2B", "delta": "+15%", "positive": True},
                {"label": "用户数", "value": "850万", "delta": "+8%", "positive": True},
                {"label": "成本", "value": "¥0.8B", "delta": "+5%", "positive": False},
            ],
        },
    },
    "process_flow_horizontal": {
        "cn": "横向流程图",
        "scene": "业务流程、操作步骤",
        "module": "consulting_pptx.slides.process_extras",
        "fn": "add_process_flow_horizontal",
        "defaults": {
            "title": "业务流程",
            "steps": [
                {"name": "需求收集", "description": "访谈各业务方，梳理AI应用场景"},
                {"name": "方案设计", "description": "制定AI工具选型与实施路径"},
                {"name": "试点验证", "description": "选定2-3个场景快速落地验证"},
                {"name": "推广复制", "description": "总结最佳实践，扩大覆盖范围"},
            ],
        },
    },
    # ──── 组织 / 团队 (Org Charts) ────
    "issue_tree": {
        "cn": "问题树/逻辑树",
        "scene": "根因分析、问题拆解",
        "module": "consulting_pptx.slides.org_charts",
        "fn": "add_issue_tree",
        "defaults": {
            "title": "问题分析",
            "root": "核心问题",
            "main_drivers": [
                {"label": "原因A", "sub_drivers": ["因素1", "因素2"]},
                {"label": "原因B", "sub_drivers": ["因素3"]},
            ],
        },
    },
    "org_chart": {
        "cn": "组织架构图",
        "scene": "汇报关系、团队架构",
        "module": "consulting_pptx.slides.org_charts",
        "fn": "add_org_chart",
        "defaults": {
            "title": "组织架构",
            "branches": [
                {"label": "CEO", "children": [
                    {"label": "CTO"}, {"label": "CFO"}
                ]},
            ],
        },
    },
    "team_chart": {
        "cn": "团队介绍图",
        "scene": "职能分工、团队成员介绍",
        "module": "consulting_pptx.slides.org_charts",
        "fn": "add_team_chart",
        "defaults": {
            "title": "团队介绍",
            "functions": [
                {"name": "战略", "lead": "张三", "members": ["李四"]},
                {"name": "技术", "lead": "王五", "members": ["赵六"]},
            ],
        },
    },
    "project_team_circles": {
        "cn": "项目团队圆形图",
        "scene": "核心团队展示、项目组成员",
        "module": "consulting_pptx.slides.org_charts",
        "fn": "add_project_team_circles",
        "defaults": {
            "title": "项目团队",
            "leader": {"name": "项目负责人", "title": "总监"},
            "members": [
                {"name": "成员A", "title": "设计"},
                {"name": "成员B", "title": "技术"},
                {"name": "成员C", "title": "运营"},
            ],
        },
    },
    # ──── 评估 / 战略矩阵 (Assessment & Strategy) ────
    "assessment_table": {
        "cn": "评估状态表",
        "scene": "项目状态、风险评估",
        "module": "consulting_pptx.slides.assessment_table",
        "fn": "add_assessment_table",
        "defaults": {
            "title": "项目评估",
            "categories": [
                {"name": "招聘模块", "rows": [
                    {"kpi": "AI简历筛选上线", "target": "Q2", "actual": "Q2", "status_label": "按计划", "status": "green"},
                    {"kpi": "面试辅助工具", "target": "Q3", "actual": "延期", "status_label": "需关注", "status": "amber"},
                ]},
                {"name": "培训模块", "rows": [
                    {"kpi": "个性化学习路径", "target": "Q3", "actual": "Q3", "status_label": "按计划", "status": "green"},
                ]},
            ],
        },
    },
    "growth_share_matrix": {
        "cn": "BCG增长份额矩阵",
        "scene": "产品组合分析、BCG矩阵",
        "module": "consulting_pptx.slides.bubble_chart",
        "fn": "add_growth_share_matrix",
        "defaults": {
            "title": "产品组合分析",
            "bus": [
                {"name": "AI招聘", "x": 65, "y": 35, "size": 500},
                {"name": "AI培训", "x": 40, "y": 28, "size": 300},
                {"name": "AI绩效", "x": 25, "y": 15, "size": 200},
                {"name": "AI薪酬", "x": 55, "y": 8, "size": 150},
            ],
        },
    },
    "prioritization_matrix": {
        "cn": "优先级矩阵",
        "scene": "任务优先级、影响力-可行性矩阵",
        "module": "consulting_pptx.slides.bubble_chart",
        "fn": "add_prioritization_matrix",
        "defaults": {
            "title": "优先级分析",
            "items": [
                {"label": "项目A", "x_band": 1, "y_band": 2},
                {"label": "项目B", "x_band": 2, "y_band": 1},
            ],
        },
    },
}

# Ordered list of all 40 template IDs for display
ALL_TEMPLATES = list(TEMPLATE_CATALOG.keys())


def list_templates():
    """Print all available templates in a readable table."""
    print(f"\n{'ID':<35} {'中文名':<20} {'适用场景'}")
    print("-" * 90)
    for tid, meta in TEMPLATE_CATALOG.items():
        print(f"{tid:<35} {meta['cn']:<20} {meta['scene']}")
    print(f"\n共 {len(TEMPLATE_CATALOG)} 个模板")


def build_slide(prs, template_id: str, overrides: dict = None):
    """Add a single slide to prs using the given template_id and optional overrides."""
    if template_id not in TEMPLATE_CATALOG:
        raise ValueError(
            f"未知模板: {template_id}\n"
            f"可用模板: {', '.join(TEMPLATE_CATALOG.keys())}"
        )
    meta = TEMPLATE_CATALOG[template_id]
    module_name = meta["module"]
    fn_name = meta["fn"]

    # Dynamic import
    import importlib
    mod = importlib.import_module(module_name)
    fn = getattr(mod, fn_name)

    # Merge defaults with overrides
    kwargs = dict(meta["defaults"])
    if overrides:
        kwargs.update(overrides)

    return fn(prs, **kwargs)


def build_presentation(template_ids: list, output_path: str,
                       overrides: dict = None) -> str:
    """Build a PPTX with the given templates and save to output_path.

    Args:
        template_ids: List of template ID strings from TEMPLATE_CATALOG
        output_path:  Absolute path for output .pptx file
        overrides:    Optional dict of {template_id: {key: value}} per-slide overrides

    Returns:
        output_path on success
    """
    # Ensure output directory exists
    out_dir = os.path.dirname(output_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    from consulting_pptx.base import init_presentation
    prs = init_presentation()

    for tid in template_ids:
        slide_overrides = (overrides or {}).get(tid)
        build_slide(prs, tid, slide_overrides)

    prs.save(output_path)
    return output_path


def demo_presentation(output_path: str) -> str:
    """Generate a demo PPTX with a representative selection of slides."""
    demo_templates = [
        "cover",
        "agenda",
        "stat_hero",
        "dark_navy_summary",
        "column_simple_growth",
        "kpi_dashboard",
        "gantt_timeline",
        "three_trends_icons",
        "pros_cons",
        "org_chart",
    ]
    return build_presentation(demo_templates, output_path)


def main():
    parser = argparse.ArgumentParser(
        description="工作流D：McKinsey-style PPTX 生成器（40个专业模板）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""示例:
  # 生成封面+议程+KPI仪表盘
  python3 workflow_d.py --templates cover,agenda,kpi_dashboard --output /tmp/deck.pptx

  # 查看所有可用模板
  python3 workflow_d.py --list

  # 生成演示文稿（10张示例页）
  python3 workflow_d.py --demo --output /tmp/demo.pptx
""",
    )
    parser.add_argument(
        "--templates", "-t",
        help="逗号分隔的模板ID列表，例如: cover,agenda,kpi_dashboard",
    )
    parser.add_argument(
        "--output", "-o",
        help="输出 PPTX 文件路径",
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="列出所有可用模板",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="生成演示文稿（包含10张示例幻灯片）",
    )

    args = parser.parse_args()

    if args.list:
        list_templates()
        return

    if args.demo:
        if not args.output:
            print("❌ --demo 模式需要指定 --output 路径", file=sys.stderr)
            sys.exit(1)
        path = demo_presentation(args.output)
        print(f"✅ 演示文稿已生成: {path}")
        return

    if not args.templates:
        parser.print_help()
        sys.exit(1)

    if not args.output:
        print("❌ 请指定 --output 输出路径", file=sys.stderr)
        sys.exit(1)

    template_ids = [t.strip() for t in args.templates.split(",") if t.strip()]
    if not template_ids:
        print("❌ 模板列表为空", file=sys.stderr)
        sys.exit(1)

    # Validate all template IDs before building
    invalid = [t for t in template_ids if t not in TEMPLATE_CATALOG]
    if invalid:
        print(f"❌ 未知模板: {', '.join(invalid)}", file=sys.stderr)
        print(f"可用模板: {', '.join(TEMPLATE_CATALOG.keys())}", file=sys.stderr)
        sys.exit(1)

    print(f"🔨 正在生成 PPTX，模板: {', '.join(template_ids)}")
    path = build_presentation(template_ids, args.output)
    print(f"✅ PPTX 已生成: {path}")


if __name__ == "__main__":
    main()
