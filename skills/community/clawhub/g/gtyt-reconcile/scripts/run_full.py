#!/usr/bin/env python3
"""一键完成 共同赢账单 vs 到货单 对账全流程。

用法:
  python3 run_full.py <bill.xls> <invoice.xlsx> [output_dir]

输出:
  <output_dir>/两表金额差异对比.xls
  <output_dir>/共同赢X月账单-上海-已标差异.xls
  <output_dir>/gtyt_parsed.json   (中间产物, 供调试)

stdout: JSON 格式汇总信息, 供调用方解析后用飞书 DM 发送。
"""
import sys, os, json, subprocess


def main():
    if len(sys.argv) < 3:
        print("用法: python3 run_full.py <bill.xls> <invoice.xlsx> [output_dir]",
              file=sys.stderr)
        sys.exit(1)
    bill_path = os.path.abspath(sys.argv[1])
    inv_path = os.path.abspath(sys.argv[2])
    out_dir = os.path.abspath(sys.argv[3]) if len(sys.argv) > 3 else '/tmp'
    os.makedirs(out_dir, exist_ok=True)

    here = os.path.dirname(os.path.abspath(__file__))
    parsed_json = os.path.join(out_dir, 'gtyt_parsed.json')
    diff_xls = os.path.join(out_dir, '两表金额差异对比.xls')

    # 提取月份标签 (从账单文件名)
    bill_basename = os.path.basename(bill_path)
    # 例: "共同赢8月账单-上海--共同赢.xls" -> "8月"
    month_tag = ''
    import re
    m = re.search(r'(\d+)月', bill_basename)
    if m:
        month_tag = f'{m.group(1)}月'
    else:
        month_tag = '当月'

    marked_xls = os.path.join(out_dir, f'共同赢{month_tag}账单-上海-已标差异.xls')

    # Step 1: 解析
    print(f"[1/3] 解析账单 + 到货单 ...", file=sys.stderr)
    subprocess.check_call(['python3', os.path.join(here, 'parse_tables.py'),
                            bill_path, inv_path, parsed_json])

    # Step 2: 差异报告
    print(f"[2/3] 生成差异对比 .xls ...", file=sys.stderr)
    subprocess.check_call(['python3', os.path.join(here, 'build_diff_report.py'),
                            parsed_json, diff_xls])

    # Step 3: 标黄
    print(f"[3/3] 在原账单上标黄差异 ...", file=sys.stderr)
    subprocess.check_call(['python3', os.path.join(here, 'mark_bill_diff.py'),
                            bill_path, parsed_json, marked_xls])

    # 输出 JSON 汇总
    with open(parsed_json) as f:
        data = json.load(f)
    meta = data.get('meta', {})
    diff_count = sum(1 for r in data['results']
                     if r['diff'] is not None and abs(r['diff']) > 0.01)
    summary = {
        'bill_path': bill_path,
        'invoice_path': inv_path,
        'output_dir': out_dir,
        'diff_report': diff_xls,
        'marked_bill': marked_xls,
        'parsed_json': parsed_json,
        'bill_rows': meta.get('bill_rows'),
        'inv_rows': meta.get('inv_rows'),
        'total_sales_amt': meta.get('total_sales_amt'),
        'total_inv_amt': meta.get('total_inv_amt'),
        'diff_store_count': diff_count,
        'diff_sku_count': len(data.get('detail', [])),
        'unmatched_invoice': data.get('unmatched_invoice', []),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
