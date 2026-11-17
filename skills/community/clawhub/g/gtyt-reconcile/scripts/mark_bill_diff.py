#!/usr/bin/env python3
"""在共同赢账单原 .xls 上用黄色背景标出每个差异单元格。

保留原表的字体/列宽/货币格式，只修改背景色 (pattern_colour_index=13)。
标黄范围: 数量(col6)/单价(col7)/金额(col8) 三列
标黄条件: 任一字段差异 > 0.01, 或账单有但到货单无 (missing_in_inv)

用法:
  python3 mark_bill_diff.py <bill.xls> <parsed.json> <output.xls>
"""
import sys, json
import xlrd, xlwt
from xlutils.copy import copy

COL_QTY = 6
COL_PRICE = 7
COL_AMT = 8

yellow_num = xlwt.easyxf('pattern: pattern solid, fore_colour yellow', num_format_str='#,##0.00')
yellow_money = xlwt.easyxf('pattern: pattern solid, fore_colour yellow', num_format_str='"￥"#,##0.00;[Red]"￥"\\-#,##0.00')


def main():
    if len(sys.argv) < 4:
        print("用法: python3 mark_bill_diff.py <bill.xls> <parsed.json> <output.xls>")
        sys.exit(1)
    bill_path = sys.argv[1]
    parsed_path = sys.argv[2]
    out_path = sys.argv[3]

    with open(parsed_path) as f:
        data = json.load(f)
    detail = data.get('detail', [])

    # (store, sku, col) 集合
    diff_set = set()
    for d in detail:
        store = d['store']
        sku = d['sku']
        if d.get('missing_in_inv'):
            diff_set.add((store, sku, COL_QTY))
            diff_set.add((store, sku, COL_PRICE))
            diff_set.add((store, sku, COL_AMT))
        else:
            if d['qty_diff']: diff_set.add((store, sku, COL_QTY))
            if d['price_diff']: diff_set.add((store, sku, COL_PRICE))
            if d['amt_diff']: diff_set.add((store, sku, COL_AMT))
    print(f"差异标记数: {len(diff_set)}")

    wb = xlrd.open_workbook(bill_path, formatting_info=True)
    sh = wb.sheet_by_name('销售出库序时簿')
    wbcopy = copy(wb)
    wsh = wbcopy.get_sheet('销售出库序时簿')

    hits = 0
    for r in range(1, sh.nrows):
        rv = sh.row_values(r)
        if not rv[0]: continue
        sname = rv[1]
        sku = str(rv[2]).strip()
        if (sname, sku, COL_QTY) in diff_set:
            wsh.write(r, COL_QTY, rv[COL_QTY], yellow_num); hits += 1
        if (sname, sku, COL_PRICE) in diff_set:
            wsh.write(r, COL_PRICE, rv[COL_PRICE], yellow_num); hits += 1
        if (sname, sku, COL_AMT) in diff_set:
            wsh.write(r, COL_AMT, rv[COL_AMT], yellow_money); hits += 1
    print(f"已标记单元格: {hits}")

    wbcopy.save(out_path)
    import os
    print(f"已保存: {out_path} ({os.path.getsize(out_path):,} bytes)")


if __name__ == '__main__':
    main()
