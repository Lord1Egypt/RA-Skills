import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from time import perf_counter

import requests


ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = ROOT / "logs"
DEFAULT_TIMEOUT = 20
DEFAULT_MAX_BODY = 4000
SENSITIVE_HEADERS = {"authorization", "cookie", "set-cookie", "x-api-key", "proxy-authorization"}


def parse_json_object(value: str | None, field_name: str):
    if not value:
        return None
    try:
        data = json.loads(value)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"{field_name} 不是合法 JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit(f"{field_name} 必须是 JSON 对象")
    return data


def redact_headers(headers: dict | None):
    if not headers:
        return None
    redacted = {}
    for k, v in headers.items():
        if k.lower() in SENSITIVE_HEADERS:
            redacted[k] = "<redacted>"
        else:
            redacted[k] = v
    return redacted


def build_log_record(args, response=None, error=None, duration_ms=0):
    record = {
        "ts": datetime.now().astimezone().isoformat(timespec="seconds"),
        "method": args.method.upper(),
        "url": args.url,
        "status": response.status_code if response is not None else None,
        "ok": bool(response is not None and response.ok),
        "duration_ms": round(duration_ms, 2),
        "response_bytes": len(response.content) if response is not None else 0,
        "error": error,
    }
    return record


def write_log(record: dict):
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOG_DIR / f"{datetime.now().date().isoformat()}.jsonl"
    with log_file.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def format_body(response: requests.Response, max_body: int):
    text = response.text
    if len(text) > max_body:
        return text[:max_body] + f"\n...[truncated, total {len(text)} chars]"
    return text


def main():
    parser = argparse.ArgumentParser(description="Send HTTP requests with Python requests")
    parser.add_argument("--method", required=True, choices=["GET", "POST", "PUT", "DELETE", "get", "post", "put", "delete"])
    parser.add_argument("--url", required=True)
    parser.add_argument("--headers")
    parser.add_argument("--params")
    parser.add_argument("--json")
    parser.add_argument("--data")
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT)
    parser.add_argument("--show-headers", action="store_true")
    parser.add_argument("--max-body", type=int, default=DEFAULT_MAX_BODY)
    parser.add_argument("--no-log", action="store_true")
    args = parser.parse_args()

    headers = parse_json_object(args.headers, "headers")
    params = parse_json_object(args.params, "params")
    json_body = parse_json_object(args.json, "json")
    data_body = parse_json_object(args.data, "data")

    if json_body is not None and data_body is not None:
        raise SystemExit("--json 和 --data 不能同时使用")

    started = perf_counter()
    response = None
    error = None

    try:
        response = requests.request(
            method=args.method.upper(),
            url=args.url,
            headers=headers,
            params=params,
            json=json_body,
            data=data_body,
            timeout=args.timeout,
        )
        duration_ms = (perf_counter() - started) * 1000

        print(f"METHOD: {args.method.upper()}")
        print(f"URL: {response.url}")
        print(f"STATUS: {response.status_code}")
        print(f"OK: {response.ok}")
        print(f"ELAPSED_MS: {round(duration_ms, 2)}")

        if args.show_headers:
            print("HEADERS:")
            print(json.dumps(dict(response.headers), ensure_ascii=False, indent=2))

        print("BODY:")
        print(format_body(response, args.max_body))

    except requests.RequestException as exc:
        duration_ms = (perf_counter() - started) * 1000
        error = f"{type(exc).__name__}: {exc}"
        print(f"METHOD: {args.method.upper()}")
        print(f"URL: {args.url}")
        print("STATUS: REQUEST_FAILED")
        print("OK: False")
        print(f"ELAPSED_MS: {round(duration_ms, 2)}")
        print("ERROR:")
        print(error)
        if not args.no_log:
            write_log(build_log_record(args, response=None, error=error, duration_ms=duration_ms))
        sys.exit(1)

    if not args.no_log:
        write_log(build_log_record(args, response=response, error=error, duration_ms=duration_ms))


if __name__ == "__main__":
    main()
