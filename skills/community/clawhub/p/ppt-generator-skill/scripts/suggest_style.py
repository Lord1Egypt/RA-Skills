#!/usr/bin/env python3
"""
suggest_style.py — Analyze content and suggest PPT style/category.

v4.3 improvements:
  - Palette and font data loaded from CSV files (data/colors.csv, data/fonts.csv)
  - Returns top-3 palette candidates per category instead of single hardcoded choice
  - Content keyword matching can further rank palettes within a category
  - Falls back to built-in defaults if CSV files are missing

Outputs JSON with:
- suggested_category
- palette_candidates (top 3)
- font_candidates (top 2)
- suggested_tone
- slide_count_estimate
- key_sections
- score_breakdown
- rationale
"""

import sys
import json
import csv
import os
import argparse
import random


_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_DATA_DIR   = os.path.join(os.path.dirname(_SCRIPT_DIR), "data")


# ── CSV loaders ──────────────────────────────────────────────────────────────

def _load_csv(filename: str) -> list[dict]:
    path = os.path.join(_DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_palettes() -> dict[str, list[dict]]:
    rows = _load_csv("colors.csv")
    if not rows:
        return {}
    grouped = {}
    for row in rows:
        cat = row.get("category", "")
        if cat not in grouped:
            grouped[cat] = []
        grouped[cat].append({
            "name":      row.get("palette_name", ""),
            "primary":   row.get("primary", "36454F"),
            "secondary": row.get("secondary", "F2F2F2"),
            "accent":    row.get("accent", "212121"),
            "tags":      row.get("tags", ""),
        })
    return grouped


def load_fonts() -> dict[str, list[dict]]:
    rows = _load_csv("fonts.csv")
    if not rows:
        return {}
    grouped = {}
    for row in rows:
        cat = row.get("category", "")
        if cat not in grouped:
            grouped[cat] = []
        grouped[cat].append({
            "heading": row.get("heading_font", "Calibri"),
            "body":    row.get("body_font", "Calibri"),
            "tone":    row.get("tone", "formal"),
            "tags":    row.get("tags", ""),
        })
    return grouped


# ── Built-in fallbacks ───────────────────────────────────────────────────────

FALLBACK_PALETTES = {
    "企业商务": {"name": "Midnight Executive", "primary": "1E2761", "secondary": "CADCFC", "accent": "FFFFFF"},
    "未来科技": {"name": "Ocean Gradient",     "primary": "065A82", "secondary": "1C7293", "accent": "FFFFFF"},
    "卡通手绘": {"name": "Coral Energy",       "primary": "F96167", "secondary": "F9E795", "accent": "2F3C7E"},
    "年终总结": {"name": "Midnight Executive", "primary": "1E2761", "secondary": "CADCFC", "accent": "FFFFFF"},
    "扁平简约": {"name": "Charcoal Minimal",   "primary": "36454F", "secondary": "F2F2F2", "accent": "212121"},
    "中国风":   {"name": "Cherry Bold",        "primary": "990011", "secondary": "FCF6F5", "accent": "2F3C7E"},
    "文化艺术": {"name": "Berry & Cream",      "primary": "6D2E46", "secondary": "ECE2D0", "accent": "A26769"},
    "文艺清新": {"name": "Sage Calm",          "primary": "84B59F", "secondary": "F5F5EE", "accent": "50808E"},
    "创意趣味": {"name": "Warm Terracotta",    "primary": "B85042", "secondary": "E7E8D1", "accent": "A7BEAE"},
    "学术研究": {"name": "Teal Trust",         "primary": "028090", "secondary": "E0F4F1", "accent": "FFFFFF"},
    "默认":     {"name": "Charcoal Minimal",   "primary": "36454F", "secondary": "F2F2F2", "accent": "212121"},
}

FALLBACK_FONT = {"heading": "Calibri", "body": "Calibri"}


# ── Category keyword mapping ────────────────────────────────────────────────

CATEGORY_KEYWORDS = [
    ("企业商务", [
        (2, ["商业计划书", "投资人", "融资", "商业模式", "竞争分析", "市值", "股东", "董事会", "ipo", "年报", "季报", "财报"]),
        (1, ["企业", "公司", "商务", "商业", "营销", "市场", "销售", "财务", "会计", "审计",
             "投资", "战略", "管理", "运营", "人力资源", "hr", "kpi", "okr", "提案",
             "策划", "方案", "报告", "规划", "计划", "产品", "品牌", "竞争", "客户"]),
    ]),
    ("未来科技", [
        (2, ["人工智能", "机器学习", "深度学习", "大数据", "云计算", "区块链", "物联网",
             "量子计算", "神经网络", "llm", "gpt", "数字孪生", "智慧城市", "智能制造"]),
        (1, ["未来", "科技", "ai", "iot", "5g", "6g", "机器人", "自动化",
             "vr", "ar", "元宇宙", "芯片", "半导体", "算法", "网络安全",
             "数字化转型", "前沿", "创新技术"]),
    ]),
    ("卡通手绘", [
        (2, ["课件", "教案", "幼儿", "小学生", "中学生", "绘本", "动漫"]),
        (1, ["卡通", "动画", "儿童", "教育", "教学", "培训", "学习", "教程",
             "趣味", "有趣", "可爱", "活泼", "漫画", "插画", "游戏", "玩乐", "校园", "班级", "亲子"]),
    ]),
    ("年终总结", [
        (2, ["年终总结", "年度报告", "述职报告", "工作汇报", "绩效考核", "annual report", "year-end review"]),
        (1, ["年终", "年度", "季度", "月度", "周报", "总结", "回顾", "汇报", "述职",
             "考核", "评估", "成果", "成绩", "绩效", "目标", "完成", "season", "review", "annual"]),
    ]),
    ("扁平简约", [
        (2, ["用户体验", "产品设计", "ui设计", "ux设计", "信息架构", "dashboard", "数据可视化"]),
        (1, ["简约", "简洁", "简单", "极简", "现代", "设计", "视觉", "ui", "ux",
             "数据", "图表", "分析", "统计", "互联网", "app", "软件", "交互"]),
    ]),
    ("中国风", [
        (2, ["水墨", "书法", "国画", "诗词", "国学", "传统节日", "中华文明", "文化遗产"]),
        (1, ["中国", "中华", "传统", "古典", "古风", "历史", "东方",
             "古文", "经典", "春节", "中秋", "端午", "节气", "儒", "道", "禅", "茶", "瓷器", "丝绸"]),
    ]),
    ("文化艺术", [
        (2, ["展览", "博物馆", "美术馆", "画廊", "音乐会", "艺术节", "文化产业"]),
        (1, ["艺术", "美学", "审美", "创作", "音乐", "舞蹈", "戏剧", "电影", "影视",
             "摄影", "绘画", "雕塑", "建筑", "时尚", "文学", "诗歌", "哲学", "人文"]),
    ]),
    ("文艺清新", [
        (2, ["小清新", "治愈系", "生活方式", "旅行日记", "wellness", "lifestyle blog"]),
        (1, ["清新", "治愈", "温暖", "浪漫", "唯美", "优雅", "精致", "自然", "生态",
             "环保", "绿色", "植物", "花卉", "风景", "旅行", "游记", "生活", "情感", "lifestyle"]),
    ]),
    ("创意趣味", [
        (2, ["头脑风暴", "设计思维", "创意工坊", "workshop", "hackathon", "brainstorm"]),
        (1, ["创意", "创新", "创造", "发明", "新奇", "独特", "个性", "脑洞",
             "想象力", "灵感", "娱乐", "休闲"]),
    ]),
    ("学术研究", [
        (2, ["论文", "学术", "研究方法", "文献综述", "实验数据", "统计分析", "peer review",
             "hypothesis", "methodology", "abstract", "citations"]),
        (1, ["研究", "实验", "调查", "医学", "法律", "政治", "生物", "化学", "物理",
             "数学", "工程", "经济学", "社会学", "心理学", "课题", "项目", "理论",
             "科学", "学科", "分析", "结论", "数据", "样本"]),
    ]),
]

TONE_MAP = {
    "企业商务": "formal",  "未来科技": "technical", "卡通手绘": "educational",
    "年终总结": "formal",  "扁平简约": "technical", "中国风":   "creative",
    "文化艺术": "creative", "文艺清新": "creative", "创意趣味": "creative",
    "学术研究": "formal",  "默认":     "formal",
}

SECTIONS_ZH = {
    "企业商务": ["封面", "执行摘要", "市场概况", "核心策略", "执行计划", "团队介绍", "财务预测", "下一步行动"],
    "未来科技": ["封面", "技术背景", "核心架构", "关键能力", "应用场景", "技术优势", "路线图", "总结展望"],
    "卡通手绘": ["封面", "课程目标", "知识点一", "知识点二", "互动练习", "知识回顾", "作业布置"],
    "年终总结": ["封面", "年度回顾", "重点成果", "数据亮点", "挑战与反思", "团队成长", "明年目标", "致谢"],
    "扁平简约": ["封面", "问题背景", "解决方案", "核心数据", "产品演示", "竞品对比", "总结"],
    "中国风":   ["封面", "背景介绍", "文化渊源", "核心内容", "传承价值", "现代意义", "总结"],
    "文化艺术": ["封面", "主题引言", "艺术背景", "核心作品", "创作理念", "影响与价值", "结语"],
    "文艺清新": ["封面", "灵感来源", "内容主题", "精选内容", "情感共鸣", "结语"],
    "创意趣味": ["封面", "痛点洞察", "创意方案", "实现路径", "案例展示", "行动呼吁"],
    "学术研究": ["封面", "研究背景", "文献综述", "研究方法", "实验数据", "结果分析", "结论", "参考文献"],
    "默认":     ["封面", "背景介绍", "主要内容", "核心观点", "数据支撑", "总结", "下一步"],
}

SECTIONS_EN = {
    "企业商务": ["Cover", "Executive Summary", "Market Overview", "Core Strategy", "Action Plan", "Team", "Financials", "Next Steps"],
    "未来科技": ["Cover", "Background", "Architecture", "Key Capabilities", "Use Cases", "Advantages", "Roadmap", "Outlook"],
    "卡通手绘": ["Cover", "Learning Goals", "Topic One", "Topic Two", "Practice", "Review", "Assignment"],
    "年终总结": ["Cover", "Year in Review", "Key Achievements", "Data Highlights", "Challenges", "Team Growth", "Goals for Next Year", "Thank You"],
    "扁平简约": ["Cover", "Problem", "Solution", "Key Data", "Demo", "Comparison", "Summary"],
    "中国风":   ["Cover", "Introduction", "Cultural Origins", "Core Content", "Heritage Value", "Modern Relevance", "Summary"],
    "文化艺术": ["Cover", "Theme Introduction", "Background", "Featured Works", "Creative Vision", "Impact", "Closing"],
    "文艺清新": ["Cover", "Inspiration", "Theme", "Featured Content", "Emotional Resonance", "Closing"],
    "创意趣味": ["Cover", "Pain Points", "Creative Solution", "Implementation", "Case Studies", "Call to Action"],
    "学术研究": ["Cover", "Background", "Literature Review", "Methodology", "Data & Results", "Analysis", "Conclusion", "References"],
    "默认":     ["Cover", "Background", "Main Content", "Key Points", "Data Support", "Summary", "Next Steps"],
}


# ── Scoring ──────────────────────────────────────────────────────────────────

def score_content(text: str) -> tuple[str, dict]:
    text_lower = text.lower()
    scores = {}
    for category, weight_groups in CATEGORY_KEYWORDS:
        total = 0
        for weight, keywords in weight_groups:
            for kw in keywords:
                if kw in text_lower:
                    total += weight
        if total > 0:
            scores[category] = total
    if not scores:
        return "默认", {}
    best = max(scores, key=scores.get)
    sorted_scores = dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))
    return best, sorted_scores


def rank_palettes(palettes: list[dict], content_text: str) -> list[dict]:
    text_lower = content_text.lower()
    scored = []
    for p in palettes:
        tag_score = sum(1 for tag in p["tags"].split() if tag in text_lower)
        scored.append((tag_score, p))
    scored.sort(key=lambda x: x[0], reverse=True)
    if scored and scored[0][0] == 0:
        random.shuffle(scored)
    return [p for _, p in scored[:3]]


def rank_fonts(fonts: list[dict], content_text: str) -> list[dict]:
    text_lower = content_text.lower()
    scored = []
    for f in fonts:
        tag_score = sum(1 for tag in f["tags"].split() if tag in text_lower)
        scored.append((tag_score, f))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [f for _, f in scored[:2]]


def detect_language(text: str) -> str:
    if not text:
        return "zh"
    cjk = sum(1 for c in text if "\u4e00" <= c <= "\u9fff")
    return "zh" if cjk / max(len(text), 1) > 0.15 else "en"


def estimate_slides(text: str, category: str) -> int:
    words = len(text.split())
    estimate = max(6, min(20, words // 150 + 4))
    if category == "年终总结":
        estimate = max(estimate, 12)
    if category == "学术研究":
        estimate = max(estimate, 10)
    return estimate


def suggest_sections(category: str, n: int, lang: str) -> list:
    table = SECTIONS_ZH if lang == "zh" else SECTIONS_EN
    sections = list(table.get(category, table["默认"]))
    if len(sections) > n:
        keep = [sections[0]] + sections[1:n-1] + [sections[-1]]
        sections = keep[:n]
    elif len(sections) < n:
        filler = "内容补充" if lang == "zh" else "Additional Content"
        while len(sections) < n:
            sections.insert(-1, filler)
    return sections


# ── Entry point ──────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Suggest PPT style from content")
    parser.add_argument("--content", help="Raw content text to analyze")
    parser.add_argument("--query", help="Short topic/query string")
    parser.add_argument("--content-file", help="Path to content_analysis.json")
    parser.add_argument("--slides", type=int, help="Override slide count estimate")
    parser.add_argument("--lang", choices=["zh", "en", "auto"], default="auto")
    args = parser.parse_args()

    text = ""
    if args.content:
        text += args.content + "\n"
    if args.query:
        text += args.query + "\n"
    if args.content_file:
        try:
            with open(args.content_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            for file_info in data.get("files", []):
                if file_info.get("role") == "content":
                    text += file_info.get("content", "") + "\n"
            for file_info in data.get("files", []):
                text += file_info.get("filename", "") + " "
        except Exception:
            pass

    if not text.strip():
        text = "通用商务演示"

    lang = args.lang if args.lang != "auto" else detect_language(text)
    category, score_breakdown = score_content(text)
    slide_count = args.slides or estimate_slides(text, category)
    sections = suggest_sections(category, slide_count, lang)

    # Palette candidates from CSV (or fallback)
    all_palettes = load_palettes()
    cat_palettes = all_palettes.get(category, [])
    if cat_palettes:
        palette_candidates = rank_palettes(cat_palettes, text)
    else:
        fb = FALLBACK_PALETTES.get(category, FALLBACK_PALETTES["默认"])
        palette_candidates = [fb]

    # Font candidates from CSV (or fallback)
    all_fonts = load_fonts()
    cat_fonts = all_fonts.get(category, [])
    font_candidates = rank_fonts(cat_fonts, text) if cat_fonts else [FALLBACK_FONT]

    top_palette = palette_candidates[0]
    top_font    = font_candidates[0]

    result = {
        "suggested_category": category,
        "suggested_palette": top_palette.get("name", "Default"),
        "palette_hex": {
            "primary":   top_palette.get("primary", "36454F"),
            "secondary": top_palette.get("secondary", "F2F2F2"),
            "accent":    top_palette.get("accent", "212121"),
        },
        "palette_candidates": [
            {"name": p.get("name",""), "primary": p.get("primary",""),
             "secondary": p.get("secondary",""), "accent": p.get("accent","")}
            for p in palette_candidates
        ],
        "font_heading": top_font.get("heading", "Calibri"),
        "font_body":    top_font.get("body", "Calibri"),
        "font_candidates": [
            {"heading": f.get("heading","Calibri"), "body": f.get("body","Calibri")}
            for f in font_candidates
        ],
        "suggested_tone": TONE_MAP.get(category, "formal"),
        "detected_language": lang,
        "slide_count_estimate": slide_count,
        "key_sections": sections,
        "score_breakdown": score_breakdown,
        "rationale": (
            f"Matched '{category}' (score: {score_breakdown.get(category, 0)}) "
            f"from weighted keyword analysis. "
            + (f"Runner-up: '{list(score_breakdown.keys())[1]}' (score: {list(score_breakdown.values())[1]})"
               if len(score_breakdown) > 1 else "No competing categories.")
        ),
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
