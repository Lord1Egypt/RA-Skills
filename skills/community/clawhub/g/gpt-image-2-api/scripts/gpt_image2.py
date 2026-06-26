#!/usr/bin/env python3
"""
gpt-image-2 CLI — Text-to-Image & Image-to-Image

Agent-agnostic: works with Hermes, Claude Code, OpenClaw, Codex, or any agent.
Config discovery: --config flag > XDG_CONFIG_HOME > ~/.config/ > ~/.hermes/ (legacy compat)

Usage:
  # Text-to-image
  python3 gpt_image2.py generate "A cute cat" -o cat.png --quality low

  # Image-to-image
  python3 gpt_image2.py edit input.png "Change sofa to green" -o out.png

  # Explicit config
  python3 gpt_image2.py generate "sunset" --config /path/to/config.json

  # Inline override
  python3 gpt_image2.py generate "sunset" --base-url https://relay.example.com/v1 --api-key sk-xxx
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Optional

DEFAULT_BASE_URL = "https://api.openai.com/v1"

# ── Config Discovery ──────────────────────────────────────────────
# Priority: --config flag > XDG_CONFIG_HOME/gpt-image-2/config.json
#           > ~/.config/gpt-image-2/config.json
#           > ~/.gpt-image-2-config.json  (single-file fallback)
#           > ~/.hermes/gpt-image-2-config.json  (legacy compat)

def _xdg_config_home() -> Path:
    return Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))

def _config_candidates() -> list[Path]:
    """Return config file candidates in priority order."""
    xdg = _xdg_config_home()
    return [
        xdg / "gpt-image-2" / "config.json",
        Path.home() / ".gpt-image-2-config.json",
        Path.home() / ".hermes" / "gpt-image-2-config.json",  # legacy
    ]

def _find_config_path(explicit: str | None = None) -> Path | None:
    """Find the first existing config file, or return the explicit path."""
    if explicit:
        p = Path(explicit)
        if not p.exists():
            print(f"WARNING: Explicit config not found: {p}", file=sys.stderr)
        return p
    for p in _config_candidates():
        if p.exists():
            return p
    return None

def _default_config_path() -> Path:
    """Where to write a new config if none exists (XDG location)."""
    return _xdg_config_home() / "gpt-image-2" / "config.json"


def load_config(explicit_path: str | None = None) -> dict:
    """Load config from the best available location."""
    p = _find_config_path(explicit_path)
    if p is None or not p.exists():
        return {}
    # Warn on loose permissions
    try:
        mode = p.stat().st_mode & 0o777
        if mode & 0o077:
            import warnings
            warnings.warn(f"Config has loose permissions ({oct(mode)}). Run: chmod 600 {p}")
    except OSError:
        pass
    try:
        with open(p) as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"WARNING: Failed to parse config {p}: {e}", file=sys.stderr)
        return {}


# ── Auth Resolution ───────────────────────────────────────────────

def get_base_url(cli_value: str | None = None, config: dict | None = None) -> str:
    """Priority: CLI > config.base_url > GPT_IMAGE2_BASE_URL env > default"""
    if cli_value:
        return cli_value.rstrip("/")
    if config is None:
        config = {}
    if config.get("base_url"):
        return config["base_url"].rstrip("/")
    env_val = os.environ.get("GPT_IMAGE2_BASE_URL", "")
    if env_val:
        return env_val.rstrip("/")
    return DEFAULT_BASE_URL


def get_api_key(cli_value: str | None = None, config: dict | None = None) -> str:
    """Priority: CLI > config.api_key > config.api_key_env > GPT_IMAGE2_API_KEY env"""
    if cli_value:
        return cli_value
    if config is None:
        config = {}
    if config.get("api_key"):
        return config["api_key"]
    if config.get("api_key_env"):
        return os.environ.get(config["api_key_env"], "")
    return os.environ.get("GPT_IMAGE2_API_KEY", "")


# ── Response Handling ─────────────────────────────────────────────

def decode_and_save(response_path: str, output_path: str) -> list[tuple[str, int]]:
    """Decode API b64_json response and save image(s). Returns [(path, size_bytes)]."""
    raw = Path(response_path).read_text(errors="replace")
    if not raw.strip():
        print("ERROR: Empty response from API (server may be down or timed out)", file=sys.stderr)
        sys.exit(1)
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        # Show first 500 chars of non-JSON response for debugging
        print(f"ERROR: Non-JSON response (first 500 chars): {raw[:500]}", file=sys.stderr)
        sys.exit(1)

    if "error" in data:
        print(f"API ERROR: {json.dumps(data['error'], ensure_ascii=False)}", file=sys.stderr)
        sys.exit(1)

    if "data" not in data or len(data["data"]) == 0:
        print("ERROR: No image data in response", file=sys.stderr)
        sys.exit(1)

    saved = []
    for i, item in enumerate(data["data"]):
        b64 = item.get("b64_json", "")
        if not b64:
            print(f"WARNING: Item {i} has no b64_json, skipping", file=sys.stderr)
            continue
        img_bytes = base64.b64decode(b64)

        if len(data["data"]) == 1:
            out = output_path
        else:
            p = Path(output_path)
            out = str(p.with_name(f"{p.stem}-{i}{p.suffix}"))

        with open(out, "wb") as f:
            f.write(img_bytes)
        saved.append((out, len(img_bytes)))

    for path, size in saved:
        print(f"Saved: {path} ({size / 1024:.1f} KB)")
    return saved


# ── curl helpers ──────────────────────────────────────────────────

def _curl_auth_header(api_key: str) -> str:
    """Write Authorization header to a temp curl-config file. Caller must unlink."""
    fd, path = tempfile.mkstemp(suffix=".headers")
    with os.fdopen(fd, "w") as f:
        f.write(f'-H "Authorization: Bearer {api_key}"\n')
    return path


def _curl_post_json(url: str, api_key: str, body: dict, resp_path: str, timeout: int) -> subprocess.CompletedProcess:
    """POST JSON body via curl, auth via -K temp file (not visible in ps)."""
    body_fd, body_path = tempfile.mkstemp(suffix=".json")
    with os.fdopen(body_fd, "w") as f:
        json.dump(body, f, ensure_ascii=False)

    header_path = _curl_auth_header(api_key)

    # Also add Content-Type via the same -K file
    with open(header_path, "a") as f:
        f.write('-H "Content-Type: application/json"\n')

    try:
        result = subprocess.run(
            [
                "curl", "-s", "-X", "POST", url,
                "-K", header_path,
                "-d", f"@{body_path}",
                "-o", resp_path,
                "-w", "\nHTTP_CODE:%{http_code}\nTIME:%{time_total}s",
            ],
            capture_output=True, text=True, timeout=timeout,
        )
        return result
    except subprocess.TimeoutExpired:
        print(f"ERROR: curl timed out after {timeout}s", file=sys.stderr)
        sys.exit(1)
    finally:
        for p in [body_path, header_path]:
            if os.path.exists(p):
                os.unlink(p)


def _curl_post_multipart(url: str, api_key: str, fields: list[tuple[str, str]],
                          resp_path: str, timeout: int) -> subprocess.CompletedProcess:
    """POST multipart/form-data via curl, auth via -K temp file."""
    header_path = _curl_auth_header(api_key)
    try:
        cmd = ["curl", "-s", "-X", "POST", url, "-K", header_path]
        for key, val in fields:
            cmd += ["-F", f"{key}={val}"]
        cmd += ["-o", resp_path, "-w", "\nHTTP_CODE:%{http_code}\nTIME:%{time_total}s"]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return result
    except subprocess.TimeoutExpired:
        print(f"ERROR: curl timed out after {timeout}s", file=sys.stderr)
        sys.exit(1)
    finally:
        if os.path.exists(header_path):
            os.unlink(header_path)


# ── Commands ──────────────────────────────────────────────────────

def cmd_generate(args):
    """Text-to-image: POST /images/generations"""
    config = load_config(args.config)
    base_url = get_base_url(args.base_url, config)
    api_key = get_api_key(args.api_key, config)

    if not api_key:
        print("ERROR: No API key found. Use --api-key, config.json, or GPT_IMAGE2_API_KEY env.", file=sys.stderr)
        sys.exit(1)

    body: dict = {"model": "gpt-image-2", "prompt": args.prompt, "n": args.n}
    if args.size:
        body["size"] = args.size
    if args.quality:
        body["quality"] = args.quality
    if args.format:
        body["format"] = args.format

    url = f"{base_url}/images/generations"
    output = args.output or os.path.expanduser("~/gpt-image2-output.png")
    _, resp_path = tempfile.mkstemp(suffix=".json")

    print(f"Calling: POST {url}")
    print(f"Prompt: {args.prompt[:100]}{'...' if len(args.prompt) > 100 else ''}")
    print(f"Quality: {args.quality or 'auto'}, Size: {args.size or 'auto'}, N: {args.n}")

    start = time.time()
    try:
        result = _curl_post_json(url, api_key, body, resp_path, args.timeout)
        elapsed = time.time() - start
        print(result.stdout.strip() if result.stdout else "")

        if result.returncode != 0:
            print(f"curl failed (exit {result.returncode})", file=sys.stderr)
            sys.exit(1)

        decode_and_save(resp_path, output)
    finally:
        if os.path.exists(resp_path):
            os.unlink(resp_path)

    print(f"Done in {elapsed:.1f}s")


def cmd_edit(args):
    """Image-to-image: POST /images/edits"""
    config = load_config(args.config)
    base_url = get_base_url(args.base_url, config)
    api_key = get_api_key(args.api_key, config)

    if not api_key:
        print("ERROR: No API key found. Use --api-key, config.json, or GPT_IMAGE2_API_KEY env.", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(args.image):
        print(f"ERROR: Image not found: {args.image}", file=sys.stderr)
        sys.exit(1)

    # Write prompt to temp file to avoid shell escaping issues
    prompt_fd, prompt_path = tempfile.mkstemp(suffix=".txt")
    with os.fdopen(prompt_fd, "w") as f:
        f.write(args.prompt)

    try:
        with open(prompt_path, "r") as f:
            prompt_text = f.read()
    finally:
        if os.path.exists(prompt_path):
            os.unlink(prompt_path)

    url = f"{base_url}/images/edits"
    output = args.output or os.path.expanduser("~/gpt-image2-edit-output.png")
    _, resp_path = tempfile.mkstemp(suffix=".json")

    print(f"Calling: POST {url}")
    print(f"Image: {args.image}")
    print(f"Prompt: {args.prompt[:100]}{'...' if len(args.prompt) > 100 else ''}")
    print(f"Quality: {args.quality or 'auto'}, Size: {args.size or 'auto'}")

    start = time.time()
    try:
        # Build multipart fields
        fields = [
            ("image", f"@{args.image}"),
            ("prompt", prompt_text),
            ("model", "gpt-image-2"),
            ("n", str(args.n)),
        ]
        if args.quality:
            fields.append(("quality", args.quality))
        if args.size:
            fields.append(("size", args.size))
        if args.mask:
            fields.append(("mask", f"@{args.mask}"))
        if args.moderation:
            fields.append(("moderation", args.moderation))

        result = _curl_post_multipart(url, api_key, fields, resp_path, args.timeout)
        elapsed = time.time() - start
        print(result.stdout.strip() if result.stdout else "")

        if result.returncode != 0:
            print(f"curl failed (exit {result.returncode})", file=sys.stderr)
            sys.exit(1)

        decode_and_save(resp_path, output)
    finally:
        if os.path.exists(resp_path):
            os.unlink(resp_path)

    print(f"Done in {elapsed:.1f}s")


def cmd_config(args):
    """Show or initialize config file"""
    found = _find_config_path(args.config)
    default = _default_config_path()

    if args.init:
        # Create a template config
        default.parent.mkdir(parents=True, exist_ok=True)
        template = {
            "base_url": "https://api.openai.com/v1",
            "api_key_env": "OPENAI_API_KEY",
        }
        if default.exists() and not args.force:
            print(f"Config already exists: {default}  (use --force to overwrite)")
            sys.exit(1)
        with open(default, "w") as f:
            json.dump(template, f, indent=2)
        os.chmod(default, 0o600)
        print(f"Created: {default}")
        print("Edit it to set your API key or base_url.")
    elif args.show:
        if found:
            print(f"Config file: {found}")
            with open(found) as f:
                data = json.load(f)
            # Mask api_key for safety
            if "api_key" in data:
                k = data["api_key"]
                data["api_key"] = k[:4] + "..." + k[-4:] if len(k) > 8 else "***"
            print(json.dumps(data, indent=2))
        else:
            print("No config file found. Run: gpt_image2.py config --init")
    else:
        print(f"Default config location: {default}")
        if found:
            print(f"Active config: {found}")
        else:
            print("No config file found. Run: gpt_image2.py config --init")


# ── CLI ───────────────────────────────────────────────────────────

def add_common_args(p):
    """Add shared arguments to a subparser."""
    p.add_argument("--config", help="Explicit path to config.json")
    p.add_argument("--base-url", help="API base URL (default: https://api.openai.com/v1)")
    p.add_argument("--api-key", help="API key (WARNING: visible in shell history; prefer config/env)")
    p.add_argument("--output", "-o", help="Output file path")
    p.add_argument("--quality", choices=["low", "medium", "high", "auto"], help="Image quality")
    p.add_argument("--size", help="Image size (e.g. 1024x1024, 1536x1024, auto)")
    p.add_argument("--n", type=int, default=1, help="Number of images (1-10)")
    p.add_argument("--timeout", type=int, default=600, help="curl timeout in seconds (default: 600)")


def main():
    parser = argparse.ArgumentParser(
        description="gpt-image-2 image generation and editing CLI (agent-agnostic)"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # generate
    gen = subparsers.add_parser("generate", help="Text-to-image generation")
    gen.add_argument("prompt", help="Image description (max 1000 chars)")
    gen.add_argument("--format", choices=["png", "jpeg", "webp"], help="Output format")
    add_common_args(gen)

    # edit
    edt = subparsers.add_parser("edit", help="Image-to-image editing")
    edt.add_argument("image", help="Input image path")
    edt.add_argument("prompt", help="Edit instruction (max 32000 chars)")
    edt.add_argument("--mask", help="PNG mask image (transparent=edit area)")
    edt.add_argument("--moderation", choices=["low", "auto"], help="Moderation level")
    add_common_args(edt)

    # config
    cfg = subparsers.add_parser("config", help="Show or initialize config")
    cfg.add_argument("--init", action="store_true", help="Create template config")
    cfg.add_argument("--show", action="store_true", help="Show active config (masks keys)")
    cfg.add_argument("--force", action="store_true", help="Overwrite existing config with --init")
    cfg.add_argument("--config", help="Explicit config path (for --show)")

    args = parser.parse_args()

    if args.command == "generate":
        cmd_generate(args)
    elif args.command == "edit":
        cmd_edit(args)
    elif args.command == "config":
        cmd_config(args)


if __name__ == "__main__":
    main()
