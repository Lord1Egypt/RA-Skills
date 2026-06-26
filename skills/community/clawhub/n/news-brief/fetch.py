#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fetch.py
从权威媒体抓取指定分类新闻（Serper API）
"""

import logging
import os
import re
import time
import requests
from datetime import datetime

# ============================================================
# 分类 → Serper搜索词映射（只用权威媒体）
# ============================================================
CATEGORY_QUERIES = {
    "时政": {
        "queries": [
            "government policy politics news site:reuters.com OR site:apnews.com OR site:xinhuanet.com",
            "国家政策 政府 外交 site:xinhuanet.com OR site:people.com.cn",
        ],
        "sources_en": ["Reuters", "AP News", "BBC"],
        "sources_cn": ["新华社", "人民网"],
    },
    "经济": {
        "queries": [
            "economy finance market news site:bloomberg.com OR site:reuters.com OR site:ft.com",
            "经济 金融 股市 site:cls.cn OR site:yicai.com",
        ],
        "sources_en": ["Bloomberg", "Reuters", "Financial Times"],
        "sources_cn": ["财联社", "第一财经"],
    },
    "社会": {
        "queries": [
            "society social news site:bbc.com OR site:cnn.com OR site:apnews.com",
            "社会 民生 突发 site:thepaper.cn OR site:nandu.com",
        ],
        "sources_en": ["BBC", "CNN", "AP News"],
        "sources_cn": ["澎湃新闻", "南方都市报"],
    },
    "国际": {
        "queries": [
            "international world news site:reuters.com OR site:apnews.com OR site:bbc.com",
            "国际 外交 冲突 site:huanqiu.com OR site:cankaoxiaoxi.com",
        ],
        "sources_en": ["Reuters", "AP News", "BBC"],
        "sources_cn": ["环球时报", "参考消息"],
    },
    "科技": {
        "queries": [
            "technology AI industry news site:techcrunch.com OR site:theverge.com OR site:wired.com",
            "科技 人工智能 互联网 site:36kr.com OR site:huxiu.com",
        ],
        "sources_en": ["TechCrunch", "The Verge", "Wired"],
        "sources_cn": ["36氪", "虎嗅"],
    },
    "体育": {
        "queries": [
            "sports news site:espn.com OR site:bbc.com/sport OR site:reuters.com/sports",
            "体育 赛事 足球 篮球 site:dongqiudi.com OR site:sports.qq.com",
        ],
        "sources_en": ["ESPN", "BBC Sport", "Reuters Sports"],
        "sources_cn": ["懂球帝", "腾讯体育"],
    },
    "文娱": {
        "queries": [
            "entertainment film music news site:variety.com OR site:hollywoodreporter.com",
            "娱乐 电影 音乐 综艺 site:yulezibenlun.com OR site:ent.163.com",
        ],
        "sources_en": ["Variety", "Hollywood Reporter"],
        "sources_cn": ["娱乐资本论", "网易娱乐"],
    },
    "军事": {
        "queries": [
            "military defense security news site:defensenews.com OR site:reuters.com OR site:janes.com",
            "军事 国防 武器 site:guancha.cn OR site:81.cn",
        ],
        "sources_en": ["Defense News", "Reuters", "Jane's"],
        "sources_cn": ["观察者网", "解放军报"],
    },
    "教育": {
        "queries": [
            "education university research news site:timeshighereducation.com OR site:reuters.com",
            "教育 高考 大学 政策 site:jyb.cn OR site:edu.cn",
        ],
        "sources_en": ["Times Higher Education", "Reuters"],
        "sources_cn": ["中国教育报", "教育部官网"],
    },
    "法治": {
        "queries": [
            "law legal court justice news site:reuters.com OR site:apnews.com",
            "法律 司法 案件 反腐 site:legaldaily.com.cn OR site:court.gov.cn",
        ],
        "sources_en": ["Reuters Legal", "AP News"],
        "sources_cn": ["法制日报", "最高人民法院"],
    },
    "环境": {
        "queries": [
            "environment climate ecology news site:theguardian.com OR site:reuters.com",
            "环境 气候 生态 自然 site:caixin.com/environment OR site:cenews.com.cn",
        ],
        "sources_en": ["The Guardian", "Reuters"],
        "sources_cn": ["财新环境", "中国环境报"],
    },
    "农业": {
        "queries": [
            "agriculture food farming news site:reuters.com OR site:bloomberg.com",
            "农业 农村 粮食 乡村振兴 site:farmer.com.cn OR site:agri.cn",
        ],
        "sources_en": ["Reuters Agriculture", "Bloomberg"],
        "sources_cn": ["农民日报", "农业农村部"],
    },
}

# 过滤掉的非新闻URL特征（聚合页/话题页）
EXCLUDE_URL_PATTERNS = [
    r"/hub/", r"/topic/", r"/tag/", r"/category/",
    r"/search\?", r"/topics/", r"/section/",
]


def _serper_search(query: str, serper_key: str, num: int = 10,
                   time_range: str = "24h") -> list:
    """单次 Serper 搜索，返回新闻列表"""
    # tbs: qdr:d=24小时, qdr:2d=48小时
    tbs = "qdr:d" if time_range == "24h" else "qdr:2d"
    for attempt in range(3):
        try:
            resp = requests.post(
                "https://google.serper.dev/news",
                headers={"X-API-KEY": serper_key, "Content-Type": "application/json"},
                json={"q": query, "gl": "us", "hl": "en", "num": num, "tbs": tbs},
                timeout=15,
            )
            resp.raise_for_status()
            return resp.json().get("news", [])
        except Exception as e:
            logging.warning(f"  Serper第{attempt+1}次失败: {e}")
            if attempt == 2:
                return []
            time.sleep(2)
    return []


def _is_valid_url(url: str) -> bool:
    """排除聚合页/话题页"""
    for pat in EXCLUDE_URL_PATTERNS:
        if re.search(pat, url):
            return False
    return True


def _is_valid_title(title: str) -> bool:
    """排除问句/分析文章/单词标题"""
    if len(title) < 8:
        return False
    bad_starts = ["为什么", "如何", "什么是", "会发生什么", "How ", "Why ", "What is"]
    for s in bad_starts:
        if title.startswith(s):
            return False
    return True


def fetch_category(category: str, count: int, serper_key: str,
                   deepseek_key: str, time_range: str = "24h") -> list:
    """
    抓取指定分类新闻
    返回：[{title, desc, source, url, date, region}, ...]
    """
    cfg = CATEGORY_QUERIES.get(category)
    if not cfg:
        logging.error(f"未知分类: {category}")
        return []

    logging.info(f"  📡 抓取「{category}」（时间范围：{time_range}）...")

    seen_urls, raw_items = set(), []

    for query in cfg["queries"]:
        results = _serper_search(query, serper_key, num=10, time_range=time_range)
        for n in results:
            url = n.get("link", "")
            if not url or url in seen_urls:
                continue
            if not _is_valid_url(url):
                continue
            title = n.get("title", "")
            if not _is_valid_title(title):
                continue
            seen_urls.add(url)
            # 判断是国内还是国际来源
            source = n.get("source", "")
            region = "domestic" if any(
                s in source for s in cfg["sources_cn"]
            ) else "international"
            raw_items.append({
                "title":  title,
                "desc":   n.get("snippet", ""),
                "source": source,
                "url":    url,
                "date":   n.get("date", ""),
                "region": region,
                "category": category,
            })

        if len(raw_items) >= count * 2:
            break

    logging.info(f"     原始 {len(raw_items)} 条 → 时效验证中...")

    # DeepSeek 时效验证 + 翻译 + 结构化
    if raw_items:
        raw_items = _verify_and_enrich(raw_items[:count * 2], deepseek_key, category)

    return raw_items[:count]


def _verify_and_enrich(items: list, deepseek_key: str, category: str) -> list:
    """
    一次 API 调用完成：时效验证 + 翻译 + 结构化（出处/时间/地点/内容）
    """
    today = datetime.now().strftime("%Y年%m月%d日")
    news_list = "\n".join([
        f"[{i+1}] 标题:{it['title']} | 来源:{it['source']} | 日期:{it['date']} | URL:{it['url']}"
        for i, it in enumerate(items)
    ])

    prompt = (
        f"今天是{today}，分类是「{category}」。\n\n"
        f"对以下新闻条目进行处理，筛选并结构化。\n\n"
        f"筛选规则（同时满足才保留）：\n"
        f"1. 是过去48小时内的真实新闻事件\n"
        f"2. 标题是具体事件陈述，不是问句/分析文章/观点评论\n"
        f"3. 来源是知名新闻媒体，不是智库/公关稿/博客\n\n"
        f"对保留的每条新闻输出：\n"
        f"- id: 原始序号\n"
        f"- title_cn: 中文标题（已是中文则保留，英文则翻译）\n"
        f"- source_cn: 来源中文名（Reuters→路透社，Bloomberg→彭博社，BBC→BBC，等）\n"
        f"- pub_time: 发布日期，格式YYYY/M/D\n"
        f"- location: 事件发生地（国家或城市，不明则'国际'）\n"
        f"- content: 1-2句中文摘要，包含主体+事件+影响\n\n"
        f"只输出JSON数组，不加说明：\n"
        f"[{{\"id\":1,\"title_cn\":\"\",\"source_cn\":\"\",\"pub_time\":\"\",\"location\":\"\",\"content\":\"\"}}]\n\n"
        f"新闻列表：\n{news_list}"
    )

    try:
        resp = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {deepseek_key}", "Content-Type": "application/json"},
            json={"model": "deepseek-chat", "messages": [{"role": "user", "content": prompt}],
                  "max_tokens": 2000, "temperature": 0.1},
            timeout=30,
        )
        resp.raise_for_status()
        raw = resp.json()["choices"][0]["message"]["content"].strip()
        raw = re.sub(r"```json\s*|```\s*", "", raw).strip()
        m = re.search(r"\[.*\]", raw, re.DOTALL)
        if not m:
            return items
        enriched = {}
        for d in __import__("json").loads(m.group(0)):
            enriched[d["id"]] = d

        result = []
        for i, it in enumerate(items):
            e = enriched.get(i + 1)
            if not e:
                continue  # 被筛掉
            it["title"]     = e.get("title_cn") or it["title"]
            it["source_cn"] = e.get("source_cn") or it["source"]
            it["pub_time"]  = e.get("pub_time", "")
            it["location"]  = e.get("location", "")
            it["content"]   = e.get("content") or it["desc"]
            result.append(it)

        logging.info(f"     验证通过 {len(result)} 条")
        return result

    except Exception as e:
        logging.warning(f"  验证/结构化失败({e})，返回原始数据")
        return items


def fetch_all(categories: list, news_per_category: int,
              serper_key: str, deepseek_key: str,
              time_range: str = "24h") -> dict:
    """
    抓取所有分类新闻
    返回：{category: [items...]}
    """
    result = {}
    for cat in categories[:3]:  # 最多3类
        items = fetch_category(cat, news_per_category, serper_key,
                               deepseek_key, time_range)
        result[cat] = items
        logging.info(f"  ✅ 「{cat}」完成，共 {len(items)} 条")
    return result
