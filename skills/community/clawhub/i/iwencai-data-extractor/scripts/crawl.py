#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
同花顺问财涨停数据抓取脚本
用法：cmd /c python crawl.py
依赖：需先以 CDP 调试模式启动 Chrome 并导航到问财 AI选股页面
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import subprocess, json, sqlite3, re, time
from datetime import date

# ──────────────────────────────────────────────
#  ★ 用户配置区（按实际路径修改）
# ──────────────────────────────────────────────
AGENT    = r"C:\Users\JacobWu\AppData\Roaming\npm\agent-browser.cmd"
DB_PATH  = r"D:\workbuddyclaw\iwencai_zt.db"
CDP_PORT = "9222"

# 要爬取的交易日列表（ISO格式），按需修改
TRADE_DAYS = [
    "2026-03-02", "2026-03-03", "2026-03-04", "2026-03-05", "2026-03-06",
    "2026-03-09", "2026-03-10", "2026-03-11", "2026-03-12", "2026-03-13",
    "2026-03-16", "2026-03-17", "2026-03-18", "2026-03-19", "2026-03-20",
    "2026-03-23", "2026-03-24", "2026-03-25", "2026-03-26", "2026-03-27",
]
# ──────────────────────────────────────────────

JS_EXTRACT = (
    "(function(){"
    "var rows=document.querySelectorAll('tr');"
    "var result=[];"
    "rows.forEach(function(row){"
    "var cells=row.querySelectorAll('td');"
    "if(cells.length<5)return;"
    "var cellData=Array.from(cells).map(function(c){"
    "return c.innerText.replace(/[\\n\\r]/g,' ').replace(/\\|/g,'/').trim();"
    "});"
    "var hasCode=cellData.some(function(c){return /^\\d{6}$/.test(c);});"
    "if(hasCode){result.push(cellData);}"
    "});"
    "return JSON.stringify(result);"
    "})()"
)

JS_PAGE_INFO = (
    "(function(){"
    "var active=document.querySelector('.page-item.active');"
    "var items=document.querySelectorAll('.page-item');"
    "var nums=[];"
    "items.forEach(function(el){var t=el.innerText.trim();if(/^\\d+$/.test(t))nums.push(parseInt(t));});"
    "return JSON.stringify({current:active?active.innerText.trim():'1',pages:nums,max:nums.length>0?Math.max.apply(null,nums):1});"
    "})()"
)


def ab(*args):
    if not args:
        return ""
    cmd = [AGENT, "--cdp", CDP_PORT] + list(args)
    r = subprocess.run(cmd, capture_output=True)
    out = r.stdout.decode("utf-8", errors="replace").strip()
    if not out and r.stderr:
        err = re.sub(r'\x1b\[[0-9;]*m', '', r.stderr.decode("utf-8", errors="replace").strip())
        if err:
            print(f"  [AB ERR] {err[:200]}")
    return out


def ab_eval(js):
    raw = ab("eval", js)
    try:
        step1 = json.loads(raw)
        return json.loads(step1) if isinstance(step1, str) else step1
    except:
        return raw


def clean_number(s):
    if not s: return None
    m = re.match(r'^-?[\d.]+', str(s).strip().replace(',', ''))
    return float(m.group()) if m else None


def parse_mv(s):
    if not s: return None
    s = str(s).strip().replace(',', '')
    if '亿' in s: return clean_number(s.replace('亿', ''))
    elif '万' in s:
        v = clean_number(s.replace('万', ''))
        return v / 10000 if v else None
    return clean_number(s)


def parse_amount(s):
    if not s: return None
    s = str(s).strip().replace(',', '')
    if '亿' in s:
        v = clean_number(s.replace('亿', ''))
        return v * 1e8 if v else None
    elif '万' in s:
        v = clean_number(s.replace('万', ''))
        return v * 1e4 if v else None
    return clean_number(s)


def rows_to_records(rows, trade_date):
    records = []
    for row in rows:
        if len(row) < 13: continue
        code = row[2] if len(row) > 2 else ''
        if not re.match(r'^\d{6}$', code): continue
        lb_count = 0
        try:
            lb_count = int(row[18]) if len(row) > 18 else 0
        except:
            m = re.search(r'(\d+)', str(row[18]) if len(row) > 18 else '')
            lb_count = int(m.group(1)) if m else 0
        records.append({
            'trade_date': trade_date,
            'stock_code': code,
            'stock_name': row[3] if len(row) > 3 else '',
            'price': clean_number(row[4]) if len(row) > 4 else None,
            'change_pct': clean_number(row[5]) if len(row) > 5 else None,
            'zt_time': row[6] if len(row) > 6 else '',
            'zt_status': row[7] if len(row) > 7 else '',
            'volume': parse_amount(row[9]) if len(row) > 9 else None,
            'amount': parse_amount(row[10]) if len(row) > 10 else None,
            'first_zt_time': row[11] if len(row) > 11 else '',
            'lb_count': lb_count,
            'zt_type': row[13] if len(row) > 13 else '',
            'float_mv': parse_mv(row[14]) if len(row) > 14 else None,
            'vol_ratio': clean_number(row[15]) if len(row) > 15 else None,
            'themes': row[16] if len(row) > 16 else '',
            'zt_tags': row[17] if len(row) > 17 else '',
            'total_mv': parse_mv(row[19]) if len(row) > 19 else None,
        })
    return records


def ensure_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS zt_stocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trade_date TEXT, stock_code TEXT, stock_name TEXT,
            price REAL, change_pct REAL, zt_time TEXT, zt_status TEXT,
            volume TEXT, amount TEXT, first_zt_time TEXT, lb_count INTEGER,
            zt_type TEXT, float_mv TEXT, vol_ratio TEXT, themes TEXT,
            zt_tags TEXT, total_mv TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()


def save_records(conn, records, existing_codes):
    cursor = conn.cursor()
    inserted = 0
    for rec in records:
        if rec['stock_code'] in existing_codes:
            continue
        try:
            cursor.execute("""
                INSERT INTO zt_stocks
                (trade_date,stock_code,stock_name,price,change_pct,zt_time,zt_status,
                 volume,amount,first_zt_time,lb_count,zt_type,float_mv,vol_ratio,
                 themes,zt_tags,total_mv)
                VALUES (:trade_date,:stock_code,:stock_name,:price,:change_pct,:zt_time,
                        :zt_status,:volume,:amount,:first_zt_time,:lb_count,:zt_type,
                        :float_mv,:vol_ratio,:themes,:zt_tags,:total_mv)
            """, rec)
            existing_codes.add(rec['stock_code'])
            inserted += 1
        except sqlite3.Error as e:
            print(f"    [DB ERR] {rec['stock_code']}: {e}")
    conn.commit()
    return inserted


def search_date(trade_date):
    d = date.fromisoformat(trade_date)
    query = f"{d.year}年{d.month}月{d.day}日涨停股票"
    print(f"  搜索: {query}")

    snap = ab("snapshot", "-i", "-c")
    search_ref = None

    # 优先找带"筛选条件"的 textbox
    for line in snap.split('\n'):
        if 'textbox' in line.lower() and 'ref=' in line:
            if '筛选条件' in line or '请输入您的' in line:
                m = re.search(r'ref=(e\d+)', line)
                if m:
                    search_ref = m.group(1)
                    break

    # 退而求其次：任意 textbox（排除无关框）
    if not search_ref:
        for line in snap.split('\n'):
            if 'textbox' in line.lower() and 'ref=' in line:
                if '快速搜' not in line and '代码/名称' not in line and '概念' not in line:
                    m = re.search(r'ref=(e\d+)', line)
                    if m:
                        search_ref = m.group(1)
                        break

    # 尝试点 AI选股 菜单
    if not search_ref:
        print("  [WARN] 未找到搜索框，尝试点击AI选股菜单...")
        for line in snap.split('\n'):
            if 'AI选股' in line and 'ref=' in line:
                m = re.search(r'ref=(e\d+)', line)
                if m:
                    ab("click", m.group(1))
                    time.sleep(2)
                    snap = ab("snapshot", "-i", "-c")
                    break
        for line in snap.split('\n'):
            if 'textbox' in line.lower() and 'ref=' in line:
                if '快速搜' not in line and '代码/名称' not in line:
                    m = re.search(r'ref=(e\d+)', line)
                    if m:
                        search_ref = m.group(1)
                        break

    if not search_ref:
        print("  [ERROR] 找不到搜索框")
        print("  SNAP:", snap[:300])
        return []

    print(f"  找到搜索框 ref={search_ref}")
    ab("fill", search_ref, query)
    time.sleep(0.5)
    ab("press", "Enter")
    print("  等待结果加载...")
    time.sleep(7)

    all_rows = []
    page = 1
    while True:
        print(f"  提取第{page}页...")
        data = ab_eval(JS_EXTRACT)
        if isinstance(data, list) and len(data) > 0:
            print(f"    获取到 {len(data)} 条")
            all_rows.extend(data)
        else:
            print(f"    [WARN] 第{page}页无数据")
            break

        page_info = ab_eval(JS_PAGE_INFO)
        print(f"    分页: {page_info}")
        max_page = 1
        if isinstance(page_info, dict):
            max_page = int(page_info.get('max', 1))
        if page >= max_page:
            break

        # Vue 兼容翻页（dispatchEvent）
        next_num = str(page + 1)
        js_next = (
            "(function(){"
            "var items=document.querySelectorAll('.page-item');"
            "var target=null;"
            "items.forEach(function(el){"
            "if(el.innerText.trim()==='" + next_num + "'&&!el.classList.contains('active')){target=el;}"
            "});"
            "if(!target){var links=document.querySelectorAll('a');"
            "links.forEach(function(l){if(l.innerText.trim()==='\u4e0b\u9875'&&!target){target=l;}});}"
            "if(!target){return 'not found';}"
            "var a=target.querySelector('a')||target;"
            "a.dispatchEvent(new MouseEvent('click',{bubbles:true,cancelable:true,view:window}));"
            "return 'ok:'+a.tagName;"
            "})()"
        )
        result = ab_eval(js_next)
        print(f"  翻页结果: {result}")
        time.sleep(3)
        page += 1
        if page > 20:
            print("  [WARN] 翻页超过20次，强制退出")
            break

    print(f"  共获取 {len(all_rows)} 条")
    return all_rows


def crawl_date(trade_date, conn):
    print(f"\n{'='*50}")
    print(f"  处理 {trade_date}")
    print(f"{'='*50}")
    c = conn.cursor()
    c.execute("SELECT stock_code FROM zt_stocks WHERE trade_date=?", (trade_date,))
    existing_codes = {r[0] for r in c.fetchall()}
    existing_count = len(existing_codes)

    if existing_count > 0 and existing_count % 50 != 0:
        print(f"  [SKIP] 已有 {existing_count} 条（完整），跳过")
        return 0

    rows = search_date(trade_date)
    if not rows:
        print(f"  [WARN] 未获取到数据")
        return 0
    records = rows_to_records(rows, trade_date)
    inserted = save_records(conn, records, existing_codes)
    print(f"  OK {trade_date}: 插入 {inserted} 条")
    return inserted


def main():
    conn = sqlite3.connect(DB_PATH)
    ensure_table(conn)
    total = 0
    failed = []
    print(f"开始抓取，共 {len(TRADE_DAYS)} 个交易日")
    for d in TRADE_DAYS:
        try:
            n = crawl_date(d, conn)
            total += n
            if n > 0:
                time.sleep(3)
        except Exception as e:
            print(f"  [ERROR] {d}: {e}")
            import traceback; traceback.print_exc()
            failed.append(d)
            time.sleep(5)
    conn.close()
    print(f"\n完成！总插入 {total} 条")
    if failed:
        print(f"失败日期: {failed}")


if __name__ == "__main__":
    main()
