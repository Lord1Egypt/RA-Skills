# -*- coding: utf-8 -*-
"""
配置文件 v2 - 从数据库读取配置
"""

import sqlite3
from datetime import datetime
import os

# ============================================================
# 数据库配置
# ============================================================
# 支持环境变量覆盖，默认当前目录下的 news.db
DB_PATH = os.environ.get('NEWS_DIGEST_DB', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'news.db'))
# 配置表已合并到 news.db，不再使用单独的 config_db

# ============================================================
# 从数据库加载配置
# ============================================================
def load_websites():
    """从数据库加载监测网站列表，按优先级排序"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, name, url, selector, category, priority
            FROM monitor_websites 
            WHERE enabled = 1
            ORDER BY priority, category, id
        ''')
        websites = []
        for row in cursor.fetchall():
            websites.append({
                'id': row[0],
                'name': row[1],
                'url': row[2],
                'selector': row[3],
                'category': row[4],
                'priority': row[5] if len(row) > 5 else 3
            })
        conn.close()
        return websites
    except Exception as e:
        print(f"加载网站配置失败：{e}")
        return get_default_websites()

def load_keywords():
    """从数据库加载系统关键词"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT keyword, category, weight 
            FROM system_keywords 
            WHERE enabled = 1
            ORDER BY weight DESC, keyword
        ''')
        keywords = {'core': [], 'auxiliary': []}
        for row in cursor.fetchall():
            kw, category, weight = row
            if category == 'core':
                keywords['core'].append(kw)
            elif category == 'auxiliary':
                keywords['auxiliary'].append(kw)
        conn.close()
        return keywords
    except Exception as e:
        print(f"加载关键词配置失败：{e}")
        return get_default_keywords()

def get_default_websites():
    """默认网站列表（备用）"""
    return [
        {"name": "中国经济网", "url": "http://www.ce.cn/", "selector": "a", "category": "财经"},
        {"name": "新华网科技", "url": "http://www.news.cn/tech/kjkx/index.html", "selector": "a", "category": "科技"},
        {"name": "人民网头条", "url": "http://www.people.com.cn/GB/59476/index.html", "selector": "a", "category": "综合"},
    ]

def get_default_keywords():
    """默认关键词（备用）"""
    return {
        'core': ['产业', '政策', '经济', '科技', '创新'],
        'auxiliary': ['发展', '市场', '企业']
    }

# 初始化配置
WEBSITES = load_websites()
KEYWORDS_CONFIG = load_keywords()
CORE_KEYWORDS = KEYWORDS_CONFIG['core']
AUXILIARY_KEYWORDS = KEYWORDS_CONFIG['auxiliary']

# ============================================================
# 输出配置
# ============================================================
MAX_OUTPUT_COUNT = 50  # 最大输出条数
SIMILARITY_THRESHOLD = 0.90  # 相似度阈值

# ============================================================
# 2026 年中国法定节假日
# ============================================================
HOLIDAYS_2026 = [
    "2026-01-01",
    "2026-02-17", "2026-02-18", "2026-02-19", "2026-02-20", "2026-02-21", "2026-02-22", "2026-02-23",
    "2026-04-05", "2026-04-06", "2026-04-07",
    "2026-05-01", "2026-05-02", "2026-05-03", "2026-05-04", "2026-05-05",
    "2026-06-19", "2026-06-20", "2026-06-21",
    "2026-09-25", "2026-09-26", "2026-09-27",
    "2026-10-01", "2026-10-02", "2026-10-03", "2026-10-04", "2026-10-05", "2026-10-06", "2026-10-07", "2026-10-08",
]

# ============================================================
# HTTP 请求头
# ============================================================
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

# ============================================================
# 来源映射
# ============================================================
SOURCE_MAP = {
    # 新华网子频道统一归并为新华网
    '新华网': '新华网', '新华能源': '新华网', '新华科创': '新华网',
    '新华时政': '新华网', '新华汽车': '新华网', '新华社': '新华网',
    # 其他权威来源
    '中国经济网': '中国经济网', '经济日报': '经济日报',
    '人民网': '人民网', '央广网': '央广网',
    '大皖新闻': '大皖新闻', '中安在线': '中安在线',
    '科技日报': '科技日报', '中国科技网': '中国科技网',
    '中国产业经济信息网': '中国产业经济信息网',
    '中国工信新闻网': '中国工信新闻网', '中国工业新闻网': '中国工业新闻网',
    '中宏网': '中宏网', '科学网': '科学网',
    '36 氪': '36 氪', '钛媒体': '钛媒体', '科创版日报': '科创版日报',
    '中国产经网': '中国产经网', '中国工信网': '中国工信网',
}

# ============================================================
# 输出渠道配置
# ============================================================
OUTPUT_CHANNELS = {
    'feishu_personal': '.feishu-message-out.md',
    'feishu_group': '.feishu-group-message-out.md',
    'desktop': 'Desktop',
}

# ============================================================
# LLM 摘要配置
# ============================================================
USE_LLM_SUMMARY = False  # 方案 A 已关闭，改用方案 B（输出前批量总结）
LLM_MAX_LENGTH = 300     # 每条摘要最大字数
LLM_BATCH_SIZE = 50      # 批量总结的新闻条数（与 MAX_OUTPUT_COUNT 一致）

# ============================================================
# 跨天去重配置
# ============================================================
CROSS_DAY_DEDUP_ENABLED = True    # 是否启用跨天去重
CROSS_DAY_HISTORY_DAYS = 3        # 历史摘要窗口天数
CROSS_DAY_THRESHOLD = 0.75        # 拦截阈值（≥此值直接拦截）
CROSS_DAY_WARN_THRESHOLD = 0.60   # 警告阈值（0.60-0.75 保留但打印日志）
