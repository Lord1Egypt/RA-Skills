#!/usr/bin/env python3
import argparse
import subprocess
from pathlib import Path

from get_zai_api_key import get_key


def run(cmd: list[str]) -> None:
    result = subprocess.run(cmd, text=True, capture_output=True)
    if result.returncode != 0:
        raise RuntimeError((result.stderr or result.stdout).strip())


def add_http_server(config_path: str, name: str, url: str, api_key: str) -> None:
    run([
        "mcporter",
        "--config",
        config_path,
        "config",
        "add",
        name,
        "--url",
        url,
        "--transport",
        "http",
        "--header",
        f"Authorization=Bearer {api_key}",
    ])


def add_vision_stdio(config_path: str, api_key: str) -> None:
    run([
        "mcporter",
        "--config",
        config_path,
        "config",
        "add",
        "zai-vision",
        "--command",
        "npx",
        "--arg",
        "-y",
        "--arg",
        "@z_ai/mcp-server",
        "--env",
        f"Z_AI_API_KEY={api_key}",
        "--env",
        "Z_AI_MODE=ZAI",
    ])


def main() -> int:
    parser = argparse.ArgumentParser(description="Configure 4 official GLM MCP servers in a mcporter config")
    parser.add_argument("--config", default="./tmp/mcporter-glm.json", help="mcporter config path")
    parser.add_argument("--api-key", default=None, help="Z.AI API key (default: read from env vars)")
    parser.add_argument("--keep", action="store_true", help="keep existing config file")
    args = parser.parse_args()

    config_path = str(Path(args.config).expanduser().resolve())
    cfg = Path(config_path)
    cfg.parent.mkdir(parents=True, exist_ok=True)
    if cfg.exists() and not args.keep:
        cfg.unlink()

    api_key = (args.api_key or get_key() or "").strip()
    if not api_key:
        raise SystemExit("No API key found. Set Z_AI_API_KEY (or ZAI_API_KEY/GLM_API_KEY/ZHIPU_API_KEY), or run with --api-key.")

    add_http_server(config_path, "web-search-prime", "https://api.z.ai/api/mcp/web_search_prime/mcp", api_key)
    add_http_server(config_path, "web-reader", "https://api.z.ai/api/mcp/web_reader/mcp", api_key)
    add_http_server(config_path, "zread", "https://api.z.ai/api/mcp/zread/mcp", api_key)
    add_vision_stdio(config_path, api_key)

    print(config_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
