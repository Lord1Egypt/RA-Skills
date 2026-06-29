#!/usr/bin/env python3
"""create_order.py — Phase 1：创建订单（调用远程 API）"""

import sys
import json
import hashlib
import urllib.request
import urllib.error

import file_utils

# ============================================================
# 配置（可根据实际服务端地址修改）
# ============================================================
CREATE_ORDER_URL = "http://129.226.222.150:80/createOrder"
SLUG = "industry-deep-report"


def compute_indicator(slug: str) -> str:
    return hashlib.md5(slug.encode("utf-8")).hexdigest()


def create_order(question: str) -> tuple:
    """
    POST 到服务端 createOrder 接口。
    返回 (order_no, amount, encrypted_data, pay_to)
    """
    payload = json.dumps({"question": question}).encode("utf-8")
    req = urllib.request.Request(
        CREATE_ORDER_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as e:
        raise RuntimeError(f"网络请求异常，请确认网络链接并稍后重试: {e}") from e

    response_code = body.get("responseCode", "")
    if response_code != "200":
        raise RuntimeError(
            f"服务端返回错误: {body.get('responseMessage', '未知错误')}"
        )

    order_no = body.get("orderNo")
    if not order_no:
        raise RuntimeError("服务端响应缺少 orderNo")

    amount = body.get("amount")
    encrypted_data = body.get("encryptedData")
    pay_to = body.get("payTo", "")

    return order_no, amount, encrypted_data, pay_to


def save_order_info(order_no: str, amount, question: str,
                    encrypted_data: str, pay_to: str, indicator: str) -> str:
    order_data = {
        "skill-id": f"si-{SLUG}",
        "order_no": order_no,
        "amount": int(amount) if amount else 0,
        "question": question,
        "encrypted_data": encrypted_data,
        "pay_to": pay_to,
        "description": "竞品/行业深度报告 — 1元/份",
        "slug": SLUG,
        "resource_url": "http://129.226.222.150:80",
    }
    return file_utils.save_order(indicator, order_no, order_data)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("订单创建失败: 缺少用户请求参数")
        sys.exit(1)

    question = sys.argv[1]
    indicator = compute_indicator(SLUG)

    try:
        order_no, amount, encrypted_data, pay_to = create_order(question)
    except RuntimeError as e:
        print(f"订单创建失败: {e}")
        sys.exit(1)

    save_order_info(order_no, amount, question,
                    encrypted_data, pay_to, indicator)

    # 必须遵守的输出格式
    print(f"ORDER_NO={order_no}")
    print(f"AMOUNT={amount}")
    print(f"QUESTION={question}")
    print(f"INDICATOR={indicator}")
