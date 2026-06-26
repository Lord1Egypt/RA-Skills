"""
支付凭证服务 - 供 helian-health-assistant skill 调用
用于获取禾连健康支付凭证（paySign），作为后续 MCP 支付流程的前置步骤
"""

import requests
import json
from typing import Optional


# 获取支付凭证的真实接口地址
PAY_SIGN_URL = "https://healthcheck-web-client.helianhealth.com/thirdPlat/skillPaySign"


def get_pay_sign(params: dict) -> str:
    """
    获取支付凭证接口，供 Agent 调用。

    Args:
        params: 支付凭证请求参数，格式如下：
            {
                "userId": "17212161129",
                "requestId": "test2026031801",
                "orderTime": "2026-03-18 11:19:15",
                "orderAmount": "0.01",
                "notifyUrl": "https://healthcheck-web-client.helianhealth.com/thirdPlat/payBackForSkill",
                "goodsName": "测试独立号源提前"
            }

    Returns:
        str: 支付凭证字符串（paySign）。失败时返回空字符串。
    """
    print(f"[支付凭证] 获取支付凭证 → 入参: {json.dumps(params, ensure_ascii=False)}")

    try:
        response = requests.post(
            PAY_SIGN_URL,
            headers={"Content-Type": "application/json"},
            json=params,
            timeout=30
        )

        print(f"[支付凭证] 响应状态码: {response.status_code}")
        print(f"[支付凭证] 响应体: {response.text}")

        response.raise_for_status()
        result = response.json()

        if result.get("success") and result.get("code") == "0":
            pay_sign = result.get("data", "")
            print(f"[支付凭证] 获取成功，凭证长度: {len(pay_sign)}")
            return pay_sign
        else:
            msg = result.get("msg") or result.get("detailMsg") or "未知错误"
            print(f"[支付凭证] 接口返回失败: code={result.get('code')}, msg={msg}")
            return ""

    except requests.exceptions.Timeout:
        print("[支付凭证] 请求超时")
        return ""
    except requests.exceptions.RequestException as e:
        print(f"[支付凭证] 请求异常: {e}")
        return ""
    except Exception as e:
        print(f"[支付凭证] 未知异常: {e}")
        return ""


# ==================== 使用示例 ====================

if __name__ == "__main__":
    test_params = {
        "userId": "17212161129",
        "requestId": "test2026031801",
        "orderTime": "2026-03-18 11:19:15",
        "orderAmount": "0.01",
        "notifyUrl": "https://healthcheck-web-client.helianhealth.com/thirdPlat/payBackForSkill",
        "goodsName": "测试独立号源提前"
    }

    pay_sign = get_pay_sign(test_params)
    if pay_sign:
        print(f"\n支付凭证获取成功:")
        print(pay_sign)
    else:
        print("\n支付凭证获取失败")
