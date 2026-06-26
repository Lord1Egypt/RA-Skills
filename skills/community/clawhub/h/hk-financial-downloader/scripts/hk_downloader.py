#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
港股公司财报下载器 v1.0 (2026-04-12)

数据源优先级: 东方财富 → 同花顺 → 披露易
核心原则: 完整报告优先于业绩公告，同年同类型只保留一份
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.request
import urllib.parse

# ============================================================
# 配置
# ============================================================
BASE_ARCHIVE = "/root/.openclaw/workspace/archive"

HEADERS_EASTMONEY = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://data.eastmoney.com/notices/",
}

HEADERS_10JQKA = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://stockpage.10jqka.com.cn/",
}

HEADERS_HKEX = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
}

# 已验证 stockId 映射
STOCK_ID_MAP = {
    '00700': '7609',
    '09988': '1000015694',
    '03690': '198419',
    '01810': '190371',
    '09618': '1000042149',
    '09999': '1000041666',
    '01211': '2696',
    '09633': '1000054238',
}

# ============================================================
# 股票代码格式转换
# ============================================================
def format_code_eastmoney(stock_code):
    """东方财富港股代码格式: 5位 (如 0700 → 00700)"""
    code = stock_code.strip()
    if code.startswith('HK'):
        code = code[2:]
    return code.zfill(5)


def format_code_10jqka(stock_code):
    """同花顺港股代码格式: HK + 4位有效数字 (如 0700 → HK0700)"""
    code = stock_code.strip()
    if code.startswith('HK'):
        code = code[2:]
    code_num = code.lstrip('0') or '0'
    code_num = code_num.zfill(4)  # 700 → 0700
    return "HK%s" % code_num


def format_code_hkex(stock_code):
    """披露易港股代码格式: 4位 (如 0700 → 00700, stockId 需要额外查找)"""
    code = stock_code.strip()
    if code.startswith('HK'):
        code = code[2:]
    return code.zfill(4)


def print_code_formats(stock_code):
    """打印各数据源所需的代码格式（调试用）"""
    code = stock_code.strip()
    print("  股票代码格式转换:")
    print("    东方财富: %s" % format_code_eastmoney(code))
    print("    同花顺:   %s" % format_code_10jqka(code))
    print("    披露易:   %s" % format_code_hkex(code))


# ============================================================
# 分类函数
# ============================================================
def classify_doc(title):
    """分类文档类型，返回 (doc_type, is_complete)"""
    # 完整年报
    if any(k in title for k in ['年報', '年度报告', 'Annual Report']):
        if '中期' not in title:
            return ('年报', True)
    # 完整中期报告
    if any(k in title for k in ['中期報告', '中期报告', 'Interim Report']):
        return ('中报', True)
    # 年报业绩公告 (支持简繁体)
    if any(k in title for k in ['全年业绩', '全年業績', '年度业绩', '年度業績', '末期業績', 'Annual Results', '年度业绩公告', '年度業績公告']):
        if '中期' not in title:
            return ('年报', False)
    # 半年报业绩公告 (支持简繁体)
    if any(k in title for k in ['六个月', '中期業績', '中期业绩', '六個月']):
        return ('中报', False)
    # Q3 季报
    if any(k in title for k in ['九个月', '九個月']):
        return ('Q3季报', False)
    # Q1 季报
    if any(k in title for k in ['三个月']):
        if '九个月' not in title and '六个月' not in title:
            return ('Q1季报', False)
    # 招股书
    if any(k in title for k in ['招股', '全球发售', 'Prospectus', '聆讯', '上市文件', '發售']):
        return ('招股书', True)
    return (None, None)


def get_year_from_title(title):
    """从标题提取财年"""
    # "2025 年报" → 2025
    m = re.search(r'(\d{4})\s*年[報报]', title)
    if m:
        return m.group(1)
    # "年报2025" → 2025
    m = re.search(r'年[報报]\s*(\d{4})', title)
    if m:
        return m.group(1)
    # "2025年报" → 2025
    m = re.search(r'(\d{4})年[報报]', title)
    if m:
        return m.group(1)
    # "截至2025年12月31日" → 2025
    m = re.search(r'截至(\d{4})年', title)
    if m:
        return m.group(1)
    # "中期报告 2025" → 2025
    m = re.search(r'中期报告\s*(\d{4})', title)
    if m:
        return m.group(1)
    # "截至二零二五年" → 2025 (繁体中文)
    num_map = {'零': '0', '一': '1', '二': '2', '三': '3', '四': '4',
               '五': '5', '六': '6', '七': '7', '八': '8', '九': '9'}
    m = re.search(r'截至二零([一二三四五六七八九〇]+)年', title)
    if m:
        digits = ''.join(num_map.get(c, c) for c in m.group(1))
        return '20' + digits.zfill(2)
    return None


# ============================================================
# 数据源 1: 东方财富
# ============================================================
def fetch_eastmoney(stock_code, from_year=2020, to_year=2025):
    """从东方财富获取港股公告"""
    print("  【1/3】东方财富获取公告...")
    norm_code = format_code_eastmoney(stock_code)
    all_items = []
    page = 1
    while page <= 80:
        url = ("https://np-anotice-stock.eastmoney.com/api/security/ann"
               "?page_size=100&page_index=%d&ann_type=H&stock_list=%s" % (page, norm_code))
        try:
            req = urllib.request.Request(url, headers=HEADERS_EASTMONEY)
            resp = urllib.request.urlopen(req, timeout=10)
            raw = resp.read().decode('utf-8', errors='replace')
            idx = raw.rfind('}')
            data = json.loads(raw[:idx + 1]) if idx > 0 else {}
        except Exception as e:
            print("    请求失败: %s" % str(e)[:60])
            break

        items = data.get('data', {}).get('list', [])
        if not items:
            break

        # 过滤出目标公司的公告
        for item in items:
            codes = item.get('codes', [])
            is_target = any(c.get('stock_code') == norm_code for c in codes)
            if is_target:
                all_items.append(item)

        page += 1
        if len(items) < 100:
            break
        time.sleep(0.1)

    print("    获取 %d 条公告" % len(all_items))
    return all_items


# ============================================================
# 数据源 2: 同花顺
# ============================================================
def format_code_10jqka(stock_code):
    """同花顺港股代码格式: HK + 4位有效数字 (如 00700 → HK0700)"""
    code = stock_code.strip()
    if code.startswith('HK'):
        code = code[2:]
    # 去掉前导0后，补到4位，再加HK
    code_num = code.lstrip('0') or '0'
    code_num = code_num.zfill(4)  # 700 → 0700
    return "HK%s" % code_num


def fetch_10jqka(stock_code, from_year=2020, to_year=2025):
    """从同花顺获取港股公告"""
    print("  【2/3】同花顺获取公告...")
    all_items = []
    page = 1
    code_param = format_code_10jqka(stock_code)

    while True:
        url = ("https://basic.10jqka.com.cn/basicapi/notice/pub"
               "?type=hk&code=%s&classify=all&page=%d&limit=15" % (code_param, page))
        try:
            req = urllib.request.Request(url, headers=HEADERS_10JQKA)
            resp = urllib.request.urlopen(req, timeout=10)
            data = json.loads(resp.read().decode('utf-8', errors='replace'))
        except Exception as e:
            break

        items = data.get('data', {}).get('data', [])
        if not items:
            break

        all_items.extend(items)
        page += 1
        if len(items) < 15:
            break
        time.sleep(0.1)

    print("    获取 %d 条公告" % len(all_items))
    return all_items


# ============================================================
# 数据源 3: 披露易
# ============================================================
def get_stock_id(stock_code):
    """获取港交所 stockId"""
    norm_code = format_code_eastmoney(stock_code)  # 统一用5位格式查找
    if norm_code in STOCK_ID_MAP:
        return STOCK_ID_MAP[norm_code]
    # 也尝试4位格式
    code_4 = format_code_hkex(stock_code)
    if code_4 in STOCK_ID_MAP:
        return STOCK_ID_MAP[code_4]

    try:
        url = ("https://www1.hkexnews.hk/search/prefix.do"
               "?type=A&market=SEHK&name=%s&lang=ZH&callback=callback" % norm_code)
        req = urllib.request.Request(url, headers=HEADERS_HKEX)
        resp = urllib.request.urlopen(req, timeout=10)
        raw = resp.read().decode('utf-8', errors='replace')
        # 提取 stockId
        m = re.search(r'stockId["\']:\s*["\'](\d+)["\']', raw)
        if m:
            sid = m.group(1)
            STOCK_ID_MAP[stock_code] = sid
            return sid
    except:
        pass
    return None


def fetch_hkex(stock_code, from_year=2020, to_year=2025):
    """从披露易获取公告"""
    print("  【3/3】披露易获取公告...")
    stock_id = get_stock_id(stock_code)
    if not stock_id:
        print("    无法获取 stockId")
        return []

    try:
        # 简化实现: 披露易搜索需要 POST + 解析 HTML
        # 这里返回空，实际使用时通过 web_search 获取 PDF URL
        print("    披露易搜索需要浏览器渲染，建议使用 web_search 定位 PDF")
        return []
    except Exception as e:
        print("    失败: %s" % str(e)[:60])
        return []


# ============================================================
# 去重 + 完整报告优先
# ============================================================
def dedup_docs(docs):
    """按年份去重，优先保留完整报告"""
    # 按 (类型, 年份) 分组
    from collections import defaultdict
    groups = defaultdict(list)
    for doc in docs:
        year = doc.get('_year', '')
        doc_type = doc.get('_type', '')
        key = (doc_type, year)
        groups[key].append(doc)

    result = []
    for key, group_docs in groups.items():
        # 优先完整报告
        complete = [d for d in group_docs if d.get('_is_complete', False)]
        if complete:
            result.append(complete[0])
        else:
            result.append(group_docs[0])

    return result


def filter_and_dedup(all_items, doc_types=None, from_year=2020, to_year=2025):
    """筛选 + 分类 + 去重"""
    if doc_types is None:
        doc_types = ['年报', '中报', 'Q1季报', 'Q3季报', '招股书']

    docs = []
    for item in all_items:
        title = item.get('title', '')
        date_str = item.get('date', '') or item.get('notice_date', '')[:10]
        
        # 提取财年（从标题）
        fy = get_year_from_title(title)
        
        # 年份过滤：优先用财年，其次用公告日期
        year_to_check = fy if fy else (date_str[:4] if date_str else '')
        
        if year_to_check and (int(year_to_check) < from_year or int(year_to_check) > to_year):
            continue

        doc_type, is_complete = classify_doc(title)
        if doc_type is None or doc_type not in doc_types:
            continue

        # 提取年份
        fy = fy or year_to_check

        docs.append({
            '_type': doc_type,
            '_is_complete': is_complete,
            '_year': fy,
            'title': title,
            'date': date_str,
            'art_code': item.get('art_code', ''),
            'raw_url': item.get('raw_url', ''),
            'source': item.get('_source', ''),
        })

    # 去重
    result = dedup_docs(docs)
    result.sort(key=lambda x: (
        {'年报': 0, '中报': 1, 'Q3季报': 2, 'Q1季报': 3, '招股书': 4}.get(x['_type'], 9),
        x.get('_year', '')
    ))

    return result


# ============================================================
# PDF 下载
# ============================================================
def download_pdf(doc, output_dir):
    """下载单个 PDF"""
    doc_type = doc['_type']
    year = doc.get('_year', '')
    title = doc['title'][:60]
    is_complete = doc['_is_complete']

    # 确定子目录
    type_dir = {
        '年报': 'annual',
        '中报': 'interim',
        'Q1季报': 'quarterly',
        'Q3季报': 'quarterly',
        '招股书': 'prospectus',
    }.get(doc_type, 'other')

    subdir = os.path.join(output_dir, 'financial_reports', type_dir)
    os.makedirs(subdir, exist_ok=True)

    # 文件名
    safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_', '（）()', '·'))[:60]
    quarter = 'Q1' if 'Q1' in doc_type else ('Q3' if 'Q3' in doc_type else '')
    if quarter:
        filename = "%s_%s_%s_%s.pdf" % (year, quarter, type_dir, safe_title)
    else:
        filename = "%s_%s_%s.pdf" % (year, type_dir, safe_title)
    filepath = os.path.join(subdir, filename)

    if os.path.exists(filepath):
        return ('skipped', filepath)

    # 获取 PDF URL
    pdf_url = None
    source = doc.get('source', '')

    if source == 'eastmoney' and doc.get('art_code'):
        pdf_url = "https://pdf.dfcfw.com/pdf/H2_%s_1.pdf" % doc['art_code']
    elif doc.get('raw_url'):
        pdf_url = doc['raw_url'].replace('http://', 'https://')

    if not pdf_url:
        return ('no_url', filepath)

    try:
        req = urllib.request.Request(pdf_url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=15)
        content = resp.read()

        if content.startswith(b'%PDF'):
            with open(filepath, 'wb') as f:
                f.write(content)
            size_kb = len(content) / 1024
            return ('ok', filepath, size_kb)
        else:
            return ('not_pdf', filepath)
    except Exception as e:
        return ('error', filepath, str(e)[:50])


# ============================================================
# 主函数
# ============================================================
def main():
    parser = argparse.ArgumentParser(description='港股公司财报下载器')
    parser.add_argument('--stock', type=str, help='股票代码 (如 0700)')
    parser.add_argument('--stocks', type=str, help='批量股票代码 (逗号分隔)')
    parser.add_argument('--from', dest='from_year', type=int, default=2020, help='起始年份')
    parser.add_argument('--to', dest='to_year', type=int, default=2025, help='结束年份')
    parser.add_argument('--type', dest='doc_type', type=str, default='all',
                        help='报告类型: 年报/中报/季报/招股书/all')
    parser.add_argument('--pdf', action='store_true', help='下载 PDF')
    parser.add_argument('--source', type=str, default='eastmoney,10jqka,hkex',
                        help='数据源优先级')

    args = parser.parse_args()

    if not args.stock and not args.stocks:
        print("错误: 请指定 --stock 或 --stocks")
        sys.exit(1)

    stock_list = []
    if args.stocks:
        stock_list = [s.strip() for s in args.stocks.split(',')]
    elif args.stock:
        stock_list = [args.stock.strip()]

    # 报告类型
    type_map = {
        '年报': ['年报'],
        '中报': ['中报'],
        '季报': ['Q1季报', 'Q3季报'],
        '招股书': ['招股书'],
        'all': ['年报', '中报', 'Q1季报', 'Q3季报', '招股书'],
    }
    doc_types = type_map.get(args.doc_type, type_map['all'])

    sources = [s.strip() for s in args.source.split(',')]

    for stock_code in stock_list:
        print("\n" + "=" * 70)
        print("📊 港股财报下载: %s" % stock_code)
        print("=" * 70)
        
        # 打印代码格式转换
        print_code_formats(stock_code)
        
        print("📡 数据源: %s" % " → ".join(sources))
        print("📅 时间范围: %d-%d" % (args.from_year, args.to_year))
        print("📋 报告类型: %s" % ', '.join(doc_types))

        # 输出目录
        company_name = stock_code
        output_dir = os.path.join(BASE_ARCHIVE, "%s_%s" % (stock_code.zfill(5), company_name))
        
        # 获取公告
        all_items = []
        for source in sources:
            if source == 'eastmoney':
                items = fetch_eastmoney(stock_code, args.from_year, args.to_year)
                for item in items:
                    item['_source'] = 'eastmoney'
                all_items.extend(items)
            elif source == '10jqka':
                items = fetch_10jqka(stock_code, args.from_year, args.to_year)
                for item in items:
                    item['_source'] = '10jqka'
                all_items.extend(items)
            elif source == 'hkex':
                items = fetch_hkex(stock_code, args.from_year, args.to_year)
                for item in items:
                    item['_source'] = 'hkex'
                all_items.extend(items)

        # 筛选 + 去重
        docs = filter_and_dedup(all_items, doc_types, args.from_year, args.to_year)
        print("\n  筛选结果: %d 份" % len(docs))

        # 按类型统计
        from collections import Counter
        type_count = Counter(d['_type'] for d in docs)
        complete_count = sum(1 for d in docs if d['_is_complete'])
        ann_count = sum(1 for d in docs if not d['_is_complete'])

        print("  完整报告: %d 份 | 业绩公告: %d 份" % (complete_count, ann_count))
        for t, c in sorted(type_count.items()):
            print("    %s: %d 份" % (t, c))

        # 下载 PDF
        if args.pdf:
            output_dir = os.path.join(BASE_ARCHIVE, "%s_%s" % (stock_code, company_name))
            os.makedirs(output_dir, exist_ok=True)

            print("\n  下载 PDF...")
            results = []
            for doc in docs:
                result = download_pdf(doc, output_dir)
                status = result[0]
                filepath = result[1]

                if status == 'ok':
                    print("    ✅ %s (%.0fKB)" % (os.path.basename(filepath), result[2]))
                    results.append({'status': 'ok', 'path': filepath, 'size_kb': result[2]})
                elif status == 'skipped':
                    print("    ⏭️  已存在: %s" % os.path.basename(filepath))
                    results.append({'status': 'skipped', 'path': filepath})
                else:
                    print("    ❌ %s: %s" % (os.path.basename(filepath), status))
                    results.append({'status': status, 'path': filepath})

            # 生成清单
            manifest = []
            for doc, res in zip(docs, results):
                manifest.append({
                    'type': doc['_type'],
                    'year': doc.get('_year', ''),
                    'title': doc['title'],
                    'date': doc['date'],
                    'is_complete': doc['_is_complete'],
                    'source': doc.get('source', ''),
                    'download_status': res['status'],
                    'filepath': os.path.relpath(res['path'], output_dir) if 'path' in res else '',
                })

            manifest_path = os.path.join(output_dir, 'manifest.json')
            with open(manifest_path, 'w', encoding='utf-8') as f:
                json.dump(manifest, f, ensure_ascii=False, indent=2)
            print("\n  清单: %s" % manifest_path)

            ok_count = sum(1 for r in results if r['status'] == 'ok')
            print("  成功: %d/%d" % (ok_count, len(results)))


if __name__ == '__main__':
    main()
