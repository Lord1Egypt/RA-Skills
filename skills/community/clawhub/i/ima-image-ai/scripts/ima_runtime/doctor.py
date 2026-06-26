from __future__ import annotations

import argparse
import importlib
import importlib.util
import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path

from ima_runtime.shared.config import (
    DEFAULT_BASE_URL,
    DEFAULT_MODEL_BY_TASK_TYPE,
    DEFAULT_MODEL_LABEL_BY_TASK_TYPE,
    DEFAULT_MODEL_RECOMMENDATION_BY_TASK_TYPE,
)
from ima_runtime.shared.errors import extract_error_info


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="IMA Image AI Doctor — verify local setup and basic API access",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--api-key", required=False, help="IMA Open API key. Can also use IMA_API_KEY env var")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="API base URL")
    parser.add_argument("--language", default="en", help="Language for product labels (en/zh)")
    parser.add_argument("--output-json", action="store_true", help="Output doctor report as JSON")
    return parser


def _load_requests_module():
    if importlib.util.find_spec("requests") is None:
        return None
    return importlib.import_module("requests")


def _requests_info() -> dict:
    requests_module = _load_requests_module()
    if requests_module is None:
        return {
            "ok": False,
            "version": None,
            "message": "requests is not installed.",
        }
    return {
        "ok": True,
        "version": requests_module.__version__,
        "message": "requests is installed.",
    }


def _get_product_list_func():
    client_module = importlib.import_module("ima_runtime.shared.client")
    return client_module.get_product_list


def _run_cli_list_models_smoke(base_url: str, api_key: str, language: str) -> dict:
    entrypoint = Path(__file__).resolve().parents[1] / "ima_runtime_cli.py"
    env = os.environ.copy()
    env["IMA_API_KEY"] = api_key
    result = subprocess.run(
        [
            sys.executable,
            str(entrypoint),
            "--task-type",
            "text_to_image",
            "--list-models",
            "--output-json",
            "--base-url",
            base_url,
            "--language",
            language,
        ],
        capture_output=True,
        text=True,
        env=env,
    )
    if result.returncode != 0:
        return {
            "status": "error",
            "message": (result.stderr or result.stdout).strip() or "CLI smoke failed.",
        }
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        return {
            "status": "error",
            "message": f"CLI smoke returned invalid JSON: {exc}",
        }
    return {
        "status": "ok",
        "model_count": len(payload) if isinstance(payload, list) else 0,
    }


def _get_product_list_with_retry(
    base_url: str,
    api_key: str,
    category: str,
    language: str,
    attempts: int = 5,
    delay_seconds: float = 0.1,
) -> list:
    last_error: Exception | None = None
    get_product_list = _get_product_list_func()
    for attempt in range(1, attempts + 1):
        try:
            return get_product_list(base_url, api_key, category, language=language)
        except Exception as exc:
            last_error = exc
            if attempt == attempts:
                raise
            time.sleep(delay_seconds)
    assert last_error is not None
    raise last_error


def collect_diagnostics(api_key: str | None, base_url: str, language: str, include_network: bool = True) -> dict:
    requests_info = _requests_info()
    report = {
        "python": {
            "ok": True,
            "version": platform.python_version(),
        },
        "requests": requests_info,
        "api_key": {
            "ok": bool(api_key),
            "source": "env_or_flag" if api_key else "missing",
            "message": "IMA_API_KEY detected." if api_key else "IMA_API_KEY is missing.",
        },
        "network": {
            "status": "skipped",
            "task_types": {},
        },
        "recommended_defaults": {
            task_type: {
                "model_id": model_id,
                "label": DEFAULT_MODEL_LABEL_BY_TASK_TYPE[task_type],
                "summary": DEFAULT_MODEL_RECOMMENDATION_BY_TASK_TYPE.get(task_type, {}).get("summary"),
                "features": list(DEFAULT_MODEL_RECOMMENDATION_BY_TASK_TYPE.get(task_type, {}).get("features", ())),
            }
            for task_type, model_id in DEFAULT_MODEL_BY_TASK_TYPE.items()
        },
    }

    if not api_key or not include_network or not requests_info["ok"]:
        return report

    network_report: dict[str, object] = {"status": "ok", "task_types": {}}
    ok_task_types = 0
    for task_type in ("text_to_image", "image_to_image"):
        try:
            tree = _get_product_list_with_retry(base_url, api_key, task_type, language=language)
            network_report["task_types"][task_type] = {
                "status": "ok",
                "model_count": len(tree),
            }
            ok_task_types += 1
        except Exception as exc:
            error_info = extract_error_info(exc)
            network_report["task_types"][task_type] = {
                "status": "error",
                "message": error_info.get("message", str(exc)),
            }
    if ok_task_types == 0:
        fallback = _run_cli_list_models_smoke(base_url, api_key, language)
        network_report["fallback"] = fallback
        if fallback["status"] == "ok":
            network_report["status"] = "degraded"
        else:
            network_report["status"] = "error"
    elif ok_task_types < 2:
        network_report["status"] = "degraded"
    report["network"] = network_report
    return report


def _print_text_report(report: dict) -> None:
    print("IMA Image AI Doctor")
    print(f"Python: OK ({report['python']['version']})")
    requests_status = "OK" if report["requests"]["ok"] else "MISSING"
    requests_detail = report["requests"]["version"] or report["requests"]["message"]
    print(f"requests: {requests_status} ({requests_detail})")
    api_key_status = "OK" if report["api_key"]["ok"] else "MISSING"
    print(f"API key: {api_key_status} ({report['api_key']['message']})")
    print("Recommended defaults:")
    for task_type, info in report["recommended_defaults"].items():
        print(f"  - {task_type}: {info['label']} ({info['model_id']})")
        if info.get("summary"):
            print(f"    {info['summary']}")
    print(f"Network: {report['network']['status']}")
    for task_type, info in report["network"]["task_types"].items():
        if info["status"] == "ok":
            print(f"  - {task_type}: OK ({info['model_count']} model groups returned)")
        else:
            print(f"  - {task_type}: ERROR ({info['message']})")
    if report["network"].get("fallback"):
        fallback = report["network"]["fallback"]
        if fallback["status"] == "ok":
            print(f"  - fallback-cli: OK ({fallback['model_count']} model rows returned)")
        else:
            print(f"  - fallback-cli: ERROR ({fallback['message']})")


def run_doctor(api_key: str | None, base_url: str, language: str, output_json: bool) -> int:
    report = collect_diagnostics(api_key=api_key, base_url=base_url, language=language)
    success = (
        bool(report["api_key"]["ok"])
        and bool(report["requests"]["ok"])
    )
    if output_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if success else 1

    _print_text_report(report)
    return 0 if success else 1


def main() -> int:
    args = build_parser().parse_args()
    api_key = args.api_key or os.getenv("IMA_API_KEY")
    return run_doctor(
        api_key=api_key,
        base_url=args.base_url,
        language=args.language,
        output_json=args.output_json,
    )


if __name__ == "__main__":
    sys.exit(main())
