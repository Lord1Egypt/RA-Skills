import sys
import json
import os
import hashlib
import platform
import argparse
import urllib.request
import urllib.error

CREATE_ORDER_URL = "https://adeeptools.com/api/clawtip/create-order"
SKILL_NAME = "human-style-writer"
SKILL_DESCRIPTION = "AI 长文创作服务，具备人工写作特征，零AI腔调"
RESOURCE_URL = "https://adeeptools.com"


def compute_indicator(skill_name: str) -> str:
    return hashlib.md5(skill_name.encode("utf-8")).hexdigest()


def orders_dir(indicator: str) -> str:
    home_dir = os.path.expanduser("~")
    if platform.system() == "Windows":
        return os.path.join(home_dir, "openclaw", "skills", "orders", indicator)
    return os.path.join(home_dir, ".openclaw", "skills", "orders", indicator)


def create_order(question: str) -> dict:
    payload = json.dumps({"question": question}).encode("utf-8")
    req = urllib.request.Request(
        CREATE_ORDER_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as e:
        raise RuntimeError(f"网络请求异常，请确认网络连接并稍后重试: {e}") from e

    if body.get("responseCode") != "200":
        raise RuntimeError(
            f"Order creation failed: {body.get('responseMessage', 'unknown error')}"
        )

    if not body.get("orderNo"):
        raise RuntimeError("Order creation response missing 'orderNo'")

    return body


def write_order_file(question: str, api_response: dict) -> tuple:
    indicator = compute_indicator(SKILL_NAME)
    target_dir = orders_dir(indicator)
    os.makedirs(target_dir, exist_ok=True)

    order_no = api_response["orderNo"]
    order_file = os.path.join(target_dir, f"{order_no}.json")

    order_data = {
        "order_no": order_no,
        "amount": api_response.get("amount"),
        "payTo": api_response.get("payTo"),
        "encrypted_data": api_response.get("encryptedData"),
        "question": question,
        "skill_name": SKILL_NAME,
        "slug": SKILL_NAME,
        "description": SKILL_DESCRIPTION,
        "resource_url": RESOURCE_URL,
    }

    with open(order_file, "w", encoding="utf-8") as f:
        json.dump(order_data, f, ensure_ascii=False, indent=2)

    return order_no, indicator, order_file


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create AI creation order")
    parser.add_argument("question", help="User's content creation requirement")
    args = parser.parse_args()

    try:
        api_response = create_order(args.question)
        order_no, indicator, order_file = write_order_file(args.question, api_response)
    except RuntimeError as e:
        print(f"订单创建失败: {e}")
        sys.exit(1)
    except OSError as e:
        print(f"订单创建失败: 无法写入订单文件 {e}")
        sys.exit(1)

    print(f"ORDER_NO={order_no}")
    print(f"INDICATOR={indicator}")
    print(f"AMOUNT={api_response.get('amount')}")
    print(f"ORDER_FILE={order_file}")
