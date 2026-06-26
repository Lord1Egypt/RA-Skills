#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""快速 dump 任意 .xls/.xlsx 的结构，供 OpenClaw agent 决定 sheet/表头行/列映射。

用法: python inspect_form.py <文件...> [--rows 8] [--cols 30]
对每个文件每个 sheet 打印：维度、合并单元格、前 N 行预览，并给出“疑似表头行/疑似日期列”提示。
"""
from __future__ import annotations
import sys, os, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_forms import read_any, parse_date_header, is_probably_non_date, norm_text


def guess_header_row(rows, scan=8):
    best, score = 0, -1
    for i in range(min(scan, len(rows))):
        non_empty = sum(1 for c in rows[i] if c is not None and str(c).strip())
        text_cells = sum(1 for c in rows[i]
                         if isinstance(c, str) and c.strip() and not c.strip().replace(".", "").isdigit())
        s = non_empty + text_cells
        if s > score:
            best, score = i, s
    return best


def guess_date_cols(row):
    out = []
    for j, c in enumerate(row):
        if is_probably_non_date(c):
            continue
        d = parse_date_header(c, allow_serial=True)
        if d and d.get("iso") and d["kind"] in ("day", "month"):
            out.append((j, d["iso"]))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--rows", type=int, default=8)
    ap.add_argument("--cols", type=int, default=28)
    args = ap.parse_args()

    for path in args.files:
        print("=" * 78)
        print("📄", os.path.basename(path))
        try:
            import warnings; warnings.filterwarnings("ignore")
            import pandas as pd
            sheets = pd.ExcelFile(path).sheet_names if not path.lower().endswith(".csv") else ["csv"]
        except Exception as e:
            print("  打开失败:", e); continue
        print("  sheets:", sheets)
        for sn in sheets[:8]:
            try:
                info = read_any(path, sheet=sn, max_rows=max(args.rows, 6))
            except Exception as e:
                print(f"  [{sn}] 读取失败: {e}"); continue
            rows = info["rows"]
            if not rows:
                print(f"  --- '{sn}' 空 ---"); continue
            ncol = max((len(r) for r in rows), default=0)
            hg = guess_header_row(rows)
            dcols = guess_date_cols(rows[hg]) if hg < len(rows) else []
            print(f"  --- '{sn}'  约 {len(rows)}+ 行 × {ncol} 列  | 疑似表头行={hg}  "
                  f"疑似日期列={len(dcols)}{'('+dcols[0][1]+'~'+dcols[-1][1]+')' if dcols else ''} ---")
            for i, r in enumerate(rows[:args.rows]):
                cells = []
                for j, v in enumerate(r[:args.cols]):
                    if v is not None and str(v).strip() != "":
                        s = str(v).replace("\n", "\\n")
                        if len(s) > 16:
                            s = s[:16] + "…"
                        cells.append(f"{j}:{s}")
                mark = " «表头?" if i == hg else ""
                if cells:
                    print(f"     R{i}{mark}:", " | ".join(cells))


if __name__ == "__main__":
    main()
