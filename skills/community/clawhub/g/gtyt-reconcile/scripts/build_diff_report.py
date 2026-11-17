#!/usr/bin/env python3
"""根据 parse_tables.py 输出的 JSON，生成「两表金额差异对比.xls」。

输出 4 个工作表:
  - 差异对比明细: 25 行（按差额绝对值降序）
  - 差异店清单: 25 个店名
  - 全量对比(126店): 完整店名对比
  - 对比说明: 口径、统计、业务说明

用法:
  python3 build_diff_report.py <parsed.json> <output.xls>
"""
import sys, json
import xlwt
from datetime import datetime


def main():
    if len(sys.argv) < 3:
        print("用法: python3 build_diff_report.py <parsed.json> <output.xls>")
        sys.exit(1)
    with open(sys.argv[1]) as f:
        data = json.load(f)
    out_path = sys.argv[2]

    all_rows = data['results']
    diff_rows = sorted([r for r in all_rows
                        if r['diff'] is not None and abs(r['diff']) > 0.01],
                       key=lambda x: -abs(x['diff'] or 0))

    total_sales = sum(r['sales_amt'] or 0 for r in all_rows)
    total_inv = sum(r['invoice_amt'] or 0 for r in all_rows if r['invoice_amt'] is not None)
    matched = sum(1 for r in all_rows if r['invoice_amt'] is not None)
    unmatched_inv = data.get('unmatched_invoice', [])

    wb = xlwt.Workbook(encoding='utf-8')
    title_style = xlwt.easyxf('font: bold on, height 360; align: horiz center, vert center')
    header_style = xlwt.easyxf('font: bold on, color white; pattern: pattern solid, fore_colour blue; align: horiz center, vert center; borders: left thin, right thin, top thin, bottom thin')
    cell_style = xlwt.easyxf('align: horiz left, vert center; borders: left thin, right thin, top thin, bottom thin')
    num_style = xlwt.easyxf('align: horiz right, vert center; borders: left thin, right thin, top thin, bottom thin')
    num_red = xlwt.easyxf('font: color red; align: horiz right, vert center; borders: left thin, right thin, top thin, bottom thin')
    num_green = xlwt.easyxf('font: color green; align: horiz right, vert center; borders: left thin, right thin, top thin, bottom thin')
    pct_style = xlwt.easyxf('align: horiz right, vert center; borders: left thin, right thin, top thin, bottom thin', num_format_str='0.00%')
    sub_style = xlwt.easyxf('font: italic on, color dark_blue; align: horiz center')
    label_style = xlwt.easyxf('font: bold on; align: horiz left, vert center; pattern: pattern solid, fore_colour light_green; borders: left thin, right thin, top thin, bottom thin')
    val_style = xlwt.easyxf('align: horiz left, vert center, wrap on; borders: left thin, right thin, top thin, bottom thin')

    # === Sheet 1: 差异对比明细 ===
    ws1 = wb.add_sheet('差异对比明细')
    ws1.write_merge(0, 0, 0, 7, '两表金额差异对比明细表', title_style)
    ws1.row(0).height_mismatch = True; ws1.row(0).height = 360
    ws1.write_merge(1, 1, 0, 7,
                     f'生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | 数据源: 共同赢账单(销售出库序时簿) + 到货单',
                     sub_style)
    headers = ['序号', '销售表店名', '到货表店名', '销售金额(元)', '到货金额(元)', '差额(元)', '差额率', '方向']
    for c, h in enumerate(headers):
        ws1.write(3, c, h, header_style)
    ws1.row(3).height_mismatch = True; ws1.row(3).height = 320

    for i, r in enumerate(diff_rows):
        row = 4 + i
        sn = (r['sales_name'] or '').replace('哥哥的深夜食堂-', '')
        inv = r['invoice_name'] or '—'
        sa = r['sales_amt'] or 0
        ia = r['invoice_amt'] or 0
        diff = r['diff'] or 0
        rate = (diff / sa) if sa else 0
        direction = '销售>到货(库存压力)' if diff > 0 else '销售<到货(可能积压)'
        ws1.write(row, 0, i + 1, cell_style)
        ws1.write(row, 1, sn, cell_style)
        ws1.write(row, 2, inv, cell_style)
        ws1.write(row, 3, sa, num_style)
        ws1.write(row, 4, ia, num_style)
        ws1.write(row, 5, diff, num_red if diff > 0 else num_green)
        ws1.write(row, 6, rate, pct_style)
        ws1.write(row, 7, direction, cell_style)
    widths = [8, 32, 38, 14, 14, 14, 12, 22]
    for i, w in enumerate(widths):
        ws1.col(i).width = w * 256
    total_row = 4 + len(diff_rows)
    ws1.write(total_row, 0, '', cell_style)
    ws1.write(total_row, 1, '合计(差异行)', header_style)
    ws1.write(total_row, 2, '', header_style)
    ws1.write(total_row, 3, sum(r['sales_amt'] or 0 for r in diff_rows), header_style)
    ws1.write(total_row, 4, sum(r['invoice_amt'] or 0 for r in diff_rows), header_style)
    ws1.write(total_row, 5, sum(r['diff'] or 0 for r in diff_rows), header_style)
    ws1.write(total_row, 6, '', header_style)
    ws1.write(total_row, 7, f'共 {len(diff_rows)} 行', header_style)
    ws1.set_panes_frozen(True); ws1.set_horz_split_pos(4); ws1.set_vert_split_pos(1)

    # === Sheet 2: 差异店清单 ===
    ws2 = wb.add_sheet('差异店清单')
    ws2.write_merge(0, 0, 0, 1, f'差异店清单(共 {len(diff_rows)} 个)', title_style)
    ws2.row(0).height_mismatch = True; ws2.row(0).height = 320
    ws2.write(2, 0, '序号', header_style)
    ws2.write(2, 1, '店名', header_style)
    for i, r in enumerate(diff_rows):
        ws2.write(3 + i, 0, i + 1, cell_style)
        ws2.write(3 + i, 1, (r['sales_name'] or '').replace('哥哥的深夜食堂-', ''), cell_style)
    ws2.col(0).width = 8 * 256
    ws2.col(1).width = 35 * 256

    # === Sheet 3: 全量对比 ===
    ws3 = wb.add_sheet('全量对比(126店)')
    ws3.write_merge(0, 0, 0, 5, '两表全量店名金额对比', title_style)
    ws3.row(0).height_mismatch = True; ws3.row(0).height = 320
    h3 = ['序号', '销售表店名', '到货表店名', '销售金额(元)', '到货金额(元)', '差额(元)']
    for c, h in enumerate(h3):
        ws3.write(2, c, h, header_style)
    ws3.row(2).height_mismatch = True; ws3.row(2).height = 320
    all_sorted = sorted(all_rows, key=lambda x: -(x['sales_amt'] or 0))
    for i, r in enumerate(all_sorted):
        row = 3 + i
        ws3.write(row, 0, i + 1, cell_style)
        ws3.write(row, 1, (r['sales_name'] or '').replace('哥哥的深夜食堂-', ''), cell_style)
        ws3.write(row, 2, r['invoice_name'] or '未匹配', cell_style)
        ws3.write(row, 3, r['sales_amt'] or 0, num_style)
        if r['invoice_amt'] is not None:
            ws3.write(row, 4, r['invoice_amt'], num_style)
            diff = r['diff'] or 0
            if diff > 0: ws3.write(row, 5, diff, num_red)
            elif diff < 0: ws3.write(row, 5, diff, num_green)
            else: ws3.write(row, 5, 0, num_style)
        else:
            ws3.write(row, 4, '—', cell_style)
            ws3.write(row, 5, '—', cell_style)
    w3 = [8, 32, 38, 14, 14, 14]
    for i, w in enumerate(w3):
        ws3.col(i).width = w * 256
    sum_row = 3 + len(all_sorted)
    ws3.write(sum_row, 0, '', cell_style)
    ws3.write(sum_row, 1, '全量合计', header_style)
    ws3.write(sum_row, 2, '', header_style)
    ws3.write(sum_row, 3, total_sales, header_style)
    ws3.write(sum_row, 4, total_inv, header_style)
    ws3.write(sum_row, 5, total_sales - total_inv, header_style)

    # === Sheet 4: 对比说明 ===
    ws4 = wb.add_sheet('对比说明')
    ws4.write_merge(0, 0, 0, 1, '对比说明', title_style)
    ws4.row(0).height_mismatch = True; ws4.row(0).height = 320
    info = [
        ('数据源 1', '共同赢X月账单(销售出库序时簿)'),
        ('数据源 2', '到货单明细表 (剔除末尾『合计』空行)'),
        ('匹配规则', '销售全称 → 到货简称 152 条人工映射'),
        ('', ''),
        ('总销售金额', f'¥{total_sales:,.2f}'),
        ('总到货金额', f'¥{total_inv:,.2f}'),
        ('匹配店数', f'{matched}/{len(all_rows)}'),
        ('差异店数', f'{len(diff_rows)}'),
        ('', ''),
        ('未匹配到货店', f'{len(unmatched_inv)} 个'),
        ('未匹配明细', ', '.join(unmatched_inv) if unmatched_inv else '—'),
        ('', ''),
        ('正差异', f'{sum(1 for r in diff_rows if (r["diff"] or 0) > 0)} 个'),
        ('负差异', f'{sum(1 for r in diff_rows if (r["diff"] or 0) < 0)} 个'),
        ('', ''),
        ('业务说明', '账单=门店出账(共同赢系统)，到货=供应商送货(ERP)'),
        ('店名歧义', '陆悦天地+金杨陆悦坊 映射到同一到货仓库'),
    ]
    for i, (k, v) in enumerate(info):
        ws4.write(2 + i, 0, k, label_style)
        ws4.write(2 + i, 1, v, val_style)
        ws4.row(2 + i).height_mismatch = True; ws4.row(2 + i).height = 280
    ws4.col(0).width = 18 * 256
    ws4.col(1).width = 80 * 256

    wb.save(out_path)
    import os
    print(f"已保存: {out_path} ({os.path.getsize(out_path):,} bytes)")


if __name__ == '__main__':
    main()
