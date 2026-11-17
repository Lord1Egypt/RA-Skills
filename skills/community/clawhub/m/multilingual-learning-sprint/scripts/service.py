import argparse
import hashlib
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

from file_utils import load_order

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


def default_payload(order_data: dict) -> dict:
    return {
        "targetLanguage": "English",
        "nativeLanguage": "Chinese",
        "currentLevel": "unknown",
        "goal": "conversation",
        "deadline": "30 days",
        "dailyMinutes": 20,
        "interests": order_data.get("question") or "daily life",
    }


def call_service(order_no: str, order_data: dict) -> dict:
    credential = order_data.get("payCredential")
    if not credential:
        raise RuntimeError("订单文件中缺少 payCredential 字段")

    kind = order_data.get("languageSprintKind") or "placement"
    payload = order_data.get("languageSprintRequest") or default_payload(order_data)
    resource_url = order_data.get("resource_url") or order_data.get("resourceUrl")
    if resource_url:
        url = resource_url
    else:
        base_url = os.environ.get("LANGUAGE_SPRINT_API_BASE_URL") or os.environ.get("APP_BASE_URL")
        if not base_url:
            base_url = DEFAULT_API_BASE_URL
        url = f"{base_url.rstrip('/')}/api/language-sprint/{kind}"

    request = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "X-Language-Sprint-Order-No": order_no,
            "X-ClawTip-Pay-Credential": credential,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        response_text = error.read().decode("utf-8")
        raise RuntimeError(f"HTTP {error.code}: {response_text}") from error
    except urllib.error.URLError as error:
        raise RuntimeError(f"Service request failed: {error}") from error


def main() -> int:
    load_env_file()
    parser = argparse.ArgumentParser(description="Fulfill a paid Multilingual Learning Sprint order")
    parser.add_argument("order_no", help="ClawTip order number")
    args = parser.parse_args()

    try:
        indicator = compute_indicator(SLUG)
        order_data = load_order(indicator, args.order_no)
        result = call_service(args.order_no, order_data)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as error:
        print(f"ERROR: {error}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
