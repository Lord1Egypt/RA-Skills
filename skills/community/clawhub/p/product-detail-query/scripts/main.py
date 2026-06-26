#!/usr/bin/env python3
"""
产品详情查询脚本

调用红袋宝贝产品详情API，获取产品详细信息

API信息：
- URL: https://openapi-test.hongdibaobei.com/v1/chat/robot/product/detail
- 方法: GET
- 参数: productCode, secondTypeId
"""

import argparse
import json
import sys
from urllib.parse import urlencode
from urllib.request import urlopen, Request


def query_product_detail(product_code: str, second_type_id: str) -> dict:
    """
    查询产品详情

    Args:
        product_code: 产品编码
        second_type_id: 二级分类ID

    Returns:
        dict: 产品详情数据

    Raises:
        Exception: API调用失败时抛出异常
    """
    # 构建请求URL
    base_url = "https://openapi-test.hongdibaobei.com/v1/chat/robot/product/detail"
    params = {
        "productCode": product_code,
        "secondTypeId": second_type_id
    }
    url = f"{base_url}?{urlencode(params)}"

    # 发起GET请求
    try:
        req = Request(url, method='GET')
        req.add_header('User-Agent', 'Mozilla/5.0')

        with urlopen(req, timeout=30) as response:
            # 检查HTTP状态码
            if response.status >= 400:
                raise Exception(
                    f"HTTP请求失败: 状态码 {response.status}"
                )

            # 读取响应内容
            response_text = response.read().decode('utf-8')

            # 解析JSON响应
            data = json.loads(response_text)

            # 检查API业务错误（根据实际API响应结构调整）
            # 注意：该API可能返回格式为 {"code": 0, "data": {...}, "msg": "success"}
            # 也可能直接返回数据对象，需要根据实际情况调整
            if isinstance(data, dict):
                # 检查是否有 code 字段，如果 code 不为 0 且 msg 不是 "success" 则视为错误
                if "code" in data and data["code"] != 0 and data.get("msg") != "success":
                    msg = data.get("msg", "未知错误")
                    raise Exception(f"API业务错误: {msg}")

            return data

    except Exception as e:
        if isinstance(e, (json.JSONDecodeError, Exception)):
            raise Exception(f"API调用失败: {str(e)}")
        raise


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description="查询产品详情")
    parser.add_argument(
        "--product-code",
        required=True,
        help="产品编码 (productCode)"
    )
    parser.add_argument(
        "--second-type-id",
        required=True,
        help="二级分类ID (secondTypeId)"
    )

    args = parser.parse_args()

    try:
        # 调用API查询产品详情
        result = query_product_detail(args.product_code, args.second_type_id)

        # 输出结果（JSON格式）
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)

    except Exception as e:
        # 输出错误信息
        print(json.dumps({
            "error": True,
            "message": str(e)
        }, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
