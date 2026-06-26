#!/usr/bin/env python
import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


DEFAULT_TIMEOUT = 60
SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_CONFIG_PATH = SCRIPT_DIR.parent / "config.json"


def parse_bool(value: str) -> bool:
    lowered = value.strip().lower()
    if lowered in {"1", "true", "yes", "y", "on"}:
        return True
    if lowered in {"0", "false", "no", "n", "off"}:
        return False
    raise argparse.ArgumentTypeError(f"invalid boolean value: {value}")


def build_endpoint(base_url: str) -> str:
    base = base_url.rstrip("/")
    if base.endswith("/api/v1"):
        return f"{base}/librag/knowbase/recall"
    if base.endswith("/api"):
        return f"{base}/v1/librag/knowbase/recall"
    return f"{base}/api/v1/librag/knowbase/recall"


def load_config(config_path: Path) -> dict[str, Any]:
    if not config_path.exists():
        raise SystemExit(f"Missing config file: {config_path}")
    try:
        return json.loads(config_path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON config: {config_path}") from exc


def get_required_config(config: dict[str, Any], name: str) -> str:
    value = str(config.get(name, "")).strip()
    if not value:
        raise SystemExit(f"Missing required config field: {name}")
    return value


def get_config_value(config: dict[str, Any], name: str, default: Any) -> Any:
    value = config.get(name)
    if value is None or value == "":
        return default
    return value


def get_int(cli_value: int | None, config: dict[str, Any], name: str, default: int | None = None) -> int:
    if cli_value is not None:
        return cli_value
    raw = get_config_value(config, name, default)
    if raw is None or str(raw).strip() == "":
        raise SystemExit(f"Missing required config field: {name}")
    try:
        return int(raw)
    except ValueError as exc:
        raise SystemExit(f"Config field {name} must be an integer") from exc


def get_float(cli_value: float | None, config: dict[str, Any], name: str, default: float) -> float:
    if cli_value is not None:
        return cli_value
    raw = get_config_value(config, name, default)
    try:
        return float(raw)
    except ValueError as exc:
        raise SystemExit(f"Config field {name} must be a number") from exc


def get_bool(cli_value: bool | None, config: dict[str, Any], name: str, default: bool) -> bool:
    if cli_value is not None:
        return cli_value
    raw = get_config_value(config, name, default)
    if isinstance(raw, bool):
        return raw
    return parse_bool(str(raw))


def get_choice(cli_value: str | None, config: dict[str, Any], name: str, default: str, choices: set[str]) -> str:
    value = cli_value if cli_value is not None else str(get_config_value(config, name, default)).strip()
    if value not in choices:
        raise SystemExit(f"Config field {name} must be one of: {', '.join(sorted(choices))}")
    return value


def derive_summary(data: Any) -> dict[str, Any]:
    if isinstance(data, list):
        result_shape = "list"
        item_count = len(data)
        if data and isinstance(data[0], dict) and "paragraphs" in data[0]:
            result_shape = "tree"
        return {
            "result_shape": result_shape,
            "item_count": item_count,
        }
    if isinstance(data, dict):
        return {
            "result_shape": "object",
            "item_count": len(data),
        }
    return {
        "result_shape": type(data).__name__,
        "item_count": None,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Call LibRAG recall API and print normalized JSON.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH), help="Path to skill config JSON")
    parser.add_argument("--kb-id", type=int, required=False, help="Target knowledge base id. Defaults to config.json kb_id")
    parser.add_argument("--question", required=True, help="Recall question")
    parser.add_argument("--recall-mode", default=None, choices=["reasoning", "hybrid", "vector"], help="Recall mode")
    parser.add_argument("--vector-top-k", type=int, default=None, help="Vector top_k")
    parser.add_argument("--fulltext-top-k", type=int, default=None, help="Fulltext top_k")
    parser.add_argument("--return-tree", type=parse_bool, default=None, help="Return tree output")
    parser.add_argument("--has-source-text", type=parse_bool, default=None, help="Include source text")
    parser.add_argument("--has-score", type=parse_bool, default=None, help="Include score")
    parser.add_argument("--filter-effective", type=parse_bool, default=None, help="Filter ineffective results")
    parser.add_argument("--reasoning-enhance", type=parse_bool, default=None, help="Enable reasoning enhance")
    parser.add_argument("--score-threshold", type=float, default=None, help="Score threshold used for filtered scoring")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="HTTP timeout in seconds")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    args = parser.parse_args()

    config_path = Path(args.config).resolve()
    config = load_config(config_path)
    base_url = get_required_config(config, "base_url")
    api_key = get_required_config(config, "api_key")
    kb_id = get_int(args.kb_id, config, "kb_id")
    endpoint = build_endpoint(base_url)

    params = {
        "kb_id": kb_id,
        "question": args.question,
        "recall_mode": get_choice(args.recall_mode, config, "recall_mode", "hybrid", {"reasoning", "hybrid", "vector"}),
        "streaming": "false",
        "return_tree": str(get_bool(args.return_tree, config, "return_tree", True)).lower(),
        "has_source_text": str(get_bool(args.has_source_text, config, "has_source_text", True)).lower(),
        "has_score": str(get_bool(args.has_score, config, "has_score", True)).lower(),
        "filter_effective": str(get_bool(args.filter_effective, config, "filter_effective", True)).lower(),
        "vector_top_k": get_int(args.vector_top_k, config, "vector_top_k", 20),
        "fulltext_top_k": get_int(args.fulltext_top_k, config, "fulltext_top_k", 20),
        "reasoning_enhance": str(get_bool(args.reasoning_enhance, config, "reasoning_enhance", True)).lower(),
        "score_threshold": get_float(args.score_threshold, config, "score_threshold", 0.0),
    }

    request = urllib.request.Request(
        url=f"{endpoint}?{urllib.parse.urlencode(params)}",
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="GET",
    )

    try:
        with urllib.request.urlopen(request, timeout=args.timeout) as response:
            body = response.read().decode("utf-8")
            payload = json.loads(body)
            result = {
                "config_path": str(config_path),
                "request": params,
                "response": payload,
                "summary": derive_summary(payload.get("data")),
            }
            print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None))
            return 0
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(error_body)
        except json.JSONDecodeError:
            parsed = {"detail": error_body}
        result = {
            "config_path": str(config_path),
            "request": params,
            "error": {
                "status": exc.code,
                "detail": parsed,
            },
        }
        print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None), file=sys.stderr)
        return 1
    except urllib.error.URLError as exc:
        result = {
            "config_path": str(config_path),
            "request": params,
            "error": {
                "status": None,
                "detail": str(exc.reason),
            },
        }
        print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
