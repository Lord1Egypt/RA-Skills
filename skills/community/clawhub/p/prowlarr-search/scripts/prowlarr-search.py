#!/usr/bin/env python3
"""
Prowlarr API 搜索脚本
通过 Prowlarr API 获取资源搜索结果
"""

import os
import sys
import json
import argparse
import urllib.parse
import urllib.request
import urllib.error


def format_size(size_bytes: int) -> str:
    """将字节大小转换为人类可读的格式"""
    if size_bytes is None:
        return "Unknown"

    units = ['B', 'KB', 'MB', 'GB', 'TB']
    size = float(size_bytes)
    unit_index = 0

    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1

    if unit_index == 0:
        return f"{int(size)} {units[unit_index]}"
    else:
        return f"{size:.2f} {units[unit_index]}"


def search_prowlarr(query: str, api_key: str, base_url: str = "http://localhost:9696",
                    search_type: str = None, season: str = None, ep: str = None) -> list:
    """
    调用 Prowlarr API 进行搜索

    Args:
        query: 搜索词
        api_key: Prowlarr API Key
        base_url: Prowlarr 服务地址
        search_type: 搜索类型 (movie, tv, music)
        season: 剧集季数
        ep: 剧集集数

    Returns:
        搜索结果列表
    """
    # 对搜索词进行 URL 编码（支持中文）
    encoded_query = urllib.parse.quote(query)

    # 构建 API URL 基础参数
    # type 参数：如果指定了 search_type 则使用它，否则使用默认的 search
    search_type_param = search_type if search_type else 'search'
    api_url = f"{base_url}/api/v1/search?query={encoded_query}&type={search_type_param}&limit=100&apiKey={api_key}"

    # 添加可选参数
    if season:
        api_url += f"&season={season}"
    if season:
        api_url += f"&season={season}"
    if ep:
        api_url += f"&ep={ep}"

    try:
        request = urllib.request.Request(api_url)
        request.add_header('Accept', 'application/json')

        with urllib.request.urlopen(request, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))

            # 处理搜索结果
            results = []
            for item in data:
                result = {
                    'title': item.get('title', 'Unknown'),
                    'size': format_size(item.get('size', 0)),
                    'indexer': item.get('indexer', 'Unknown'),
                    'guid': item.get('guid', 'Unknown'),
                    'publishDate': item.get('publishDate', None)
                }
                results.append(result)

            return results

    except urllib.error.HTTPError as e:
        print(json.dumps({'error': f'HTTP Error: {e.code} - {e.reason}'}), file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(json.dumps({'error': f'URL Error: {e.reason}'}), file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(json.dumps({'error': f'JSON Decode Error: {str(e)}'}), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(json.dumps({'error': f'Unexpected Error: {str(e)}'}), file=sys.stderr)
        sys.exit(1)


def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='Prowlarr API 搜索工具')
    parser.add_argument('query', nargs='+', help='搜索关键词')
    parser.add_argument('--type', choices=['movie', 'tv', 'music'], help='搜索类型：movie, tv, music')
    parser.add_argument('--season', type=str, help='剧集季数')
    parser.add_argument('--ep', type=str, help='剧集集数')

    args = parser.parse_args()

    # 从环境变量获取 API Key 和  Base URL
    api_key = os.environ.get('PROWLARR_API_KEY')
    base_url = os.environ.get('PROWLARR_BASE_URL')

    if not api_key:
        print(json.dumps({'error': 'Missing PROWLARR_API_KEY environment variable'}), file=sys.stderr)
        sys.exit(1)
    if not base_url:
        base_url="http://localhost:9696"

    # 拼接搜索词
    search_query = ' '.join(args.query)

    # 执行搜索
    results = search_prowlarr(
        search_query,
        api_key,
        base_url=base_url,
        search_type=args.type,
        season=args.season,
        ep=args.ep
    )

    # 输出 JSON 格式的搜索结果
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
