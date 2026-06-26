#!/usr/bin/env python3
import argparse
import json
import os
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

import requests


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def derive_api_base_from_gateway(gateway_url: str) -> str | None:
    if not gateway_url:
        return None
    parsed = urlparse(gateway_url)
    if not parsed.scheme or not parsed.netloc:
        return None
    return f"{parsed.scheme}://{parsed.netloc}/api/v1"


def resolve_api_base(cli_value: str | None) -> str:
    if cli_value:
        return cli_value.rstrip("/")
    env_value = os.environ.get("KNODS_API_BASE_URL", "").strip()
    if env_value:
        return env_value.rstrip("/")
    derived = derive_api_base_from_gateway(os.environ.get("KNODS_BASE_URL", "").strip())
    if derived:
        return derived.rstrip("/")
    raise SystemExit("missing KNODS_API_BASE_URL")


def resolve_api_key(cli_value: str | None) -> str:
    if cli_value:
        return cli_value.strip()
    env_value = os.environ.get("KNODS_API_KEY", "").strip()
    if env_value:
        return env_value
    raise SystemExit("missing KNODS_API_KEY")


def parse_inputs(args: argparse.Namespace) -> list[dict]:
    if args.inputs_json:
        return json.loads(args.inputs_json)
    if args.inputs_file:
        return json.loads(Path(args.inputs_file).read_text(encoding="utf-8"))
    return []


def request_json(
    session: requests.Session,
    method: str,
    url: str,
    payload: dict | None = None,
    timeout: int = 60,
) -> tuple[dict, requests.Response]:
    response = session.request(method, url, json=payload, timeout=timeout)
    if response.status_code == 429:
        retry_after = 1.0
        try:
            retry_after = float(response.json().get("retry_after", 1.0))
        except Exception:
            pass
        time.sleep(retry_after + 0.25)
        response = session.request(method, url, json=payload, timeout=timeout)
    response.raise_for_status()
    return response.json() if response.content else {}, response


def print_json(payload: dict) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--env-file", default=str(Path.home() / ".openclaw" / ".env"))
    parser.add_argument("--base-url")
    parser.add_argument("--api-key")


def main() -> int:
    parser = argparse.ArgumentParser(description="Knods headless flows API client")
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List available flows")
    add_common_args(list_parser)

    resolve_parser = subparsers.add_parser("resolve", help="Find flows matching a query")
    add_common_args(resolve_parser)
    resolve_parser.add_argument("--query", required=True)

    get_parser = subparsers.add_parser("get", help="Get flow details and input schema")
    add_common_args(get_parser)
    get_parser.add_argument("--flow-id", required=True)

    run_parser = subparsers.add_parser("run", help="Start a flow run")
    add_common_args(run_parser)
    run_parser.add_argument("--flow-id", required=True)
    run_parser.add_argument("--inputs-json")
    run_parser.add_argument("--inputs-file")

    poll_parser = subparsers.add_parser("poll", help="Poll a run status once")
    add_common_args(poll_parser)
    poll_parser.add_argument("--run-id", required=True)

    wait_parser = subparsers.add_parser("wait", help="Poll a run until terminal state")
    add_common_args(wait_parser)
    wait_parser.add_argument("--run-id", required=True)
    wait_parser.add_argument("--interval", type=float, default=3.0)
    wait_parser.add_argument("--timeout-seconds", type=float, default=300.0)
    wait_parser.add_argument("--cancel-on-timeout", action="store_true")

    cancel_parser = subparsers.add_parser("cancel", help="Cancel a run")
    add_common_args(cancel_parser)
    cancel_parser.add_argument("--run-id", required=True)

    run_wait_parser = subparsers.add_parser("run-wait", help="Start a run and wait for result")
    add_common_args(run_wait_parser)
    run_wait_parser.add_argument("--flow-id", required=True)
    run_wait_parser.add_argument("--inputs-json")
    run_wait_parser.add_argument("--inputs-file")
    run_wait_parser.add_argument("--interval", type=float, default=3.0)
    run_wait_parser.add_argument("--timeout-seconds", type=float, default=300.0)
    run_wait_parser.add_argument("--cancel-on-timeout", action="store_true")

    args = parser.parse_args()
    load_env_file(Path(args.env_file))
    base_url = resolve_api_base(getattr(args, "base_url", None))
    api_key = resolve_api_key(getattr(args, "api_key", None))

    session = requests.Session()
    session.headers.update(
        {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
            "User-Agent": "openclaw-knods-headless/1.0",
        }
    )

    if args.command == "list":
        payload, _ = request_json(session, "GET", f"{base_url}/knods")
        print_json(payload)
        return 0

    if args.command == "resolve":
        payload, _ = request_json(session, "GET", f"{base_url}/knods")
        query = args.query.strip().lower()
        flows = payload.get("flows", [])
        matches = [
            flow
            for flow in flows
            if query in str(flow.get("name", "")).lower() or query in str(flow.get("description", "")).lower()
        ]
        print_json({"query": args.query, "matches": matches})
        return 0

    if args.command == "get":
        payload, _ = request_json(session, "GET", f"{base_url}/knods/{args.flow_id}")
        print_json(payload)
        return 0

    if args.command == "run":
        inputs = parse_inputs(args)
        payload, _ = request_json(
            session,
            "POST",
            f"{base_url}/knods/{args.flow_id}/run",
            payload={"inputs": inputs},
        )
        print_json(payload)
        return 0

    if args.command == "poll":
        payload, _ = request_json(session, "GET", f"{base_url}/runs/{args.run_id}")
        print_json(payload)
        return 0

    if args.command == "cancel":
        payload, _ = request_json(session, "POST", f"{base_url}/runs/{args.run_id}/cancel")
        print_json(payload)
        return 0

    def wait_for_run(run_id: str, interval: float, timeout_seconds: float, cancel_on_timeout: bool) -> dict:
        started = time.time()
        while True:
            payload, _ = request_json(session, "GET", f"{base_url}/runs/{run_id}")
            status = str(payload.get("status", "")).strip().lower()
            if status not in {"pending", "running"}:
                return payload
            if time.time() - started >= timeout_seconds:
                if cancel_on_timeout:
                    try:
                        request_json(session, "POST", f"{base_url}/runs/{run_id}/cancel")
                    except Exception:
                        pass
                raise TimeoutError(f"run {run_id} timed out after {timeout_seconds} seconds")
            time.sleep(interval)

    if args.command == "wait":
        payload = wait_for_run(args.run_id, args.interval, args.timeout_seconds, args.cancel_on_timeout)
        print_json(payload)
        return 0

    if args.command == "run-wait":
        inputs = parse_inputs(args)
        run_payload, _ = request_json(
            session,
            "POST",
            f"{base_url}/knods/{args.flow_id}/run",
            payload={"inputs": inputs},
        )
        run_id = str(run_payload.get("runId", "")).strip()
        if not run_id:
            raise SystemExit("run response missing runId")
        final_payload = wait_for_run(run_id, args.interval, args.timeout_seconds, args.cancel_on_timeout)
        print_json({"run": run_payload, "final": final_payload})
        return 0

    raise SystemExit(f"unknown command: {args.command}")


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except requests.HTTPError as exc:
        response = exc.response
        body = {}
        if response is not None:
            try:
                body = response.json()
            except Exception:
                body = {"text": response.text}
        print(json.dumps({"error": str(exc), "status": getattr(response, "status_code", None), "body": body}, ensure_ascii=False, indent=2), file=sys.stderr)
        raise
