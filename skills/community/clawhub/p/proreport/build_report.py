#!/usr/bin/env python3
"""报告构建器 - 接收 AI 生成的文字内容 + 分析数据，输出 PDF/DOCX

用法:
    python quant_report/build_report.py --analysis output/analysis.json --content output/content.json --format pdf
    python quant_report/build_report.py --analysis output/analysis.json --content output/content.json --format docx
    python quant_report/build_report.py --analysis output/analysis.json --content output/content.json --format all

content.json 格式:
{
  "executive_summary": "...",
  "nav_daily_analysis": "...",
  "nav_weekly_analysis": "...",
  "nav_monthly_analysis": "...",
  "nav_yearly_analysis": "...",
  "indicator_analysis": "...",
  "heatmap_analysis": "...",
  "cta_comparison": "...",
  "suggestions": ["建议1...", "建议2...", ...],
  "conclusion": "...",
  "rolling_sharpe_analysis": "...",
  "per_10k_analysis": "...",
  "drawdown_analysis": "...",
  "sector_analysis": "...",
  "variety_analysis": "..."
}
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def main():
    parser = argparse.ArgumentParser(description="报告构建器")
    parser.add_argument("--analysis", required=True, help="analysis.json 路径")
    parser.add_argument("--content", required=True, help="AI生成的 content.json 路径")
    parser.add_argument("--format", default="all", choices=["pdf", "docx", "all"])
    parser.add_argument("--output", default=None, help="输出目录（默认用 analysis 里的）")
    args = parser.parse_args()

    with open(args.analysis, "r", encoding="utf-8") as f:
        analysis = json.load(f)

    with open(args.content, "r", encoding="utf-8") as f:
        content = json.load(f)

    output_dir = args.output or analysis.get("output_dir", "output")
    name = analysis["strategy_name"]
    outputs = []

    if args.format in ("pdf", "all"):
        from quant_report.pdf_report_v2 import generate_pdf
        pdf_path = f"{output_dir}/{name}_策略评估报告.pdf"
        generate_pdf(analysis, content, pdf_path)
        outputs.append(pdf_path)
        print(f"PDF: {pdf_path}")

    if args.format in ("docx", "all"):
        from quant_report.docx_report_v2 import generate_docx
        docx_path = f"{output_dir}/{name}_策略分析报告.docx"
        generate_docx(analysis, content, docx_path)
        outputs.append(docx_path)
        print(f"DOCX: {docx_path}")

    result = {"outputs": outputs, "status": "success"}
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
