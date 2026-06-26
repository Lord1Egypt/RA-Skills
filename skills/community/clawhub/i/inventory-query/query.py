#!/usr/bin/env python3
import sys, os, re, openpyxl

INVENTORY_PATH = "/root/.openclaw/workspace/skills/inventory-query/inventory.xlsx"
DATE_PATH = "/root/.openclaw/workspace/skills/inventory-query/inventory_date.txt"

def get_date():
    if os.path.exists(DATE_PATH):
        with open(DATE_PATH) as f:
            return f.read().strip()
    return "未知日期"

def normalize(text):
    return re.sub(r'\s+', '', text).upper()

def query_inventory(keyword):
    wb = openpyxl.load_workbook(INVENTORY_PATH, data_only=True)
    ws = wb['库存']
    results = []
    kw = normalize(keyword)
    for row in ws.iter_rows(min_row=6, max_row=ws.max_row):
        c = row[2].value
        if c and kw in normalize(str(c)):
            def val(v):
                if v is None or str(v).strip() in ('', '-'):
                    return 0
                try:
                    return int(float(v))
                except:
                    return 0
            results.append({
                'model': str(c).strip(),
                'total': val(row[5].value),
                'shanghai': val(row[3].value),
                'langfang': val(row[4].value),
                'pending': val(row[8].value),
                'signed': val(row[9].value),
                'overstock': val(row[25].value)
            })
    wb.close()
    return results

def query_plan(keyword):
    wb = openpyxl.load_workbook(INVENTORY_PATH, data_only=True)
    ws = wb['计划']
    results = {}
    kw = normalize(keyword)
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
        c = row[11].value
        if c and kw in normalize(str(c)):
            model = str(c).strip()
            def val(v):
                try:
                    return int(float(v))
                except:
                    return 0
            total_order = val(row[14].value)
            remaining = val(row[15].value)
            delivered = total_order - remaining
            date_str = str(row[18].value).split(' ')[0] if row[18].value else '未定'
            if model not in results:
                results[model] = {'model': model, 'total': 0, 'delivered': 0, 'remaining': 0, 'plans': []}
            results[model]['total'] += total_order
            results[model]['delivered'] += delivered
            results[model]['remaining'] += remaining
            results[model]['plans'].append(f"{date_str}({remaining}台)")
    wb.close()
    return list(results.values())

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法：python3 query.py [库存|补货|全部] 型号关键词")
        sys.exit(1)
    mode, keyword = sys.argv[1], sys.argv[2]
    date = get_date()
    if mode in ("库存", "全部"):
        inv = query_inventory(keyword)
        if not inv:
            print(f"以下是根据{date}库存表查询的结果\n\n未找到包含\"{keyword}\"的型号，请确认型号是否正确。")
        else:
            print(f"以下是根据{date}库存表查询的结果\n")
            for r in inv:
                print(r['model'])
                print(f"库存：{r['total']}台（上海{r['shanghai']} + 廊坊{r['langfang']}），待批准：{r['pending']}，已签合同：{r['signed']}，滞留超一年：{r['overstock']}")
                print()
    if mode in ("补货", "全部"):
        plan = query_plan(keyword)
        if plan:
            if mode == "补货":
                inv2 = query_inventory(keyword)
                if inv2:
                    print(f"以下是根据{date}库存表查询的结果\n")
                    for r in inv2:
                        print(r['model'])
                        print(f"库存：{r['total']}台（上海{r['shanghai']} + 廊坊{r['langfang']}），待批准：{r['pending']}，已签合同：{r['signed']}，滞留超一年：{r['overstock']}")
                        print()
            print("补货计划：\n")
            for r in plan:
                plans_str = ", ".join(r['plans'])
                print(r['model'])
                print(f"总采购量：{r['total']}，已交货：{r['delivered']}，待交货：{r['remaining']}")
                print(f"交货计划：{plans_str}")
                print()
        else:
            print("无补货计划")
