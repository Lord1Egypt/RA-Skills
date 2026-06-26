#!/usr/bin/env python3
"""
JokeAPI Python CLI Tool
用法：python joke.py <command> [options]
"""

import argparse
import json
import sys
import urllib.request
import urllib.error
from urllib.parse import quote, urlencode

BASE_URL = "https://v2.jokeapi.dev"


def make_request(endpoint, params=None):
    """发送 API 请求并返回解析后的 JSON 数据"""
    url = f"{BASE_URL}{endpoint}"
    
    if params:
        url += f"?{urlencode(params)}"
    
    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'JokeAPI-Python-CLI/1.0')
        
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        print(f"HTTP 错误 {e.code}: {e.reason}", file=sys.stderr)
        return None
    except urllib.error.URLError as e:
        print(f"URL 错误：{e.reason}", file=sys.stderr)
        return None
    except json.JSONDecodeError as e:
        print(f"JSON 解析错误：{e}", file=sys.stderr)
        return None


def get_joke(args):
    """获取笑话"""
    params = {}
    
    if args.category:
        params['category'] = args.category
    if args.type:
        params['type'] = args.type
    if args.format:
        params['format'] = args.format
    if args.lang:
        params['lang'] = args.lang
    if args.blacklist:
        params['blacklistFlags'] = args.blacklist
    if args.amount and args.amount > 1:
        params['amount'] = args.amount
    if args.contains:
        params['contains'] = quote(args.contains)
    if args.safe_mode:
        params['safe-mode'] = True
    
    if not params.get('category'):
        params['category'] = 'Any'
    
    data = make_request(f"/joke/{params['category']}", params)
    
    if not data:
        sys.exit(1)
    
    if data.get('error'):
        print(f"错误：{data.get('message', 'Unknown error')}", file=sys.stderr)
        if data.get('additionalInfo'):
            print(f"详情：{data['additionalInfo']}", file=sys.stderr)
        sys.exit(1)
    
    # 处理多笑话
    if args.amount and args.amount > 1:
        jokes = data.get('jokes', [])
        for i, joke in enumerate(jokes, 1):
            print(f"\n--- 笑话 {i} ---")
            if joke['type'] == 'single':
                print(joke['joke'])
            else:
                print(joke['setup'])
                print()
                print(joke['delivery'])
    else:
        # 单笑话
        if data['type'] == 'single':
            print(data['joke'])
        else:
            print(data['setup'])
            print()
            print(data['delivery'])


def list_categories(args):
    """列出所有可用分类"""
    data = make_request("/categories")
    
    if not data:
        sys.exit(1)
    
    print("可用分类:")
    for category in data.get('categories', []):
        print(f"  - {category}")


def list_languages(args):
    """列出所有支持的语言"""
    data = make_request("/languages")
    
    if not data:
        sys.exit(1)
    
    print("支持的编程语言:")
    for lang in data.get('jokeLanguages', []):
        print(f"  - {lang}")


def get_info(args):
    """获取 API 信息"""
    data = make_request("/info")
    
    if not data:
        sys.exit(1)
    
    print(json.dumps(data, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(
        description='JokeAPI CLI - 获取幽默笑话',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python joke.py random                    # 获取随机笑话
  python joke.py random -c Programming     # 获取编程笑话
  python joke.py random -c Misc,Pun -t twopart
  python joke.py random --safe-mode        # 仅获取安全内容
  python joke.py random -a 5               # 获取 5 个笑话
  python joke.py categories                # 列出所有分类
  python joke.py langs                     # 列出所有语言
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # random 命令
    random_parser = subparsers.add_parser('random', help='获取随机笑话')
    random_parser.add_argument('-c', '--category', help='指定分类')
    random_parser.add_argument('-t', '--type', choices=['single', 'twopart'], help='指定类型')
    random_parser.add_argument('-f', '--format', choices=['json', 'xml', 'yaml', 'txt'], help='指定格式')
    random_parser.add_argument('-l', '--lang', help='指定语言代码')
    random_parser.add_argument('-b', '--blacklist', help='过滤标志')
    random_parser.add_argument('-a', '--amount', type=int, help='获取笑话数量')
    random_parser.add_argument('-s', '--contains', help='搜索包含特定文本的笑话')
    random_parser.add_argument('--safe-mode', action='store_true', help='仅获取安全内容')
    random_parser.set_defaults(func=get_joke)
    
    # categories 命令
    categories_parser = subparsers.add_parser('categories', help='列出所有可用分类')
    categories_parser.set_defaults(func=list_categories)
    
    # langs 命令
    langs_parser = subparsers.add_parser('langs', help='列出所有支持的语言')
    langs_parser.set_defaults(func=list_languages)
    
    # info 命令
    info_parser = subparsers.add_parser('info', help='获取 API 信息')
    info_parser.set_defaults(func=get_info)
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == '__main__':
    main()
