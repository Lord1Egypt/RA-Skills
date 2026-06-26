#!/usr/bin/env python3
"""Helpers for OpenMarlin registration sessions."""

from __future__ import annotations

import argparse
import json
import os
import platform
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

from openclaw_skill_config import (
    DEFAULT_SERVER_URL,
    build_server_connection_error,
    get_skill_env,
    probe_server_openapi,
    require_server_url,
)
from openclaw_platform_auth import (
    DEFAULT_AGENT_ID,
    DEFAULT_PROFILE_ID,
    upsert_platform_api_key,
)


DEFAULT_POLL_INTERVAL_SECONDS = 2.0
DEFAULT_TIMEOUT_SECONDS = 300.0
DEFAULT_API_KEY_LABEL = "OpenClaw bootstrap"


def parse_args() -> argparse.Namespace:
    default_server_url, server_url_source = get_skill_env("OPENMARLIN_SERVER_URL")
    parser = argparse.ArgumentParser(
        description="Create, inspect, and poll OpenMarlin registration sessions."
    )
    parser.set_defaults(_server_url_source=server_url_source)
    parser.add_argument(
        "--server-url",
        default=(default_server_url or "").strip(),
        help=f"Base URL for the OpenMarlin server. Defaults to OPENMARLIN_SERVER_URL, then OpenClaw skill config, then {DEFAULT_SERVER_URL}. Do not include /v1.",
    )
    json_parent = argparse.ArgumentParser(add_help=False)
    json_parent.add_argument(
        "--json",
        action="store_true",
        help="Print raw JSON only.",
    )
    json_parent.add_argument(
        "--dry-run",
        action="store_true",
        help="Show resolved configuration and a lightweight connectivity check without executing the command.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    create_parser = subparsers.add_parser(
        "create",
        help="Create a registration session.",
        parents=[json_parent],
    )
    create_parser.add_argument(
        "--auth-flow",
        choices=("device", "workos_callback"),
        default="device",
        help="Registration auth flow. Default: device.",
    )

    status_parser = subparsers.add_parser(
        "status",
        help="Fetch the current session state.",
        parents=[json_parent],
    )
    status_parser.add_argument("--session-id", required=True, help="Registration session ID.")

    watch_parser = subparsers.add_parser(
        "watch",
        help="Poll until completion or expiration.",
        parents=[json_parent],
    )
    watch_parser.add_argument("--session-id", required=True, help="Registration session ID.")
    watch_parser.add_argument(
        "--interval-seconds",
        type=float,
        default=DEFAULT_POLL_INTERVAL_SECONDS,
        help=f"Polling interval in seconds. Default: {DEFAULT_POLL_INTERVAL_SECONDS}.",
    )
    watch_parser.add_argument(
        "--timeout-seconds",
        type=float,
        default=DEFAULT_TIMEOUT_SECONDS,
        help=f"Maximum total wait time in seconds. Default: {DEFAULT_TIMEOUT_SECONDS}.",
    )

    issue_parser = subparsers.add_parser(
        "issue-api-key",
        help="Issue a workspace API key for a completed registration session.",
        parents=[json_parent],
    )
    issue_parser.add_argument("--session-id", required=True, help="Registration session ID.")
    issue_parser.add_argument(
        "--label",
        default=DEFAULT_API_KEY_LABEL,
        help=f"Optional API key label. Default: {DEFAULT_API_KEY_LABEL}.",
    )
    issue_parser.add_argument(
        "--store",
        action="store_true",
        help="Store the issued API key in OpenClaw auth-profiles.json.",
    )
    issue_parser.add_argument(
        "--profile-id",
        default=DEFAULT_PROFILE_ID,
        help=f"Auth profile ID used when --store is set. Default: {DEFAULT_PROFILE_ID}.",
    )
    issue_parser.add_argument(
        "--agent-id",
        default=DEFAULT_AGENT_ID,
        help=f"OpenClaw agent ID used when --store is set. Default: {DEFAULT_AGENT_ID}.",
    )

    bootstrap_parser = subparsers.add_parser(
        "bootstrap",
        help="Wait for completion, then issue a workspace API key.",
        parents=[json_parent],
    )
    bootstrap_parser.add_argument("--session-id", required=True, help="Registration session ID.")
    bootstrap_parser.add_argument(
        "--label",
        default=DEFAULT_API_KEY_LABEL,
        help=f"Optional API key label. Default: {DEFAULT_API_KEY_LABEL}.",
    )
    bootstrap_parser.add_argument(
        "--interval-seconds",
        type=float,
        default=DEFAULT_POLL_INTERVAL_SECONDS,
        help=f"Polling interval in seconds. Default: {DEFAULT_POLL_INTERVAL_SECONDS}.",
    )
    bootstrap_parser.add_argument(
        "--timeout-seconds",
        type=float,
        default=DEFAULT_TIMEOUT_SECONDS,
        help=f"Maximum total wait time in seconds. Default: {DEFAULT_TIMEOUT_SECONDS}.",
    )
    bootstrap_parser.add_argument(
        "--store",
        action="store_true",
        help="Store the issued API key in OpenClaw auth-profiles.json.",
    )
    bootstrap_parser.add_argument(
        "--profile-id",
        default=DEFAULT_PROFILE_ID,
        help=f"Auth profile ID used when --store is set. Default: {DEFAULT_PROFILE_ID}.",
    )
    bootstrap_parser.add_argument(
        "--agent-id",
        default=DEFAULT_AGENT_ID,
        help=f"OpenClaw agent ID used when --store is set. Default: {DEFAULT_AGENT_ID}.",
    )

    return parser.parse_args()


def print_dry_run(args: argparse.Namespace, server_url: str) -> int:
    reachable, detail = probe_server_openapi(server_url)
    payload = {
        "ok": reachable,
        "dry_run": True,
        "command": args.command,
        "server_url": server_url,
        "server_url_source": args.server_url and (args._server_url_source or "flag-or-arg"),
        "connectivity": detail,
    }
    if args.command == "create":
        payload["auth_flow"] = args.auth_flow
    elif hasattr(args, "session_id"):
        payload["session_id"] = args.session_id

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print("Dry run only. No registration session action was executed.")
        print(f"Command: {args.command}")
        print(f"Resolved server URL: {server_url}")
        print(f"Server URL source: {payload['server_url_source']}")
        print(f"Connectivity check: {detail}")
        if args.command == "create":
            print(f"Auth flow: {args.auth_flow}")
        elif "session_id" in payload:
            print(f"Session ID: {payload['session_id']}")
    return 0 if reachable else 1

def request_json(url: str, method: str = "GET", payload: dict[str, Any] | None = None) -> dict[str, Any]:
    body = None
    headers = {"Accept": "application/json"}
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = urllib.request.Request(url, data=body, method=method, headers=headers)
    try:
        with urllib.request.urlopen(request) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as error:
        raw = error.read().decode("utf-8")
        message = raw or error.reason
        try:
            payload_obj = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            payload_obj = {"error": message}
        raise SystemExit(
            f"HTTP {error.code} for {method} {url}: {json.dumps(payload_obj, sort_keys=True)}"
        ) from error
    except urllib.error.URLError as error:
        parsed = urllib.parse.urlparse(url)
        base_url = f"{parsed.scheme}://{parsed.netloc}" if parsed.scheme and parsed.netloc else url
        raise SystemExit(build_server_connection_error(base_url, str(error.reason))) from error


def build_browser_url(session: dict[str, Any]) -> str | None:
    handoff = session.get("handoff")
    if not isinstance(handoff, dict):
        return None

    authorization_url = handoff.get("authorization_url")
    if not isinstance(authorization_url, str) or not authorization_url.strip():
        return None
    return authorization_url.strip()


def auto_open_browser_url(browser_url: str) -> tuple[bool, str]:
    system = platform.system().lower()
    try:
        if system == "darwin":
            completed = subprocess.run(
                ["open", browser_url],
                check=False,
                capture_output=True,
                text=True,
            )
        elif system == "windows":
            os.startfile(browser_url)  # type: ignore[attr-defined]
            return True, "Opened the authorization page in your default browser."
        else:
            completed = subprocess.run(
                ["xdg-open", browser_url],
                check=False,
                capture_output=True,
                text=True,
            )
    except FileNotFoundError as error:
        return False, f"Could not auto-open the browser because the opener is missing: {error.filename}"
    except OSError as error:
        return False, f"Could not auto-open the browser: {error}"

    if completed.returncode == 0:
        return True, "Opened the authorization page in your default browser."

    detail = (completed.stderr or completed.stdout or "").strip()
    if detail:
        return False, f"Could not auto-open the browser: {detail}"
    return False, "Could not auto-open the browser."


def completion_summary(session: dict[str, Any]) -> list[str]:
    completion = session.get("completion")
    if not isinstance(completion, dict):
        return []

    workspace = completion.get("workspace")
    provider_identity = completion.get("provider_identity")
    credential_bootstrap = completion.get("credential_bootstrap")

    lines = [
        f"Account ID: {completion.get('account_id', '<unknown>')}",
        f"New account: {completion.get('is_new_account', '<unknown>')}",
    ]

    if isinstance(workspace, dict):
        lines.extend(
            [
                f"Workspace ID: {workspace.get('workspace_id', '<unknown>')}",
                f"Workspace: {workspace.get('display_name', '<unknown>')} ({workspace.get('slug', '<unknown>')})",
            ]
        )

    if isinstance(provider_identity, dict):
        lines.extend(
            [
                f"Provider: {provider_identity.get('provider', '<unknown>')}",
                f"Provider subject: {provider_identity.get('provider_subject', '<unknown>')}",
            ]
        )
        primary_email = provider_identity.get("primary_email")
        if primary_email:
            lines.append(f"Primary email: {primary_email}")

    if isinstance(credential_bootstrap, dict):
        lines.append(
            f"Credential bootstrap: {credential_bootstrap.get('status', '<unknown>')}"
        )

    return lines


def print_session(session: dict[str, Any]) -> None:
    handoff = session.get("handoff")
    browser_url = build_browser_url(session)

    print(f"Session ID: {session.get('registration_session_id', '<unknown>')}")
    print(f"State: {session.get('state', '<unknown>')}")
    print(f"Auth flow: {session.get('auth_flow', '<unknown>')}")
    print(f"Provider: {session.get('provider', '<unknown>')}")
    print(f"Created at: {session.get('created_at', '<unknown>')}")
    print(f"Expires at: {session.get('expires_at', '<unknown>')}")

    if isinstance(handoff, dict):
        print(f"Handoff type: {handoff.get('type', '<unknown>')}")
        if handoff.get("device_code"):
            print(f"Device code: {handoff.get('device_code')}")
        if handoff.get("callback_state"):
            print(f"Callback state: {handoff.get('callback_state')}")

    if browser_url:
        print(f"Browser URL: {browser_url}")
    elif session.get("state") == "pending_external_auth":
        print("Browser URL: <not provided by server>")

    completion_lines = completion_summary(session)
    if completion_lines:
        print("Completion:")
        for line in completion_lines:
            print(f"  {line}")
    elif session.get("state") == "pending_external_auth":
        print("Completion: waiting for external auth")


def print_create_next_steps(session: dict[str, Any]) -> None:
    if session.get("state") != "pending_external_auth":
        return

    browser_url = build_browser_url(session)
    handoff = session.get("handoff")

    if browser_url:
        opened, message = auto_open_browser_url(browser_url)
        print(message)
        if not opened:
            print(f"Open this URL manually: {browser_url}")
    elif isinstance(handoff, dict) and handoff.get("device_code"):
        print("No browser URL was provided by the server.")

    if isinstance(handoff, dict):
        device_code = handoff.get("device_code")
        if isinstance(device_code, str) and device_code:
            print(f"Use device code: {device_code}")

    session_id = session.get("registration_session_id")
    if isinstance(session_id, str) and session_id:
        print("Do not depend on the browser callback page returning machine-readable JSON.")
        print("OpenClaw should keep polling the registration session until it becomes completed or expired.")
        print(f"Continue in OpenClaw with: python3 scripts/registration_session.py watch --session-id {session_id}")
        print('After completing the browser step or landing on the frontend page, say "done" or run the watch command above.')


def build_api_key_issue_payload(session: dict[str, Any], label: str | None) -> dict[str, Any]:
    handoff = session.get("handoff")
    if not isinstance(handoff, dict):
        raise SystemExit("Registration session is missing handoff details.")

    payload: dict[str, Any] = {}
    handoff_type = handoff.get("type")
    if handoff_type == "device":
        device_code = handoff.get("device_code")
        if not isinstance(device_code, str) or not device_code:
            raise SystemExit("Registration session is missing device_code for API key bootstrap.")
        payload["device_code"] = device_code
    elif handoff_type == "browser":
        callback_state = handoff.get("callback_state")
        if not isinstance(callback_state, str) or not callback_state:
            raise SystemExit("Registration session is missing callback_state for API key bootstrap.")
        payload["callback_state"] = callback_state
    else:
        raise SystemExit(f"Unsupported handoff type for API key bootstrap: {handoff_type}")

    if label:
        payload["label"] = label

    return payload


def issue_api_key(server_url: str, session: dict[str, Any], label: str | None) -> dict[str, Any]:
    session_id = session.get("registration_session_id")
    if not isinstance(session_id, str) or not session_id:
        raise SystemExit("Registration session is missing registration_session_id.")
    if session.get("state") != "completed":
        raise SystemExit("Registration session must be completed before issuing an API key.")

    return request_json(
        f"{server_url}/v1/registration/sessions/{urllib.parse.quote(session_id)}/api-keys",
        method="POST",
        payload=build_api_key_issue_payload(session, label),
    )


def print_api_key_issue(result: dict[str, Any], session: dict[str, Any] | None = None) -> None:
    if session is not None:
        print(f"Session ID: {session.get('registration_session_id', '<unknown>')}")
        completion = session.get("completion")
        if isinstance(completion, dict):
            print(f"Account ID: {completion.get('account_id', '<unknown>')}")
            workspace = completion.get("workspace")
            if isinstance(workspace, dict):
                print(
                    f"Workspace: {workspace.get('display_name', '<unknown>')} "
                    f"({workspace.get('slug', '<unknown>')})"
                )

    api_key = result.get("api_key")
    if not isinstance(api_key, dict):
        raise SystemExit("API key bootstrap response is missing api_key metadata.")

    print(f"Key ID: {api_key.get('key_id', '<unknown>')}")
    print(f"Workspace ID: {api_key.get('workspace_id', '<unknown>')}")
    print(f"Status: {api_key.get('status', '<unknown>')}")
    print(f"Label: {api_key.get('label', '<unknown>')}")
    print(f"Created at: {api_key.get('created_at', '<unknown>')}")
    print(f"Last used at: {api_key.get('last_used_at', '<unknown>')}")
    print(f"Secret: {result.get('secret', '<missing>')}")
    print("Export:")
    print(f"  export OPENMARLIN_PLATFORM_API_KEY='{result.get('secret', '')}'")


def build_storage_metadata(
    *,
    server_url: str,
    session: dict[str, Any],
    result: dict[str, Any],
) -> dict[str, str]:
    metadata: dict[str, str] = {"server_url": server_url}

    api_key = result.get("api_key")
    if isinstance(api_key, dict):
        for field in ("key_id", "workspace_id", "created_at", "label", "status"):
            value = api_key.get(field)
            if isinstance(value, str) and value:
                metadata[field] = value

    completion = session.get("completion")
    if isinstance(completion, dict):
        account_id = completion.get("account_id")
        if isinstance(account_id, str) and account_id:
            metadata["account_id"] = account_id
        workspace = completion.get("workspace")
        if isinstance(workspace, dict):
            workspace_slug = workspace.get("slug")
            if isinstance(workspace_slug, str) and workspace_slug:
                metadata["workspace_slug"] = workspace_slug
            workspace_display_name = workspace.get("display_name")
            if isinstance(workspace_display_name, str) and workspace_display_name:
                metadata["workspace_display_name"] = workspace_display_name

    return metadata


def maybe_store_api_key(
    *,
    should_store: bool,
    server_url: str,
    session: dict[str, Any],
    result: dict[str, Any],
    profile_id: str,
    agent_id: str,
) -> dict[str, Any] | None:
    if not should_store:
        return None

    secret = result.get("secret")
    if not isinstance(secret, str) or not secret:
        raise SystemExit("API key bootstrap response is missing the secret required for storage.")

    return upsert_platform_api_key(
        secret=secret,
        profile_id=profile_id,
        agent_id=agent_id,
        metadata=build_storage_metadata(server_url=server_url, session=session, result=result),
    )


def create_session(server_url: str, auth_flow: str) -> dict[str, Any]:
    return request_json(
        f"{server_url}/v1/registration/sessions",
        method="POST",
        payload={"provider": "workos", "auth_flow": auth_flow},
    )


def fetch_session(server_url: str, session_id: str) -> dict[str, Any]:
    return request_json(f"{server_url}/v1/registration/sessions/{urllib.parse.quote(session_id)}")


def watch_session(server_url: str, session_id: str, interval_seconds: float, timeout_seconds: float) -> dict[str, Any]:
    deadline = time.monotonic() + timeout_seconds
    while True:
        session = fetch_session(server_url, session_id)
        state = session.get("state")
        if state in {"completed", "expired"}:
            return session
        if time.monotonic() >= deadline:
            raise SystemExit(
                f"Timed out after {timeout_seconds:.1f}s waiting for session {session_id}."
            )
        time.sleep(interval_seconds)

def main() -> int:
    args = parse_args()
    server_url = require_server_url(args.server_url)
    if args.dry_run:
        return print_dry_run(args, server_url)

    if args.command == "create":
        session = create_session(server_url, args.auth_flow)
    elif args.command == "status":
        session = fetch_session(server_url, args.session_id)
    elif args.command == "watch":
        session = watch_session(
            server_url,
            args.session_id,
            args.interval_seconds,
            args.timeout_seconds,
        )
    elif args.command == "issue-api-key":
        session = fetch_session(server_url, args.session_id)
        result = issue_api_key(server_url, session, args.label)
        storage = maybe_store_api_key(
            should_store=args.store,
            server_url=server_url,
            session=session,
            result=result,
            profile_id=args.profile_id,
            agent_id=args.agent_id,
        )
    elif args.command == "bootstrap":
        session = watch_session(
            server_url,
            args.session_id,
            args.interval_seconds,
            args.timeout_seconds,
        )
        result = issue_api_key(server_url, session, args.label)
        storage = maybe_store_api_key(
            should_store=args.store,
            server_url=server_url,
            session=session,
            result=result,
            profile_id=args.profile_id,
            agent_id=args.agent_id,
        )
    else:
        raise SystemExit(f"Unsupported command: {args.command}")

    if args.command in {"issue-api-key", "bootstrap"}:
        output: dict[str, Any]
        if args.command == "bootstrap":
            output = {
                "session": session,
                "issued": result,
            }
        else:
            output = result
        if storage:
            output["stored"] = storage

        if args.json:
            print(json.dumps(output, indent=2, sort_keys=True))
        else:
            print_api_key_issue(result, session)
            if storage:
                print("Stored:")
                print(f"  Auth store: {storage['auth_store_path']}")
                print(f"  Profile ID: {storage['profile_id']}")
                print(f"  Agent ID: {storage['agent_id']}")
    else:
        if args.json:
            print(json.dumps(session, indent=2, sort_keys=True))
        else:
            print_session(session)
            if args.command == "create":
                print_create_next_steps(session)

    return 3 if args.command in {"create", "status", "watch"} and session.get("state") == "expired" else 0


if __name__ == "__main__":
    sys.exit(main())
