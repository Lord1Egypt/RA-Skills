#!/usr/bin/env python3
import json
import sys

from route_query import main


CASES = [
    '看腾讯最近10根日K',
    '看腾讯资金流向',
    '看腾讯盘口',
    '看腾讯基础信息',
    '看腾讯市场状态',
    '看苹果5分钟K',
    '看英伟达最近5根周K',
]


def run_cases():
    results = []
    for case in CASES:
        results.append({'query': case, 'result': main(case)})
    return results


if __name__ == '__main__':
    print(json.dumps(run_cases(), ensure_ascii=False, indent=2, default=str))
