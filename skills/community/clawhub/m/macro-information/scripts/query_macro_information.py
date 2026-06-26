#!/usr/bin/env python3
"""
宏观经济资讯查询脚本 (Macro Information)

基于 FEEDAX API 的宏观经济资讯与舆情监测工具，提供全面的宏观经济数据查询能力。

支持查询：
- 经济数据：GDP、CPI、PPI、PMI、失业率等
- 货币政策：美联储、人民银行、降准降息等
- 财政政策：财政刺激、基建投资、减税政策等
- 国际贸易：中美贸易、关税政策、进出口数据等
- 金融市场：股市、债市、汇率、房地产等

用法:
    python query_macro_information.py --keyword "美联储" --macro-type 国际宏观 --days 7
    python query_macro_information.py --keyword "GDP" --macro-type 国内宏观 --days 14
    python query_macro_information.py --keyword "通胀" --sentiments 负面 --days 30

输出:
    - macro_information_<timestamp>.csv: 资讯结果 CSV 文件
    - macro_information_<timestamp>.md: 数据说明文件（含统计分布）

API Key 配置（三选一）:
    1. 命令行参数：--api-key "your-api-key"
    2. 环境变量：export FEEDAX_API_KEY="your-api-key"
    3. 配置文件：在 scripts/ 目录创建 config.json，内容为 {"api_key": "your-api-key"}
"""

import os
import sys
import json
import argparse
import requests
from datetime import datetime, timedelta


# FEEDAX API 配置
# API Key 需要通过以下方式之一提供：
# 1. 环境变量：export FEEDAX_API_KEY="your-api-key"
# 2. 命令行参数：--api-key "your-api-key"
# 3. 配置文件：在同目录创建 config.json，内容为 {"api_key": "your-api-key"}
FEEDAX_API_KEY = os.environ.get('FEEDAX_API_KEY', '')
FEEDAX_BASE_URL = "http://221.6.15.90:18011"


def query_macro_information(
    api_key: str,
    keyword: str,
    macro_type: str = None,
    sentiments: list = None,
    days: int = 7,
    page: int = 0,
    size: int = 20,
    sort_by: str = "publish_date",
    sort_type: str = "DESC"
):
    """
    查询宏观资讯
    
    Args:
        keyword: 搜索关键词
        macro_type: 宏观类型（国内宏观/国际宏观）
        sentiments: 情感倾向列表（正面/负面/中性）
        days: 查询天数（默认 7 天）
        page: 页码（从 0 开始）
        size: 每页数量
        sort_by: 排序字段
        sort_type: 排序类型（ASC/DESC）
    
    Returns:
        dict: API 响应数据
    """
    url = f"{FEEDAX_BASE_URL}/data-service/v1/news/macro/external/query?apiKey={api_key}"
    
    # 计算时间范围
    end_time = int(datetime.now().timestamp() * 1000)
    start_time = int((datetime.now() - timedelta(days=days)).timestamp() * 1000)
    
    # 构建请求体
    payload = {
        "endTime": end_time,
        "keyWordQuery": {
            "keyword": keyword,
            "queryFields": ["1", "2"]  # 1-正文，2-标题
        },
        "macroEconomyResul": [macro_type] if macro_type else [],
        "macroTags": [],
        "mediaTypes": [],
        "newsImportanceLevels": [],
        "pageNum": page,
        "pageSize": size,
        "sentiments": sentiments if sentiments else [],
        "sortBy": sort_by,
        "sortType": sort_type,
        "startTime": start_time
    }
    
    params = {"apiKey": api_key}
    
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key
    }
    
    try:
        response = requests.post(url, params=params, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求失败：{e}")
        sys.exit(1)


def generate_csv(data_list: list, output_path: str):
    """
    生成 CSV 文件
    
    包含 10 个必须展示字段：
    1. 新闻标题 2. 新闻摘要 3. 新闻内容 4. 新闻来源 5. 发布时间
    6. 宏观类型 7. 宏观事件标签 8. 涉及地区 9. 重要程度 10. 热度数据
    
    Args:
        data_list: 资讯数据数组
        output_path: 输出文件路径
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        # 写入表头（包含 10 个必须展示字段）
        headers = [
            "发布时间", "标题", "摘要", "内容", "来源", "宏观类型", "事件标签",
            "涉及地区", "重要程度", "热度得分", "浏览数", "转发数", "URL"
        ]
        f.write(','.join(headers) + '\n')
        
        # 写入数据行
        for item in data_list:
            # 格式化发布时间
            publish_date = item.get('publishDate', 0)
            if publish_date:
                publish_date_str = datetime.fromtimestamp(publish_date / 1000).strftime('%Y-%m-%d %H:%M')
            else:
                publish_date_str = ''
            
            row = [
                publish_date_str,
                item.get('title', '') or '',
                item.get('summary', '') or '',
                item.get('content', '') or '',
                item.get('source', '') or '',
                item.get('macroEconomyResult', '') or '',
                item.get('macroTag', '') or '',
                (item.get('areaResult') or ''),
                item.get('newsImportanceLevel', '') or '',
                str(item.get('heatScores', 0) or 0),
                str(item.get('viewNum', 0) or 0),
                str(item.get('forwardedNum', 0) or 0),
                item.get('url', '') or ''
            ]
            # 清理逗号
            row = [str(v).replace(',', ' ').replace('\n', ' ') for v in row]
            f.write(','.join(row) + '\n')
    
    print(f"CSV 文件已生成：{output_path}")


def generate_description(response: dict, output_path: str, keyword: str, macro_type: str, days: int):
    """
    生成数据说明文件
    
    Args:
        response: API 响应数据
        output_path: 输出文件路径
        keyword: 原始查询关键词
        macro_type: 宏观类型
        days: 查询天数
    """
    code = response.get('code', 0)
    message = response.get('message', '')
    total = response.get('total', 0)
    data = response.get('data', [])
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# 宏观资讯查询结果说明\n\n")
        f.write(f"**查询关键词**: {keyword}\n")
        if macro_type:
            f.write(f"**宏观类型**: {macro_type}\n")
        f.write(f"**查询时间范围**: 近 {days} 天\n")
        f.write(f"**数据日期**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**结果总数**: {total} 条\n")
        f.write(f"**接口状态**: code={code}, message={message}\n\n")
        
        # 宏观类型分布
        macro_count = {}
        for item in data:
            macro = item.get('macroEconomyResult', '未知')
            macro_count[macro] = macro_count.get(macro, 0) + 1
        
        f.write("## 宏观类型分布\n\n")
        for macro, count in macro_count.items():
            f.write(f"- {macro}: {count} 条\n")
        
        # 情感分布统计
        sentiment_count = {}
        for item in data:
            sentiment = item.get('sentiment', '未知')
            sentiment_count[sentiment] = sentiment_count.get(sentiment, 0) + 1
        
        f.write("\n## 情感分布\n\n")
        for sentiment, count in sentiment_count.items():
            f.write(f"- {sentiment}: {count} 条\n")
        
        # 重要程度分布
        importance_count = {}
        for item in data:
            level = item.get('newsImportanceLevel', '未知')
            importance_count[level] = importance_count.get(level, 0) + 1
        
        f.write("\n## 重要程度分布\n\n")
        for level, count in importance_count.items():
            f.write(f"- {level}: {count} 条\n")
        
        # 宏观事件标签统计
        f.write("\n## 宏观事件标签\n\n")
        tag_count = {}
        for item in data:
            tag = item.get('macroTag', '')
            if tag:
                tag_count[tag] = tag_count.get(tag, 0) + 1
        
        if tag_count:
            for tag, count in sorted(tag_count.items(), key=lambda x: x[1], reverse=True)[:15]:
                f.write(f"- {tag}: {count} 条\n")
            if len(tag_count) > 15:
                f.write(f"... 共 {len(tag_count)} 种标签\n")
        else:
            f.write("无事件标签数据\n")
        
        # 涉及地区统计
        f.write("\n## 涉及地区\n\n")
        areas = set()
        for item in data:
            area = item.get('areaResult', '')
            if area:
                areas.add(area)
        
        if areas:
            for area in list(areas)[:15]:
                f.write(f"- {area}\n")
            if len(areas) > 15:
                f.write(f"... 共 {len(areas)} 个地区\n")
        else:
            f.write("未识别到具体地区\n")
        
        # 数据来源说明
        f.write("\n## 数据来源\n\n")
        f.write("数据来自 FEEDAX 宏观资讯监测平台，涵盖新闻、微信公众号、微博等多种信源。\n")
        f.write("\n### 宏观类型说明\n")
        f.write("- **国内宏观**: 中国宏观经济相关政策、数据、事件\n")
        f.write("- **国际宏观**: 全球宏观经济、主要央行政策、国际经济事件\n")
        f.write("\n---\n")
        f.write(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    print(f"说明文件已生成：{output_path}")


def format_output(data_list: list, verbose: bool = False):
    """
    格式化输出结果到终端
    
    必须展示 10 个核心字段：
    1. 新闻标题 2. 新闻摘要 3. 新闻内容 4. 新闻来源 5. 发布时间
    6. 宏观类型 7. 宏观事件标签 8. 涉及地区 9. 重要程度 10. 热度数据
    
    Args:
        data_list: 资讯数据数组
        verbose: 是否显示详细内容
    """
    if not data_list:
        print("未找到相关资讯数据")
        return
    
    print(f"\n共找到 {len(data_list)} 条资讯:\n")
    print("=" * 80)
    
    for i, item in enumerate(data_list, 1):
        # 1. 发布时间
        publish_date = item.get('publishDate', 0)
        if publish_date:
            date_str = datetime.fromtimestamp(publish_date / 1000).strftime('%Y-%m-%d %H:%M')
        else:
            date_str = '未知时间'
        
        # 2. 宏观类型
        macro_type = item.get('macroEconomyResult', '')
        macro_emoji = {'国内宏观': '🇨🇳', '国际宏观': '🌍'}.get(macro_type, '⚪')
        
        # 3. 情感倾向
        sentiment = item.get('sentiment', '未知')
        sentiment_emoji = {'正面': '🟢', '负面': '🔴', '中性': '🟡'}.get(sentiment, '⚪')
        
        # 4. 新闻标题
        title = item.get('title', '')
        
        # 5. 新闻来源
        source = item.get('source', '')
        
        # 6. 宏观事件标签
        macro_tag = item.get('macroTag', '')
        
        # 7. 涉及地区
        area = item.get('areaResult', '')
        
        # 8. 重要程度
        importance = item.get('newsImportanceLevel', '')
        
        # 9. 热度数据
        heat = item.get('heatScores', 0)
        views = item.get('viewNum', 0)
        forwards = item.get('forwardedNum', 0)
        
        # 10. 新闻摘要
        summary = item.get('summary', '')
        
        # 格式化输出（必须展示的 10 个字段）
        print(f"{i}. [{date_str}] {sentiment_emoji} {sentiment} {macro_emoji} {macro_type}")
        print(f"   📰 标题：{title}")
        print(f"   📝 摘要：{summary[:200] if summary else '无'}...")
        print(f"   📍 来源：{source} | 重要程度：{importance if importance else '未分级'}")
        print(f"   🏷️ 事件标签：{macro_tag if macro_tag else '无'} | 涉及地区：{area if area else '未指定'}")
        print(f"   🔥 热度：{heat} | 浏览：{views} | 转发：{forwards}")
        
        # 详细内容（verbose 模式或用户要求时显示）
        if verbose:
            content = item.get('content', '')
            if content:
                # 去除 HTML 标签
                import re
                text_content = re.sub(r'<[^>]+>', '', content)[:300]
                print(f"   📄 内容：{text_content}...")
        
        print("-" * 80)


def main():
    parser = argparse.ArgumentParser(
        description='宏观资讯查询工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基础搜索
  python query_macro_information.py --keyword "美联储"
  
  # 搜索指定宏观类型（最近 7 天）
  python query_macro_information.py --keyword "GDP" --macro-type 国内宏观 --days 7
  
  # 搜索指定情感倾向
  python query_macro_information.py --keyword "通胀" --sentiments 负面 --days 30
  
  # 搜索国际宏观资讯
  python query_macro_information.py --keyword "美联储" --macro-type 国际宏观 --days 14
  
  # 按热度排序
  python query_macro_information.py --keyword "加息" --macro-type 国际宏观 --sort-by heat_scores
        """
    )
    
    parser.add_argument('--keyword', '-k', required=True, help='搜索关键词')
    parser.add_argument('--macro-type', '-m', choices=['国内宏观', '国际宏观'],
                        help='宏观类型（国内宏观/国际宏观）')
    parser.add_argument('--sentiments', '-s', nargs='+', choices=['正面', '负面', '中性'],
                        help='情感倾向（可多选）')
    parser.add_argument('--days', '-d', type=int, default=7, help='查询天数（默认 7 天）')
    parser.add_argument('--page', '-p', type=int, default=0, help='页码（从 0 开始，默认 0）')
    parser.add_argument('--size', '-n', type=int, default=20, help='每页数量（默认 20）')
    parser.add_argument('--sort-by', default='publish_date', 
                        help='排序字段：publish_date（默认，按发布时间）/ heat_scores（按热度）')
    parser.add_argument('--sort-type', choices=['ASC', 'DESC'], default='DESC', help='排序方式（默认 DESC）')
    parser.add_argument('--verbose', '-v', action='store_true', help='显示详细内容（摘要）')
    parser.add_argument('--output-dir', default='.', help='输出目录（默认当前目录）')
    parser.add_argument('--no-output', action='store_true', help='不生成输出文件，仅显示结果')
    parser.add_argument('--api-key', help='FEEDAX API Key（也可通过环境变量 FEEDAX_API_KEY 提供）')
    
    args = parser.parse_args()
    
    # 获取 API Key（优先级：命令行参数 > 环境变量 > 配置文件）
    if args.api_key:
        api_key = args.api_key
    elif os.environ.get('FEEDAX_API_KEY'):
        api_key = os.environ.get('FEEDAX_API_KEY')
    else:
        # 尝试从配置文件读取
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                api_key = config.get('api_key', '')
        else:
            api_key = ''
    
    if not api_key:
        print("错误：未提供 API Key")
        print("")
        print("**GE1003**: 未配置 API Key，请前往 https://www.feedax.cn 申请")
        print("")
        print("请通过以下方式之一提供：")
        print("  1. 命令行参数：--api-key \"your-api-key\"")
        print("  2. 环境变量：export FEEDAX_API_KEY=\"your-api-key\"")
        print("  3. 配置文件：在 scripts/ 目录创建 config.json，内容为 {\"api_key\": \"your-api-key\"}")
        sys.exit(1)
    
    # 调用 API
    print(f"正在查询宏观资讯...")
    print(f"关键词：{args.keyword}")
    if args.macro_type:
        print(f"宏观类型：{args.macro_type}")
    print(f"时间范围：近 {args.days} 天")
    if args.sentiments:
        print(f"情感倾向：{', '.join(args.sentiments)}")
    
    response = query_macro_information(
        api_key=api_key,
        keyword=args.keyword,
        macro_type=args.macro_type,
        sentiments=args.sentiments,
        days=args.days,
        page=args.page,
        size=args.size,
        sort_by=args.sort_by,
        sort_type=args.sort_type
    )
    
    # 检查响应
    code = response.get('code')
    message = response.get('message', '')
    
    if code != 200:
        # 错误码说明
        error_codes = {
            'GE1003': '未配置 API Key',
            'GE1004': 'API Key 已失效',
            'GE1005': 'API Key 已过期',
            'GE1006': 'API Key 无效',
            'GE1007': '账户余额不足'
        }
        error_hint = error_codes.get(str(code), '')
        
        print(f"查询失败：code={code}")
        if message:
            print(f"message={message}")
        if error_hint:
            print(f"说明：{error_hint}")
            if code in ['GE1003', 'GE1005', 'GE1006']:
                print("解决方案：请前往 https://www.feedax.cn 重新申请 API Key")
        print("")
        print(json.dumps(response, indent=2, ensure_ascii=False))
        sys.exit(1)
    
    data = response.get('data') or []
    total = response.get('total', 0)
    
    print(f"\n查询成功！共 {total} 条结果，当前返回 {len(data)} 条")
    
    # 格式化输出到终端
    format_output(data, verbose=args.verbose)
    
    # 生成输出文件
    if not args.no_output and data:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir = args.output_dir
        
        csv_path = os.path.join(output_dir, f"macro_information_{timestamp}.csv")
        md_path = os.path.join(output_dir, f"macro_information_{timestamp}.md")
        
        generate_csv(data, csv_path)
        generate_description(response, md_path, args.keyword, args.macro_type, args.days)


if __name__ == '__main__':
    main()
