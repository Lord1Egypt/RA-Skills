# -*- coding: utf-8 -*-
"""
阶段 2.5:LLM 批量总结模块
功能:从数据库查询 Top 35 新闻,用 LLM 批量总结,存入 digest_output 表
"""
import sys, os
import json
import time
import re
import sqlite3
import urllib.request
from datetime import datetime

# 设置 UTF-8 输出
sys.stdout.reconfigure(encoding='utf-8', errors='ignore')

# Support standalone execution
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from .config import DB_PATH, LLM_MAX_LENGTH, LLM_BATCH_SIZE
except ImportError:
    from config import DB_PATH, LLM_MAX_LENGTH, LLM_BATCH_SIZE

# LLM Configuration (use environment variables, fallback to OpenClaw config)
API_KEY = os.environ.get('NEWS_DIGEST_LLM_API_KEY', '')
BASE_URL = os.environ.get('NEWS_DIGEST_LLM_BASE_URL', '')
MODEL = os.environ.get('NEWS_DIGEST_LLM_MODEL', 'qwen3.6-plus')

def load_llm_config():
    """Fallback: try to load from OpenClaw config if env vars not set"""
    global API_KEY, BASE_URL
    if API_KEY and BASE_URL:
        return True
    try:
        config_path = os.path.expanduser(r"~\.openclaw\openclaw.json")
        with open(config_path, 'r', encoding='utf-8-sig') as f:
            config = json.load(f)
        provider = config['models']['providers']['custom-coding-dashscope-aliyuncs-com']
        API_KEY = provider['apiKey']
        BASE_URL = provider['baseUrl']
        return True
    except Exception as e:
        print(f"  ⚠️ LLM config load failed: {e}")
        return False

def call_llm(prompt, max_tokens=4000, temperature=0.3):
    """Call LLM API"""
    if not API_KEY or not BASE_URL:
        load_llm_config()
    if not API_KEY or not BASE_URL:
        print(f"  ⚠️ LLM not configured, skipping summary")
        return None
    if not API_KEY:
        return None

    req_data = json.dumps({
        'model': MODEL,
        'messages': [{'role': 'user', 'content': prompt}],
        'temperature': temperature,
        'max_tokens': max_tokens
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/chat/completions',
        data=req_data,
        headers={
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json'
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            return result.get('choices', [{}])[0].get('message', {}).get('content', '')
    except Exception as e:
        print(f"  ⚠️ LLM API Error: {e}")
        return None

def parse_llm_response(content, news_count):
    """Parse LLM response"""
    summaries = {}
    pattern = r'\[(\d+)\]\s*(.+?)\n(.+?)(?=\n\n|\[\d+\]|$)'
    matches = re.findall(pattern, content, re.DOTALL)

    for match in matches:
        idx = int(match[0])
        title = match[1].strip()
        summary = match[2].strip()
        summaries[idx] = {'title': title, 'summary': summary}

    return summaries

def llm_summarize_batch(batch_news_list, batch_num, batch_total):
    """Summarize one batch"""
    articles_text = ""
    for i, n in enumerate(batch_news_list):
        content_snippet = (n.get('content', '') or n.get('summary', ''))[:800]
        # 乱码标题检测:Cyrillic 字符或异常高比例的非CJK字符
        raw_title = n['title']
        has_cyrillic = bool(re.search(r'[а-яА-Я]', raw_title))
        if has_cyrillic:
            # 标题乱码 → 通知 LLM 从正文生成正确标题
            articles_text += f"[{i+1}] {n['source']}:(标题编码异常,请根据正文生成准确标题)\n{content_snippet}\n\n"
        else:
            articles_text += f"[{i+1}] {n['source']}:{n['title']}\n{content_snippet}\n\n"

    prompt = f"""你是一个专业新闻编辑。请将以下 {len(batch_news_list)} 条新闻分别总结成一段话,每条不超过{LLM_MAX_LENGTH}字。

要求:
1. 保留核心事实(谁、做了什么、关键数据、影响),尽量全面完整
2. **摘要不要简单重复标题**,重点补充标题之外的细节、背景和数据
3. 语言规范、简洁、专业
4. 若原文引用了政策文件、方案、通知等,必须提供文件全称(如《XXX方案(2026-2027年)》)
5. 每条字数控制在200-{LLM_MAX_LENGTH}字之间
6. 去掉电头和记者署名(如"羊城晚报讯 记者XXX报道:""本报讯""记者XXX从XX获悉"等)
7. 每条格式为:
[编号] 来源:标题
总结内容(不超过{LLM_MAX_LENGTH}字)
8. 如果标题标注为"(标题编码异常,请根据正文生成准确标题)",请根据正文内容生成准确的中文标题,替换该标注
9. **标题改写规则**:仅当原标题中公司只是**参展/出席/参与**某个活动时,才将标题改写为以活动/事件为主体,公司名不出现在标题里。例如:"长虹华丰亮相2026无人机展" → "第十届世界无人机大会在深圳举办"。
   **但以下情况保留公司名在标题中**:IPO/上市/融资/收购/合并/财报/重大签约/核心产品发布--公司本身就是新闻主体,公司名必须保留。例如:"美量子计算公司Quantinuum上调IPO规模" 保持不变。
10. **严格禁止编造**:摘要中的每一条信息(事实、数据、政策、措施)都必须来源于提供的原文,不得添加原文中不存在的内容。如果原文信息不足,就基于原文已有内容精简概括,绝不自行补充外部知识。

新闻列表:
{articles_text}

请开始:"""

    response = call_llm(prompt, max_tokens=4000, temperature=0.3)
    if not response:
        print(f"  ⚠️ Batch {batch_num} LLM call failed")
        return {}

    return parse_llm_response(response, len(batch_news_list))

def llm_batch_summarize(news_list):
    """Batch summarize all news"""
    if len(news_list) == 0:
        return []
    
    # 修复 2：内容不足的文章直接跳过 LLM，用原文作为摘要
    MIN_CONTENT_CHARS = 50  # 原文至少 50 字才值得 LLM 总结
    skip_count = 0
    for news in news_list:
        content = (news.get('content', '') or '') + (news.get('summary', '') or '')
        if len(content) < MIN_CONTENT_CHARS:
            news['_skip_llm'] = True
            # 原文太短，直接用 title + summary 作为摘要
            news['summary'] = news.get('summary', '') or news.get('title', '')
            skip_count += 1
    
    # 过滤掉跳过的文章，剩下的送 LLM
    # 保留原始索引以便后续正确更新 summary
    news_for_llm = [(i, n) for i, n in enumerate(news_list) if not n.get('_skip_llm', False)]
    
    if skip_count > 0:
        print(f"  [{skip_count} 条原文不足 {MIN_CONTENT_CHARS} 字，跳过 LLM 直接使用原文]")
    
    if len(news_for_llm) == 0:
        print(f"  No articles need LLM summary")
        return news_list
    
    print(f"  Starting LLM batch summary ({len(news_for_llm)} articles)...")
    start = time.time()

    # 拆分成小批次,每批 8 条,避免触发限流
    articles_per_batch = 8
    batches = []
    for i in range(0, len(news_for_llm), articles_per_batch):
        batches.append(news_for_llm[i:i + articles_per_batch])

    all_summaries = {}  # maps original_index -> summary_text
    for batch_idx, batch in enumerate(batches):
        if len(batch) == 0:
            continue

        print(f"  Processing batch {batch_idx+1}/{len(batches)} ({len(batch)} articles)...")

        # 准备给 LLM 的文本（用 batch 里的 news 对象）
        batch_news_for_llm = [n for _, n in batch]

        # 重试机制(最多 3 次)
        max_retries = 3
        for attempt in range(max_retries):
            try:
                summaries = llm_summarize_batch(batch_news_for_llm, batch_idx+1, len(batches))
                if summaries:
                    break
                # 如果返回空,等待后重试
                if attempt < max_retries - 1:
                    wait_time = 30 * (attempt + 1)  # 30s, 60s
                    print(f"  ⚠️ Batch {batch_idx+1} returned empty, retrying in {wait_time}s...")
                    time.sleep(wait_time)
            except Exception as e:
                if attempt < max_retries - 1:
                    wait_time = 30 * (attempt + 1)
                    print(f"  ⚠️ Batch {batch_idx+1} error: {e}, retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    print(f"  ❌ Batch {batch_idx+1} failed after {max_retries} retries: {e}")
                    summaries = {}

        # 将 LLM 返回的摘要映射回原始索引
        for local_idx, data in summaries.items():
            orig_idx = batch[local_idx - 1][0]  # local_idx is 1-based, batch has (orig_idx, news) tuples
            all_summaries[orig_idx] = data['summary']

        # 批次间延迟 20 秒,避免限流
        if batch_idx < len(batches) - 1:
            print(f"  ⏳ Waiting 20s before next batch...")
            time.sleep(20)

    # Update summaries（按原始索引更新）
    updated = 0
    for orig_idx, summary_text in all_summaries.items():
        news_list[orig_idx]['summary'] = summary_text
        updated += 1

    elapsed = time.time() - start
    print(f"  ✅ LLM summary complete: {updated}/{len(news_list)} articles, took {elapsed:.1f}s")

    return news_list

def main():
    """Main flow"""
    print(f"\n{'='*60}")
    print(f"  Stage 2.5: LLM Batch Summary")
    print(f"{'='*60}\n")

    start = time.time()

    # 1. Init digest_output table
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS digest_output (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            source TEXT NOT NULL,
            publish_date TEXT NOT NULL,
            summary TEXT NOT NULL,
            url TEXT UNIQUE NOT NULL,
            keywords TEXT,
            digest_date TEXT NOT NULL,
            source_article_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()

    # 2. Query ALL eligible articles (exclude any url already in digest_output)
    today = datetime.now().strftime('%Y-%m-%d')
    date_from = (datetime.now() - __import__('datetime').timedelta(days=7)).strftime('%Y-%m-%d')

    c.execute('''
        SELECT a.id, a.title, a.source, a.publish_date, a.summary, a.url, a.keywords, a.content
        FROM articles a
        WHERE a.publish_date >= ?
        AND a.is_duplicate = 0
        AND a.url NOT IN (SELECT url FROM digest_output)
        ORDER BY a.id DESC
    ''', (date_from,))

    all_rows = c.fetchall()
    all_news = []
    for row in all_rows:
        all_news.append({
            'id': row[0], 'title': row[1], 'source': row[2],
            'publish_date': row[3], 'summary': row[4],
            'url': row[5], 'keywords': row[6], 'content': row[7]
        })

    if len(all_news) == 0:
        print("  No new articles to summarize (or all done)")
        conn.close()
        return 0

    print(f"  Total eligible articles: {len(all_news)}")

    # Apply authoritative priority: each authoritative source gets at least min_per_authoritative
    authoritative_sources = [
        '人民网', '新华网', '新华社', '人民日报',
        '央广网', '经济日报', '科技日报', '科学网',
        '中国科技网', '科创版日报', '中国经济网'
    ]
    min_per_authoritative = 2
    max_count = LLM_BATCH_SIZE  # 35

    if len(all_news) > max_count:
        # Group by source
        by_source = {}
        for n in all_news:
            src = n['source']
            if src not in by_source:
                by_source[src] = []
            by_source[src].append(n)

        # Select authoritative sources first (at least 2 each)
        selected_ids = set()
        selected = []
        for src in authoritative_sources:
            if src in by_source:
                articles = sorted(by_source[src], key=lambda x: x['id'], reverse=True)
                for a in articles[:min_per_authoritative]:
                    if a['id'] not in selected_ids:
                        selected.append(a)
                        selected_ids.add(a['id'])

        # Fill remaining by ID descending
        remaining = [n for n in all_news if n['id'] not in selected_ids]
        remaining.sort(key=lambda x: x['id'], reverse=True)

        for n in remaining:
            if len(selected) >= max_count:
                break
            selected.append(n)
            selected_ids.add(n['id'])

        news_list = selected[:max_count]
        auth_count = sum(1 for n in news_list if n['source'] in authoritative_sources)
        print(f"  Articles to summarize: {len(news_list)} (authoritative priority applied, {auth_count} from authoritative sources)")
    else:
        news_list = all_news
        print(f"  Articles to summarize: {len(news_list)} (all eligible)")

    # 2.5 跨天标题去重(在 LLM 之前,不浪费 token)
    # 注意：url 重复已在 SQL 层排除，此处仅拦截 url 不同但标题高度相似的文章
    try:
        from .config import CROSS_DAY_DEDUP_ENABLED
        if CROSS_DAY_DEDUP_ENABLED:
            from .cross_day_dedup import filter_cross_day_duplicates
            print(f"\n  [跨天标题去重] 检查最近历史摘要（标题相似度，url 已在 SQL 层排除）...")
            news_list, blocked = filter_cross_day_duplicates(news_list, verbose=True)
            if blocked:
                print(f"  [跨天标题去重] 保留 {len(news_list)} 条,标题拦截 {len(blocked)} 条\n")
            else:
                print(f"  [跨天标题去重] 保留 {len(news_list)} 条,无标题拦截\n")
    except ImportError:
        pass

    # 3. LLM Summary
    news_list = llm_batch_summarize(news_list)

    # 4. Save to digest_output
    saved = 0
    for news in news_list:
        try:
            c.execute('''
                INSERT OR IGNORE INTO digest_output
                (title, source, publish_date, summary, url, keywords, digest_date, source_article_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                news['title'], news['source'], news['publish_date'],
                news['summary'], news['url'], news.get('keywords', ''),
                today, news['id']
            ))
            if c.rowcount > 0:
                saved += 1
        except Exception as e:
            print(f"  Save failed: {news['title'][:30]}... - {e}")

    conn.commit()
    conn.close()

    elapsed = time.time() - start
    print(f"\n  ✅ Saved {saved} articles to digest_output")
    print(f"  Total time: {elapsed:.1f}s")

    return saved

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        import traceback
        print(f"\n[ERROR] {e}")
        traceback.print_exc()
        sys.exit(1)
