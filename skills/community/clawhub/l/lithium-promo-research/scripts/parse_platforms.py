#!/usr/bin/env python3
"""
抓取平台详情页并提取结构化数据
支持从搜索结果中提取平台信息
"""

import json
import sys
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse


def extract_platform_info(html_content, source_url, country_hint="", type_hint=""):
    """
    从HTML内容中提取平台信息
    这是一个简化版本，实际使用时需要更复杂的解析逻辑
    """
    platform = {
        "country": country_hint,
        "platform_type": type_hint,
        "source_url": source_url,
        "discovered_at": datetime.now().isoformat(),
    }
    
    # 提取标题（通常是页面标题或h1）
    title_match = re.search(r'<title>(.*?)</title>', html_content, re.IGNORECASE | re.DOTALL)
    if title_match:
        platform["platform_name"] = title_match.group(1).strip()
    
    # 提取描述（meta description）
    desc_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\'](.*?)["\']', 
                           html_content, re.IGNORECASE | re.DOTALL)
    if desc_match:
        platform["notes"] = desc_match.group(1).strip()
    
    # 提取网站链接
    url_match = re.search(r'href=["\'](https?://[^"\']+)["\']', html_content)
    if url_match:
        platform["website"] = url_match.group(1)
    else:
        platform["website"] = source_url
    
    return platform


def parse_from_search_results(results_file, output_file=None):
    """
    解析搜索结果，提取平台信息
    
    Args:
        results_file: 搜索结果JSON文件
        output_file: 输出文件路径
    """
    with open(results_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    platforms = []
    
    # 这里简化处理，实际应该从搜索结果中提取链接并抓取
    # 现在使用模拟数据演示结构
    for task in data.get("tasks", []):
        # 模拟提取一个平台
        platform = {
            "country": task["country"],
            "platform_type": task["type"],
            "platform_name": f"{task['country']} {task['type'].title()} Platform",
            "website": task["search_url"],
            "source_url": task["search_url"],
            "discovered_at": datetime.now().isoformat(),
            "influence_score": 5,  # 默认中等
            "audience_type": "待调研",
            "matching_products": [],
            "promo_form": "待调研",
            "price_range": "待询价",
            "language": "待确认",
            "contact_info": "待收集",
            "notes": f"从搜索任务提取: {task['query']}",
        }
        platforms.append(platform)
    
    output_data = {
        "generated_at": datetime.now().isoformat(),
        "total_platforms": len(platforms),
        "platforms": platforms,
    }
    
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = Path(__file__).parent.parent / "data"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"platforms_raw_{timestamp}.json"
    else:
        output_file = Path(output_file)
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"平台数据已保存: {output_file}")
    print(f"共提取 {len(platforms)} 个平台")
    
    return output_file


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="解析平台详情")
    parser.add_argument("input", help="搜索结果JSON文件")
    parser.add_argument("--output", default=None, help="输出文件路径")
    
    args = parser.parse_args()
    
    if not Path(args.input).exists():
        print(f"错误: 输入文件不存在: {args.input}")
        return 1
    
    parse_from_search_results(args.input, args.output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
