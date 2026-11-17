import sys
import json
import urllib.request
import urllib.error

CREATE_ORDER_URL = "https://adeeptools.com/api/clawtip/create-order"


def create_order(question: str) -> tuple:
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

    order_no = body.get("orderNo")
    if not order_no:
        raise RuntimeError("Order creation response missing 'orderNo'")

    amount = body.get("amount")
    encrypted_data = body.get("encryptedData")
    pay_to = body.get("payTo")

    return order_no, amount, encrypted_data, pay_to


import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create AI creation order")
    parser.add_argument("question", help="User's content creation requirement")
    args = parser.parse_args()

    try:
        order_no, amount, encrypted_data, pay_to = create_order(args.question)
    except RuntimeError as e:
        print(f"订单创建失败: {e}")
        sys.exit(1)

    print(f"ORDER_NO={order_no}")
    print(f"AMOUNT={amount}")
    print(f"ENCRYPTED_DATA={encrypted_data}")
    print(f"PAY_TO={pay_to}")
