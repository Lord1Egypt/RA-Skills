#!/usr/bin/env python3
"""
AI珠宝鉴定与选购 — 交互式 HTML 报告生成器
用法: python generate_report.py --type <品类> --mode <模式> --query "<用户问题>" [--output <路径>]
品类: diamond | colored-gem | jadeite | pearl | colored-diamond | metal | certificate | investment | custom
模式: knowledge | purchase | appraisal | price | certificate | investment | full
"""

import argparse
import json
import sys
import os
from datetime import datetime
from pathlib import Path

# Template path relative to skill
SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = SKILL_DIR / "assets" / "report_template.html"

CATEGORY_LABELS = {
    "diamond": "钻石",
    "colored-gem": "彩色宝石",
    "jadeite": "翡翠",
    "pearl": "珍珠",
    "colored-diamond": "彩钻",
    "metal": "贵金属",
    "certificate": "鉴定证书",
    "investment": "投资收藏",
    "custom": "婚戒定制",
}

CATEGORY_EMOJIS = {
    "diamond": "💎",
    "colored-gem": "💠",
    "jadeite": "🟢",
    "pearl": "🦪",
    "colored-diamond": "💖",
    "metal": "🪙",
    "certificate": "📜",
    "investment": "📈",
    "custom": "💍",
}

CATEGORY_BADGE_CLASSES = ["badge-tag1", "badge-tag2", "badge-tag3", "badge-tag4"]


def load_template():
    """Load the HTML report template."""
    if TEMPLATE_PATH.exists():
        with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
            return f.read()
    # Fallback: minimal inline template
    return get_fallback_template()


def get_fallback_template():
    """Provide a minimal template if the asset file is missing."""
    return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{TITLE}}</title>
<style>
  body { font-family: 'PingFang SC','Microsoft YaHei',sans-serif; max-width:800px; margin:40px auto; padding:20px; background:#faf8f5; color:#2c2c2c; line-height:1.7; }
  h1 { color:#1a1a2e; border-bottom:3px solid #d4a574; padding-bottom:10px; }
  .card { background:#fff; border-radius:12px; padding:24px; margin-bottom:20px; box-shadow:0 2px 12px rgba(0,0,0,.06); }
  h2 { color:#1a1a2e; font-size:1.2rem; }
  table { width:100%; border-collapse:collapse; margin:12px 0; font-size:.9rem; }
  th { background:#1a1a2e; color:#fff; padding:8px 12px; text-align:left; }
  td { padding:8px 12px; border-bottom:1px solid #e8e0d5; }
  .badge { display:inline-block; padding:4px 14px; border-radius:20px; font-size:.8rem; font-weight:500; margin:4px; }
  .badge-tag1 { background:#e8d5c4; color:#5a3e2b; }
  .badge-tag2 { background:#d4e5d9; color:#2a5a3a; }
  .badge-tag3 { background:#d4dce5; color:#2a3a5a; }
  .badge-tag4 { background:#e5d4e0; color:#5a2a4a; }
  .warning { background:#fff8f0; border:1px solid #e8c48a; border-radius:8px; padding:16px; margin:12px 0; }
  .advice-item { display:flex; gap:12px; padding:10px 0; border-bottom:1px dashed #e8e0d5; }
  .priority { width:36px; height:24px; border-radius:12px; display:flex; align-items:center; justify-content:center; font-size:.7rem; font-weight:700; color:#fff; flex-shrink:0; }
  .p0 { background:#c0392b; } .p1 { background:#c77d20; } .p2 { background:#2c6faa; }
  .disclaimer { text-align:center; padding:20px; color:#666; font-size:.82rem; border-top:1px solid #e8e0d5; margin-top:30px; }
  .price-tag { display:inline-block; background:linear-gradient(135deg,#d4a574,#c9a96e); color:#fff; padding:4px 14px; border-radius:20px; font-weight:600; font-size:.85rem; margin:3px; }
</style>
</head>
<body>
{{CONTENT}}
<div class="disclaimer">⚠️ 本报告基于公开数据和 AI 分析生成，仅供参考。实际购买前请核实实物、查看权威鉴定证书，并咨询专业鉴定师。</div>
</body>
</html>"""


def build_html(args, template):
    """Build the full HTML report by replacing template placeholders."""
    category = args.type
    mode = args.mode
    query = args.query or ""
    emoji = CATEGORY_EMOJIS.get(category, "💎")
    label = CATEGORY_LABELS.get(category, category)

    # Title
    title = f"AI珠宝鉴定报告 — {label}"
    hero_title = f"{emoji} {label} · {get_mode_label(mode)}"
    hero_subtitle = query if query else f"基于专业知识的{label}分析报告"

    # Badges
    badges = build_badges(category, mode)

    # Section placeholders — will be filled by WorkBuddy AI at generation time
    content = {
        "TITLE": title,
        "HERO_TITLE": hero_title,
        "HERO_SUBTITLE": hero_subtitle,
        "BADGES": badges,
        "KNOWLEDGE_CONTENT": "<!-- 由 AI 动态填充核心知识 -->",
        "ANALYSIS_CONTENT": "<!-- 由 AI 动态填充分析结论 -->",
        "SCORE_SECTION": "",
        "PRICE_CONTENT": "<!-- 由 AI 动态填充价格参考 -->",
        "ADVICE_TITLE": "选购与鉴定建议",
        "ADVICE_ITEMS": "<!-- 由 AI 动态填充建议列表 -->",
        "WARNING_ITEMS": "<!-- 由 AI 动态填充风险提示 -->",
        "CHECKLIST_ITEMS": "<!-- 由 AI 动态填充行动清单 -->",
        "CERT_SECTION": "",
    }

    # Certificate mode
    if mode == "certificate" or category == "certificate":
        content["CERT_SECTION"] = """<div class="card">
    <h2><span class="icon">📜</span> 证书关键信息解读</h2>
    <!-- 由 AI 动态填充证书解读 -->
</div>"""
    if category == "investment":
        content["ADVICE_TITLE"] = "投资建议"

    html = template
    for key, val in content.items():
        html = html.replace("{{" + key + "}}", val)

    return html


def build_badges(category, mode):
    """Generate badge HTML based on category and mode."""
    badges = []
    label = CATEGORY_LABELS.get(category, category)
    mode_labels = {
        "knowledge": "知识科普",
        "purchase": "选购指导",
        "appraisal": "真伪鉴定",
        "price": "价格评估",
        "certificate": "证书解读",
        "investment": "投资建议",
        "full": "综合分析",
    }
    badges.append(f'<span class="badge badge-tag1">{label}</span>')
    badges.append(f'<span class="badge badge-tag2">{mode_labels.get(mode, mode)}</span>')
    badges.append(f'<span class="badge badge-tag3">{datetime.now().strftime("%Y-%m-%d")}</span>')
    return "\n    ".join(badges)


def get_mode_label(mode):
    """Get display label for mode."""
    labels = {
        "knowledge": "知识科普",
        "purchase": "选购指导",
        "appraisal": "真伪鉴定",
        "price": "价格评估",
        "certificate": "证书解读",
        "investment": "投资收藏建议",
        "full": "综合分析报告",
    }
    return labels.get(mode, mode)


def main():
    parser = argparse.ArgumentParser(
        description="AI珠宝鉴定与选购 — HTML报告生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python generate_report.py --type diamond --mode purchase --query "1克拉钻石怎么选？预算5万"
  python generate_report.py --type jadeite --mode appraisal --query "这个翡翠是A货还是B货？"
  python generate_report.py --type pearl --mode knowledge --query "Akoya和淡水珍珠有什么区别？"
  python generate_report.py --type investment --mode investment --query "红宝石值得投资吗？"
  python generate_report.py --type custom --mode full --query "婚戒定制，预算3万"
        """
    )
    parser.add_argument("--type", required=True,
                        choices=list(CATEGORY_LABELS.keys()),
                        help="珠宝品类")
    parser.add_argument("--mode", default="full",
                        choices=["knowledge", "purchase", "appraisal", "price", "certificate", "investment", "full"],
                        help="分析模式 (默认: full)")
    parser.add_argument("--query", default="", help="用户原始问题")
    parser.add_argument("--output", default="", help="输出文件路径（默认: 品类_YYYYMMDD_HHMMSS.html）")

    args = parser.parse_args()

    # Default output path
    if not args.output:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.output = f"{args.type}_{args.mode}_{timestamp}.html"

    # Load template
    template = load_template()

    # Build HTML
    html = build_html(args, template)

    # Write output
    out_path = Path(args.output)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

    label = CATEGORY_LABELS.get(args.type, args.type)
    emoji_text = {"diamond": "[Diamond]", "colored-gem": "[Gem]", "jadeite": "[Jade]", "pearl": "[Pearl]", "colored-diamond": "[Fancy]", "metal": "[Metal]", "certificate": "[Cert]", "investment": "[Invest]", "custom": "[Ring]"}.get(args.type, "")
    print(f"{emoji_text} {label} report generated: {out_path.absolute()}")
    print(f"   Category: {label} | Mode: {get_mode_label(args.mode)}")
    if args.query:
        print(f"   Query: {args.query}")

    # Output JSON for AI to fill content
    result = {
        "report_path": str(out_path.absolute()),
        "category": args.type,
        "category_label": label,
        "mode": args.mode,
        "mode_label": get_mode_label(args.mode),
        "query": args.query,
        "action": "AI_MUST_FILL_CONTENT",
        "instruction": "读取生成的HTML报告，用专业知识填充所有 <!-- 由 AI 动态填充 --> 占位符。参考 references/ 目录下的对应知识库文件。"
    }
    # Write metadata alongside
    meta_path = out_path.with_suffix(".meta.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
