"""主入口 - 量化策略评估报告生成器

用法:
    python -m skill                          # 自动检测 data/ 目录
    python -m skill --data data/             # 指定数据目录
    python -m skill --nav xx策略净值.xlsx     # 指定净值文件
    python -m skill --format pdf             # 仅生成 PDF
    python -m skill --format docx            # 仅生成 Word
    python -m skill --format all             # 生成 PDF + Word (默认)
    python -m skill --output output/         # 指定输出目录
    python -m skill --name "策略名称"        # 指定策略名称
"""
import argparse
import sys
import time
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="量化策略评估报告生成器")
    parser.add_argument("--data", default="data", help="数据目录路径")
    parser.add_argument("--nav", default=None, help="策略净值文件路径")
    parser.add_argument("--variety", default=None, help="品种净值文件路径")
    parser.add_argument("--name", default=None, help="策略名称")
    parser.add_argument("--format", default="all", choices=["pdf", "docx", "all"],
                       help="输出格式: pdf/docx/all")
    parser.add_argument("--output", default="output", help="输出目录")
    args = parser.parse_args()

    print("=" * 60)
    print("  量化策略评估报告生成器 v1.0")
    print("=" * 60)

    # 1. 加载数据
    print("\n[1/4] 加载数据...")
    from .data_loader import load_strategy_data, auto_detect_data

    if args.nav:
        nav_path = args.nav
        variety_path = args.variety
        name = args.name or "策略"
    else:
        nav_path, variety_path, name = auto_detect_data(args.data)
        if args.name:
            name = args.name

    if not nav_path:
        print("错误: 未找到策略净值文件，请确认 data/ 目录下有 xlsx 文件")
        sys.exit(1)

    print(f"  策略净值: {nav_path}")
    print(f"  品种净值: {variety_path or '无'}")
    print(f"  策略名称: {name}")

    data = load_strategy_data(nav_path, variety_path, name)
    print(f"  数据范围: {data.start_date} ~ {data.end_date} ({data.trading_days}个交易日)")

    # 2. 分析计算
    print("\n[2/4] 分析计算...")
    t0 = time.time()
    from .analyzer import analyze
    result = analyze(data)
    c = result.core
    print(f"  累计收益率: {c.cumulative_return:.2%}")
    print(f"  年化收益率: {c.annualized_return:.2%}")
    print(f"  最大回撤:   {c.max_drawdown:.2%}")
    print(f"  夏普比率:   {c.sharpe_ratio:.2f}")
    print(f"  卡玛比率:   {c.calmar_ratio:.2f}")
    print(f"  日胜率:     {c.daily_win_rate:.1%}")
    print(f"  分析耗时:   {time.time()-t0:.1f}s")

    # 3. 生成图表
    print("\n[3/4] 生成图表...")
    t0 = time.time()
    from .chart_generator import generate_all_charts
    chart_dir = f"{args.output}/charts"
    charts = generate_all_charts(result, chart_dir)
    print(f"  生成 {len(charts)} 张图表 → {chart_dir}/")
    print(f"  图表耗时: {time.time()-t0:.1f}s")

    # 4. 生成报告
    print("\n[4/4] 生成报告...")
    outputs = []

    # 构建 v2 报告需要的 dict 格式 (analysis + content)
    from .run_analysis import result_to_dict
    analysis = result_to_dict(result, name, nav_path, variety_path, charts)
    # main.py 直接运行时用模板文字（非 AI skill 模式）
    from .analyzer import generate_text_summary
    summaries = generate_text_summary(result)
    content = {
        "executive_summary": summaries.get("executive", ""),
        "nav_yearly_analysis": summaries.get("yearly", ""),
        "drawdown_analysis": summaries.get("drawdown", ""),
        "sector_analysis": summaries.get("sector", ""),
        "variety_analysis": summaries.get("variety", ""),
        "suggestions": summaries.get("suggestions", []),
        "conclusion": "",
        "indicator_evaluations": {},
    }

    if args.format in ("pdf", "all"):
        t0 = time.time()
        from .pdf_report_v2 import generate_pdf
        pdf_path = f"{args.output}/{name}_策略评估报告.pdf"
        generate_pdf(analysis, content, pdf_path)
        outputs.append(pdf_path)
        print(f"  PDF 报告: {pdf_path} ({time.time()-t0:.1f}s)")

    if args.format in ("docx", "all"):
        t0 = time.time()
        from .docx_report_v2 import generate_docx
        docx_path = f"{args.output}/{name}_策略分析报告.docx"
        generate_docx(analysis, content, docx_path)
        outputs.append(docx_path)
        print(f"  Word报告: {docx_path} ({time.time()-t0:.1f}s)")

    print("\n" + "=" * 60)
    print("  报告生成完成！")
    for o in outputs:
        print(f"  → {o}")
    print("=" * 60)


if __name__ == "__main__":
    main()
