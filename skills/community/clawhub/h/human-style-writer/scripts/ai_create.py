import sys
import json
import urllib.request
import urllib.error

GET_RESULT_URL = "https://adeeptools.com/api/clawtip/get-service-result"


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
        with urllib.request.urlopen(req, timeout=120) as resp:
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

    if pay_status != "SUCCESS":
        raise RuntimeError(f"支付状态异常: {pay_status}，请重试")

    answer = body.get("answer", "")
    if not answer:
        raise RuntimeError("AI 创作结果为空，请重试")

    return answer


import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Execute AI content creation after payment")
    parser.add_argument("question",    help="User's content creation requirement")
    parser.add_argument("order_no",    help="Order number from Phase 1")
    parser.add_argument("credential",  help="Payment credential from clawtip (Phase 2)")
    parser.add_argument("--style",     default="general",
                        help="Writing style: general / emotional / technical / news (default: general)")
    args = parser.parse_args()

    try:
        result = get_ai_creation(args.question, args.order_no, args.credential, args.style)
        print(result)
    except RuntimeError as e:
        print(f"ERROR_INFO: {e}")
        sys.exit(1)
