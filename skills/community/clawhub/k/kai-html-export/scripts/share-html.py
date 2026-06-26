#!/usr/bin/env python3
"""
Route HTML sharing to the configured provider.

Default provider: Cloudflare Pages
Fallback provider: Vercel
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


TRUTHY = {"1", "true", "yes", "on"}
LOCAL_OVERRIDE_VARS = ("KAI_HTML_EXPORT_ENABLE_AUTO_SHARE",)
CLOUD_DISABLE_VARS = (
    "KAI_HTML_EXPORT_DISABLE_AUTO_SHARE",
    "OPENCLAW_CLOUD_SANDBOX",
    "CLAWHUB_SANDBOX",
    "CODEX_SANDBOX",
    "OPENAI_SANDBOX",
)
CLOUD_HINT_VARS = (
    "CI",
    "GITHUB_ACTIONS",
    "GITHUB_CODESPACES",
    "CODESPACES",
    "GITPOD_WORKSPACE_ID",
    "REMOTE_CONTAINERS",
    "DEVCONTAINER",
    "K_SERVICE",
    "K_REVISION",
    "AWS_EXECUTION_ENV",
    "RAILWAY_ENVIRONMENT",
    "RENDER",
    "HEROKU_APP_ID",
)
PROVIDER_SCRIPTS = {
    "cloudflare": "deploy-cloudflare.py",
    "vercel": "deploy-vercel.py",
}


def _is_truthy(value: str | None) -> bool:
    return value is not None and value.strip().lower() in TRUTHY


def detect_share_environment(env: dict[str, str] | os._Environ[str] | None = None) -> str:
    env_map = env or os.environ

    if any(_is_truthy(env_map.get(name)) for name in LOCAL_OVERRIDE_VARS):
        return "local"

    share_mode = (env_map.get("KAI_HTML_EXPORT_SHARE_MODE") or "").strip().lower()
    if share_mode == "manual":
        return "cloud-sandbox"
    if share_mode == "auto":
        return "local"

    if any(_is_truthy(env_map.get(name)) for name in CLOUD_DISABLE_VARS):
        return "cloud-sandbox"

    if any(_is_truthy(env_map.get(name)) for name in CLOUD_HINT_VARS):
        return "cloud-sandbox"

    return "local"


def build_manual_share_message(input_path: str) -> str:
    source_name = Path(input_path).name
    return "\n".join(
        [
            "Automatic sharing is disabled in this cloud sandbox.",
            "Hosted sandboxes should not keep interactive deploy auth or tenant keys.",
            "Recommended manual flow:",
            f"1. Download `{source_name}` to your local machine.",
            "2. Publish it manually with Cloudflare Pages (recommended) or Vercel.",
            f"3. Local command: python scripts/share-html.py \"{source_name}\" --provider cloudflare",
        ]
    )


def _provider_command(provider: str, input_path: str, project_name: str | None, branch: str) -> list[str]:
    script_path = Path(__file__).resolve().with_name(PROVIDER_SCRIPTS[provider])
    command = [sys.executable, str(script_path), input_path]
    if provider == "cloudflare":
        if project_name:
            command += ["--project-name", project_name]
        if branch != "main":
            command += ["--branch", branch]
    return command


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_path", help="HTML file or folder containing index.html")
    parser.add_argument("--provider", choices=sorted(PROVIDER_SCRIPTS), default="cloudflare")
    parser.add_argument("--project-name", help="Cloudflare Pages project name override")
    parser.add_argument("--branch", default="main", help="Cloudflare Pages branch name (default: main)")
    args = parser.parse_args(argv)

    if detect_share_environment() != "local":
        print(build_manual_share_message(args.input_path), file=sys.stderr)
        return 2

    result = subprocess.run(_provider_command(args.provider, args.input_path, args.project_name, args.branch), check=False)
    return int(result.returncode)


if __name__ == "__main__":
    raise SystemExit(main())
