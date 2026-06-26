"""
历史数据比对脚本 — 支持 Excel/CSV 的同比、环比分析
用法: python3 compare.py <file> --date-col <列> --metric-cols <列1,列2> --compare <yoy|mom|both> --period <daily|monthly|quarterly> [--output <path>]
"""

import argparse
import sys
from pathlib import Path

import pandas as pd


def load_data(path: str) -> pd.DataFrame:
    """读取 Excel 或 CSV 文件"""
    p = Path(path)
    if p.suffix.lower() in (".xlsx", ".xls"):
        df = pd.read_excel(path)
    elif p.suffix.lower() == ".csv":
        df = pd.read_csv(path)
    else:
        raise ValueError(f"不支持的文件格式: {p.suffix}，仅支持 .xlsx / .xls / .csv")
    return df


def parse_date_col(df: pd.DataFrame, col: str, period: str) -> pd.DataFrame:
    """解析日期列并提取周期"""
    df["_date"] = pd.to_datetime(df[col], errors="coerce")
    if df["_date"].isna().all():
        raise ValueError(f"日期列 '{col}' 无法解析为日期格式")

    if period == "daily":
        df["_period"] = df["_date"].dt.date
    elif period == "monthly":
        df["_period"] = df["_date"].dt.to_period("M").astype(str)
    elif period == "quarterly":
        df["_period"] = df["_date"].dt.to_period("Q").astype(str)
    else:
        raise ValueError(f"不支持的 period: {period}，可选 daily/monthly/quarterly")

    return df


def compute_compare(df: pd.DataFrame, metric_cols: list, compare_type: str) -> pd.DataFrame:
    """按 _period 聚合并计算变动率"""
    agg = df.groupby("_period")[metric_cols].sum()

    result_rows = []
    periods = list(agg.index)

    for i, period in enumerate(periods):
        row = {"周期": period}
        for col in metric_cols:
            row[f"{col}"] = agg.loc[period, col]
            if compare_type in ("mom", "both") and i > 0:
                prev = agg.loc[periods[i - 1], col]
                if prev != 0:
                    row[f"{col}_环比变动额"] = agg.loc[period, col] - prev
                    row[f"{col}_环比变动率"] = round((agg.loc[period, col] - prev) / abs(prev) * 100, 2)
                else:
                    row[f"{col}_环比变动额"] = None
                    row[f"{col}_环比变动率"] = None

            if compare_type in ("yoy", "both"):
                # 尝试匹配去年同期：取周期字符串中的年/月/季
                yoy_period = shift_period(period)
                if yoy_period and yoy_period in agg.index:
                    yoy_val = agg.loc[yoy_period, col]
                    if yoy_val != 0:
                        row[f"{col}_同比变动额"] = agg.loc[period, col] - yoy_val
                        row[f"{col}_同比变动率"] = round((agg.loc[period, col] - yoy_val) / abs(yoy_val) * 100, 2)
                    else:
                        row[f"{col}_同比变动额"] = None
                        row[f"{col}_同比变动率"] = None
                else:
                    row[f"{col}_同比变动额"] = None
                    row[f"{col}_同比变动率"] = None
        result_rows.append(row)

    return pd.DataFrame(result_rows)


def shift_period(period: str) -> str | None:
    """将周期字符串回退一年 (e.g. 2024-03 -> 2023-03, 2024Q1 -> 2023Q1, 2024-01-01 -> 2023-01-01)"""
    try:
        if "Q" in period:
            # e.g. "2024Q1"
            parts = period.split("Q")
            return f"{int(parts[0]) - 1}Q{parts[1]}"
        elif period.count("-") == 1:
            # e.g. "2024-03"
            parts = period.split("-")
            return f"{int(parts[0]) - 1}-{parts[1]}"
        elif period.count("-") == 2:
            # e.g. "2024-03-15"
            parts = period.split("-")
            return f"{int(parts[0]) - 1}-{parts[1]}-{parts[2]}"
    except (ValueError, IndexError):
        pass
    return None


def format_output(df: pd.DataFrame, compare_type: str, metric_cols: list) -> str:
    """格式化输出结果"""
    lines = []
    lines.append("=" * 80)
    compare_label = {"yoy": "同比", "mom": "环比", "both": "同比+环比"}[compare_type]
    lines.append(f"  📊 历史数据比对报告（{compare_label}）")
    lines.append("=" * 80)
    lines.append("")

    # 显示对比表
    lines.append("【对比数据表】")
    # 构建精简列
    display_cols = ["周期"]
    for col in metric_cols:
        display_cols.append(col)
        if compare_type in ("mom", "both"):
            display_cols.extend([f"{col}_环比变动额", f"{col}_环比变动率"])
        if compare_type in ("yoy", "both"):
            display_cols.extend([f"{col}_同比变动额", f"{col}_同比变动率"])

    existing_cols = [c for c in display_cols if c in df.columns]
    show_df = df[existing_cols].copy()

    # 数字格式化
    for col in metric_cols:
        if col in show_df.columns:
            show_df[col] = show_df[col].apply(lambda x: f"{x:,.2f}" if pd.notna(x) else "-")
    for col in show_df.columns:
        if "变动额" in col:
            show_df[col] = show_df[col].apply(lambda x: f"{x:,.2f}" if pd.notna(x) else "-")
        elif "变动率" in col:
            show_df[col] = show_df[col].apply(lambda x: f"{x:+.2f}%" if pd.notna(x) else "-")

    lines.append(show_df.to_string(index=False))
    lines.append("")

    # 摘要
    lines.append("【关键发现摘要】")
    last = df.iloc[-1] if len(df) > 1 else None
    if last is not None:
        for col in metric_cols:
            current_val = last.get(col)
            if pd.isna(current_val):
                continue
            lines.append(f"  指标「{col}」最新值: {current_val:,.2f}")
            if compare_type in ("mom", "both"):
                rate = last.get(f"{col}_环比变动率")
                if pd.notna(rate):
                    direction = "↑" if rate > 0 else "↓" if rate < 0 else "→"
                    lines.append(f"    环比: {direction} {abs(rate):.2f}%")
            if compare_type in ("yoy", "both"):
                rate = last.get(f"{col}_同比变动率")
                if pd.notna(rate):
                    direction = "↑" if rate > 0 else "↓" if rate < 0 else "→"
                    lines.append(f"    同比: {direction} {abs(rate):.2f}%")
    else:
        lines.append("  数据仅有一期，无法计算变动。")

    lines.append("")
    lines.append("=" * 80)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="历史数据比对分析")
    parser.add_argument("file", help="数据文件路径 (.xlsx / .csv)")
    parser.add_argument("--date-col", required=True, help="日期列名")
    parser.add_argument("--metric-cols", required=True, help="指标列名（逗号分隔）")
    parser.add_argument("--compare", required=True, choices=["yoy", "mom", "both"], help="对比类型")
    parser.add_argument("--period", required=True, choices=["daily", "monthly", "quarterly"], help="数据周期粒度")
    parser.add_argument("--output", default=None, help="输出文件路径（可选，默认 stdout）")

    args = parser.parse_args()
    metric_cols = [c.strip() for c in args.metric_cols.split(",")]

    df = load_data(args.file)
    cols_lower = {c.lower(): c for c in df.columns}
    # 检查列是否存在（不区分大小写匹配）
    date_col = cols_lower.get(args.date_col.lower(), args.date_col)
    metric_cols_resolved = [cols_lower.get(c.lower(), c) for c in metric_cols]

    if date_col not in df.columns:
        print(f"❌ 错误：找不到日期列 '{args.date_col}'", file=sys.stderr)
        print(f"   可用列: {list(df.columns)}", file=sys.stderr)
        sys.exit(1)
    for col in metric_cols_resolved:
        if col not in df.columns:
            print(f"❌ 错误：找不到指标列 '{col}'", file=sys.stderr)
            print(f"   可用列: {list(df.columns)}", file=sys.stderr)
            sys.exit(1)

    df = parse_date_col(df, date_col, args.period)
    result = compute_compare(df, metric_cols_resolved, args.compare)
    output = format_output(result, args.compare, metric_cols_resolved)

    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"✅ 报告已保存到: {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
