#!/usr/bin/env python3
"""
跨境魔方 Agent 调用 Skill 异常上报
向平台上报 Agent 调用 Skill 过程中出现的异常，用于平台侧问题追踪与优化。
"""
import argparse
import sys

from common import make_request, print_json_output, parse_params
from version_check import get_skill_name, get_skill_version


def report_error(params: dict) -> dict:
    """
    上报 Agent 调用 Skill 异常。

    Args:
        params: 上报参数（skillId, skillVersion, requestId, requestPath, context 等）

    Returns:
        包含 reportId 的API响应
    """
    # 自动填充 skillId 与 skillVersion（外部显式传入时以外部为准）
    params.setdefault('skillId', get_skill_name())
    params.setdefault('skillVersion', get_skill_version())
    # 验证必要参数
    for field in ('skillId', 'skillVersion', 'requestId', 'requestPath', 'context'):
        if not params.get(field):
            print(f"错误：params中缺少{field}", file=sys.stderr)
            sys.exit(1)
    response = make_request('/agent/skill/error/report', params)
    return response


def main():
    parser = argparse.ArgumentParser(
        description='向跨境魔方开放平台上报Agent调用Skill异常'
    )
    parser.add_argument(
        '--params',
        required=True,
        help='JSON格式的上报参数，如 \'{"requestPath":"/agent/customs/analysis/area","requestId":"f47ac10b58cc4372a5670e02b2c3d479","context":"接口返回异常"}\''
    )

    args = parser.parse_args()

    params = parse_params(args.params)

    response = report_error(params)

    if response.get('code') in (0, 200):
        print_json_output(response.get('data', {}))
    else:
        print(f"错误：{response.get('msg', '未知错误')}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
