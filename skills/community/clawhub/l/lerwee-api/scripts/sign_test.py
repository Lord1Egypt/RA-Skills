#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lerwee API Signature Test Tool
乐维 API 签名测试工具
"""

import hashlib
import json
import time


def make_sign(params: dict, secret: str) -> str:
    """
    生成签名

    Args:
        params: 请求参数
        secret: API 密钥

    Returns:
        签名字符串（小写SHA1）
    """
    # 按字母顺序排序
    sorted_items = sorted(params.items())

    # 拼接参数（跳过 sign 字段、空值和数组）
    str_to_sign = ''
    for k, v in sorted_items:
        if k == 'sign':
            continue
        if v != "" and v is not None and not isinstance(v, (list, dict)):
            str_to_sign += f"{k}{v}"

    # 加密钥前缀并 SHA1 加密
    sign_str = secret + str_to_sign
    return hashlib.sha1(sign_str.encode('utf-8')).hexdigest().lower()


def test_sign():
    """测试签名生成"""
    secret = ""

    # 测试用例1：基础参数
    params1 = {
        "aa": 111,
        "bb": 222,
        "timestamp": 1654825429
    }
    sign1 = make_sign(params1, secret)
    print(f"测试用例1:")
    print(f"  参数: {params1}")
    print(f"  签名: {sign1}")
    print(f"  预期: 5bb575edea620452d3b03ccefaf76c9bdd8241a2")
    print(f"  匹配: {sign1 == '5bb575edea620452d3b03ccefaf76c9bdd8241a2'}")
    print()

    # 测试用例2：监控对象列表
    params2 = {
        "keyword": "linux",
        "classification": 101,
        "page": 1,
        "pageSize": 20,
        "timestamp": int(time.time())
    }
    sign2 = make_sign(params2, secret)
    print(f"测试用例2 - 监控对象列表:")
    print(f"  参数: {json.dumps(params2, indent=4)}")
    print(f"  签名: {sign2}")
    print()

    # 测试用例3：包含空值和数组的参数
    params3 = {
        "keyword": "test",
        "ip": "",
        "group_ids": [1, 2, 3],
        "page": 1,
        "pageSize": 10,
        "timestamp": int(time.time())
    }
    sign3 = make_sign(params3, secret)
    print(f"测试用例3 - 包含空值和数组:")
    print(f"  参数: {json.dumps(params3, indent=4)}")
    print(f"  签名: {sign3}")
    print(f"  说明: 空值和数组不参与签名")
    print()

    # 测试用例4：aialert 接口特殊处理
    inner_data = {
        "page": 1,
        "pageSize": 2,
        "status": 0
    }
    params4 = {
        "data": json.dumps(inner_data, separators=(',', ':')),
        "timestamp": int(time.time())
    }
    sign4 = make_sign(params4, secret)
    print(f"测试用例4 - 事件平台告警列表:")
    print(f"  data 内容: {json.dumps(inner_data, indent=4)}")
    print(f"  序列化后: {params4['data']}")
    print(f"  完整参数: {json.dumps(params4, indent=4)}")
    print(f"  签名: {sign4}")
    print()

    # 显示详细签名过程
    print("=== 签名生成详细过程 ===")
    print(f"原始参数: {params1}")
    sorted_items = sorted(params1.items())
    print(f"排序后: {sorted_items}")

    str_parts = []
    for k, v in sorted_items:
        if k != 'sign' and v != "" and v is not None and not isinstance(v, (list, dict)):
            str_parts.append(f"{k}{v}")
    str_to_sign = ''.join(str_parts)

    print(f"拼接后: {str_to_sign}")
    print(f"加前缀: {secret}{str_to_sign}")
    print(f"SHA1: {hashlib.sha1((secret + str_to_sign).encode('utf-8')).hexdigest().lower()}")


if __name__ == '__main__':
    test_sign()
