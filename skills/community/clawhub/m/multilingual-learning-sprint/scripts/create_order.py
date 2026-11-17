import argparse
import hashlib
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

from file_utils import save_order

SLUG = os.environ.get("CLAWTIP_SKILL_SLUG", "multilingual-learning-sprint")
DEFAULT_API_BASE_URL = "https://language-sprint-clawtip.pages.dev"


def load_env_file() -> None:
    candidates = [Path.cwd() / ".env.local", Path(__file__).resolve().parents[3] / ".env.local"]
    for path in candidates:
        if not path.is_file():
            continue
        for raw_line in path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip("\"'"))


def compute_indicator(slug: str) -> str:
    return os.environ.get("CLAWTIP_INDICATOR") or hashlib.md5(slug.encode("utf-8")).hexdigest()


def build_payload(args: argparse.Namespace) -> dict:
    return {
        "targetLanguage": args.target_language,
        "nativeLanguage": args.native_language,
        "currentLevel": args.current_level,
        "goal": args.goal,
        "deadline": args.deadline,
        "dailyMinutes": args.daily_minutes,
        "interests": args.interests or args.question,
        "sampleAnswer": args.sample_answer,
        "day": args.day,
        "focus": args.focus,
    }


def compact_payload(payload: dict) -> dict:
    return {key: value for key, value in payload.items() if value not in (None, "", [])}


def create_order(kind: str, payload: dict) -> dict:
    base_url = os.environ.get("LANGUAGE_SPRINT_API_BASE_URL") or os.environ.get("APP_BASE_URL")
    if not base_url:
        base_url = DEFAULT_API_BASE_URL
    url = f"{base_url.rstrip('/')}/api/language-sprint/{kind}"
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        response_text = error.read().decode("utf-8")
        if error.code == 402:
            return json.loads(response_text)
        raise RuntimeError(f"HTTP {error.code}: {response_text}") from error
    except urllib.error.URLError as error:
        raise RuntimeError(f"Order creation request failed: {error}") from error


def main() -> int:
    load_env_file()
    parser = argparse.ArgumentParser(description="Create a ClawTip order for Multilingual Learning Sprint")
    parser.add_argument("question", help="Learner request or interest profile")
    parser.add_argument("--kind", choices=["placement", "lesson", "quiz"], default="placement")
    parser.add_argument("--target-language", default="English")
    parser.add_argument("--native-language", default="Chinese")
    parser.add_argument("--current-level", default="unknown")
    parser.add_argument("--goal", default="conversation")
    parser.add_argument("--deadline", default="30 days")
    parser.add_argument("--daily-minutes", type=int, default=20)
    parser.add_argument("--interests", default="")
    parser.add_argument("--sample-answer", default="")
    parser.add_argument("--day", type=int)
    parser.add_argument("--focus", default="")
    args = parser.parse_args()

    indicator = compute_indicator(SLUG)
    request_payload = compact_payload(build_payload(args))

    try:
        response = create_order(args.kind, request_payload)
        clawtip = response.get("clawtip") or {}
        order = clawtip.get("order")
        order_no = response.get("orderNo")
        product = response.get("product") or {}
        amount = product.get("amountFen") or (order or {}).get("amount")
        if not order or not order_no or not amount:
            raise RuntimeError("API response missing clawtip.order, orderNo, or product.amountFen")
        order["question"] = args.question
        order["languageSprintKind"] = args.kind
        order["languageSprintRequest"] = request_payload
        save_order(indicator, order_no, order)
    except Exception as error:
        print(f"订单创建失败: {error}")
        return 1

    print(f"ORDER_NO={order_no}")
    print(f"AMOUNT={amount}")
    print(f"QUESTION={args.question}")
    print(f"INDICATOR={indicator}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
