# -*- coding: utf-8 -*-
"""
数据库操作模块
"""

import sqlite3
import re
from datetime import datetime, timedelta
try:
    from .config import DB_PATH
    from .similarity import calculate_similarity
except ImportError:
    from config import DB_PATH
    from similarity import calculate_similarity


def init_database():
    """初始化数据库表结构"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 创建 articles 表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        source TEXT NOT NULL,
        publish_date TEXT NOT NULL,
        summary TEXT,
        content TEXT,
        url TEXT UNIQUE NOT NULL,
        keywords TEXT,
        is_duplicate INTEGER DEFAULT 0,
        similarity_score REAL DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 创建 system_keywords 表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS system_keywords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        keyword TEXT UNIQUE NOT NULL,
        category TEXT,
        weight INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 创建索引
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_publish_date ON articles(publish_date)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_keywords ON articles(keywords)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_is_duplicate ON articles(is_duplicate)')
    
    conn.commit()
    conn.close()


def save_to_database(news_list):
    """
    保存新闻到数据库
    
    Args:
        news_list: 新闻列表，每项为 dict，包含 title, source, publish_date, summary, url
    
    Returns:
        int: 新增数量
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    inserted = 0
    skipped = 0
    
    for news in news_list:
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO articles 
                (title, source, publish_date, summary, url, content)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                news['title'],
                news['source'],
                news['publish_date'],
                news['summary'],
                news['url'],
                news.get('content', '')
            ))
            
            if cursor.rowcount > 0:
                inserted += 1
            else:
                skipped += 1
        except Exception as e:
            title_safe = news['title'][:30].encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
            print(f"  保存失败：{title_safe}... - {e}")
            skipped += 1
    
    conn.commit()
    conn.close()
    
    return inserted


def get_recent_news(date_from=None, limit=100):
    """
    获取最近的新闻
    
    Args:
        date_from: 起始日期（字符串 'YYYY-MM-DD' 或 datetime）
        limit: 数量限制
    
    Returns:
        list: 新闻列表
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if date_from is None:
        date_from = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
    elif isinstance(date_from, datetime):
        date_from = date_from.strftime('%Y-%m-%d')
    
    cursor.execute('''
        SELECT id, title, source, publish_date, summary, content, url, keywords, is_duplicate
        FROM articles
        WHERE publish_date >= ?
        ORDER BY publish_date DESC, id DESC
        LIMIT ?
    ''', (date_from, limit))
    
    results = []
    for row in cursor.fetchall():
        results.append({
            'id': row[0],
            'title': row[1],
            'source': row[2],
            'publish_date': row[3],
            'summary': row[4],
            'content': row[5],
            'url': row[6],
            'keywords': row[7],
            'is_duplicate': row[8]
        })
    
    conn.close()
    return results


def mark_duplicates(threshold=0.90):
    """
    标记重复新闻
    
    Args:
        threshold: 相似度阈值
    
    Returns:
        int: 标记为重复的数量
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 获取最近 3 天的新闻
    date_from = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
    cursor.execute('''
        SELECT id, title, summary
        FROM articles
        WHERE publish_date >= ?
        AND is_duplicate = 0
        ORDER BY publish_date DESC, id DESC
    ''', (date_from,))
    
    news_list = cursor.fetchall()
    
    # 辅助函数：最长公共子串长度
    def _get_lcs_len(s1, s2):
        m, n = len(s1), len(s2)
        if m == 0 or n == 0: return 0
        max_len = 0
        for i in range(m):
            for j in range(n):
                k = 0
                while (i + k < m and j + k < n and s1[i+k] == s2[j+k]):
                    k += 1
                if k > max_len: max_len = k
        return max_len

    # 两两比较
    dup_ids = set()
    for i in range(len(news_list)):
        if news_list[i][0] in dup_ids:
            continue
        
        title1 = news_list[i][1]
        text1 = title1 + ' ' + (news_list[i][2] or '')
        
        for j in range(i + 1, len(news_list)):
            if news_list[j][0] in dup_ids:
                continue
            
            title2 = news_list[j][1]
            text2 = title2 + ' ' + (news_list[j][2] or '')
            
            similarity = 0.0
            
            # 1. 标题包含检测：如果标题 A 出现在文本 B 中（或反之），判定为重复
            if title1 in text2 or title2 in text1:
                similarity = 1.0
            # 2. 标题长公共子串：如果标题包含 >=8 字符的相同事件名（如"世界品牌莫干山大会"）
            elif _get_lcs_len(title1, title2) >= 8:
                similarity = 1.0
            else:
                # 3. 常规 Jaccard 相似度
                text_sim = calculate_similarity(text1, text2)
                title_sim = calculate_similarity(title1, title2)
                
                # 优化：针对“同题多源”报道（标题不同但内容相同）
                # 如果标题差异大（< 0.5），但内容相似度尚可（> 0.45），判定为重复
                if title_sim < 0.5 and text_sim > 0.45:
                    similarity = 1.0
                else:
                    similarity = text_sim
            
            if similarity >= threshold:
                dup_ids.add(news_list[j][0])
                # 更新相似度
                cursor.execute('''
                    UPDATE articles 
                    SET is_duplicate = 1, similarity_score = ?
                    WHERE id = ?
                ''', (similarity, news_list[j][0]))
    
    conn.commit()
    conn.close()
    
    return len(dup_ids)


def update_keywords(date_from=None, max_keywords=5):
    """
    更新新闻关键词
    
    Args:
        date_from: 起始日期
        max_keywords: 每条新闻最多关键词数
    
    Returns:
        int: 更新数量
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if date_from is None:
        date_from = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
    
    # 加载系统关键词
    cursor.execute('SELECT keyword, category, weight FROM system_keywords')
    keyword_dict = {
        row[0]: {'category': row[1], 'weight': row[2]} 
        for row in cursor.fetchall()
    }
    
    # 获取需要更新的新闻
    cursor.execute('''
        SELECT id, title, summary, content
        FROM articles
        WHERE publish_date >= ?
        ORDER BY publish_date DESC
    ''', (date_from,))
    
    news_list = cursor.fetchall()
    updated = 0
    
    for news in news_list:
        news_id, title, summary, content = news
        text = title + ' ' + (summary or '') + ' ' + (content or '')
        
        # 匹配关键词并计算得分
        matched = []
        for kw, info in keyword_dict.items():
            count = text.count(kw)
            if count > 0:
                title_bonus = 2 if kw in title else 1
                score = info['weight'] * count * title_bonus
                matched.append((kw, score))
        
        # 按得分排序，取前 N 个
        matched.sort(key=lambda x: x[1], reverse=True)
        top_keywords = [kw for kw, _ in matched[:max_keywords]]
        
        # 更新
        if top_keywords:
            keywords_str = ', '.join(top_keywords)
            cursor.execute('''
                UPDATE articles 
                SET keywords = ?
                WHERE id = ?
            ''', (keywords_str, news_id))
            updated += 1
    
    conn.commit()
    conn.close()
    
    return updated


def get_news_for_output(max_count=35, exclude_duplicates=True):
    """
    获取用于输出的新闻
    
    Args:
        max_count: 最大数量
        exclude_duplicates: 是否排除重复
    
    Returns:
        list: 新闻列表
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    date_from = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    
    if exclude_duplicates:
        cursor.execute('''
            SELECT a.id, a.title, a.source, a.publish_date, a.summary, a.content, a.url, a.keywords,
                   COALESCE(w.priority, 99) as site_priority
            FROM articles a
            LEFT JOIN monitor_websites w ON a.source = w.name AND w.enabled = 1
            WHERE a.publish_date >= ?
            AND a.is_duplicate = 0
            ORDER BY site_priority ASC, a.id DESC
            LIMIT ?
        ''', (date_from, max_count))
    else:
        cursor.execute('''
            SELECT a.id, a.title, a.source, a.publish_date, a.summary, a.content, a.url, a.keywords,
                   COALESCE(w.priority, 99) as site_priority
            FROM articles a
            LEFT JOIN monitor_websites w ON a.source = w.name AND w.enabled = 1
            WHERE a.publish_date >= ?
            ORDER BY site_priority ASC, a.id DESC
            LIMIT ?
        ''', (date_from, max_count))
    
    results = []
    for row in cursor.fetchall():
        results.append({
            'id': row[0],
            'title': row[1],
            'source': row[2],
            'publish_date': row[3],
            'summary': row[4],
            'content': row[5],
            'url': row[6],
            'keywords': row[7],
            'priority': row[8]
        })
    
    conn.close()
    return results


def mark_new_flag():
    """
    标记最新抓取的新闻（new_flag=1）
    用于标识最近一次抓取的新数据
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 先清除旧的 new_flag
    cursor.execute('UPDATE articles SET new_flag = 0 WHERE new_flag = 1')
    
    # 标记最近 1 小时内创建的数据
    cursor.execute('''
        UPDATE articles 
        SET new_flag = 1 
        WHERE created_at >= datetime('now', '-1 hour')
        AND new_flag = 0
    ''')
    
    updated = cursor.rowcount
    conn.commit()
    conn.close()
    
    return updated


def update_keywords_for_new(date_from=None, max_keywords=5):
    """
    更新新闻关键词（仅处理 new_flag=1 或最近 2 天的数据）
    
    Args:
        date_from: 起始日期
        max_keywords: 每条新闻最多关键词数
    
    Returns:
        int: 更新数量
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if date_from is None:
        date_from = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')
    
    # 加载系统关键词
    cursor.execute('SELECT keyword, category, weight FROM system_keywords')
    keyword_dict = {
        row[0]: {'category': row[1], 'weight': row[2]} 
        for row in cursor.fetchall()
    }
    
    # 获取需要更新的新闻（new_flag=1 或最近 2 天且关键词为空）
    cursor.execute('''
        SELECT id, title, summary
        FROM articles
        WHERE (new_flag = 1 OR publish_date >= ?)
        AND (keywords IS NULL OR keywords = '')
        ORDER BY publish_date DESC
    ''', (date_from,))
    
    news_list = cursor.fetchall()
    updated = 0
    
    for news in news_list:
        news_id, title, summary = news
        text = title + ' ' + (summary or '')
        
        # 匹配关键词并计算得分
        matched = []
        for kw, info in keyword_dict.items():
            count = text.count(kw)
            if count > 0:
                title_bonus = 2 if kw in title else 1
                score = info['weight'] * count * title_bonus
                matched.append((kw, score))
        
        # 按得分排序，取前 N 个
        matched.sort(key=lambda x: x[1], reverse=True)
        top_keywords = [kw for kw, _ in matched[:max_keywords]]
        
        # 更新
        if top_keywords:
            keywords_str = ', '.join(top_keywords)
            cursor.execute('''
                UPDATE articles 
                SET keywords = ?, keyword_updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (keywords_str, news_id))
            updated += 1
    
    conn.commit()
    conn.close()
    
    return updated
