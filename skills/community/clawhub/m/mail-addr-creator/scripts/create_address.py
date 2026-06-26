#!/usr/bin/env python3
import argparse
import csv
import json
import os
import re
import socket
import sys
from io import StringIO
from pathlib import Path
from typing import Iterable, Optional
from urllib import error, request


DEFAULT_API_URL = "https://mail-api.suilong.online/admin/new_address"
DEFAULT_DOMAIN = "suilong.online"

ENV_ADMIN_AUTH = "CLOUDFLARE_MAIL_ADMIN_AUTH"
ENV_BEARER_TOKEN = "CLOUDFLARE_MAIL_BEARER_TOKEN"
ENV_FINGERPRINT = "CLOUDFLARE_MAIL_FINGERPRINT"
ENV_LANG = "CLOUDFLARE_MAIL_LANG"
ENV_USER_TOKEN = "CLOUDFLARE_MAIL_USER_TOKEN"
ENV_API_URL = "CLOUDFLARE_MAIL_API_URL"

NAME_RE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9._-]{0,62}[A-Za-z0-9])?$")
DOMAIN_RE = re.compile(
    r"^(?=.{1,253}$)(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+[A-Za-z]{2,63}$"
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create Cloudflare temporary mail addresses through the admin API."
    )
    parser.add_argument("--name", help="Single mailbox name or full email address.")
    parser.add_argument("--names", help="Comma-separated mailbox names.")
    parser.add_argument("--names-file", help="Path to a text file containing one name per line.")
    parser.add_argument(
        "--domain",
        default=DEFAULT_DOMAIN,
        help=f"Mailbox domain. Defaults to {DEFAULT_DOMAIN}.",
    )
    parser.add_argument(
        "--enable-prefix",
        default="true",
        help="Whether enablePrefix should be true or false. Defaults to true.",
    )
    parser.add_argument("--admin-auth", help="Value for the x-admin-auth header.")
    parser.add_argument("--bearer-token", help="Bearer token without or with the Bearer prefix.")
    parser.add_argument("--fingerprint", help="Optional x-fingerprint header.")
    parser.add_argument("--lang", help="Optional x-lang header.")
    parser.add_argument("--user-token", help="Optional x-user-token header.")
    parser.add_argument(
        "--api-url",
        default=os.getenv(ENV_API_URL, DEFAULT_API_URL),
        help=f"Admin API URL. Defaults to {DEFAULT_API_URL}.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=15.0,
        help="Request timeout in seconds. Defaults to 15.",
    )
    parser.add_argument(
        "--output-format",
        choices=("json", "csv"),
        default="json",
        help="Output format. Defaults to json.",
    )
    parser.add_argument(
        "--output-file",
        help="Optional path to write the formatted output.",
    )
    return parser


def parse_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return True
    normalized = str(value).strip().lower()
    if normalized in {"1", "true", "t", "yes", "y", "on"}:
        return True
    if normalized in {"0", "false", "f", "no", "n", "off"}:
        return False
    raise ValueError(f"invalid boolean value: {value}")


def normalize_name(raw_name: Optional[str]) -> tuple[Optional[str], Optional[str]]:
    if raw_name is None:
        return None, "name is required"

    name = raw_name.strip()
    if not name:
        return None, "name is required"
    if len(name) > 64:
        return None, "name is too long"
    if ".." in name:
        return None, "name cannot contain consecutive dots"
    if not NAME_RE.match(name):
        return None, "name contains invalid characters"
    return name, None


def normalize_domain(raw_domain: Optional[str]) -> tuple[Optional[str], Optional[str]]:
    if raw_domain is None:
        return None, "domain is required"

    domain = raw_domain.strip().lower()
    if not domain:
        return None, "domain is required"
    if domain.endswith("."):
        domain = domain[:-1]
    if not DOMAIN_RE.match(domain):
        return None, "domain is invalid"
    return domain, None


def split_address_input(raw_name: Optional[str], raw_domain: Optional[str]) -> tuple[Optional[str], Optional[str], Optional[str]]:
    if raw_name is None:
        return raw_name, raw_domain, None

    candidate = raw_name.strip()
    if "@" not in candidate:
        return candidate, raw_domain, None

    if candidate.count("@") != 1:
        return None, raw_domain, "email address is invalid"

    local_part, domain_part = candidate.split("@", 1)
    if not local_part or not domain_part:
        return None, raw_domain, "email address is invalid"

    if raw_domain and raw_domain.strip():
        normalized_supplied = raw_domain.strip().lower().rstrip(".")
        normalized_address = domain_part.strip().lower().rstrip(".")
        if normalized_supplied != normalized_address:
            return None, raw_domain, "name contains a full address that conflicts with the supplied domain"
        return local_part, normalized_supplied, None

    return local_part, domain_part, None


def error_result(status: str, message: str, address: Optional[str] = None, name: Optional[str] = None) -> dict:
    payload = {
        "status": status,
        "address": address,
        "jwt": None,
        "password": None,
        "error": message,
    }
    if name is not None:
        payload["name"] = name
    return payload


def success_result(data: dict, fallback_address: str, name: Optional[str] = None) -> dict:
    payload = {
        "status": "created",
        "address": data.get("address") or fallback_address,
        "jwt": data.get("jwt"),
        "password": data.get("password"),
        "error": None,
    }
    if name is not None:
        payload["name"] = name
    return payload


def load_json_bytes(raw_bytes: bytes) -> Optional[dict]:
    if not raw_bytes:
        return None
    try:
        decoded = raw_bytes.decode("utf-8")
        payload = json.loads(decoded)
        return payload if isinstance(payload, dict) else None
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None


def extract_error_message(status_code: Optional[int], raw_bytes: bytes, fallback: str) -> str:
    payload = load_json_bytes(raw_bytes)
    if payload:
        for key in ("error", "message", "detail"):
            value = payload.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
    body_text = raw_bytes.decode("utf-8", errors="replace").strip()
    if body_text:
        return body_text
    if status_code is not None:
        return f"http {status_code}: {fallback}"
    return fallback


def classify_error(status_code: Optional[int], message: str) -> str:
    normalized = message.lower()
    if status_code in {401, 403}:
        return "auth_error"
    if status_code == 409:
        return "already_exists"
    if any(token in normalized for token in ("already exists", "already exist", "duplicate", "has been taken")):
        return "already_exists"
    if any(token in normalized for token in ("unauthorized", "forbidden", "auth", "token", "credential")):
        return "auth_error"
    return "error"


def build_headers(args: argparse.Namespace) -> tuple[Optional[dict], Optional[str]]:
    admin_auth = args.admin_auth or os.getenv(ENV_ADMIN_AUTH)
    if not admin_auth:
        return None, f"missing admin credential: provide --admin-auth or {ENV_ADMIN_AUTH}"

    headers = {
        "Content-Type": "application/json",
        "x-admin-auth": admin_auth,
    }

    bearer_token = args.bearer_token or os.getenv(ENV_BEARER_TOKEN)
    if bearer_token:
        token = bearer_token.strip()
        headers["Authorization"] = token if token.lower().startswith("bearer ") else f"Bearer {token}"

    fingerprint = args.fingerprint or os.getenv(ENV_FINGERPRINT)
    if fingerprint:
        headers["x-fingerprint"] = fingerprint

    lang = args.lang or os.getenv(ENV_LANG)
    if lang:
        headers["x-lang"] = lang

    user_token = args.user_token or os.getenv(ENV_USER_TOKEN)
    if user_token:
        headers["x-user-token"] = user_token

    return headers, None


def call_create_address(
    api_url: str,
    headers: dict,
    timeout: float,
    name: str,
    domain: str,
    enable_prefix: bool,
) -> dict:
    address = f"{name}@{domain}"
    body = json.dumps(
        {
            "enablePrefix": enable_prefix,
            "name": name,
            "domain": domain,
        }
    ).encode("utf-8")
    req = request.Request(api_url, data=body, headers=headers, method="POST")

    try:
        with request.urlopen(req, timeout=timeout) as response:
            raw_bytes = response.read()
            payload = load_json_bytes(raw_bytes)
            if payload is None:
                return error_result("error", "server returned a non-JSON success response", address=address, name=name)
            return success_result(payload, fallback_address=address, name=name)
    except error.HTTPError as exc:
        raw_bytes = exc.read()
        message = extract_error_message(exc.code, raw_bytes, exc.reason or "request failed")
        status = classify_error(exc.code, message)
        return error_result(status, message, address=address, name=name)
    except error.URLError as exc:
        reason = exc.reason
        if isinstance(reason, socket.timeout):
            message = "network error: request timed out"
        else:
            message = f"network error: {reason}"
        return error_result("error", message, address=address, name=name)
    except TimeoutError:
        return error_result("error", "network error: request timed out", address=address, name=name)
    except Exception as exc:  # pragma: no cover - defensive fallback
        return error_result("error", f"unexpected error: {exc}", address=address, name=name)


def read_names_from_file(path_value: str) -> tuple[list[str], Optional[str]]:
    path = Path(path_value)
    if not path.is_file():
        return [], f"names file not found: {path}"
    content = path.read_text(encoding="utf-8")
    return content.splitlines(), None


def gather_batch_inputs(args: argparse.Namespace) -> tuple[list[str], Optional[str]]:
    raw_names: list[str] = []

    if args.names:
        raw_names.extend(args.names.split(","))

    if args.names_file:
        file_names, file_error = read_names_from_file(args.names_file)
        if file_error:
            return [], file_error
        raw_names.extend(file_names)

    return raw_names, None


def unique_non_empty(values: Iterable[str]) -> list[str]:
    seen = set()
    unique_values: list[str] = []
    for value in values:
        trimmed = value.strip()
        if not trimmed:
            continue
        key = trimmed.lower()
        if key in seen:
            continue
        seen.add(key)
        unique_values.append(trimmed)
    return unique_values


def summarize_results(results: list[dict]) -> dict:
    created = sum(1 for item in results if item["status"] == "created")
    already_exists = sum(1 for item in results if item["status"] == "already_exists")
    failed = sum(1 for item in results if item["status"] not in {"created", "already_exists"})
    return {
        "requested": len(results),
        "created": created,
        "already_exists": already_exists,
        "failed": failed,
    }


def json_text(payload: dict) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2)


def csv_text(payload: dict) -> str:
    buffer = StringIO()
    fieldnames = [
        "row_type",
        "requested",
        "created",
        "already_exists",
        "failed",
        "name",
        "status",
        "address",
        "jwt",
        "password",
        "error",
    ]
    writer = csv.DictWriter(buffer, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()

    if "summary" in payload and "results" in payload:
        summary = payload.get("summary", {})
        writer.writerow(
            {
                "row_type": "summary",
                "requested": summary.get("requested", 0),
                "created": summary.get("created", 0),
                "already_exists": summary.get("already_exists", 0),
                "failed": summary.get("failed", 0),
            }
        )
        for item in payload.get("results", []):
            writer.writerow(
                {
                    "row_type": "result",
                    "name": item.get("name") or "",
                    "status": item.get("status") or "",
                    "address": item.get("address") or "",
                    "jwt": item.get("jwt") or "",
                    "password": item.get("password") or "",
                    "error": item.get("error") or "",
                }
            )
    else:
        writer.writerow(
            {
                "row_type": "result",
                "status": payload.get("status") or "",
                "address": payload.get("address") or "",
                "jwt": payload.get("jwt") or "",
                "password": payload.get("password") or "",
                "error": payload.get("error") or "",
            }
        )

    return buffer.getvalue()


def emit_output(payload: dict, output_format: str, output_file: Optional[str]) -> None:
    rendered = json_text(payload) if output_format == "json" else csv_text(payload)
    if output_file:
        path = Path(output_file)
        if path.parent and not path.parent.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered, encoding="utf-8", newline="")
    print(rendered, end="" if rendered.endswith("\n") else "\n")


def single_mode(args: argparse.Namespace) -> int:
    split_name, split_domain, split_error = split_address_input(args.name, args.domain)
    if split_error:
        emit_output(error_result("error", split_error), args.output_format, args.output_file)
        return 1

    name, name_error = normalize_name(split_name)
    if name_error:
        emit_output(error_result("error", name_error), args.output_format, args.output_file)
        return 1

    domain, domain_error = normalize_domain(split_domain)
    if domain_error:
        emit_output(error_result("error", domain_error), args.output_format, args.output_file)
        return 1

    try:
        enable_prefix = parse_bool(args.enable_prefix)
    except ValueError as exc:
        emit_output(
            error_result("error", str(exc), address=f"{name}@{domain}"),
            args.output_format,
            args.output_file,
        )
        return 1

    headers, header_error = build_headers(args)
    if header_error:
        emit_output(
            error_result("auth_error", header_error, address=f"{name}@{domain}"),
            args.output_format,
            args.output_file,
        )
        return 1

    result = call_create_address(args.api_url, headers, args.timeout, name, domain, enable_prefix)
    result.pop("name", None)
    emit_output(result, args.output_format, args.output_file)
    return 0 if result["status"] in {"created", "already_exists"} else 1


def batch_mode(args: argparse.Namespace) -> int:
    raw_names, names_error = gather_batch_inputs(args)
    if names_error:
        payload = {
            "summary": {"requested": 0, "created": 0, "already_exists": 0, "failed": 1},
            "results": [error_result("error", names_error, name=None)],
        }
        emit_output(payload, args.output_format, args.output_file)
        return 1

    unique_names = unique_non_empty(raw_names)
    if not unique_names:
        payload = {
            "summary": {"requested": 0, "created": 0, "already_exists": 0, "failed": 1},
            "results": [],
            "error": "no valid names were provided",
        }
        emit_output(payload, args.output_format, args.output_file)
        return 1

    domain, domain_error = normalize_domain(args.domain)
    if domain_error:
        results = [
            error_result("error", domain_error, address=None, name=raw_name)
            for raw_name in unique_names
        ]
        emit_output(
            {"summary": summarize_results(results), "results": results},
            args.output_format,
            args.output_file,
        )
        return 1

    try:
        enable_prefix = parse_bool(args.enable_prefix)
    except ValueError as exc:
        results = [
            error_result("error", str(exc), address=f"{raw_name}@{domain}", name=raw_name)
            for raw_name in unique_names
        ]
        emit_output(
            {"summary": summarize_results(results), "results": results},
            args.output_format,
            args.output_file,
        )
        return 1

    normalized_entries: list[tuple[str, Optional[str], Optional[str]]] = []
    for raw_name in unique_names:
        normalized_name, name_error = normalize_name(raw_name)
        normalized_entries.append((raw_name, normalized_name, name_error))

    headers, header_error = build_headers(args)
    if header_error:
        results = []
        for raw_name, normalized_name, name_error in normalized_entries:
            if name_error:
                results.append(
                    error_result("error", name_error, address=f"{raw_name}@{domain}", name=raw_name)
                )
                continue
            results.append(
                error_result(
                    "auth_error",
                    header_error,
                    address=f"{normalized_name}@{domain}",
                    name=raw_name,
                )
            )
        emit_output(
            {"summary": summarize_results(results), "results": results},
            args.output_format,
            args.output_file,
        )
        return 1

    results: list[dict] = []
    for raw_name, normalized_name, name_error in normalized_entries:
        if name_error:
            results.append(
                error_result("error", name_error, address=f"{raw_name}@{domain}", name=raw_name)
            )
            continue

        assert normalized_name is not None
        result = call_create_address(
            api_url=args.api_url,
            headers=headers,
            timeout=args.timeout,
            name=normalized_name,
            domain=domain,
            enable_prefix=enable_prefix,
        )
        if result.get("name") != raw_name:
            result["name"] = raw_name
        results.append(result)

    payload = {
        "summary": summarize_results(results),
        "results": results,
    }
    emit_output(payload, args.output_format, args.output_file)
    return 0 if payload["summary"]["failed"] == 0 else 1


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    has_single = bool(args.name)
    has_batch = bool(args.names or args.names_file)

    if has_single and has_batch:
        emit_output(
            error_result("error", "use either --name or batch inputs, not both"),
            args.output_format,
            args.output_file,
        )
        return 1
    if not has_single and not has_batch:
        emit_output(
            error_result("error", "provide --name, --names, or --names-file"),
            args.output_format,
            args.output_file,
        )
        return 1

    if has_single:
        return single_mode(args)
    return batch_mode(args)


if __name__ == "__main__":
    sys.exit(main())
