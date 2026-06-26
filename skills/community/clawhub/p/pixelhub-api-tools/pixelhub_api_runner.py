#!/usr/bin/env python3
import argparse
import json
import os
import socket
import time
import urllib.error
import urllib.parse
import urllib.request

DEFAULT_BASE_URL = "https://www.pixellelabs.com"
DEFAULT_API_KEY = "PENDING_USER_API_KEY"
DEFAULT_REQUEST_RETRIES = 3
DEFAULT_RETRY_DELAY = 2.0


def _normalize_base_url(base_url: str) -> str:
    return base_url.rstrip("/")


class PixelhubAPI:
    def __init__(
        self,
        base_url: str,
        api_key: str,
        timeout: int = 30,
        request_retries: int = DEFAULT_REQUEST_RETRIES,
        retry_delay: float = DEFAULT_RETRY_DELAY,
    ):
        self.base_url = _normalize_base_url(base_url)
        self.api_key = api_key
        self.timeout = timeout
        self.request_retries = max(0, request_retries)
        self.retry_delay = max(0.0, retry_delay)

    def _request(self, method: str, path: str, payload=None, retryable: bool = False):
        url = f"{self.base_url}{path}"
        headers = {"X-API-Key": self.api_key}
        data = None
        if payload is not None:
            headers["Content-Type"] = "application/json"
            data = json.dumps(payload).encode("utf-8")

        attempts = self.request_retries + 1 if retryable else 1
        last_error = None
        for attempt in range(attempts):
            req = urllib.request.Request(url, data=data, headers=headers, method=method)
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    text = resp.read().decode("utf-8", "replace")
                    return resp.status, json.loads(text)
            except urllib.error.HTTPError as e:
                body = e.read().decode("utf-8", "replace")
                try:
                    parsed = json.loads(body)
                except Exception:
                    parsed = {"detail": body}
                return e.code, parsed
            except (TimeoutError, socket.timeout) as e:
                last_error = e
            except urllib.error.URLError as e:
                last_error = e
                if not _is_timeout_error(e):
                    return 599, {
                        "detail": str(e),
                        "error_type": type(e).__name__,
                        "path": path,
                    }

            if attempt < attempts - 1:
                time.sleep(self.retry_delay * (attempt + 1))

        return 599, {
            "detail": str(last_error) if last_error else "request failed",
            "error_type": type(last_error).__name__ if last_error else "RequestError",
            "path": path,
            "retryable": retryable,
            "attempts": attempts,
        }

    def list_tools(self):
        return self._request("GET", "/api/workflow/tools", retryable=True)

    def list_agents(self):
        return self._request("GET", "/api/chat/agents", retryable=True)

    def run_tool(self, tool_name: str, params: dict, name: str = ""):
        payload = {"params": params, "name": name or f"api-{tool_name}"}
        return self._request(
            "POST",
            f"/api/workflow/run/{urllib.parse.quote(tool_name)}",
            payload,
            retryable=False,
        )

    def get_task(self, task_id: str):
        return self._request(
            "GET", f"/api/workflow/tasks/{urllib.parse.quote(task_id)}", retryable=True
        )


def _is_timeout_error(exc) -> bool:
    if isinstance(exc, (TimeoutError, socket.timeout)):
        return True
    if isinstance(exc, urllib.error.URLError):
        reason = getattr(exc, "reason", None)
        return isinstance(reason, (TimeoutError, socket.timeout))
    return False


def _print_json(data):
    if isinstance(data, (dict, list)):
        text = json.dumps(data, ensure_ascii=False, indent=2)
        try:
            print(text)
        except UnicodeEncodeError:
            print(json.dumps(data, ensure_ascii=True, indent=2))
    else:
        text = str(data)
        try:
            print(text)
        except UnicodeEncodeError:
            print(text.encode("ascii", "xmlcharrefreplace").decode("ascii"))


def _extract_tools(payload: dict) -> list[dict]:
    if not isinstance(payload, dict):
        return []
    tools = payload.get("tools", [])
    if isinstance(tools, list):
        return [tool for tool in tools if isinstance(tool, dict)]
    return []


def _extract_balance(payload: dict) -> dict:
    if not isinstance(payload, dict):
        return {}

    display = payload.get("current_points_display")
    if not display and "current_points" in payload:
        display = f"{payload.get('current_points')} 像素币"

    if display:
        return {"当前余额": display}
    return {}


def _group_tools_by_category(tools: list[dict]) -> dict[str, list[str]]:
    grouped: dict[str, list[str]] = {}
    for tool in tools:
        category = tool.get("category") or "uncategorized"
        name = tool.get("name")
        description = tool.get("description", "")
        pricing_display = tool.get("pricing_display")
        if not name:
            continue
        # Extract first line or first sentence of description
        summary = description.split("\n")[0].split(". ")[0].strip("# ")
        if not summary:
            summary = "No description available"

        display_name = f"{name}: {summary}"
        if pricing_display:
            display_name += f" [{pricing_display}]"

        grouped.setdefault(str(category), []).append(display_name)

    for names in grouped.values():
        names.sort()
    return dict(sorted(grouped.items()))


def _sanitize_tool(tool: dict) -> dict:
    return {key: value for key, value in tool.items() if key != "is_runninghub"}


def _select_tools_by_names(tools: list[dict], tool_names: list[str]) -> list[dict]:
    selected = []
    missing = []
    by_name = {tool.get("name"): tool for tool in tools if tool.get("name")}
    for tool_name in tool_names:
        tool = by_name.get(tool_name)
        if tool is None:
            missing.append(tool_name)
            continue
        selected.append(_sanitize_tool(tool))

    if missing:
        raise ValueError(f"tool schema not found: {', '.join(missing)}")
    return selected


def _load_params(params_text: str) -> dict:
    if not params_text:
        return {}
    try:
        value = json.loads(params_text)
        if not isinstance(value, dict):
            raise ValueError("params must be a JSON object")
        return value
    except json.JSONDecodeError as e:
        raise ValueError(f"invalid params JSON: {e}")


def _find_tool_schema(tools_payload: dict, tool_name: str) -> dict | None:
    tools = tools_payload.get("tools", []) if isinstance(tools_payload, dict) else []
    for tool in tools:
        if tool.get("name") == tool_name:
            return tool
    return None


def _autofill_params_with_schema(input_params: dict, tool_schema: dict) -> dict:
    """
    Autofill missing params with defaults from /api/workflow/tools schema.
    - Only fills when key is missing in input params
    - Does not fill defaults that are None
    """
    params = dict(input_params or {})
    schema_params = (
        tool_schema.get("params", []) if isinstance(tool_schema, dict) else []
    )

    for param in schema_params:
        name = param.get("name")
        if not name:
            continue
        if name not in params:
            default_val = param.get("default", None)
            if default_val is not None:
                params[name] = default_val

    return params


def _validate_required_params(params: dict, tool_schema: dict):
    schema_params = (
        tool_schema.get("params", []) if isinstance(tool_schema, dict) else []
    )
    missing = []
    for param in schema_params:
        name = param.get("name")
        required = bool(param.get("required", False))
        if not name or not required:
            continue
        if name not in params or params[name] is None or params[name] == "":
            missing.append(name)

    if missing:
        raise ValueError(f"missing required params: {', '.join(missing)}")


def _prepare_params_with_tools_schema(
    client: PixelhubAPI, tool_name: str, raw_params: dict
) -> dict:
    code, payload = client.list_tools()
    if code != 200:
        detail = payload.get("detail") if isinstance(payload, dict) else payload
        raise ValueError(
            "failed to fetch tool schema: "
            f"status={code}, detail={detail}. "
            "This is usually a transient network or server response timeout; retry the command."
        )

    tool_schema = _find_tool_schema(payload, tool_name)
    if not tool_schema:
        raise ValueError(f"tool schema not found: {tool_name}")

    merged = _autofill_params_with_schema(raw_params, tool_schema)
    _validate_required_params(merged, tool_schema)
    return merged


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Pixelhub API runner (non-MCP)")
    p.add_argument(
        "--base-url",
        default=os.getenv("Pixelhub_BASE_URL", DEFAULT_BASE_URL),
        help="Pixelhub base URL",
    )
    p.add_argument(
        "--api-key",
        default=os.getenv("Pixelhub_API_KEY", DEFAULT_API_KEY),
        help="Pixelhub API key",
    )
    p.add_argument("--timeout", type=int, default=30, help="HTTP timeout seconds")
    p.add_argument(
        "--request-retries",
        type=int,
        default=DEFAULT_REQUEST_RETRIES,
        help="Retry count for transient GET request failures",
    )
    p.add_argument(
        "--retry-delay",
        type=float,
        default=DEFAULT_RETRY_DELAY,
        help="Base delay seconds between transient request retries",
    )

    sp = p.add_subparsers(dest="command", required=True)

    sp.add_parser("agents", help="List agents and their tools")
    tools = sp.add_parser(
        "tools", help="List workflow tools by category or show schemas"
    )
    tools.add_argument(
        "--tool",
        action="append",
        default=[],
        help="Tool name to inspect in detail. Repeat for multiple tools.",
    )

    run = sp.add_parser("run", help="Submit a tool task")
    run.add_argument("--tool", required=True, help="Tool name")
    run.add_argument("--params", default="{}", help="Params JSON object")
    run.add_argument("--name", default="", help="Task name")

    poll = sp.add_parser("poll", help="Poll task status")
    poll.add_argument("--task-id", required=True, help="Task ID")
    poll.add_argument(
        "--interval", type=float, default=3.0, help="Poll interval seconds"
    )
    poll.add_argument("--max-wait", type=int, default=480, help="Max wait seconds")

    execute = sp.add_parser("execute", help="Execute tool and wait for completion")
    execute.add_argument("--tool", required=True, help="Tool name")
    execute.add_argument("--params", default="{}", help="Params JSON object")
    execute.add_argument("--name", default="", help="Task name")
    execute.add_argument(
        "--interval", type=float, default=3.0, help="Poll interval seconds"
    )
    execute.add_argument("--max-wait", type=int, default=480, help="Max wait seconds")

    return p


def _ensure_auth(args):
    if not args.base_url:
        raise SystemExit("Missing --base-url (or Pixelhub_BASE_URL)")
    if not args.api_key or args.api_key == "PENDING_USER_API_KEY":
        raise SystemExit(
            "Missing Pixelhub API key. Ask the user to log in at https://www.pixellelabs.com/, open Personal Center -> API Keys, copy their key, and replace DEFAULT_API_KEY in pixelhub_api_runner.py."
        )


def _poll_until_done(client: PixelhubAPI, task_id: str, interval: float, max_wait: int):
    deadline = time.time() + max_wait
    last_payload = None
    while True:
        code, payload = client.get_task(task_id)
        if isinstance(payload, dict):
            last_payload = payload
        if code == 599:
            if time.time() >= deadline:
                return 408, {
                    "detail": "poll timeout after transient request failures",
                    "task_id": task_id,
                    "last": last_payload,
                    "last_error": payload,
                }
            time.sleep(interval)
            continue
        if code != 200:
            return code, payload
        status = payload.get("status")
        if status in ("completed", "failed"):
            return code, payload
        if time.time() >= deadline:
            return 408, {"detail": "poll timeout", "task_id": task_id, "last": payload}
        time.sleep(interval)


def main():
    parser = build_parser()
    args = parser.parse_args()
    _ensure_auth(args)
    client = PixelhubAPI(
        args.base_url,
        args.api_key,
        timeout=args.timeout,
        request_retries=args.request_retries,
        retry_delay=args.retry_delay,
    )

    if args.command == "agents":
        code, payload = client.list_agents()
        _print_json(payload)
        raise SystemExit(0 if code == 200 else 1)

    if args.command == "tools":
        code, payload = client.list_tools()
        if code != 200:
            _print_json(payload)
            raise SystemExit(1)

        tools = _extract_tools(payload)
        balance = _extract_balance(payload)
        if args.tool:
            try:
                selected = _select_tools_by_names(tools, args.tool)
            except ValueError as e:
                _print_json({"detail": str(e)})
                raise SystemExit(1)
            _print_json({**balance, "tools": selected})
        else:
            _print_json({**balance, "categories": _group_tools_by_category(tools)})
        raise SystemExit(0 if code == 200 else 1)

    if args.command == "run":
        raw_params = _load_params(args.params)
        try:
            params = _prepare_params_with_tools_schema(client, args.tool, raw_params)
        except ValueError as e:
            _print_json({"detail": str(e)})
            raise SystemExit(1)
        code, payload = client.run_tool(args.tool, params=params, name=args.name)
        _print_json(payload)
        raise SystemExit(0 if code == 200 else 1)

    if args.command == "poll":
        code, payload = _poll_until_done(
            client, args.task_id, args.interval, args.max_wait
        )
        result_obj = payload.get("result")
        if isinstance(result_obj, dict) and result_obj.get("message"):
            _print_json(result_obj["message"])
        else:
            _print_json(payload)
        ok = code == 200 and payload.get("status") == "completed"
        raise SystemExit(0 if ok else 1)

    if args.command == "execute":
        raw_params = _load_params(args.params)
        try:
            params = _prepare_params_with_tools_schema(client, args.tool, raw_params)
        except ValueError as e:
            _print_json({"detail": str(e)})
            raise SystemExit(1)
        code, payload = client.run_tool(args.tool, params=params, name=args.name)
        if code != 200:
            _print_json(payload)
            raise SystemExit(1)

        task_id = payload.get("task_id")
        if not task_id:
            _print_json({"detail": "missing task_id", "raw": payload})
            raise SystemExit(1)

        code2, payload2 = _poll_until_done(
            client, task_id, args.interval, args.max_wait
        )
        result_obj = payload2.get("result")
        if isinstance(result_obj, dict) and result_obj.get("message"):
            _print_json(result_obj["message"])
        else:
            _print_json(payload2)
        ok = code2 == 200 and payload2.get("status") == "completed"
        raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
