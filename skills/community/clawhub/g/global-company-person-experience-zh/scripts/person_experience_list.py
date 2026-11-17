#!/usr/bin/env python3
"""
跨境魔方全球企业库工作经历列表查询
根据人物ID获取某人的历史工作经历列表，支持游标翻页。
"""
import argparse
import sys
from common import make_request, print_json_output, cover_fee_info

def get_experience_list(hid: str, pid: str = None, cursor: str = None) -> dict:
    """
    根据人物ID获取工作经历列表。

    Args:
        hid: 人物ID
        pid: 公司ID（可选，筛选指定公司的工作经历）
        cursor: 分页游标，首次请求不传，翻页时传入上一次响应返回的cursor

    Returns:
        包含工作经历列表的API响应
    """
    params = {'hid': hid}
    if pid:
        params['pid'] = pid
    if cursor:
        params['cursor'] = cursor
    response = make_request('/agent/search/depth_company/person/experience/list', params)
    return response

def main():
    parser = argparse.ArgumentParser(
        description='从跨境魔方开放平台获取全球企业库人物工作经历列表'
    )
    parser.add_argument(
        '--hid',
        required=True,
        help='人物ID（如 H_67890）'
    )
    parser.add_argument(
        '--pid',
        default=None,
        help='公司ID（可选，如 US_12345）'
    )
    parser.add_argument(
        '--cursor',
        default=None,
        help='分页游标，首次查询不传，翻页时传入上一次响应返回的cursor'
    )

    args = parser.parse_args()

    response = get_experience_list(args.hid, args.pid, args.cursor)

    if response.get('code') in (0, 200):
        data = response.get('data', {})
        print_json_output({
            "data": data,
            "fee": cover_fee_info(response.get('fee', {})),
            "requestId": response.get('requestId')
        })
    else:
        print(f"错误：{response.get('msg', '未知错误')}", file=sys.stderr)
        if response.get('requestId'):
            print(f"requestId：{response.get('requestId')}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
