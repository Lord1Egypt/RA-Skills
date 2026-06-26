#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import mimetypes
import os
import pathlib
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Tuple

DEFAULT_API_VERSION = os.getenv("META_API_VERSION", "v25.0")
DEFAULT_GRAPH_BASE = os.getenv("META_GRAPH_BASE", "https://graph.facebook.com")
USER_AGENT = "meta-ads-control/1.0"

RETRIABLE_HTTP_STATUS = {429, 500, 502, 503, 504}
RETRIABLE_ERROR_CODES = {1, 2, 4, 17, 32, 341, 613, 80004}
WRITE_METHODS = {"POST", "PUT", "PATCH", "DELETE"}

EXIT_BAD_ARGS = 2
EXIT_AUTH = 3
EXIT_API = 4
EXIT_TIMEOUT = 5
EXIT_SAFETY = 6

OBJECT_TO_EDGE = {
    "campaign": "campaigns",
    "campaigns": "campaigns",
    "adset": "adsets",
    "adsets": "adsets",
    "ad": "ads",
    "ads": "ads",
    "adcreative": "adcreatives",
    "adcreatives": "adcreatives",
    "customaudience": "customaudiences",
    "customaudiences": "customaudiences",
    "saved_audience": "saved_audiences",
    "saved_audiences": "saved_audiences",
    "adimage": "adimages",
    "adimages": "adimages",
    "advideo": "advideos",
    "advideos": "advideos",
    "pixel": "adspixels",
    "pixels": "adspixels",
    "instagram_account": "instagram_accounts",
    "instagram_accounts": "instagram_accounts",
}

DEFAULT_LIST_FIELDS = {
    "campaigns": "id,name,objective,status,effective_status",
    "adsets": "id,name,campaign_id,status,effective_status,daily_budget,lifetime_budget,optimization_goal,bid_strategy",
    "ads": "id,name,adset_id,campaign_id,status,effective_status",
    "adcreatives": "id,name,effective_object_story_id,thumbnail_url",
    "customaudiences": "id,name,subtype,delivery_status,approximate_count_lower_bound,approximate_count_upper_bound",
    "adimages": "hash,name,url,permalink_url",
    "advideos": "id,title,status,created_time",
    "adspixels": "id,name,last_fired_time",
    "instagram_accounts": "id,username",
}

DEFAULT_ACCOUNT_FIELDS = "id,name,account_id,account_status,currency,timezone_name,amount_spent,spend_cap,business_name"
DEFAULT_ACCOUNTS_FIELDS = "id,account_id,name,account_status,currency,timezone_name"
DEFAULT_INSIGHTS_FIELDS = "account_id,account_name,campaign_id,campaign_name,adset_id,adset_name,ad_id,ad_name,impressions,reach,clicks,inline_link_clicks,spend,cpm,cpc,ctr,actions,action_values,purchase_roas"


class CliError(Exception):
    def __init__(self, message: str, exit_code: int = EXIT_BAD_ARGS, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.exit_code = exit_code
        self.details = details or {}


def eprint(*args: Any) -> None:
    print(*args, file=sys.stderr)


def normalise_account_id(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    value = str(value).strip()
    if not value:
        return None
    if value.startswith("act_"):
        return value
    if value.isdigit():
        return f"act_{value}"
    return value


def try_json_parse(text: str) -> Any:
    stripped = text.strip()
    if not stripped:
        return text
    if stripped[0] not in '{"[0123456789-ntf"':
        return text
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        return text


def load_json_or_text(path: str) -> Any:
    content = pathlib.Path(path).read_text(encoding="utf-8")
    parsed = try_json_parse(content)
    return parsed


def parse_value(raw: str) -> Any:
    if raw.startswith("@"):
        path = raw[1:]
        if not path:
            raise CliError("Expected a file path after '@' in a --set value.")
        return load_json_or_text(path)
    return try_json_parse(raw)


def deep_set(target: Dict[str, Any], dotted_key: str, value: Any) -> None:
    parts = dotted_key.split(".")
    cursor: Dict[str, Any] = target
    for part in parts[:-1]:
        existing = cursor.get(part)
        if existing is None:
            cursor[part] = {}
            existing = cursor[part]
        if not isinstance(existing, dict):
            raise CliError(f"Cannot set nested key '{dotted_key}' because '{part}' is not an object.")
        cursor = existing
    cursor[parts[-1]] = value


def merge_params(params_file: Optional[str], set_items: Optional[List[str]]) -> Dict[str, Any]:
    params: Dict[str, Any] = {}
    if params_file:
        loaded = load_json_or_text(params_file)
        if not isinstance(loaded, dict):
            raise CliError(f"Parameter file must contain a JSON object: {params_file}")
        params = loaded
    for item in set_items or []:
        if "=" not in item:
            raise CliError(f"--set values must use key=value syntax. Got: {item}")
        key, raw_value = item.split("=", 1)
        key = key.strip()
        if not key:
            raise CliError(f"Invalid --set key in '{item}'")
        deep_set(params, key, parse_value(raw_value))
    return params


def normalise_form_value(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (dict, list)):
        return json.dumps(value, separators=(",", ":"), ensure_ascii=False)
    return str(value)


def normalise_params(params: Optional[Dict[str, Any]]) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for key, value in (params or {}).items():
        rendered = normalise_form_value(value)
        if rendered is not None:
            out[key] = rendered
    return out


def append_query(url: str, params: Dict[str, str]) -> str:
    if not params:
        return url
    split = urllib.parse.urlsplit(url)
    existing = urllib.parse.parse_qsl(split.query, keep_blank_values=True)
    query = urllib.parse.urlencode(existing + list(params.items()))
    return urllib.parse.urlunsplit((split.scheme, split.netloc, split.path, query, split.fragment))


def guess_content_type(filename: str) -> str:
    guessed = mimetypes.guess_type(filename)[0]
    return guessed or "application/octet-stream"


def build_multipart(fields: Dict[str, str], files: Dict[str, Tuple[str, bytes, str]]) -> Tuple[bytes, str]:
    boundary = f"----metaads{uuid.uuid4().hex}"
    chunks: List[bytes] = []

    def add_line(line: str) -> None:
        chunks.append(line.encode("utf-8"))
        chunks.append(b"\r\n")

    for name, value in fields.items():
        add_line(f"--{boundary}")
        add_line(f'Content-Disposition: form-data; name="{name}"')
        add_line("")
        add_line(value)

    for field_name, (filename, file_bytes, content_type) in files.items():
        add_line(f"--{boundary}")
        add_line(
            f'Content-Disposition: form-data; name="{field_name}"; filename="{pathlib.Path(filename).name}"'
        )
        add_line(f"Content-Type: {content_type}")
        add_line("")
        chunks.append(file_bytes)
        chunks.append(b"\r\n")

    add_line(f"--{boundary}--")
    body = b"".join(chunks)
    return body, f"multipart/form-data; boundary={boundary}"


def parse_response_body(raw: bytes, headers: Dict[str, str]) -> Any:
    content_type = (headers.get("Content-Type") or headers.get("content-type") or "").lower()
    text = raw.decode("utf-8", errors="replace")
    if "application/json" in content_type or text.lstrip().startswith(("{", "[")):
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return text
    return text


def extract_usage_headers(headers: Dict[str, str]) -> Dict[str, Any]:
    wanted = [
        "x-app-usage",
        "x-ad-account-usage",
        "x-business-use-case-usage",
        "x-fb-trace-id",
        "x-fb-rev",
    ]
    usage: Dict[str, Any] = {}
    for key in wanted:
        for actual_key, value in headers.items():
            if actual_key.lower() == key:
                usage[actual_key] = try_json_parse(value)
    return usage


def graph_error_details(payload: Any, status: Optional[int] = None, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    details: Dict[str, Any] = {"status": status}
    if isinstance(payload, dict) and isinstance(payload.get("error"), dict):
        err = payload["error"]
        for key in [
            "message",
            "type",
            "code",
            "error_subcode",
            "error_user_title",
            "error_user_msg",
            "is_transient",
            "fbtrace_id",
        ]:
            if key in err:
                details[key] = err[key]
    elif isinstance(payload, str):
        details["message"] = payload
    if headers:
        trace_id = None
        for k, v in headers.items():
            if k.lower() == "x-fb-trace-id":
                trace_id = v
                break
        if trace_id and "fbtrace_id" not in details:
            details["fbtrace_id"] = trace_id
    return details


def extract_error_code(payload: Any) -> Optional[int]:
    if isinstance(payload, dict) and isinstance(payload.get("error"), dict):
        code = payload["error"].get("code")
        try:
            return int(code)
        except (TypeError, ValueError):
            return None
    return None


def should_retry(status: Optional[int], error_code: Optional[int], attempt: int, max_retries: int) -> bool:
    if attempt >= max_retries:
        return False
    if status in RETRIABLE_HTTP_STATUS:
        return True
    if error_code in RETRIABLE_ERROR_CODES:
        return True
    return False


def retry_delay(headers: Dict[str, str], attempt: int) -> float:
    for key, value in headers.items():
        if key.lower() == "retry-after":
            try:
                return max(0.0, float(value))
            except ValueError:
                pass
    return min(30.0, 1.5 * (2 ** attempt))


def mask_request_params(params: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    safe: Dict[str, Any] = {}
    for key, value in (params or {}).items():
        if "access_token" in key.lower():
            safe[key] = "***"
        else:
            safe[key] = value
    return safe


@dataclass
class MetaApiClient:
    access_token: str
    api_version: str = DEFAULT_API_VERSION
    graph_base: str = DEFAULT_GRAPH_BASE
    timeout: int = 60
    max_retries: int = 5

    def build_url(self, path: str) -> str:
        if path.startswith("http://") or path.startswith("https://"):
            return path
        clean = path.lstrip("/")
        base = self.graph_base.rstrip("/")
        if not clean:
            return f"{base}/{self.api_version}"
        if clean.startswith(f"{self.api_version}/"):
            return f"{base}/{clean}"
        return f"{base}/{self.api_version}/{clean}"

    def request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Tuple[str, bytes, str]]] = None,
    ) -> Dict[str, Any]:
        method = method.upper()
        url = self.build_url(path)
        encoded_params = normalise_params(params)
        data_bytes: Optional[bytes] = None
        headers: Dict[str, str] = {
            "Authorization": f"Bearer {self.access_token}",
            "User-Agent": USER_AGENT,
        }

        if method in {"GET", "HEAD"} and not files:
            url = append_query(url, encoded_params)
        elif files:
            body, content_type = build_multipart(encoded_params, files)
            headers["Content-Type"] = content_type
            data_bytes = body
        else:
            headers["Content-Type"] = "application/x-www-form-urlencoded"
            data_bytes = urllib.parse.urlencode(encoded_params).encode("utf-8") if encoded_params else b""

        last_payload: Any = None
        last_headers: Dict[str, str] = {}

        for attempt in range(self.max_retries + 1):
            req = urllib.request.Request(url, data=data_bytes, headers=headers, method=method)
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as response:
                    status = response.getcode()
                    response_headers = dict(response.info().items())
                    raw = response.read()
                payload = parse_response_body(raw, response_headers)
                error_code = extract_error_code(payload)
                if isinstance(payload, dict) and "error" in payload:
                    if should_retry(status, error_code, attempt, self.max_retries):
                        delay = retry_delay(response_headers, attempt)
                        eprint(f"Transient Graph error {error_code}; retrying in {delay:.1f}s...")
                        time.sleep(delay)
                        continue
                    raise CliError(
                        "Meta API returned an error.",
                        exit_code=EXIT_API,
                        details=graph_error_details(payload, status=status, headers=response_headers),
                    )
                return {
                    "status": status,
                    "headers": response_headers,
                    "request_url": url,
                    "payload": payload,
                }
            except urllib.error.HTTPError as exc:
                response_headers = dict(exc.headers.items())
                raw = exc.read()
                payload = parse_response_body(raw, response_headers)
                error_code = extract_error_code(payload)
                last_payload = payload
                last_headers = response_headers
                if should_retry(exc.code, error_code, attempt, self.max_retries):
                    delay = retry_delay(response_headers, attempt)
                    eprint(f"HTTP {exc.code} from Meta API; retrying in {delay:.1f}s...")
                    time.sleep(delay)
                    continue
                raise CliError(
                    f"Meta API request failed with HTTP {exc.code}.",
                    exit_code=EXIT_API,
                    details=graph_error_details(payload, status=exc.code, headers=response_headers),
                )
            except urllib.error.URLError as exc:
                if attempt < self.max_retries:
                    delay = retry_delay({}, attempt)
                    eprint(f"Network error ({exc.reason}); retrying in {delay:.1f}s...")
                    time.sleep(delay)
                    continue
                raise CliError(
                    f"Network error while calling Meta API: {exc.reason}",
                    exit_code=EXIT_API,
                    details={"reason": str(exc.reason)},
                )

        raise CliError(
            "Meta API request failed after retries.",
            exit_code=EXIT_API,
            details=graph_error_details(last_payload, headers=last_headers),
        )


def ensure_token(args: argparse.Namespace, allow_missing_for_dry_run: bool = False) -> Optional[str]:
    token = args.access_token or os.getenv("META_ACCESS_TOKEN")
    if token:
        return token
    if allow_missing_for_dry_run and getattr(args, "dry_run", False):
        return None
    raise CliError(
        "META_ACCESS_TOKEN is required for live API calls. Set it in the environment or pass --access-token.",
        exit_code=EXIT_AUTH,
    )


def require_account_id(args: argparse.Namespace) -> str:
    account_id = normalise_account_id(args.account_id or os.getenv("META_AD_ACCOUNT_ID"))
    if not account_id:
        raise CliError(
            "An ad account ID is required. Set META_AD_ACCOUNT_ID or pass --account-id.",
            exit_code=EXIT_BAD_ARGS,
        )
    return account_id


def wrap_result(
    *,
    ok: bool = True,
    command: str,
    method: str,
    path: str,
    params: Optional[Dict[str, Any]] = None,
    response: Optional[Dict[str, Any]] = None,
    dry_run: bool = False,
    warnings: Optional[List[str]] = None,
) -> Dict[str, Any]:
    envelope: Dict[str, Any] = {
        "ok": ok,
        "command": command,
        "dry_run": dry_run,
        "request": {
            "method": method.upper(),
            "path": path,
            "params": mask_request_params(params),
        },
    }
    if response:
        envelope["request"]["url"] = response.get("request_url")
        envelope["status"] = response.get("status")
        usage = extract_usage_headers(response.get("headers", {}))
        if usage:
            envelope["usage"] = usage
        envelope["result"] = response.get("payload")
        if "page_count" in response:
            envelope["pagination"] = {
                "pages_fetched": response["page_count"],
                "item_count": response.get("item_count"),
                "incomplete": response.get("incomplete_pagination", False),
            }
    if warnings:
        envelope["warnings"] = warnings
    return envelope


def maybe_write_output(data: Dict[str, Any], output_path: Optional[str]) -> Dict[str, Any]:
    if not output_path:
        return data
    path = pathlib.Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    result = dict(data)
    result["output_file"] = str(path)
    return result


def print_json(data: Dict[str, Any]) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=False))


def fetch_all_pages(client: MetaApiClient, first_response: Dict[str, Any], max_pages: int) -> Dict[str, Any]:
    payload = first_response.get("payload")
    if not isinstance(payload, dict):
        return first_response
    data = payload.get("data")
    if not isinstance(data, list):
        return first_response

    page_count = 1
    items = list(data)
    next_url = None
    if isinstance(payload.get("paging"), dict):
        next_url = payload["paging"].get("next")
    visited = set()

    while next_url and page_count < max_pages:
        if next_url in visited:
            break
        visited.add(next_url)
        next_response = client.request("GET", next_url)
        next_payload = next_response.get("payload")
        if not isinstance(next_payload, dict) or not isinstance(next_payload.get("data"), list):
            break
        items.extend(next_payload["data"])
        page_count += 1
        if isinstance(next_payload.get("paging"), dict):
            next_url = next_payload["paging"].get("next")
        else:
            next_url = None

    merged_payload = dict(payload)
    merged_payload["data"] = items
    if isinstance(merged_payload.get("paging"), dict) and next_url:
        merged_payload["paging"] = dict(merged_payload["paging"])
        merged_payload["paging"]["next"] = next_url

    result = dict(first_response)
    result["payload"] = merged_payload
    result["page_count"] = page_count
    result["item_count"] = len(items)
    result["incomplete_pagination"] = bool(next_url and page_count >= max_pages)
    return result


def validate_create_payload(object_name: str, params: Dict[str, Any]) -> List[str]:
    warnings: List[str] = []
    object_name = object_name.lower()
    if object_name in {"campaign", "campaigns"}:
        if "name" not in params:
            warnings.append("Campaign payload has no 'name'.")
        if "objective" not in params:
            warnings.append("Campaign payload has no 'objective'.")
        if "status" not in params:
            warnings.append("Campaign payload has no 'status'. PAUSED is the safest default.")
    elif object_name in {"adset", "adsets"}:
        for key in ["campaign_id", "name"]:
            if key not in params:
                warnings.append(f"Ad set payload has no '{key}'.")
        if "daily_budget" not in params and "lifetime_budget" not in params:
            warnings.append("Ad set payload has no budget. That can be valid under campaign budget optimisation, but verify intentionally.")
        if "targeting" not in params:
            warnings.append("Ad set payload has no 'targeting'.")
        if "status" not in params:
            warnings.append("Ad set payload has no 'status'. PAUSED is the safest default.")
    elif object_name in {"adcreative", "adcreatives"}:
        if "object_story_spec" not in params and "object_story_id" not in params and "asset_feed_spec" not in params:
            warnings.append("Creative payload has no object_story_spec, object_story_id, or asset_feed_spec.")
    elif object_name in {"ad", "ads"}:
        if "adset_id" not in params:
            warnings.append("Ad payload has no 'adset_id'.")
        if "creative" not in params:
            warnings.append("Ad payload has no 'creative'.")
        if "status" not in params:
            warnings.append("Ad payload has no 'status'. PAUSED is the safest default.")
    return warnings


def ensure_confirm(confirm: bool, dry_run: bool, message: str = "Refusing live mutation without --confirm. Use --dry-run first.") -> None:
    if dry_run:
        return
    if not confirm:
        raise CliError(message, exit_code=EXIT_SAFETY)


def resolve_edge(name: str) -> str:
    if name not in OBJECT_TO_EDGE:
        known = ", ".join(sorted(OBJECT_TO_EDGE))
        raise CliError(f"Unknown object or edge '{name}'. Known values: {known}")
    return OBJECT_TO_EDGE[name]


def command_accounts(args: argparse.Namespace) -> Dict[str, Any]:
    token = ensure_token(args)
    client = MetaApiClient(token, args.api_version, args.graph_base, args.timeout, args.max_retries)
    params: Dict[str, Any] = {
        "fields": args.fields or DEFAULT_ACCOUNTS_FIELDS,
        "limit": args.limit,
    }
    path = "/me/adaccounts"
    response = client.request("GET", path, params=params)
    if args.fetch_all:
        response = fetch_all_pages(client, response, args.max_pages)
    return wrap_result(command="accounts", method="GET", path=path, params=params, response=response)


def command_account(args: argparse.Namespace) -> Dict[str, Any]:
    token = ensure_token(args)
    account_id = require_account_id(args)
    client = MetaApiClient(token, args.api_version, args.graph_base, args.timeout, args.max_retries)
    params = {"fields": args.fields or DEFAULT_ACCOUNT_FIELDS}
    path = f"/{account_id}"
    response = client.request("GET", path, params=params)
    return wrap_result(command="account", method="GET", path=path, params=params, response=response)


def command_list(args: argparse.Namespace) -> Dict[str, Any]:
    token = ensure_token(args)
    account_id = require_account_id(args)
    client = MetaApiClient(token, args.api_version, args.graph_base, args.timeout, args.max_retries)
    edge = resolve_edge(args.edge)
    params: Dict[str, Any] = {
        "fields": args.fields or DEFAULT_LIST_FIELDS.get(edge, "id,name"),
        "limit": args.limit,
    }
    if args.filtering:
        params["filtering"] = try_json_parse(args.filtering)
    if args.effective_status:
        params["effective_status"] = args.effective_status.split(",")
    if args.summary:
        params["summary"] = args.summary
    path = f"/{account_id}/{edge}"
    response = client.request("GET", path, params=params)
    if args.fetch_all:
        response = fetch_all_pages(client, response, args.max_pages)
    return wrap_result(command="list", method="GET", path=path, params=params, response=response)


def command_get(args: argparse.Namespace) -> Dict[str, Any]:
    token = ensure_token(args)
    client = MetaApiClient(token, args.api_version, args.graph_base, args.timeout, args.max_retries)
    params = merge_params(args.params_file, args.set_items)
    if args.fields:
        params["fields"] = args.fields
    if args.limit is not None:
        params["limit"] = args.limit
    path = f"/{args.node_id}"
    if args.edge:
        path = f"{path}/{args.edge.lstrip('/')}"
    response = client.request("GET", path, params=params)
    if args.fetch_all:
        response = fetch_all_pages(client, response, args.max_pages)
    return wrap_result(command="get", method="GET", path=path, params=params, response=response)


def command_create(args: argparse.Namespace) -> Dict[str, Any]:
    account_id = require_account_id(args)
    params = merge_params(args.params_file, args.set_items)
    edge = resolve_edge(args.object_name)
    warnings = validate_create_payload(args.object_name, params)
    path = f"/{account_id}/{edge}"
    if args.dry_run:
        return wrap_result(command="create", method="POST", path=path, params=params, dry_run=True, warnings=warnings)
    ensure_confirm(args.confirm, args.dry_run)
    token = ensure_token(args)
    client = MetaApiClient(token, args.api_version, args.graph_base, args.timeout, args.max_retries)
    response = client.request("POST", path, params=params)
    return wrap_result(command="create", method="POST", path=path, params=params, response=response, warnings=warnings)


def command_update(args: argparse.Namespace) -> Dict[str, Any]:
    params = merge_params(args.params_file, args.set_items)
    path = f"/{args.node_id}"
    if args.dry_run:
        return wrap_result(command="update", method="POST", path=path, params=params, dry_run=True)
    ensure_confirm(args.confirm, args.dry_run)
    token = ensure_token(args)
    client = MetaApiClient(token, args.api_version, args.graph_base, args.timeout, args.max_retries)
    response = client.request("POST", path, params=params)
    return wrap_result(command="update", method="POST", path=path, params=params, response=response)


def command_set_status(args: argparse.Namespace) -> Dict[str, Any]:
    params = {"status": args.status}
    path = f"/{args.node_id}"
    if args.dry_run:
        return wrap_result(command="set-status", method="POST", path=path, params=params, dry_run=True)
    ensure_confirm(args.confirm, args.dry_run)
    token = ensure_token(args)
    client = MetaApiClient(token, args.api_version, args.graph_base, args.timeout, args.max_retries)
    response = client.request("POST", path, params=params)
    return wrap_result(command="set-status", method="POST", path=path, params=params, response=response)


def command_request(args: argparse.Namespace) -> Dict[str, Any]:
    method = args.method.upper()
    params = merge_params(args.params_file, args.set_items)
    path = args.path
    if args.dry_run:
        return wrap_result(command="request", method=method, path=path, params=params, dry_run=True)
    if method in WRITE_METHODS:
        ensure_confirm(args.confirm, args.dry_run)
    token = ensure_token(args, allow_missing_for_dry_run=True)
    if not token:
        raise CliError("Live requests require META_ACCESS_TOKEN.", exit_code=EXIT_AUTH)
    client = MetaApiClient(token, args.api_version, args.graph_base, args.timeout, args.max_retries)
    response = client.request(method, path, params=params)
    if args.fetch_all:
        response = fetch_all_pages(client, response, args.max_pages)
    return wrap_result(command="request", method=method, path=path, params=params, response=response)


def command_insights(args: argparse.Namespace) -> Dict[str, Any]:
    token = ensure_token(args)
    client = MetaApiClient(token, args.api_version, args.graph_base, args.timeout, args.max_retries)
    node_id = args.node_id or require_account_id(args)
    path = f"/{node_id}/insights"

    params: Dict[str, Any] = merge_params(args.params_file, args.set_items)
    params.setdefault("fields", args.fields or DEFAULT_INSIGHTS_FIELDS)
    params.setdefault("level", args.level or ("campaign" if str(node_id).startswith("act_") else None))
    if args.date_preset:
        params["date_preset"] = args.date_preset
    if args.time_range:
        params["time_range"] = try_json_parse(args.time_range)
    if args.time_range_file:
        params["time_range"] = load_json_or_text(args.time_range_file)
    if args.breakdowns:
        params["breakdowns"] = args.breakdowns.split(",")
    if args.action_breakdowns:
        params["action_breakdowns"] = args.action_breakdowns.split(",")
    if args.summary_action_breakdowns:
        params["summary_action_breakdowns"] = args.summary_action_breakdowns.split(",")
    if args.action_attribution_windows:
        params["action_attribution_windows"] = args.action_attribution_windows.split(",")
    if args.time_increment is not None:
        params["time_increment"] = args.time_increment
    if args.filtering:
        params["filtering"] = try_json_parse(args.filtering)
    if args.sort:
        params["sort"] = args.sort.split(",")
    if args.limit is not None:
        params["limit"] = args.limit

    if not args.async_job:
        response = client.request("GET", path, params=params)
        if args.fetch_all:
            response = fetch_all_pages(client, response, args.max_pages)
        return wrap_result(command="insights", method="GET", path=path, params=params, response=response)

    start_response = client.request("POST", path, params=params)
    payload = start_response.get("payload")
    report_run_id = None
    if isinstance(payload, dict):
        report_run_id = payload.get("report_run_id") or payload.get("id")
    if not report_run_id:
        raise CliError(
            "Async Insights did not return a report_run_id.",
            exit_code=EXIT_API,
            details={"response": payload},
        )

    poll_history: List[Dict[str, Any]] = []
    start_time = time.time()
    status_path = f"/{report_run_id}"
    while True:
        status_response = client.request(
            "GET",
            status_path,
            params={"fields": "id,async_status,async_percent_completion"},
        )
        status_payload = status_response.get("payload")
        if isinstance(status_payload, dict):
            poll_history.append(status_payload)
            async_status = str(status_payload.get("async_status", "")).lower()
            percent = status_payload.get("async_percent_completion")
            if async_status in {"job completed", "completed"}:
                break
            if async_status in {"job failed", "failed"}:
                raise CliError(
                    "Async Insights job failed.",
                    exit_code=EXIT_API,
                    details={"report_run_id": report_run_id, "poll_history": poll_history},
                )
            if percent == 100:
                break
        if time.time() - start_time > args.poll_timeout:
            raise CliError(
                "Timed out waiting for async Insights to finish.",
                exit_code=EXIT_TIMEOUT,
                details={"report_run_id": report_run_id, "poll_history": poll_history},
            )
        time.sleep(args.poll_interval)

    result_response = client.request("GET", f"/{report_run_id}/insights", params={"limit": args.limit or 100})
    if args.fetch_all:
        result_response = fetch_all_pages(client, result_response, args.max_pages)
    wrapped = wrap_result(command="insights", method="POST", path=path, params=params, response=result_response)
    wrapped["report_run_id"] = report_run_id
    wrapped["poll_history"] = poll_history
    return wrapped


def command_targeting_search(args: argparse.Namespace) -> Dict[str, Any]:
    token = ensure_token(args)
    client = MetaApiClient(token, args.api_version, args.graph_base, args.timeout, args.max_retries)
    params = merge_params(args.params_file, args.set_items)
    if args.type:
        params["type"] = args.type
    if args.q:
        params["q"] = args.q
    if args.limit is not None:
        params["limit"] = args.limit
    if args.locale:
        params["locale"] = args.locale

    account_id = normalise_account_id(args.account_id or os.getenv("META_AD_ACCOUNT_ID"))
    path = f"/{account_id}/targetingsearch" if account_id else "/search"
    response = client.request("GET", path, params=params)
    if args.fetch_all:
        response = fetch_all_pages(client, response, args.max_pages)
    return wrap_result(command="targeting-search", method="GET", path=path, params=params, response=response)


def replace_placeholders(value: Any, account_id: Optional[str]) -> Any:
    if account_id is None:
        return value
    raw_account_id = account_id[4:] if account_id.startswith("act_") else account_id
    if isinstance(value, str):
        return (
            value.replace("act_<account_id>", account_id)
            .replace("act_{account_id}", account_id)
            .replace("<account_id>", raw_account_id)
            .replace("{account_id}", raw_account_id)
        )
    if isinstance(value, list):
        return [replace_placeholders(v, account_id) for v in value]
    if isinstance(value, dict):
        return {k: replace_placeholders(v, account_id) for k, v in value.items()}
    return value


def command_batch(args: argparse.Namespace) -> Dict[str, Any]:
    loaded = load_json_or_text(args.batch_file)
    if not isinstance(loaded, list):
        raise CliError("--batch-file must contain a JSON array of batch operations.")
    account_id = normalise_account_id(args.account_id or os.getenv("META_AD_ACCOUNT_ID"))
    batch_items = replace_placeholders(loaded, account_id)
    has_write = any(str(item.get("method", "GET")).upper() != "GET" for item in batch_items if isinstance(item, dict))
    if args.dry_run:
        params = {"batch": batch_items}
        return wrap_result(command="batch", method="POST", path="/", params=params, dry_run=True)
    if has_write:
        ensure_confirm(args.confirm, args.dry_run)
    token = ensure_token(args)
    client = MetaApiClient(token, args.api_version, args.graph_base, args.timeout, args.max_retries)
    params = {"batch": batch_items}
    response = client.request("POST", "/", params={"batch": batch_items})
    payload = response.get("payload")
    if isinstance(payload, list):
        parsed_list = []
        for item in payload:
            if isinstance(item, dict) and isinstance(item.get("body"), str):
                parsed = try_json_parse(item["body"])
                if parsed != item["body"]:
                    item = dict(item)
                    item["parsed_body"] = parsed
            parsed_list.append(item)
        response = dict(response)
        response["payload"] = parsed_list
    return wrap_result(command="batch", method="POST", path="/", params=params, response=response)


def command_upload(args: argparse.Namespace) -> Dict[str, Any]:
    account_id = require_account_id(args)
    edge = args.edge
    if edge not in {"adimages", "advideos"}:
        raise CliError("Upload edge must be either 'adimages' or 'advideos'.")
    path = f"/{account_id}/{edge}"
    params = merge_params(args.params_file, args.set_items)
    file_path = pathlib.Path(args.file)
    if not file_path.exists():
        raise CliError(f"Upload file does not exist: {file_path}")
    warnings: List[str] = []
    if edge == "adimages" and not file_path.suffix:
        warnings.append("Image upload usually requires a real filename extension such as .jpg or .png.")
    if args.dry_run:
        params_preview = dict(params)
        params_preview["file"] = str(file_path)
        return wrap_result(command="upload", method="POST", path=path, params=params_preview, dry_run=True, warnings=warnings)
    ensure_confirm(args.confirm, args.dry_run)
    token = ensure_token(args)
    client = MetaApiClient(token, args.api_version, args.graph_base, args.timeout, args.max_retries)
    file_field = args.file_field or ("filename" if edge == "adimages" else "source")
    file_bytes = file_path.read_bytes()
    files = {
        file_field: (file_path.name, file_bytes, guess_content_type(file_path.name)),
    }
    response = client.request("POST", path, params=params, files=files)
    return wrap_result(command="upload", method="POST", path=path, params=params, response=response, warnings=warnings)


def add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--access-token", help="Meta access token. Defaults to META_ACCESS_TOKEN.")
    parser.add_argument("--account-id", help="Meta ad account ID. Defaults to META_AD_ACCOUNT_ID.")
    parser.add_argument("--api-version", default=DEFAULT_API_VERSION, help=f"Graph API version. Default: {DEFAULT_API_VERSION}")
    parser.add_argument("--graph-base", default=DEFAULT_GRAPH_BASE, help=f"Graph API base URL. Default: {DEFAULT_GRAPH_BASE}")
    parser.add_argument("--timeout", type=int, default=60, help="HTTP timeout in seconds. Default: 60")
    parser.add_argument("--max-retries", type=int, default=5, help="Max retries for transient and throttling failures. Default: 5")
    parser.add_argument("--output", help="Write the full JSON envelope to this file as well as printing it.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="meta_ads.py",
        description="Agent-friendly CLI for the Meta Marketing API.",
        epilog=(
            "Examples:\n"
            "  python3 scripts/meta_ads.py accounts\n"
            "  python3 scripts/meta_ads.py list campaigns --fetch-all\n"
            "  python3 scripts/meta_ads.py create campaign --params-file assets/campaign-create.json --dry-run\n"
            "  python3 scripts/meta_ads.py create campaign --params-file work/campaign.json --confirm\n"
            "  python3 scripts/meta_ads.py insights act_123 --level campaign --date-preset last_7d\n"
            "  python3 scripts/meta_ads.py request GET /120000000000000/previews --set ad_format=DESKTOP_FEED_STANDARD\n"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_accounts = sub.add_parser("accounts", help="List ad accounts accessible to the token.")
    add_common(p_accounts)
    p_accounts.add_argument("--fields", help="Comma-separated fields to request.")
    p_accounts.add_argument("--limit", type=int, default=25, help="Page size. Default: 25")
    p_accounts.add_argument("--fetch-all", action="store_true", help="Follow pagination.")
    p_accounts.add_argument("--max-pages", type=int, default=100, help="Maximum pages to fetch. Default: 100")
    p_accounts.set_defaults(func=command_accounts)

    p_account = sub.add_parser("account", help="Read the current or specified ad account.")
    add_common(p_account)
    p_account.add_argument("--fields", help="Comma-separated fields to request.")
    p_account.set_defaults(func=command_account)

    p_list = sub.add_parser("list", help="List an account edge such as campaigns, adsets, ads, or creatives.")
    add_common(p_list)
    p_list.add_argument("edge", help="Object or edge name, e.g. campaigns, adsets, ads, adcreatives.")
    p_list.add_argument("--fields", help="Comma-separated fields to request.")
    p_list.add_argument("--limit", type=int, default=25, help="Page size. Default: 25")
    p_list.add_argument("--filtering", help="JSON filtering value.")
    p_list.add_argument("--effective-status", help="Comma-separated effective status values.")
    p_list.add_argument("--summary", help="Summary parameter if the edge supports it.")
    p_list.add_argument("--fetch-all", action="store_true", help="Follow pagination.")
    p_list.add_argument("--max-pages", type=int, default=100, help="Maximum pages to fetch. Default: 100")
    p_list.set_defaults(func=command_list)

    p_get = sub.add_parser("get", help="Read a node or node edge.")
    add_common(p_get)
    p_get.add_argument("node_id", help="Object ID or node ID.")
    p_get.add_argument("--edge", help="Optional edge under the node.")
    p_get.add_argument("--fields", help="Comma-separated fields.")
    p_get.add_argument("--params-file", help="JSON file with extra query params.")
    p_get.add_argument("--set", dest="set_items", action="append", help="Extra params as key=value. Use dotted keys for nested objects.")
    p_get.add_argument("--limit", type=int, help="Page size for edge reads.")
    p_get.add_argument("--fetch-all", action="store_true", help="Follow pagination.")
    p_get.add_argument("--max-pages", type=int, default=100, help="Maximum pages to fetch. Default: 100")
    p_get.set_defaults(func=command_get)

    p_create = sub.add_parser("create", help="Create a supported account edge object.")
    add_common(p_create)
    p_create.add_argument("object_name", help="Object name such as campaign, adset, adcreative, ad.")
    p_create.add_argument("--params-file", help="JSON file with POST params.")
    p_create.add_argument("--set", dest="set_items", action="append", help="Extra params as key=value. Use dotted keys for nested objects.")
    p_create.add_argument("--dry-run", action="store_true", help="Print the request envelope without calling Meta.")
    p_create.add_argument("--confirm", action="store_true", help="Required for live writes.")
    p_create.set_defaults(func=command_create)

    p_update = sub.add_parser("update", help="Update a node by ID.")
    add_common(p_update)
    p_update.add_argument("node_id", help="Node ID to update.")
    p_update.add_argument("--params-file", help="JSON file with POST params.")
    p_update.add_argument("--set", dest="set_items", action="append", help="Extra params as key=value. Use dotted keys for nested objects.")
    p_update.add_argument("--dry-run", action="store_true", help="Print the request envelope without calling Meta.")
    p_update.add_argument("--confirm", action="store_true", help="Required for live writes.")
    p_update.set_defaults(func=command_update)

    p_status = sub.add_parser("set-status", help="Set status on a node.")
    add_common(p_status)
    p_status.add_argument("node_id", help="Node ID to update.")
    p_status.add_argument("status", help="New status, e.g. ACTIVE, PAUSED, ARCHIVED.")
    p_status.add_argument("--dry-run", action="store_true", help="Print the request envelope without calling Meta.")
    p_status.add_argument("--confirm", action="store_true", help="Required for live writes.")
    p_status.set_defaults(func=command_set_status)

    p_request = sub.add_parser("request", help="Low-level Graph API request.")
    add_common(p_request)
    p_request.add_argument("method", help="HTTP method, e.g. GET or POST.")
    p_request.add_argument("path", help="Graph path such as /act_123/campaigns or a full URL.")
    p_request.add_argument("--params-file", help="JSON file with request params.")
    p_request.add_argument("--set", dest="set_items", action="append", help="Extra params as key=value. Use @file.json to inject JSON from a file.")
    p_request.add_argument("--dry-run", action="store_true", help="Print the request envelope without calling Meta.")
    p_request.add_argument("--confirm", action="store_true", help="Required for live write methods.")
    p_request.add_argument("--fetch-all", action="store_true", help="Follow pagination for list responses.")
    p_request.add_argument("--max-pages", type=int, default=100, help="Maximum pages to fetch. Default: 100")
    p_request.set_defaults(func=command_request)

    p_insights = sub.add_parser("insights", help="Fetch sync or async Insights reports.")
    add_common(p_insights)
    p_insights.add_argument("node_id", nargs="?", help="Ad object ID. Defaults to the current ad account.")
    p_insights.add_argument("--fields", help="Comma-separated fields to request.")
    p_insights.add_argument("--level", help="Reporting level: account, campaign, adset, or ad.")
    p_insights.add_argument("--date-preset", default="last_7d", help="Date preset. Default: last_7d")
    p_insights.add_argument("--time-range", help='Inline JSON like {"since":"2026-03-01","until":"2026-03-14"}')
    p_insights.add_argument("--time-range-file", help="JSON file containing a time_range object.")
    p_insights.add_argument("--breakdowns", help="Comma-separated breakdowns.")
    p_insights.add_argument("--action-breakdowns", help="Comma-separated action breakdowns.")
    p_insights.add_argument("--summary-action-breakdowns", help="Comma-separated summary action breakdowns.")
    p_insights.add_argument("--action-attribution-windows", help="Comma-separated attribution windows.")
    p_insights.add_argument("--time-increment", type=int, help="Use 1 for daily rows, or a larger value.")
    p_insights.add_argument("--filtering", help="JSON filtering value.")
    p_insights.add_argument("--sort", help="Comma-separated sort keys.")
    p_insights.add_argument("--limit", type=int, help="Page size.")
    p_insights.add_argument("--async", dest="async_job", action="store_true", help="Run as an async Insights report.")
    p_insights.add_argument("--poll-interval", type=float, default=5.0, help="Seconds between async status polls. Default: 5")
    p_insights.add_argument("--poll-timeout", type=float, default=900.0, help="Total seconds to wait for async completion. Default: 900")
    p_insights.add_argument("--params-file", help="JSON file with extra Insights params.")
    p_insights.add_argument("--set", dest="set_items", action="append", help="Extra params as key=value.")
    p_insights.add_argument("--fetch-all", action="store_true", help="Follow pagination on the final Insights result.")
    p_insights.add_argument("--max-pages", type=int, default=100, help="Maximum pages to fetch. Default: 100")
    p_insights.set_defaults(func=command_insights)

    p_target = sub.add_parser("targeting-search", help="Resolve targeting descriptors.")
    add_common(p_target)
    p_target.add_argument("--type", default="adinterest", help="Targeting search type. Default: adinterest")
    p_target.add_argument("--q", help="Query text.")
    p_target.add_argument("--limit", type=int, default=25, help="Page size. Default: 25")
    p_target.add_argument("--locale", help="Optional locale value.")
    p_target.add_argument("--params-file", help="JSON file with extra params.")
    p_target.add_argument("--set", dest="set_items", action="append", help="Extra params as key=value.")
    p_target.add_argument("--fetch-all", action="store_true", help="Follow pagination if present.")
    p_target.add_argument("--max-pages", type=int, default=100, help="Maximum pages to fetch. Default: 100")
    p_target.set_defaults(func=command_targeting_search)

    p_batch = sub.add_parser("batch", help="Send a Graph batch request from a JSON file.")
    add_common(p_batch)
    p_batch.add_argument("--batch-file", required=True, help="JSON file containing a batch array.")
    p_batch.add_argument("--dry-run", action="store_true", help="Print the request envelope without calling Meta.")
    p_batch.add_argument("--confirm", action="store_true", help="Required if the batch contains writes.")
    p_batch.set_defaults(func=command_batch)

    p_upload = sub.add_parser("upload", help="Upload to adimages or advideos.")
    add_common(p_upload)
    p_upload.add_argument("edge", choices=["adimages", "advideos"], help="Upload destination edge.")
    p_upload.add_argument("--file", required=True, help="Local file path to upload.")
    p_upload.add_argument("--file-field", help="Multipart field name override. Defaults to filename for adimages and source for advideos.")
    p_upload.add_argument("--params-file", help="JSON file with extra params.")
    p_upload.add_argument("--set", dest="set_items", action="append", help="Extra params as key=value.")
    p_upload.add_argument("--dry-run", action="store_true", help="Print the request envelope without calling Meta.")
    p_upload.add_argument("--confirm", action="store_true", help="Required for live uploads.")
    p_upload.set_defaults(func=command_upload)

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        result = args.func(args)
        result = maybe_write_output(result, args.output)
        print_json(result)
        return 0
    except CliError as exc:
        error_payload: Dict[str, Any] = {
            "ok": False,
            "error": exc.message,
            "exit_code": exc.exit_code,
        }
        if exc.details:
            error_payload["details"] = exc.details
        print_json(error_payload)
        return exc.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
