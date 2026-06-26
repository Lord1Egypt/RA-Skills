#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
"""Launch the official X API XMCP server with bearer-token forwarding."""

from __future__ import annotations

import argparse
import hashlib
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

RAW_BASE_URL = "https://raw.githubusercontent.com/xdevplatform/xmcp/master"
SERVER_URL = f"{RAW_BASE_URL}/server.py"
REQUIREMENTS_URL = f"{RAW_BASE_URL}/requirements.txt"
PATCH_MARKER = "# Local wrapper patch: forward MCP Authorization bearer tokens to X API"
HEALTH_MARKER = "# Local wrapper patch: expose /health for the on-demand launcher"
DEFAULT_ALLOWLIST = ",".join(
    [
        "getUsersMe",
        "getUsersByUsername",
        "getUsersById",
        "getPostsById",
        "getPostsByIds",
        "getUsersPosts",
        "searchPostsRecent",
        "createPosts",
        "deletePosts",
    ]
)


def _cache_root() -> Path:
    configured = os.environ.get("MAVERICK_X_MCP_CACHE_DIR", "").strip()
    if configured:
        return Path(configured).expanduser()
    base = os.environ.get("XDG_CACHE_HOME", "").strip()
    root = Path(base).expanduser() if base else Path.home() / ".cache"
    return root / "local-mcp-skills" / "maverick-x-mcp"


def _run(command: list[str], *, cwd: Path | None = None, env: dict[str, str] | None = None) -> None:
    subprocess.run(command, cwd=cwd, env=env, check=True)


def _download(url: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": "maverick-x-mcp"})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            body = response.read()
    except (OSError, urllib.error.URLError) as exc:
        raise RuntimeError(f"Could not download {url}: {exc}") from exc
    if not body:
        raise RuntimeError(f"Downloaded empty file from {url}")
    temporary = destination.with_name(destination.name + f".tmp.{os.getpid()}")
    temporary.write_bytes(body)
    os.replace(temporary, destination)


def _ensure_sources(xmcp_dir: Path) -> None:
    server_path = xmcp_dir / "server.py"
    requirements_path = xmcp_dir / "requirements.txt"
    if not server_path.exists():
        _download(SERVER_URL, server_path)
    if not requirements_path.exists():
        _download(REQUIREMENTS_URL, requirements_path)


def _replace_once(text: str, old: str, new: str, *, label: str) -> str:
    if old not in text:
        raise RuntimeError(
            "Could not patch official XMCP server.py for local bearer-token forwarding. "
            f"The upstream file changed near {label}; inspect the cached server.py."
        )
    return text.replace(old, new, 1)


def _patch_server(xmcp_dir: Path) -> None:
    server_path = xmcp_dir / "server.py"
    text = server_path.read_text(encoding="utf-8")
    if PATCH_MARKER in text and HEALTH_MARKER in text:
        return
    if PATCH_MARKER in text or HEALTH_MARKER in text:
        raise RuntimeError(
            "Cached XMCP server.py is partially patched. Delete the cache directory "
            f"and retry: {xmcp_dir}"
        )

    text = _replace_once(
        text,
        "from fastmcp import FastMCP\n",
        (
            "from fastmcp import FastMCP\n"
            "from fastmcp.server.dependencies import get_http_headers\n"
            "from starlette.responses import JSONResponse\n"
        ),
        label="imports",
    )
    text = _replace_once(
        text,
        """    oauth1_client = build_oauth1_client()
    print_oauth_header = is_truthy(os.getenv("X_OAUTH_PRINT_AUTH_HEADER", "0"))
    if print_oauth_header:
        print_oauth1_header_probe(oauth1_client, base_url)
""",
        """    print_oauth_header = is_truthy(os.getenv("X_OAUTH_PRINT_AUTH_HEADER", "0"))
    auth_mode = os.getenv("X_API_AUTH_MODE", "inbound_bearer").strip().lower()
    oauth1_client = None
    if auth_mode == "oauth1":
        oauth1_client = build_oauth1_client()
        if print_oauth_header:
            print_oauth1_header_probe(oauth1_client, base_url)
""",
        label="oauth1 client setup",
    )
    text = _replace_once(
        text,
        """    async def sign_oauth1_request(request: httpx.Request) -> None:
        request.headers["X-B3-Flags"] = b3_flags
        headers = dict(request.headers)
""",
        f"""    {PATCH_MARKER}
    async def apply_inbound_bearer_request(request: httpx.Request) -> None:
        request.headers["X-B3-Flags"] = b3_flags
        if request.headers.get("Authorization"):
            return
        inbound_headers = get_http_headers()
        authorization = (
            inbound_headers.get("authorization", "")
            or inbound_headers.get("Authorization", "")
        ).strip()
        if authorization:
            request.headers["Authorization"] = authorization
            return
        fallback_token = os.getenv("X_OAUTH_ACCESS_TOKEN", "").strip()
        if fallback_token:
            request.headers["Authorization"] = f"Bearer {{fallback_token}}"
            return
        raise RuntimeError("Missing inbound bearer token for X API request.")

    async def sign_oauth1_request(request: httpx.Request) -> None:
        if oauth1_client is None:
            raise RuntimeError("OAuth1 auth mode selected without an OAuth1 client.")
        request.headers["X-B3-Flags"] = b3_flags
        headers = dict(request.headers)
""",
        label="request signer",
    )
    text = _replace_once(
        text,
        """"request": [normalize_query_params, sign_oauth1_request, log_request],""",
        """"request": [
                normalize_query_params,
                sign_oauth1_request if auth_mode == "oauth1" else apply_inbound_bearer_request,
                log_request,
            ],""",
        label="httpx event hooks",
    )
    text = _replace_once(
        text,
        """    return FastMCP.from_openapi(
        openapi_spec=filtered_spec,
        client=client,
        name="X API MCP",
    )
""",
        f"""    mcp = FastMCP.from_openapi(
        openapi_spec=filtered_spec,
        client=client,
        name="X API MCP",
    )

    {HEALTH_MARKER}
    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(request):
        _ = request
        return JSONResponse({{"ok": True}})

    return mcp
""",
        label="health route",
    )
    server_path.write_text(text, encoding="utf-8")


def _requirements_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _ensure_venv(xmcp_dir: Path) -> Path:
    venv_dir = xmcp_dir / ".venv"
    python = venv_dir / "bin" / "python"
    if not python.exists():
        _run([sys.executable, "-m", "venv", str(venv_dir)])
    requirements = xmcp_dir / "requirements.txt"
    marker = venv_dir / ".requirements.sha256"
    current_hash = _requirements_hash(requirements)
    installed_hash = marker.read_text(encoding="utf-8").strip() if marker.exists() else ""
    if installed_hash != current_hash:
        _run([str(python), "-m", "pip", "install", "--upgrade", "pip"], cwd=xmcp_dir)
        _run([str(python), "-m", "pip", "install", "-r", str(requirements)], cwd=xmcp_dir)
        marker.write_text(current_hash, encoding="utf-8")
    return python


def _write_env_file(xmcp_dir: Path, *, host: str, port: int) -> dict[str, str]:
    values = {
        "X_API_AUTH_MODE": os.environ.get("X_API_AUTH_MODE", "inbound_bearer"),
        "X_API_BASE_URL": os.environ.get("X_API_BASE_URL", "https://api.x.com"),
        "X_API_TIMEOUT": os.environ.get("X_API_TIMEOUT", "30"),
        "X_API_DEBUG": os.environ.get("X_API_DEBUG", "0"),
        "X_API_TOOL_ALLOWLIST": os.environ.get("X_API_TOOL_ALLOWLIST", DEFAULT_ALLOWLIST),
        "MCP_HOST": host,
        "MCP_PORT": str(port),
    }
    lines = [f"{key}={value}" for key, value in values.items()]
    (xmcp_dir / ".env").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return values


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args()

    xmcp_dir = _cache_root() / "xmcp"
    _ensure_sources(xmcp_dir)
    _patch_server(xmcp_dir)
    python = _ensure_venv(xmcp_dir)
    values = _write_env_file(xmcp_dir, host=args.host, port=args.port)

    child_env = os.environ.copy()
    child_env.update(values)
    server_entry = xmcp_dir / "server.py"
    os.chdir(xmcp_dir)
    os.execve(str(python), [str(python), str(server_entry)], child_env)


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as exc:
        print(f"server.py: {exc}", file=sys.stderr)
        raise SystemExit(1)
