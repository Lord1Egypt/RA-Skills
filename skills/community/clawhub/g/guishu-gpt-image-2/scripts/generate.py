#!/usr/bin/env python3
import argparse
import base64
import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path


DEFAULT_ENDPOINT = "https://api.llm-token.cn/v1/images/generations"
DEFAULT_MODEL = "gpt-image-2"
KEY_ENV_NAMES = ("LLM_TOKEN_API_KEY", "GUI_SHU_TOKEN_KEY", "OPENAI_API_KEY")


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return re.sub(r"-{2,}", "-", text).strip("-") or "image"


def default_out_dir() -> Path:
    now = dt.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    preferred = Path.home() / "Projects" / "tmp"
    base = preferred if preferred.is_dir() else Path("./tmp")
    base.mkdir(parents=True, exist_ok=True)
    return base / f"gpt-image-2-{now}"


def read_prompts(args: argparse.Namespace) -> list[str]:
    prompts: list[str] = []
    if args.prompt:
        prompts.append(args.prompt)
    if args.prompt_file:
        prompt_path = Path(args.prompt_file).expanduser()
        prompts.extend(
            line.strip()
            for line in prompt_path.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        )
    if not prompts:
        prompts.append("a small blue square icon on a white background, clean vector style")
    return prompts


def resolve_api_key(args: argparse.Namespace) -> str:
    if args.api_key:
        return args.api_key.strip()
    for name in KEY_ENV_NAMES:
        value = os.environ.get(name)
        if value:
            return value.strip()
    return ""


def build_request(args: argparse.Namespace, prompt: str) -> dict:
    body = {
        "model": args.model,
        "prompt": prompt,
        "size": args.size,
        "n": args.n,
        "response_format": args.response_format,
    }
    if args.quality:
        body["quality"] = args.quality
    if args.background:
        body["background"] = args.background
    if args.output_format:
        body["output_format"] = args.output_format
    return body


def post_json(endpoint: str, api_key: str, body: dict, timeout: int) -> dict:
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        endpoint,
        method="POST",
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        payload = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Image generation failed ({exc.code}): {payload}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Image generation request failed: {exc}") from exc


def extension_for(args: argparse.Namespace, response_item: dict) -> str:
    if args.output_format:
        return args.output_format.lower().lstrip(".")
    mime = response_item.get("mime_type") or response_item.get("content_type") or ""
    if "jpeg" in mime or "jpg" in mime:
        return "jpg"
    if "webp" in mime:
        return "webp"
    return "png"


def save_image(response_item: dict, out_path: Path) -> None:
    b64 = response_item.get("b64_json")
    url = response_item.get("url")
    if b64:
        out_path.write_bytes(base64.b64decode(b64))
        return
    if url:
        urllib.request.urlretrieve(url, out_path)
        return
    raise RuntimeError(f"Unexpected image item: {json.dumps(response_item, ensure_ascii=False)[:500]}")


def write_gallery(out_dir: Path, items: list[dict]) -> None:
    figures = "\n".join(
        f'<figure><a href="{item["file"]}"><img src="{item["file"]}" loading="lazy"></a><figcaption>{item["prompt"]}</figcaption></figure>'
        for item in items
    )
    html = f"""<!doctype html>
<meta charset="utf-8">
<title>guishu-gpt-image-2 gallery</title>
<style>
  body {{ margin: 24px; font: 14px/1.45 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #f6f8fb; color: #172033; }}
  h1 {{ font-size: 22px; margin: 0 0 8px; }}
  p {{ color: #5b6472; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 16px; }}
  figure {{ margin: 0; padding: 12px; border: 1px solid #dde4ef; border-radius: 12px; background: white; box-shadow: 0 8px 24px rgba(20, 31, 48, .08); }}
  img {{ display: block; width: 100%; height: auto; border-radius: 8px; }}
  figcaption {{ margin-top: 10px; color: #475569; }}
  code {{ background: #edf2f7; padding: 2px 5px; border-radius: 5px; }}
</style>
<h1>guishu-gpt-image-2 gallery</h1>
<p>Output: <code>{out_dir.as_posix()}</code></p>
<div class="grid">{figures}</div>
"""
    (out_dir / "index.html").write_text(html, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate images with Guishu Token gpt-image-2.")
    parser.add_argument("--prompt", default="", help="Prompt for one generation.")
    parser.add_argument("--prompt-file", default="", help="Text file with one prompt per line.")
    parser.add_argument("--endpoint", default=DEFAULT_ENDPOINT, help="Full images generation endpoint.")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Image model ID.")
    parser.add_argument("--api-key", default="", help="API key. Prefer env vars instead.")
    parser.add_argument("--size", default="1024x1024", help="Image size, e.g. 1024x1024 or 1024x1792.")
    parser.add_argument("--quality", default="high", help="Quality, e.g. auto, high, medium, low.")
    parser.add_argument("--n", type=int, default=1, help="Images per prompt.")
    parser.add_argument("--response-format", default="b64_json", choices=["b64_json", "url"], help="API response format.")
    parser.add_argument("--background", default="", help="Optional background parameter.")
    parser.add_argument("--output-format", default="", help="Optional output format: png, jpeg, webp.")
    parser.add_argument("--timeout", type=int, default=240, help="HTTP timeout seconds.")
    parser.add_argument("--out-dir", default="", help="Output directory.")
    parser.add_argument("--dry-run", action="store_true", help="Print request body without sending it.")
    args = parser.parse_args()

    prompts = read_prompts(args)
    out_dir = Path(args.out_dir).expanduser() if args.out_dir else default_out_dir()
    out_dir.mkdir(parents=True, exist_ok=True)

    sample_request = build_request(args, prompts[0])
    if args.dry_run:
        print(json.dumps({"endpoint": args.endpoint, "request": sample_request, "prompt_count": len(prompts)}, ensure_ascii=False, indent=2))
        return 0

    api_key = resolve_api_key(args)
    if not api_key:
        print(
            "Missing API key. Set LLM_TOKEN_API_KEY, GUI_SHU_TOKEN_KEY, or OPENAI_API_KEY.",
            file=sys.stderr,
        )
        return 2

    all_items: list[dict] = []
    request_log: list[dict] = []
    for prompt_index, prompt in enumerate(prompts, start=1):
        body = build_request(args, prompt)
        print(f"[{prompt_index}/{len(prompts)}] {prompt}")
        response = post_json(args.endpoint, api_key, body, args.timeout)
        data = response.get("data") or []
        if not data:
            raise RuntimeError(f"Response has no data: {json.dumps(response, ensure_ascii=False)[:500]}")
        for image_index, item in enumerate(data, start=1):
            ext = extension_for(args, item)
            filename = f"{prompt_index:03d}-{image_index:02d}-{slugify(prompt)[:42]}.{ext}"
            save_image(item, out_dir / filename)
            all_items.append({"prompt": prompt, "file": filename})
        request_log.append({"request": body, "images": len(data)})

    (out_dir / "prompts.json").write_text(json.dumps(all_items, ensure_ascii=False, indent=2), encoding="utf-8")
    (out_dir / "request.json").write_text(json.dumps(request_log, ensure_ascii=False, indent=2), encoding="utf-8")
    write_gallery(out_dir, all_items)
    print(f"Wrote: {(out_dir / 'index.html').as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
