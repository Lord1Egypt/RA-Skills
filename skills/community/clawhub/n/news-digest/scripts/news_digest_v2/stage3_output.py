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
    from .formatter import generate_output, check_article_quality
except ImportError:
    from config import DB_PATH, MAX_OUTPUT_COUNT
    from formatter import generate_output, check_article_quality
import re


def filter_low_quality(news_list):
    """低质量内容过滤（与 stage2.5 保持一致）"""
    corporate_pr_keywords = [
        r'捐赠', r'赞助', r'战略合作', r'深度联动',
        r'进驻.*奥体', r'进驻.*体育中心',
        r'体育.*健康.*融合', r'筑牢健康防线',
        r'针对我司报警', r'针对.*报警的声明',
    ]
    geopol_keywords = [
        r'谅解备忘录', r'霍尔木兹海峡', r'海上封锁',
        r'军事打击', r'美伊',
    ]
    propaganda_keywords = [
        r'绘说现代化', r'绘说', r'零时差', r'与其炒作',
    ]
    # 银行PR过滤（非产业动态）
    bank_pr_keywords = [
        r'赋能.*文旅', r'赋能.*海上', r'助老连心桥', r'养老集市',
        r'蓝色专项授信', r'专项金融服务方案', r'量身定制.*金融',
        r'智慧收单', r'资金归集', r'一站式结算',
        r'精准对接需求', r'破解融资难题', r'创新授信模式',
        r'配套综合服务', r'筑牢.*根基', r'传递金融温度',
        r'该行主动走访调研', r'授信准入', r'增信依据',
    ]
    # 地方招商/经开区/高新区宣传
    local_promotion_keywords = [
        r'经开区.*聚链', r'高新区.*落地', r'经开区.*新动能',
        r'产业园.*投产', r'产业园.*建设', r'产业园.*进展',
        r'厚植.*热土', r'打造.*高地', r'招商.*引资',
        r'企业聚链成群', r'葡萄串.*效应',
        r'小灯塔.*企业', r'链主.*企业',
        r'加快推进.*项目', r'取得.*进展',
    ]
    # 软性专栏/调研行
    soft_column_keywords = [
        r'活力中国调研行', r'尺素金声', r'一线见闻',
        r'调研行.*看', r'调研行.*走进', r'看大国',
        r'美丽中国行', r'在希望的田野上', r'新闻联播',
        r'探馆', r'探访.*馆', r'走进.*馆',
        r'从四个趋势透视', r'经济观察',
        r'从.*数据看', r'数据看懂',
    ]
    skip_title_keywords = [
        r'逆回购操作', r'中间价报', r'人民币汇率中间价',
        r'银行间外汇市场', r'中国人民银行授权',
        r'食用.*中毒', r'交通事故',
    ]
    # 不需要出现在摘要中的主题(与 stage2.5 保持一致)
    skip_topic_keywords = [
        r'调配血液', r'无偿献血.*单位',
        r'航母编队', r'甩掉偷窥者',
        r'游泳队.*参赛名单', r'亚运会.*名单',
    ]
    min_content_length = 150  # 与 stage2.5 保持一致

    filtered = []
    skipped = []
    for n in news_list:
        title = n['title']
        content = n.get('content', '') or ''
        skip = False

        text = title + ' ' + content
        for kw in corporate_pr_keywords:
            if re.search(kw, text):
                skip = True; skipped.append(f"[公关] {title[:40]}"); break
        if not skip:
            for kw in geopol_keywords:
                if re.search(kw, title):
                    skip = True; skipped.append(f"[地缘] {title[:40]}"); break
        if not skip:
            for kw in propaganda_keywords:
                if re.search(kw, title):
                    skip = True; skipped.append(f"[宣传] {title[:40]}"); break
        if not skip:
            for kw in bank_pr_keywords:
                if re.search(kw, text):
                    skip = True; skipped.append(f"[银行PR] {title[:40]}"); break
        if not skip:
            for kw in local_promotion_keywords:
                if re.search(kw, text):
                    skip = True; skipped.append(f"[地方招商] {title[:40]}"); break
        if not skip:
            for kw in soft_column_keywords:
                if re.search(kw, title):
                    skip = True; skipped.append(f"[软专栏] {title[:40]}"); break
        if not skip:
            for kw in skip_title_keywords:
                if re.search(kw, title):
                    skip = True; skipped.append(f"[例行] {title[:40]}"); break
        if not skip:
            for kw in skip_topic_keywords:
                if re.search(kw, title):
                    skip = True; skipped.append(f"[不需要] {title[:40]}"); break
        if not skip and len(content.strip()) < min_content_length:
            skip = True; skipped.append(f"[短] {title[:40]}")

        if skip:
            continue
        filtered.append(n)

    if skipped:
        print(f"  [回退过滤] 过滤 {len(skipped)} 条低质量内容")
    return filtered


def topic_dedup(nl):
    """同一主题去重（与 stage2.5 保持一致，仅 articles 路径需要）"""
    topic_map = {}
    for n in nl:
        title = n['title']
        content = n.get('content', '') or ''
        topic = None
        if 'SpaceX' in title or 'SpaceX' in content:
            topic = 'SpaceX_IPO'
        elif '脑机接口' in title:
            topic = '脑机接口'
        if topic:
            topic_map.setdefault(topic, []).append((len(content), n))

    removed_titles = []
    for topic_items in topic_map.values():
        topic_items.sort(key=lambda x: x[0], reverse=True)
        for _, n in topic_items[1:]:
            removed_titles.append(n)

    if removed_titles:
        print(f"  [主题去重] 过滤 {len(removed_titles)} 条重复主题")
    removed_ids = {r['id'] for r in removed_titles}
    return [n for n in nl if n['id'] not in removed_ids]


SOURCE_AUTHORITY = {
    '人民网': 1, '新华网': 1, '新华社': 1, '人民日报': 1,
    '央广网': 1, '经济日报': 1, '科技日报': 1,
    '中国经济网': 2, '中国科技网': 2, '科学网': 2, '科创版日报': 2,
    '中宏网': 3, '36 氪': 3, '钛媒体': 3, '中国产经网': 3,
    '中国工信网': 3, '中国工业新闻网': 3,
    '大皖新闻': 4, '中安在线': 4, '新华汽车': 4, '新华科创': 4,
    '新华时政': 4, '新华能源': 4,
}


def get_news_for_output(max_count=35):
    """Get news from digest_output or fallback to articles
    
    来源权威性优先策略：每个权威来源至少入选 min_per_authoritative 条
    剩余名额按 ID 降序填充其他来源
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    today = datetime.now().strftime('%Y-%m-%d')
    date_from = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
    
    # Try digest_output first (LLM summaries)
    # 修复(2026-06-17): 加 LIMIT 避免多次运行叠加导致旧闻混入
    c.execute('''
        SELECT id, title, source, publish_date, summary, url, keywords
        FROM digest_output
        WHERE digest_date = ?
        ORDER BY id DESC
        LIMIT ?
    ''', (today, max_count))
    
    rows = c.fetchall()
    from_digest = len(rows) > 0

    # 部分失败检测：stage2.5 写到一半崩溃导致 digest_output 只有零星数据
    # 阈值：少于 5 条且 articles 有更多候选时，判定为部分失败并回退
    MIN_DIGEST_COUNT = 5
    if from_digest and len(rows) < MIN_DIGEST_COUNT:
        print(f"  [WARN] digest_output 仅 {len(rows)} 条，可能部分失败，检查 articles...")
        c.execute('''
            SELECT count(*)
            FROM articles a
            WHERE a.publish_date >= ?
            AND a.is_duplicate = 0
        ''', (date_from,))
        art_count = c.fetchone()[0]
        if art_count > len(rows):
            print(f"  [INFO] articles 有 {art_count} 条候选，回退到 articles 路径")
            from_digest = False
            rows = []

    if not from_digest:
        print("  [INFO] No digest_output for today, falling back to articles")
        c.execute('''
            SELECT a.id, a.title, a.source, a.publish_date, a.summary, a.url, a.keywords, a.content
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
            'url': row[5], 'keywords': row[6],
            'content': row[7] if len(row) > 7 else '',
        })
    
    conn.close()
    
    # digest_output 数据已经过 stage2.5 过滤，直接返回
    if from_digest:
        news_list = all_news
        if len(news_list) > max_count:
            news_list = news_list[:max_count]
        news_list.sort(key=lambda x: (SOURCE_AUTHORITY.get(x['source'], 99), -x['id']))
        return news_list

    # 回退到 articles 路径：需要补充低质量过滤 + 主题去重 + 权威选文
    news_list = all_news
    news_list = filter_low_quality(news_list)
    news_list = topic_dedup(news_list)

    if len(news_list) > max_count:
        authoritative_sources = [
            '人民网', '新华网', '新华社', '人民日报',
            '央广网', '经济日报', '科技日报', '科学网',
            '中国科技网', '科创版日报', '中国经济网'
        ]
        min_per_authoritative = 2
        by_source = {}
        for n in news_list:
            by_source.setdefault(n['source'], []).append(n)
        selected_ids = set()
        selected = []
        for src in authoritative_sources:
            if src in by_source:
                for a in sorted(by_source[src], key=lambda x: x['id'], reverse=True)[:min_per_authoritative]:
                    if a['id'] not in selected_ids:
                        selected.append(a)
                        selected_ids.add(a['id'])
        remaining = [n for n in news_list if n['id'] not in selected_ids]
        remaining.sort(key=lambda x: x['id'], reverse=True)
        for n in remaining:
            if len(selected) >= max_count:
                break
            selected.append(n)
            selected_ids.add(n['id'])
        news_list = selected

    news_list.sort(key=lambda x: (SOURCE_AUTHORITY.get(x['source'], 99), -x['id']))
    return news_list


def main():
    """Stage 3 Main Flow"""
    start_time = datetime.now()
    print(f"{'='*60}")
    print(f"Generate Output Task (Stage 3/3)")
    print(f"Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    print("【Task 1】Reading news data...")
    news_list = get_news_for_output(max_count=MAX_OUTPUT_COUNT)
    
    if len(news_list) == 0:
        print("  No news data")
        return 1
    
    print(f"  Read {len(news_list)} articles\n")
    
    # 质量检查：过滤空壳/短内容
    print("【Task 1.5】Quality check...")
    news_list, issues = check_article_quality(news_list)
    if issues:
        print(f"  ⚠️ 发现 {len(issues)} 条空壳/短内容新闻（已过滤）:")
        for issue in issues:
            print(f"    [{issue['source']}] {issue['title']} - {issue['reason']}")
    else:
        print("  ✅ 所有内容检查通过")
    print(f"  过滤后: {len(news_list)} articles\n")
    
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
