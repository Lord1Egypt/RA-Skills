#!/usr/bin/env python3
"""解析共同赢账单 + 到货单，输出统一 keyspace 的 JSON。

输入:
  1) 共同赢账单 .xls (销售出库序时簿格式, 单号 XSCK-...)
  2) 到货单 .xlsx (单号 CGRKD-...)

输出 JSON 字段:
  results: [{sales_name, invoice_name, sales_amt, invoice_amt, diff, ...}]
  unmapped_sales: [账单店名]
  unmatched_invoice: [到货店名]
  detail: [{store, sku, name, bill_price/qty/amt, inv_price/qty/amt, ...flags}]

用法:
  python3 parse_tables.py <bill.xls> <invoice.xlsx> [output.json]
"""
import sys, json
from collections import defaultdict
import xlrd
from openpyxl import load_workbook

# 允许从同目录导入 store_mapping
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from store_mapping import STORE_MAPPING


def parse_bill(path):
    """解析共同赢账单 (销售出库序时簿 .xls)"""
    wb = xlrd.open_workbook(path, formatting_info=False)
    sh = wb.sheet_by_name('销售出库序时簿')
    rows = []
    for r in range(1, sh.nrows):
        rv = sh.row_values(r)
        if not rv[0]:
            continue
        try:
            rows.append({
                'order': rv[0], 'store': rv[1], 'sku': str(rv[2]).strip(),
                'name': rv[3], 'spec': rv[4] or '', 'unit': rv[5] or '',
                'qty': float(rv[6]) if rv[6] != '' else 0,
                'price': float(rv[7]) if rv[7] != '' else 0,
                'amt': float(rv[8]) if rv[8] != '' else 0,
            })
        except Exception:
            pass
    return rows


def parse_invoice(path):
    """解析到货单 (.xlsx)，剔除末尾『合计』空行"""
    wb = load_workbook(path, data_only=True)
    ws = wb['到货单明细表']
    rows = []
    for r in ws.iter_rows(min_row=2, values_only=True):
        if not r[1] or r[1] == '合计' or r[11] is None:
            continue
        rows.append({
            'order': r[3], 'store': r[1], 'sku': str(r[5]).strip(),
            'name': r[6], 'spec': r[7] or '', 'unit': r[8] or '',
            'qty': float(r[10]),
            'price': float(r[9]),
            'amt': float(r[11]),
            'date': str(r[4]) if r[4] else '',
        })
    return rows


def aggregate(rows, key_store='store', key_sku='sku'):
    d = defaultdict(lambda: {'qty': 0, 'amt': 0, 'price_set': set()})
    for r in rows:
        d[(r[key_store], r[key_sku])]['qty'] += r['qty']
        d[(r[key_sku],) if False else (r[key_store], r[key_sku])]['amt'] += r['amt']
        d[(r[key_store], r[key_sku])]['price_set'].add(r['price'])
    return d


def main():
    if len(sys.argv) < 3:
        print("用法: python3 parse_tables.py <bill.xls> <invoice.xlsx> [output.json]")
        sys.exit(1)
    bill_path = sys.argv[1]
    inv_path = sys.argv[2]
    out_path = sys.argv[3] if len(sys.argv) > 3 else '/tmp/gtyt_parsed.json'

    bill_rows = parse_bill(bill_path)
    inv_rows = parse_invoice(inv_path)

    # 店名映射
    results = []
    matched_inv_keys = set()
    unmapped_sales = []
    for s in {r['store'] for r in bill_rows}:
        if s not in STORE_MAPPING:
            unmapped_sales.append(s)
    for s in {r['store'] for r in inv_rows}:
        inv_v = STORE_MAPPING.get(s)
        if inv_v:
            matched_inv_keys.add(inv_v)

    # 汇总金额
    bill_by_store = defaultdict(float)
    for r in bill_rows:
        bill_by_store[r['store']] += r['amt']
    inv_by_store = defaultdict(float)
    for r in inv_rows:
        inv_by_store[r['store']] += r['amt']

    for sname, s_amt in bill_by_store.items():
        inv_store = STORE_MAPPING.get(sname)
        i_amt = inv_by_store.get(inv_store) if inv_store else None
        if i_amt is not None:
            matched_inv_keys.add(inv_store)
        diff = (s_amt - i_amt) if i_amt is not None else None
        results.append({
            'sales_name': sname,
            'invoice_name': inv_store,
            'sales_amt': round(s_amt, 2),
            'invoice_amt': round(i_amt, 2) if i_amt is not None else None,
            'diff': round(diff, 2) if diff is not None else None,
        })

    # 全量 SKU-店 差异明细（用于标黄）
    bill_agg = aggregate(bill_rows)
    inv_agg = aggregate(inv_rows)
    sku_to_name = {}
    for r in bill_rows:
        if r['sku'] not in sku_to_name:
            sku_to_name[r['sku']] = r['name']

    detail = []
    diff_store_names = {r['sales_name'] for r in results
                        if r['diff'] is not None and abs(r['diff']) > 0.01}
    for (sname, sku), b_info in bill_agg.items():
        if sname not in diff_store_names:
            continue
        bill_price = (sum(b_info['price_set']) / len(b_info['price_set'])) if b_info['price_set'] else 0
        i_info = inv_agg.get((sname if False else STORE_MAPPING.get(sname, sname), sku))
        # 注意: inv_agg 的 key 是到货店名。这里按店名映射重新查询
        inv_store = STORE_MAPPING.get(sname, sname)
        i_info = inv_agg.get((inv_store, sku))
        if i_info:
            inv_qty = i_info['qty']
            inv_amt = i_info['amt']
            inv_price = (sum(i_info['price_set']) / len(i_info['price_set'])) if i_info['price_set'] else 0
        else:
            inv_qty = 0
            inv_amt = 0
            inv_price = 0

        price_diff = abs(round(bill_price, 4) - round(inv_price, 4)) > 0.005
        qty_diff = abs(round(b_info['qty'] - inv_qty, 2)) > 0.005
        amt_diff = abs(round(b_info['amt'] - inv_amt, 2)) > 0.005
        missing_in_inv = (i_info is None) and b_info['amt'] > 0
        if price_diff or qty_diff or amt_diff or missing_in_inv:
            detail.append({
                'store': sname,
                'invoice_store': inv_store,
                'sku': sku,
                'name': sku_to_name.get(sku, ''),
                'bill_price': bill_price,
                'bill_qty': b_info['qty'],
                'bill_amt': b_info['amt'],
                'inv_price': inv_price,
                'inv_qty': inv_qty,
                'inv_amt': inv_amt,
                'price_diff': price_diff,
                'qty_diff': qty_diff,
                'amt_diff': amt_diff,
                'missing_in_inv': missing_in_inv,
            })

    unmatched_invoice = sorted(set(inv_by_store) - matched_inv_keys)
    output = {
        'results': results,
        'unmapped_sales': sorted(unmapped_sales),
        'unmatched_invoice': unmatched_invoice,
        'detail': detail,
        'meta': {
            'bill_rows': len(bill_rows),
            'inv_rows': len(inv_rows),
            'total_sales_amt': round(sum(bill_by_store.values()), 2),
            'total_inv_amt': round(sum(inv_by_store.values()), 2),
        }
    }
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"输出: {out_path}")
    print(f"  账单行: {len(bill_rows)} | 到货行: {len(inv_rows)}")
    print(f"  差异店: {sum(1 for r in results if r['diff'] is not None and abs(r['diff'])>0.01)}")
    print(f"  差异 SKU-店: {len(detail)}")
    print(f"  未映射账单店: {len(unmapped_sales)} | 未匹配到货店: {len(unmatched_invoice)}")


if __name__ == '__main__':
    main()
