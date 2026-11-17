#!/usr/bin/env python3
"""
跨境魔方全球学校详情查询
根据学校ID获取学校的详细信息。
"""
import argparse
import sys
from common import make_request, print_json_output, cover_fee_info

def get_school_detail(sid: str) -> dict:
    """
    根据学校ID获取学校详情。

    Args:
        sid: 学校ID

    Returns:
        包含学校详情的API响应
    """
    params = {'sid': sid}
    response = make_request('/agent/search/depth_company/person/school/detail', params)
    return response

def main():
    parser = argparse.ArgumentParser(
        description='从跨境魔方开放平台获取全球学校详情'
    )
    parser.add_argument(
        '--sid',
        required=True,
        help='学校ID（如 S_001）'
    )

    args = parser.parse_args()

    response = get_school_detail(args.sid)

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
