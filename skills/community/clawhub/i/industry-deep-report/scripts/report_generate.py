#!/usr/bin/env python3
"""report_generate.py — Phase 3：验证支付并从订单文件读取凭证"""

import sys
import json
import hashlib
import urllib.request
import urllib.error

import file_utils

# ============================================================
# 配置
# ============================================================
GET_RESULT_URL = "http://129.226.222.150:80/getServiceResult"
SLUG = "industry-deep-report"


def compute_indicator(slug: str) -> str:
    return hashlib.md5(slug.encode("utf-8")).hexdigest()


def get_service(order_no: str):
    """从订单文件读取 question 和 payCredential，调用服务端。"""
    indicator = compute_indicator(SLUG)

    # 从本地订单文件读取
    order_data = file_utils.load_order(indicator, order_no)
    question = order_data.get("question", "")
    credential = order_data.get("payCredential")
    if not credential:
        raise RuntimeError("订单文件中缺少 payCredential，支付尚未完成")

    payload = json.dumps({
        "question": question,
        "orderNo": order_no,
        "credential": credential,
    }).encode("utf-8")

    req = urllib.request.Request(
        GET_RESULT_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as e:
        raise RuntimeError(f"网络请求异常: {e}") from e

    response_code = body.get("responseCode", "")
    if response_code != "200":
        raise RuntimeError(
            f"服务端错误: {body.get('responseMessage', '未知错误')}"
        )

    pay_status = body.get("payStatus", "ERROR")
    print(f"PAY_STATUS: {pay_status}")

    if pay_status == "ERROR":
        error_info = body.get("errorInfo", "未知错误")
        print(f"ERROR_INFO: {error_info}")

    if pay_status == "SUCCESS":
        # 输出报告指令供 AI 消费
        message = body.get("message", "")
        structure = body.get("report_structure", [])
        print(f"REPORT_MSG: {message}")
        print(f"REPORT_SECTIONS: {json.dumps(structure, ensure_ascii=False)}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("ERROR_INFO: 缺少订单号参数")
        sys.exit(1)

    order_no = sys.argv[1]

    try:
        get_service(order_no)
    except RuntimeError as e:
        print(f"PAY_STATUS: ERROR")
        print(f"ERROR_INFO: {e}")
        sys.exit(1)
