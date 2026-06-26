import sys
import os
import json
import hashlib
import platform
import argparse
import urllib.request
import urllib.error

GET_RESULT_URL = "https://adeeptools.com/api/clawtip/get-service-result"
SKILL_NAME = "human-style-writer"


def compute_indicator(skill_name: str) -> str:
    return hashlib.md5(skill_name.encode("utf-8")).hexdigest()


def orders_dir(indicator: str) -> str:
    home_dir = os.path.expanduser("~")
    if platform.system() == "Windows":
        return os.path.join(home_dir, "openclaw", "skills", "orders", indicator)
    return os.path.join(home_dir, ".openclaw", "skills", "orders", indicator)


def read_order_file(order_no: str) -> dict:
    indicator = compute_indicator(SKILL_NAME)
    order_file = os.path.join(orders_dir(indicator), f"{order_no}.json")
    if not os.path.exists(order_file):
        raise RuntimeError(f"未找到订单文件：{order_file}，请先执行第一阶段创建订单")
    with open(order_file, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_credential(order_data: dict) -> str:
    for key in ("payCredential", "pay_credential", "credential"):
        value = order_data.get(key)
        if value:
            return value
    raise RuntimeError(
        "订单文件缺少 payCredential 字段，说明 clawtip 支付阶段尚未完成或失败，请先完成支付"
    )


def get_ai_creation(question: str, order_no: str, credential: str, style: str = "general") -> str:
    payload = json.dumps({
        "question": question,
        "orderNo": order_no,
        "credential": credential,
        "style": style,
    }).encode("utf-8")

    req = urllib.request.Request(
        GET_RESULT_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as e:
        raise RuntimeError(f"服务请求异常，请稍后重试: {e}") from e

    if body.get("responseCode") not in ("200", 200):
        raise RuntimeError(
            f"服务调用失败: {body.get('responseMessage', 'unknown error')}"
        )

    pay_status = body.get("payStatus", "ERROR")
    print(f"PAY_STATUS: {pay_status}")

    if pay_status == "ERROR":
        error_info = body.get("errorInfo", "未知错误")
        print(f"ERROR_INFO: {error_info}")
        raise RuntimeError(f"服务失败: {error_info}")

    if pay_status == "FAIL":
        raise RuntimeError("支付凭证解密后状态为失败，请回到 clawtip 查看授权/鉴权链接")

    if pay_status != "SUCCESS":
        raise RuntimeError(f"支付状态异常: {pay_status}，请重试")

    answer = body.get("answer", "")
    if not answer:
        raise RuntimeError("AI 创作结果为空，请重试")

    return answer


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Execute AI content creation after clawtip payment")
    parser.add_argument("order_no", help="Order number from Phase 1")
    parser.add_argument("--style", default="general",
                        help="Writing style: general / emotional / technical / news (default: general)")
    args = parser.parse_args()

    try:
        order_data = read_order_file(args.order_no)
        credential = extract_credential(order_data)
        question = order_data.get("question", "")
        if not question:
            raise RuntimeError("订单文件缺少 question 字段")
        result = get_ai_creation(question, args.order_no, credential, args.style)
        print(result)
    except RuntimeError as e:
        print(f"ERROR_INFO: {e}")
        sys.exit(1)
