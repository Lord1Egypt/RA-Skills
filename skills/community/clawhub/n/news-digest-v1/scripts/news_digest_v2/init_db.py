# -*- coding: utf-8 -*-
"""
数据库初始化脚本
功能：自动建表 + 插入示例网站 + 示例关键词
运行：python scripts/news_digest_v2/init_db.py
"""

import sqlite3
import os
import sys

# 支持环境变量覆盖数据库路径
DB_PATH = os.environ.get('NEWS_DIGEST_DB', 'news.db')

# 如果运行在 skill 目录下，自动加上路径
if not os.path.isabs(DB_PATH):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(script_dir, '..', '..', '..', DB_PATH)
    # 简化路径
    DB_PATH = os.path.normpath(DB_PATH)


def init_tables(conn):
    """创建数据库表"""
    cursor = conn.cursor()
    
    # articles 表
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
    
    # monitor_websites 表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS monitor_websites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            url TEXT NOT NULL,
            selector TEXT DEFAULT 'a',
            category TEXT,
            priority INTEGER DEFAULT 3,
            enabled INTEGER DEFAULT 1
        )
    ''')
    
    # system_keywords 表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_keywords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT UNIQUE NOT NULL,
            category TEXT,
            weight INTEGER DEFAULT 1,
            enabled INTEGER DEFAULT 1
        )
    ''')
    
    # digest_output 表（LLM 总结用）
    cursor.execute('''
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
    
    # 创建索引
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_publish_date ON articles(publish_date)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_keywords ON articles(keywords)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_is_duplicate ON articles(is_duplicate)')
    
    conn.commit()
    print('  OK: 表结构创建完成')


def seed_websites(conn):
    """插入示例网站"""
    cursor = conn.cursor()
    
    sites = [
        # 优先级 1：主流官方媒体
        ('人民网', 'http://www.people.com.cn/GB/59476/index.html', 'a', '综合', 1),
        ('新华网科技', 'http://www.news.cn/tech/kjkx/index.html', 'a', '科技', 1),
        ('经济日报', 'http://www.ce.cn/xwzx/gnsz/gdxw/', 'a', '财经', 1),
        ('央广网', 'https://www.cnr.cn/xmfw/jdt/', 'a', '综合', 1),
        ('科技日报', 'https://www.stdaily.com/web/gdxw/', 'a', '科技', 1),
        
        # 优先级 2：财经/产业
        ('中国经济网', 'http://www.ce.cn/', 'a', '财经', 2),
        ('中宏网', 'https://www.zhonghongwang.com/', 'a', '经济', 2),
        ('36 氪', 'https://36kr.com/newsflashes', 'a', '科技', 2),
        
        # 优先级 3：地方/行业
        ('大皖新闻', 'http://www.ahwang.cn/', 'a', '地方', 3),
        ('中国科技网', 'https://www.stdaily.com/web/gdxw/', 'a', '科技', 3),
    ]
    
    added = 0
    for name, url, selector, category, priority in sites:
        cursor.execute('''
            INSERT OR IGNORE INTO monitor_websites 
            (name, url, selector, category, priority, enabled)
            VALUES (?, ?, ?, ?, ?, 1)
        ''', (name, url, selector, category, priority))
        if cursor.rowcount > 0:
            added += 1
    
    conn.commit()
    print(f'  OK: 已添加 {added} 个示例网站（跳过 {len(sites) - added} 个已存在的）')


def seed_keywords(conn):
    """插入示例关键词"""
    cursor = conn.cursor()
    
    keywords = [
        # 核心关键词（高权重）
        ('产业', 'core', 5),
        ('政策', 'core', 5),
        ('经济', 'core', 4),
        ('科技', 'core', 4),
        ('创新', 'core', 4),
        ('数字经济', 'core', 5),
        ('人工智能', 'core', 5),
        ('新能源', 'core', 5),
        ('智能制造', 'core', 4),
        ('数字经济', 'core', 5),
        
        # 辅助关键词
        ('发展', 'auxiliary', 2),
        ('市场', 'auxiliary', 2),
        ('企业', 'auxiliary', 2),
        ('技术', 'auxiliary', 2),
        ('投资', 'auxiliary', 2),
        ('增长', 'auxiliary', 2),
        ('改革', 'auxiliary', 2),
        ('监管', 'auxiliary', 3),
    ]
    
    added = 0
    for keyword, category, weight in keywords:
        cursor.execute('''
            INSERT OR IGNORE INTO system_keywords 
            (keyword, category, weight, enabled)
            VALUES (?, ?, ?, 1)
        ''', (keyword, category, weight))
        if cursor.rowcount > 0:
            added += 1
    
    conn.commit()
    print(f'  OK: 已添加 {added} 个关键词（跳过 {len(keywords) - added} 个已存在的）')


def main():
    print()
    print('=' * 60)
    print('  新闻摘要 - 数据库初始化')
    print('=' * 60)
    print()
    print(f'  数据库路径: {DB_PATH}')
    print()
    
    # 确保目录存在
    db_dir = os.path.dirname(DB_PATH)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)
        print(f'  创建目录: {db_dir}')
    
    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
    
    try:
        # 1. 建表
        print('[1/3] 创建数据库表...')
        init_tables(conn)
        
        # 2. 插入网站
        print()
        print('[2/3] 插入示例网站...')
        seed_websites(conn)
        
        # 3. 插入关键词
        print()
        print('[3/3] 插入示例关键词...')
        seed_keywords(conn)
        
        print()
        print('=' * 60)
        print('  初始化完成！')
        print('=' * 60)
        print()
        print('  下一步：运行 python scripts/news_digest_v2/run_all_stages.py')
        print()
        
    except Exception as e:
        print(f'\n  ERROR: {e}')
        sys.exit(1)
    finally:
        conn.close()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n  已取消')
        sys.exit(0)
