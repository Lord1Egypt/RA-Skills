#!/usr/bin/env python3
"""
analyze.py — analyze an image with GPT-4o and store it as a memory

Usage:
  python analyze.py --image-path /path/to/image.jpg [--source image|chart|website] [--url URL] [--extra-tags tag1,tag2]

Output:
  Prints analysis result and confirms memory was saved.
"""

import argparse
import base64
import json
import os
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent


def load_openclaw_config() -> dict:
    """Read ~/.openclaw/openclaw.json and return the full config dict."""
    config_path = Path.home() / ".openclaw" / "openclaw.json"
    if config_path.exists():
        import json as _json
        return _json.loads(config_path.read_text())
    return {}


def resolve_api_config() -> tuple[str, str, str]:
    """
    Returns (api_key, base_url, model) to use for vision requests.

    Priority:
    1. openclaw.json imageModel -> find matching provider
    2. openclaw.json first provider that has an apiKey
    3. OPENAI_API_KEY env var -> standard OpenAI endpoint
    4. ~/.openclaw/.env OPENAI_API_KEY
    """
    cfg = load_openclaw_config()

    providers = cfg.get("models", {}).get("providers", {})
    image_model_primary = (
        cfg.get("agents", {}).get("defaults", {}).get("imageModel", {}).get("primary", "")
    )

    # Parse "provider/model" format, e.g. "openai/gpt-4o"
    if "/" in image_model_primary:
        provider_name, model_name = image_model_primary.split("/", 1)
    else:
        provider_name, model_name = "", image_model_primary or "gpt-4o"

    # Try the named provider first
    if provider_name and provider_name in providers:
        p = providers[provider_name]
        key = p.get("apiKey", "")
        base_url = p.get("baseUrl", "https://api.openai.com/v1")
        if key:
            return key, base_url, model_name

    # Try any provider that has an apiKey
    for p in providers.values():
        key = p.get("apiKey", "")
        base_url = p.get("baseUrl", "https://api.openai.com/v1")
        if key:
            return key, base_url, model_name

    # Fall back to environment / .env file
    key = os.environ.get("OPENAI_API_KEY", "")
    if not key:
        env_file = Path.home() / ".openclaw" / ".env"
        if env_file.exists():
            for line in env_file.read_text().splitlines():
                line = line.strip()
                if line.startswith("OPENAI_API_KEY="):
                    key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break
    return key, "https://api.openai.com/v1", model_name


def analyze_with_gpt4o(image_path: str, source: str, api_key: str,
                        base_url: str = "https://api.openai.com/v1",
                        model: str = "gpt-4o") -> dict:
    import urllib.request
    import urllib.error

    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")

    ext = Path(image_path).suffix.lower().lstrip(".")
    mime_map = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png", "gif": "image/gif", "webp": "image/webp"}
    mime = mime_map.get(ext, "image/jpeg")

    source_hints = {
        "chart": "Focus on: chart type, title, axis labels, data values, trends, key insights.",
        "website": "Focus on: page purpose, layout structure, navigation, key UI sections, color scheme, visible text.",
        "image": "Describe all visible content in detail.",
    }
    hint = source_hints.get(source, source_hints["image"])

    prompt = (
        f"Analyze this image. {hint}\n"
        'Respond in JSON with exactly three fields:\n'
        '  "description": detailed natural-language description (in the same language as any text in the image, default Chinese if ambiguous),\n'
        '  "tags": list of 3-8 relevant keyword strings,\n'
        '  "raw_text": all visible text verbatim (empty string if none).\n'
        "Return only the JSON object, no markdown."
    )

    payload = json.dumps({
        "model": model,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{image_data}"}},
                {"type": "text", "text": prompt},
            ],
        }],
        "max_tokens": 1024,
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{base_url.rstrip('/')}/chat/completions",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"OpenAI API error {e.code}: {e.read().decode()}") from e

    content = body["choices"][0]["message"]["content"].strip()
    # Strip markdown fences if present
    if content.startswith("```"):
        content = content.split("\n", 1)[1].rsplit("```", 1)[0].strip()

    try:
        result = json.loads(content)
    except json.JSONDecodeError:
        result = {"description": content, "tags": [], "raw_text": ""}

    result.setdefault("description", "")
    result.setdefault("tags", [])
    result.setdefault("raw_text", "")
    if isinstance(result["tags"], str):
        result["tags"] = [t.strip() for t in result["tags"].split(",") if t.strip()]

    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image-path", required=True)
    parser.add_argument("--source", default="image", choices=["image", "chart", "website"])
    parser.add_argument("--url", default="")
    parser.add_argument("--extra-tags", default="")
    args = parser.parse_args()

    if not os.path.isfile(args.image_path):
        print(f"ERROR: File not found: {args.image_path}", file=sys.stderr)
        sys.exit(1)

    api_key, base_url, model = resolve_api_config()
    if not api_key:
        print("ERROR: No API key found. Add OPENAI_API_KEY to ~/.openclaw/.env or configure a provider in openclaw.json.", file=sys.stderr)
        sys.exit(1)

    print(f"Analyzing {args.image_path} with {model} via {base_url} ...")
    result = analyze_with_gpt4o(args.image_path, args.source, api_key, base_url, model)

    extra_tags = [t.strip() for t in args.extra_tags.split(",") if t.strip()]
    all_tags = list(dict.fromkeys(result["tags"] + extra_tags))

    # Call store.py
    store_cmd = [
        sys.executable, str(SCRIPT_DIR / "store.py"),
        "--image-path", args.image_path,
        "--description", result["description"],
        "--tags", ",".join(all_tags),
        "--source", args.source,
    ]
    if args.url:
        store_cmd += ["--url", args.url]

    subprocess.run(store_cmd, check=True)

    if result["raw_text"]:
        print(f"  Detected text: {result['raw_text'][:300]}")


if __name__ == "__main__":
    main()
