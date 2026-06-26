"""
MeetingOS - SkillPay 计费模块
每次处理一场会议消耗 1 个 token
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

# 从环境变量读取，不在代码里写任何真实的 Key
SKILLPAY_API_KEY  = os.getenv("SKILLPAY_API_KEY", "")
SKILLPAY_SKILL_ID = os.getenv("SKILLPAY_SKILL_ID", "")
BILLING_URL       = "https://skillpay.me/api/v1/billing"


def charge_user(user_id: str, amount: int = 1) -> bool:
    """
    扣除用户 token

    参数：
        user_id - 用户唯一标识
        amount  - 扣除数量，默认 1

    返回：
        True  扣费成功可以继续
        False 余额不足需要充值
    """
    if not SKILLPAY_API_KEY or not SKILLPAY_SKILL_ID:
        print("未配置 SKILLPAY_API_KEY，跳过计费")
        return True

    try:
        response = requests.post(
            f"{BILLING_URL}/charge",
            headers={
                "X-API-Key":    SKILLPAY_API_KEY,
                "Content-Type": "application/json",
            },
            json={
                "user_id":  user_id,
                "skill_id": SKILLPAY_SKILL_ID,
                "amount":   amount,
            },
            timeout=10,
        )

        data = response.json()

        if response.status_code == 200 and data.get("success"):
            print(f"扣费成功，剩余 {data.get('balance', 0)} tokens")
            return True

        if response.status_code == 402:
            recharge_url = get_recharge_link(user_id)
            print(f"余额不足，充值地址：{recharge_url}")
            return False

        print(f"计费异常，放行本次请求")
        return True

    except requests.exceptions.Timeout:
        print("计费超时，放行本次请求")
        return True

    except Exception as error:
        print(f"计费服务异常：{error}，放行本次请求")
        return True


def get_balance(user_id: str) -> int:
    """
    查询用户余额

    参数：
        user_id - 用户唯一标识

    返回：
        余额数量，查询失败返回 -1
    """
    if not SKILLPAY_API_KEY or not SKILLPAY_SKILL_ID:
        return -1

    try:
        response = requests.get(
            f"{BILLING_URL}/balance",
            headers={"X-API-Key": SKILLPAY_API_KEY},
            params={
                "user_id":  user_id,
                "skill_id": SKILLPAY_SKILL_ID,
            },
            timeout=10,
        )

        if response.status_code == 200:
            return response.json().get("balance", 0)

        return -1

    except Exception:
        return -1


def get_recharge_link(user_id: str) -> str:
    """
    获取用户充值链接

    参数：
        user_id - 用户唯一标识

    返回：
        充值页面网址
    """
    if not SKILLPAY_API_KEY or not SKILLPAY_SKILL_ID:
        return "https://skillpay.me"

    try:
        response = requests.post(
            f"{BILLING_URL}/payment-link",
            headers={
                "X-API-Key":    SKILLPAY_API_KEY,
                "Content-Type": "application/json",
            },
            json={
                "user_id":  user_id,
                "skill_id": SKILLPAY_SKILL_ID,
            },
            timeout=10,
        )

        if response.status_code == 200:
            return response.json().get("payment_url", "https://skillpay.me")

        return "https://skillpay.me"

    except Exception:
        return "https://skillpay.me"


def require_tokens(user_id: str) -> bool:
    """
    调用付费功能前的统一检查入口

    参数：
        user_id - 用户唯一标识

    返回：
        True  可以继续执行
        False 余额不足，已提示充值
    """
    balance = get_balance(user_id)

    if balance == 0:
        link = get_recharge_link(user_id)
        print(f"余额为零，请充值后再试：{link}")
        return False

    return charge_user(user_id)


# 测试代码，只有直接运行才执行
if __name__ == "__main__":
    import sys

    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"

    if cmd == "test_balance":
        result = get_balance("test_user")
        print(f"余额：{result}")

    elif cmd == "test_charge":
        result = charge_user("test_user")
        print(f"扣费：{'成功' if result else '失败'}")

    elif cmd == "test_link":
        result = get_recharge_link("test_user")
        print(f"充值链接：{result}")

    else:
        print("使用方法：")
        print("  python skillpay_guard.py test_balance")
        print("  python skillpay_guard.py test_charge")
        print("  python skillpay_guard.py test_link")