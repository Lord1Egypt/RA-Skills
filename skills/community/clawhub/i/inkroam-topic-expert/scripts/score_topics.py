#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
选题打分脚本
根据热度、相关度、时效性、可写性、差异化进行综合评分
"""

import json
import sys
import argparse
from datetime import datetime


def calculate_hot_score(hot_value, source):
    """计算热度分（满分30）"""
    if source == "weibo":
        # 微博热度通常在几万到几百万
        if hot_value > 1000000:
            return 30
        elif hot_value > 500000:
            return 25
        elif hot_value > 100000:
            return 20
        else:
            return 15
    elif source == "zhihu":
        # 知乎热度文本格式，简单给分
        return 20
    else:
        return 15


def calculate_relevance_score(title, keywords):
    """计算相关度分（满分25）"""
    # AI 资讯类账号的关键词
    ai_keywords = {
        "核心词": ["AI", "人工智能", "ChatGPT", "GPT", "Claude", "OpenAI", "大模型", "机器学习", "深度学习"],
        "工具词": ["效率", "工具", "自动化", "提示词", "prompt", "应用"],
        "行业词": ["科技", "互联网", "创业", "产品", "技术"]
    }
    
    score = 0
    title_lower = title.lower()
    
    # 核心词匹配（每个10分，最多20分）
    for keyword in ai_keywords["核心词"]:
        if keyword.lower() in title_lower:
            score += 10
            if score >= 20:
                return 25  # 有核心词直接给高分
    
    # 工具词匹配（每个5分）
    for keyword in ai_keywords["工具词"]:
        if keyword.lower() in title_lower:
            score += 5
    
    # 行业词匹配（每个3分）
    for keyword in ai_keywords["行业词"]:
        if keyword.lower() in title_lower:
            score += 3
    
    return min(score, 25)


def calculate_timeliness_score():
    """计算时效性分（满分20）"""
    # 所有热榜数据都是实时的，给满分
    return 20


def calculate_writability_score(title, excerpt=""):
    """计算可写性分（满分15）"""
    # 标题长度适中
    if 10 <= len(title) <= 30:
        score = 10
    else:
        score = 5
    
    # 有摘要加分
    if excerpt:
        score += 5
    
    return min(score, 15)


def calculate_differentiation_score(title):
    """计算差异化分（满分10）"""
    # 简单判断：包含数字、问号等更有差异化
    score = 5
    
    if any(char.isdigit() for char in title):
        score += 2
    if "？" in title or "?" in title:
        score += 2
    if "如何" in title or "怎么" in title:
        score += 1
    
    return min(score, 10)


def score_topic(topic, account_type="AI工具/效率"):
    """对单个选题打分"""
    title = topic.get("title", "")
    source = topic.get("source", "")
    hot = topic.get("hot", 0)
    excerpt = topic.get("excerpt", "")
    
    # 计算各维度分数
    hot_score = calculate_hot_score(hot, source)
    relevance_score = calculate_relevance_score(title, account_type)
    timeliness_score = calculate_timeliness_score()
    writability_score = calculate_writability_score(title, excerpt)
    differentiation_score = calculate_differentiation_score(title)
    
    total_score = (
        hot_score +
        relevance_score +
        timeliness_score +
        writability_score +
        differentiation_score
    )
    
    return {
        "title": title,
        "url": topic.get("url", ""),
        "source": source,
        "rank": topic.get("rank", 0),
        "excerpt": excerpt,
        "scores": {
            "hot": hot_score,
            "relevance": relevance_score,
            "timeliness": timeliness_score,
            "writability": writability_score,
            "differentiation": differentiation_score,
            "total": total_score
        }
    }


def main():
    parser = argparse.ArgumentParser(description="选题打分")
    parser.add_argument("--hot-data", default="/tmp/hot_topics.json", help="热点数据文件")
    parser.add_argument("--account-type", default="AI工具/效率", help="账号类型")
    parser.add_argument("--min-score", type=int, default=70, help="最低分数")
    
    args = parser.parse_args()
    
    # 读取热点数据
    with open(args.hot_data, 'r', encoding='utf-8') as f:
        hot_data = json.load(f)
    
    # 合并所有来源的数据
    all_topics = []
    for source in ["weibo", "zhihu", "36kr", "jiqizhixin"]:
        all_topics.extend(hot_data.get(source, []))
    
    # 打分
    scored_topics = []
    for topic in all_topics:
        scored = score_topic(topic, args.account_type)
        if scored["scores"]["total"] >= args.min_score:
            scored_topics.append(scored)
    
    # 按分数排序
    scored_topics.sort(key=lambda x: x["scores"]["total"], reverse=True)
    
    # 输出结果
    result = {
        "timestamp": datetime.now().isoformat(),
        "total_topics": len(all_topics),
        "qualified_topics": len(scored_topics),
        "min_score": args.min_score,
        "topics": scored_topics[:10]  # 只返回前10个
    }
    
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 保存到文件
    output_file = "/tmp/scored_topics.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 打分完成：{len(scored_topics)} 个选题达标（≥{args.min_score}分）", file=sys.stderr)
    print(f"数据已保存到：{output_file}", file=sys.stderr)


if __name__ == '__main__':
    main()
