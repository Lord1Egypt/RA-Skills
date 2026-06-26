import argparse
import os
from datetime import datetime
from typing import Optional


def _truthy(s: str) -> bool:
    return str(s).strip().lower() in {"1", "true", "yes", "y", "on"}


def _contains_series(series, value: str):
    value = str(value).strip()
    if not value:
        return None
    s = series.astype(str)
    return s.str.contains(value, na=False, regex=False)


def _equals_series(series, value: str):
    value = str(value).strip()
    if not value:
        return None
    s = series.astype(str).str.strip()
    return s == value


def filter_dataframe(df, org: Optional[str], bill_type: Optional[str], strict: bool = False):
    if df is None or df.empty:
        return df

    org = (org or "").strip()
    bill_type = (bill_type or "").strip()

    # 兼容不同 sheet 的组织列命名
    org_cols = [
        "销售组织",
        "结算组织",
        "付款组织",
        "收款组织",
        "收付组织",
        "核算组织",
        "组织",
    ]
    bill_type_cols = ["单据类型", "业务类型", "单据类型名称"]

    filtered = df

    if org:
        matched = False
        for col in org_cols:
            if col not in filtered.columns:
                continue
            mask = _equals_series(filtered[col], org) if strict else _contains_series(filtered[col], org)
            if mask is None:
                continue
            filtered = filtered[mask]
            matched = True
            break
        if not matched:
            # 该 sheet 没有组织维度列：不动
            pass

    if bill_type:
        matched = False
        for col in bill_type_cols:
            if col not in filtered.columns:
                continue
            mask = _equals_series(filtered[col], bill_type) if strict else _contains_series(filtered[col], bill_type)
            if mask is None:
                continue
            filtered = filtered[mask]
            matched = True
            break
        if not matched:
            pass

    return filtered


def main():
    parser = argparse.ArgumentParser(description="对 data_exporter 导出的多 Sheet Excel 做二次筛选（按组织/单据类型）。")
    parser.add_argument("--input", required=True, help="输入 Excel 文件路径")
    parser.add_argument("--output", default="", help="输出 Excel 文件路径（默认在同目录生成 *_filtered.xlsx）")
    parser.add_argument("--sheet", default="", help="只筛选指定 sheet（不填则处理所有 sheet）")
    parser.add_argument("--org", default="", help="组织编码或名称关键词（例如 101 或 北京xxx）")
    parser.add_argument("--bill-type", default="", help="单据类型关键词（例如 手工标准应收单）")
    parser.add_argument("--strict", default="false", help="是否严格等值匹配（true/false，默认 false 用包含匹配）")

    args = parser.parse_args()

    try:
        import pandas as pd
    except ModuleNotFoundError:
        raise SystemExit("缺少依赖 pandas。请先执行：python -m pip install -r requirements.txt")

    input_path = os.path.abspath(args.input)
    if not os.path.exists(input_path):
        raise SystemExit(f"输入文件不存在：{input_path}")

    strict = _truthy(args.strict)

    if args.output:
        output_path = os.path.abspath(args.output)
    else:
        base, ext = os.path.splitext(input_path)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"{base}_filtered_{ts}.xlsx"

    xls = pd.ExcelFile(input_path)
    sheet_names = xls.sheet_names
    if args.sheet:
        if args.sheet not in sheet_names:
            raise SystemExit(f"sheet 不存在：{args.sheet}。可选：{', '.join(sheet_names)}")
        sheet_names = [args.sheet]

    out = {}
    for name in sheet_names:
        df = pd.read_excel(input_path, sheet_name=name)
        out[name] = filter_dataframe(df, org=args.org, bill_type=args.bill_type, strict=strict)

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        for name, df in out.items():
            (df if df is not None else pd.DataFrame()).to_excel(writer, sheet_name=name, index=False)

    print(f"已生成：{output_path}")


if __name__ == "__main__":
    main()

