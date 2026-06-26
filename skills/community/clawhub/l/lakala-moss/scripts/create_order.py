#!/usr/bin/env python3
"""
拉卡拉MOSS支付下单脚本
演示如何调用MOSS接口发起支付订单并获取支付链接
"""

import argparse
import json
import uuid
import sys
import requests


def generate_service_sn():
    """生成服务流水号"""
    return str(uuid.uuid4()).replace('-', '')


def create_order(order_no, total_amount, subject="订单标题测试",
                 remark="交易备注信息测试", callback_url="lakala.com"):
    """
    发起支付下单请求

    Args:
        order_no: 商户订单号（唯一）
        total_amount: 支付金额（单位：分，字符串形式）
        subject: 订单标题
        remark: 交易备注
        callback_url: 支付结果回调地址

    Returns:
        dict: 包含支付链接或错误信息的响应数据
    """

    # API地址
    url = "https://moss.lakala.com/ord-api/unified/v3"

    # 构造请求报文
    request_data = {
        "head": {
            "versionId": "1.0",
            "serviceId": "lfops.moss.order.pay",
            "serviceSn": generate_service_sn(),
            "systemCode": "MOSS",
            "channelId": "API",
            "businessChannel": "C00000404"
        },
        "request": {
            "order_no": order_no,
            "total_amount": str(total_amount),
            "mer_no": "M00002042",
            "pay_scene": "0",
            "account_type": "ALIPAY,WECHAT,UQRCODEPAY",
            "order_eff_time": "30",
            "subject": subject,
            "remark": remark,
            "callback_url": callback_url
        }
    }

    # 发起POST请求
    try:
        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(
            url,
            json=request_data,
            headers=headers,
            timeout=30
        )

        # 检查HTTP状态码
        if response.status_code >= 400:
            return {
                "success": False,
                "error": f"HTTP请求失败: 状态码 {response.status_code}",
                "response": response.text
            }

        # 解析响应
        response_data = response.json()

        # 检查业务状态 - 修复：使用实际API返回的code/desc字段
        # 原有代码使用head.respCode/respMsg，实际API返回的是code/desc
        head = response_data.get("head", {})

        # 优先检查code字段，如果不存在则检查respCode字段（向后兼容）
        resp_code = head.get("code") or head.get("respCode")
        resp_msg = head.get("desc") or head.get("respMsg")

        if resp_code != "000000":
            return {
                "success": False,
                "error": f"业务请求失败: {resp_msg}",
                "code": resp_code,
                "desc": resp_msg,
                "full_response": response_data
            }

        # 提取支付链接 - 修复：从response.counter_url获取支付链接
        # 原有代码使用request.pay_url，实际API返回的是response.counter_url
        result = response_data.get("response", {})
        pay_url = result.get("counter_url")

        if not pay_url:
            return {
                "success": False,
                "error": "响应中未包含支付链接",
                "full_response": response_data
            }

        # 提取其他有用信息
        service_sn = head.get("serviceSn")
        service_time = head.get("serviceTime")

        return {
            "success": True,
            "pay_url": pay_url,
            "order_no": order_no,
            "total_amount": total_amount,
            "service_sn": service_sn,
            "service_time": service_time,
            "full_response": response_data
        }

    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"网络请求异常: {str(e)}"
        }
    except json.JSONDecodeError as e:
        return {
            "success": False,
            "error": f"JSON解析失败: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"未知错误: {str(e)}"
        }


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="拉卡拉MOSS支付下单演示脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  基础支付订单:
    python create_order.py --order-no "TEST001" --total-amount "1"

  完整支付订单:
    python create_order.py --order-no "TEST001" --total-amount "100" \\
      --subject "测试商品" --remark "演示订单" --callback-url "https://example.com/callback"
        """
    )

    parser.add_argument(
        "--order-no",
        required=True,
        help="商户订单号（必须唯一）"
    )
    parser.add_argument(
        "--total-amount",
        required=True,
        help="支付金额（字符串形式，单位：分，例如'1'表示1分）"
    )
    parser.add_argument(
        "--subject",
        default="订单标题测试",
        help="订单标题（默认：订单标题测试）"
    )
    parser.add_argument(
        "--remark",
        default="交易备注信息测试",
        help="交易备注（默认：交易备注信息测试）"
    )
    parser.add_argument(
        "--callback-url",
        default="lakala.com",
        help="支付结果回调地址（默认：lakala.com）"
    )

    args = parser.parse_args()

    # 验证参数
    if not args.order_no:
        print("错误：订单号不能为空", file=sys.stderr)
        sys.exit(1)

    # 金额验证：必须是字符串且为正数
    if not args.total_amount:
        print("错误：金额不能为空", file=sys.stderr)
        sys.exit(1)

    try:
        # 金额为字符串形式，检查是否为有效数字
        amount_int = int(args.total_amount)
        if amount_int <= 0:
            print("错误：金额必须大于0", file=sys.stderr)
            sys.exit(1)
    except ValueError:
        print("错误：金额必须是数字字符串", file=sys.stderr)
        sys.exit(1)

    # 调用下单接口
    print(f"正在发起支付下单...")
    print(f"订单号: {args.order_no}")
    print(f"金额: {args.total_amount} 分")
    print("-" * 50)

    result = create_order(
        order_no=args.order_no,
        total_amount=args.total_amount,
        subject=args.subject,
        remark=args.remark,
        callback_url=args.callback_url
    )

    # 输出结果
    if result["success"]:
        print("✓ 下单成功！")
        print(f"订单号: {result['order_no']}")
        print(f"支付金额: {result['total_amount']} 分")
        if result.get("service_sn"):
            print(f"服务流水号: {result['service_sn']}")
        if result.get("service_time"):
            print(f"服务时间: {result['service_time']}")
        print(f"\n支付链接: {result['pay_url']}")
        print(f"\n请点击上方链接完成支付")
    else:
        print("✗ 下单失败！")
        print(f"错误信息: {result['error']}")
        if "code" in result:
            print(f"响应码: {result['code']}")
            print(f"响应消息: {result['desc']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
