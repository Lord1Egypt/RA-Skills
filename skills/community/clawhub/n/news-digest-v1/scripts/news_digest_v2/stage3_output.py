# -*- coding: utf-8 -*-
"""
阶段 3：生成摘要输出
功能：从 digest_output 表读取 LLM 总结 → 格式化输出到桌面和工作区
如果 digest_output 无数据，则回退到 articles 表
"""
import sys, os
import sqlite3
from datetime import datetime, timedelta

# Support standalone execution
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from .config import DB_PATH, MAX_OUTPUT_COUNT
    from .formatter import generate_output
except ImportError:
    from config import DB_PATH, MAX_OUTPUT_COUNT
    from formatter import generate_output


def get_news_for_output(max_count=35):
    """Get news from digest_output or fallback to articles
    
    来源权威性优先策略：每个权威来源至少入选 min_per_authoritative 条
    剩余名额按 ID 降序填充其他来源
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    today = datetime.now().strftime('%Y-%m-%d')
    date_from = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    
    # Try digest_output first (LLM summaries)
    c.execute('''
        SELECT id, title, source, publish_date, summary, url, keywords
        FROM digest_output
        WHERE digest_date = ?
        ORDER BY id DESC
    ''', (today,))
    
    rows = c.fetchall()
    from_digest = len(rows) > 0
    
    if not from_digest:
        print("  [INFO] No digest_output for today, falling back to articles")
        c.execute('''
            SELECT a.id, a.title, a.source, a.publish_date, a.summary, a.url, a.keywords
            FROM articles a
            WHERE a.publish_date >= ?
            AND a.is_duplicate = 0
            ORDER BY a.id DESC
        ''', (date_from,))
        rows = c.fetchall()
    
    all_news = []
    for row in rows:
        source = row[2]
        # 来源归一化：新华子频道归并为新华网
        if source.startswith('新华') and source != '新华社':
            source = '新华网'
        all_news.append({
            'id': row[0], 'title': row[1], 'source': source,
            'publish_date': row[3], 'summary': row[4],
            'url': row[5], 'keywords': row[6]
        })
    
    conn.close()
    
    if len(all_news) <= max_count:
        # === 即使数量不足也排序 ===
        SOURCE_AUTHORITY = {
            '人民网': 1, '新华网': 1, '新华社': 1, '人民日报': 1,
            '央广网': 1, '经济日报': 1, '科技日报': 1,
            '中国经济网': 2, '中国科技网': 2, '科学网': 2, '科创版日报': 2,
            '中宏网': 3, '36 氪': 3, '钛媒体': 3, '中国产经网': 3,
            '中国工信网': 3, '中国工业新闻网': 3,
            '大皖新闻': 4, '中安在线': 4, '新华汽车': 4, '新华科创': 4,
            '新华时政': 4, '新华能源': 4,
        }
        all_news.sort(key=lambda x: (SOURCE_AUTHORITY.get(x['source'], 99), -x['id']))
        return all_news, from_digest
    
    # === 权威性优先选文 ===
    # 每个权威来源保底 2 条
    authoritative_sources = [
        '人民网', '新华网', '新华社', '人民日报',
        '央广网', '经济日报', '科技日报', '科学网',
        '中国科技网', '科创版日报', '中国经济网'
    ]
    min_per_authoritative = 2
    
    # 按来源分组
    by_source = {}
    for n in all_news:
        src = n['source']
        if src not in by_source:
            by_source[src] = []
        by_source[src].append(n)
    
    # 每个权威来源至少取 2 条
    selected_ids = set()
    selected = []
    for src in authoritative_sources:
        if src in by_source:
            articles = sorted(by_source[src], key=lambda x: x['id'], reverse=True)
            for a in articles[:min_per_authoritative]:
                if a['id'] not in selected_ids:
                    selected.append(a)
                    selected_ids.add(a['id'])
    
    # 剩余名额按 ID 降序填充
    remaining = [n for n in all_news if n['id'] not in selected_ids]
    remaining.sort(key=lambda x: x['id'], reverse=True)
    
    for n in remaining:
        if len(selected) >= max_count:
            break
        selected.append(n)
        selected_ids.add(n['id'])
    
    # === 输出排序：权威性高的放前面 ===
    SOURCE_AUTHORITY = {
        '人民网': 1, '新华网': 1, '新华社': 1, '人民日报': 1,
        '央广网': 1, '经济日报': 1, '科技日报': 1,
        '中国经济网': 2, '中国科技网': 2, '科学网': 2, '科创版日报': 2,
        '中宏网': 3, '36 氪': 3, '钛媒体': 3, '中国产经网': 3,
        '中国工信网': 3, '中国工业新闻网': 3,
        '大皖新闻': 4, '中安在线': 4, '新华汽车': 4, '新华科创': 4,
        '新华时政': 4, '新华能源': 4,
    }
    
    def get_auth_level(src):
        return SOURCE_AUTHORITY.get(src, 99)
    
    # 按权威级别升序，同级别按 ID 降序（最新优先）
    selected.sort(key=lambda x: (get_auth_level(x['source']), -x['id']))
    
    return selected, from_digest


def main():
    """Stage 3 Main Flow"""
    start_time = datetime.now()
    print(f"{'='*60}")
    print(f"Generate Output Task (Stage 3/3)")
    print(f"Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    print("【Task 1】Reading news data...")
    news_list, from_digest = get_news_for_output(max_count=MAX_OUTPUT_COUNT)
    
    if from_digest:
        print(f"  Source: digest_output table (LLM Summary)")
    else:
        print(f"  Source: articles table (Rule Summary)")
    
    if len(news_list) == 0:
        print("  No news data")
        return 1
    
    print(f"  Read {len(news_list)} articles\n")
    
    # Generate output
    print("【Task 2】Formatting output...")
    output_start = datetime.now()
    
    output_text, stats = generate_output(news_list, max_count=MAX_OUTPUT_COUNT)
    
    # Save to desktop
    desktop = os.path.join(os.environ.get('USERPROFILE', ''), 'Desktop')
    today_date = datetime.now().strftime('%Y%m%d')
    
    # Check if today's digest already exists (avoid duplicate files)
    import glob
    existing_files = glob.glob(os.path.join(desktop, f"新闻摘要_{today_date}*.txt"))
    if existing_files:
        latest = max(existing_files, key=os.path.getmtime)
        file_size = os.path.getsize(latest)
        print(f"  [SKIP] Today's digest already exists: {os.path.basename(latest)} ({file_size} bytes)")
        print(f"  If you want a fresh run, delete the existing file first.")
        return 0
    
    today_str = datetime.now().strftime('%Y%m%d_%H%M%S')
    desktop_file = os.path.join(desktop, f"新闻摘要_{today_str}.txt")
    with open(desktop_file, 'w', encoding='utf-8') as f:
        f.write(output_text)
    
    # Save to workspace
    with open('.news-digest-out.md', 'w', encoding='utf-8') as f:
        f.write(output_text)
    
    output_elapsed = (datetime.now() - output_start).total_seconds()
    print(f"OK Generated summary: {stats['total']} articles")
    print(f"OK Desktop file: {desktop_file}")
    print(f"OK Time taken: {output_elapsed:.1f}s\n")
    
    total_elapsed = (datetime.now() - start_time).total_seconds()
    print(f"{'='*60}")
    print(f"Stage 3 Complete!")
    print(f"Total Time: {total_elapsed:.1f}s")
    print(f"{'='*60}")
    print(f"\nStats:")
    print(f"  Output Articles: {stats['total']}")
    print(f"  Sources: {stats['sources']}")
    print(f"\nPROCESS_DONE")
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        import traceback
        print(f"\nERROR: {e}")
        traceback.print_exc()
        sys.exit(1)
