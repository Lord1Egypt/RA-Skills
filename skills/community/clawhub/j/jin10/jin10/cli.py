"""
Jin10 CLI
对 OpenClaw 暴露稳定命令接口，内部隐藏 MCP 协议细节。
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Optional

from .client import Jin10Client, Jin10Error
from .calendar import CalendarClient
from .flash import FlashClient
from .news import NewsClient
from .quotes import QuotesClient


def _print_output(data: Any, output_format: str, formatter=None) -> int:
    if output_format == 'text':
        if formatter is not None:
            print(formatter(data))
        elif isinstance(data, str):
            print(data)
        else:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        return 0

    print(json.dumps(data, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='python3 -m jin10',
        description='Jin10 财经数据 CLI。内部走 MCP 端点，但命令接口不暴露 MCP 细节。',
    )
    parser.add_argument(
        '--format',
        choices=('json', 'text'),
        default='json',
        help='输出格式，默认 json。',
    )

    subparsers = parser.add_subparsers(dest='command', required=True)

    subparsers.add_parser('codes', help='列出支持的报价品种代码')

    quote_parser = subparsers.add_parser('quote', help='查询单个品种报价')
    quote_parser.add_argument('code', help='品种代码，例如 XAUUSD')

    kline_parser = subparsers.add_parser('kline', help='查询指定品种 K 线')
    kline_parser.add_argument('code', help='品种代码，例如 XAUUSD')
    kline_parser.add_argument('--time', help='K 线周期，例如 1m、5m、1h、1d')
    kline_parser.add_argument('--count', type=int, help='返回 K 线数量')

    flash_parser = subparsers.add_parser('flash', help='快讯查询')
    flash_subparsers = flash_parser.add_subparsers(dest='flash_command', required=True)
    flash_list_parser = flash_subparsers.add_parser('list', help='读取最新快讯')
    flash_list_parser.add_argument('--cursor', help='分页游标')
    flash_search_parser = flash_subparsers.add_parser('search', help='搜索快讯')
    flash_search_parser.add_argument('keyword', help='搜索关键词')

    news_parser = subparsers.add_parser('news', help='资讯查询')
    news_subparsers = news_parser.add_subparsers(dest='news_command', required=True)
    news_list_parser = news_subparsers.add_parser('list', help='读取最新资讯')
    news_list_parser.add_argument('--cursor', help='分页游标')
    news_search_parser = news_subparsers.add_parser('search', help='搜索资讯')
    news_search_parser.add_argument('keyword', help='搜索关键词')
    news_search_parser.add_argument('--cursor', help='分页游标')
    news_get_parser = news_subparsers.add_parser('get', help='读取单篇资讯详情')
    news_get_parser.add_argument('id', help='资讯 ID')

    calendar_parser = subparsers.add_parser('calendar', help='财经日历')
    calendar_parser.add_argument('--keyword', help='按关键词筛选')
    calendar_parser.add_argument(
        '--high-importance',
        action='store_true',
        help='仅返回高重要性事件（星级 >= 3）',
    )

    return parser


def run_command(args: argparse.Namespace, client: Optional[Jin10Client] = None) -> int:
    client = client or Jin10Client()

    if args.command == 'codes':
        return _print_output(client.quotes.get_codes(), args.format)

    if args.command == 'quote':
        return _print_output(
            client.quotes.get_quote(args.code),
            args.format,
            QuotesClient.format_quote,
        )

    if args.command == 'kline':
        return _print_output(
            client.quotes.get_kline(args.code, args.time, args.count),
            args.format,
            QuotesClient.format_kline,
        )

    if args.command == 'flash':
        if args.flash_command == 'list':
            result = client.flash.list(args.cursor)
        else:
            result = client.flash.search(args.keyword)
        return _print_output(result, args.format, FlashClient.format_flash_list)

    if args.command == 'news':
        if args.news_command == 'list':
            result = client.news.list(args.cursor)
            formatter = NewsClient.format_news_list
        elif args.news_command == 'search':
            result = client.news.search(args.keyword, args.cursor)
            formatter = NewsClient.format_news_list
        else:
            result = client.news.get(args.id)
            formatter = NewsClient.format_news_detail
        return _print_output(result, args.format, formatter)

    if args.command == 'calendar':
        if args.high_importance:
            result = client.calendar.get_high_importance()
            formatter = CalendarClient.format_high_importance
        elif args.keyword:
            result = client.calendar.search(args.keyword)
            formatter = lambda events: '\n\n'.join(  # noqa: E731
                CalendarClient.format_event(event) for event in events
            ) or '没有找到匹配的财经事件'
        else:
            result = client.calendar.list()
            formatter = CalendarClient.format_calendar
        return _print_output(result, args.format, formatter)

    raise Jin10Error(f'Unknown command: {args.command}')


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        return run_command(args)
    except Jin10Error as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
