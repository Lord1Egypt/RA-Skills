#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测绘/GIS 校招信息搜索脚本
用于搜索和整理测绘类、GIS 专业的招聘信息
"""

import json
import sys
import argparse
from datetime import datetime, timedelta

# 搜索关键词配置
SEARCH_KEYWORDS = [
    "测绘工程 校园招聘 2026",
    "地理信息系统 GIS 本科 招聘",
    "遥感科学与技术 校招",
    "自然资源部 事业单位招聘",
    "测绘院 招聘 应届",
    "国土空间规划 招聘",
    "测绘工程师 国企 2026",
    "GIS 开发 大厂 校招",
]

# 目标网站
TARGET_SITES = [
    "gpxd.iguopin.com",  # 国聘网
    "www.iguopin.com",
    "www.zhaopin.com",
    "www.51job.com",
    "www.zhipin.com",
]

# 优先级单位关键词
PRIORITY_KEYWORDS = {
    "国央企": ["中铁", "中建", "中交", "中国电建", "中国能建", "国家电网", "中国石油", "中国石化", "测绘科学研究院", "自然资源部"],
    "事业单位": ["测绘院", "地理信息局", "事业单位", "事业编"],
    "大厂": ["超图", "航天宏图", "中科星图", "百度", "阿里", "腾讯", "华为", "高德", "美团", "滴滴"],
}


def search_jobs(keyword, days=30):
    """
    搜索招聘信息（模拟函数，实际需要调用 web_search API）
    
    Args:
        keyword: 搜索关键词
        days: 最近 N 天的信息
    
    Returns:
        list: 搜索结果列表
    """
    # 这是一个示例实现，实际使用时需要调用 OpenClaw 的 web_search 工具
    # 这里返回示例数据结构
    
    sample_jobs = [
        {
            "title": "测绘工程师（应届）",
            "company": "中国测绘科学研究院",
            "priority": "国央企",
            "degree": "本科及以上",
            "major": "测绘工程、遥感、地理信息系统",
            "deadline": "2026-04-30",
            "location": "北京",
            "url": "https://gpxd.iguopin.com/example1",
            "publish_date": datetime.now().strftime("%Y-%m-%d"),
        },
        {
            "title": "GIS 开发工程师",
            "company": "超图软件",
            "priority": "大厂",
            "degree": "本科",
            "major": "地理信息系统、计算机科学与技术",
            "deadline": "2026-04-15",
            "location": "北京",
            "url": "https://supermap.zhiye.com/example2",
            "publish_date": (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d"),
        },
    ]
    
    return sample_jobs


def filter_jobs(jobs, degree="本科", priority_order=None):
    """
    筛选和排序岗位
    
    Args:
        jobs: 岗位列表
        degree: 学历要求
        priority_order: 优先级顺序 ["国央企", "事业单位", "大厂", "其他"]
    
    Returns:
        list: 筛选后的岗位列表
    """
    if priority_order is None:
        priority_order = ["国央企", "事业单位", "大厂", "其他"]
    
    # 按优先级排序
    def get_priority(job):
        priority = job.get("priority", "其他")
        try:
            return priority_order.index(priority)
        except ValueError:
            return len(priority_order)
    
    filtered = sorted(jobs, key=get_priority)
    return filtered


def format_output(jobs, date=None):
    """
    格式化输出结果
    
    Args:
        jobs: 岗位列表
        date: 日期字符串
    
    Returns:
        str: 格式化的输出文本
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    output = f"【测绘/GIS 校招】{date} 共 {len(jobs)} 岗\n\n"
    
    for i, job in enumerate(jobs, 1):
        priority_icon = {
            "国央企": "🏛️",
            "事业单位": "🏢",
            "大厂": "💼",
            "其他": "📌",
        }.get(job.get("priority", "其他"), "📌")
        
        output += f"{i}. {priority_icon} **{job.get('company', '未知单位')}**\n"
        output += f"   岗位：{job.get('title', '未知')}\n"
        output += f"   学历：{job.get('degree', '不限')}\n"
        output += f"   专业：{job.get('major', '不限')}\n"
        output += f"   地点：{job.get('location', '不限')}\n"
        output += f"   截止：{job.get('deadline', '详见官网')}\n"
        output += f"   发布：{job.get('publish_date', '未知')}\n"
        output += f"   链接：{job.get('url', '#')}\n\n"
    
    return output


def save_to_file(content, filepath):
    """保存结果到文件"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)


def main():
    parser = argparse.ArgumentParser(description='测绘/GIS 校招信息搜索')
    parser.add_argument('--keyword', type=str, default='测绘', help='搜索关键词')
    parser.add_argument('--degree', type=str, default='本科', help='学历要求')
    parser.add_argument('--days', type=int, default=30, help='最近 N 天的信息')
    parser.add_argument('--output', type=str, default=None, help='输出文件路径')
    
    args = parser.parse_args()
    
    # 执行搜索
    all_jobs = []
    for keyword in SEARCH_KEYWORDS:
        if args.keyword.lower() in keyword.lower() or args.keyword == '测绘':
            jobs = search_jobs(keyword, days=args.days)
            all_jobs.extend(jobs)
    
    # 去重（按公司 + 岗位名称）
    seen = set()
    unique_jobs = []
    for job in all_jobs:
        key = f"{job.get('company', '')}-{job.get('title', '')}"
        if key not in seen:
            seen.add(key)
            unique_jobs.append(job)
    
    # 筛选和排序
    filtered_jobs = filter_jobs(unique_jobs, degree=args.degree)
    
    # 格式化输出
    output = format_output(filtered_jobs)
    
    # 输出或保存
    if args.output:
        save_to_file(output, args.output)
        print(f"结果已保存到：{args.output}")
    else:
        print(output)
    
    # 返回 JSON 格式供其他程序使用
    if '--json' in sys.argv:
        print(json.dumps(filtered_jobs, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
