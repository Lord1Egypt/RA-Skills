#!/usr/bin/env python3
import argparse
import base64
import json
import mimetypes
import os
import re
import sys
import uuid
from datetime import datetime
from pathlib import Path
from urllib import error, request

STYLE_PRESETS = {
    "anime": "anime style, clean lineart, high detail, expressive eyes, soft lighting",
    "cute": "cute aesthetic, soft colors, charming expression, polished illustration",
    "photoreal": "photorealistic, realistic lighting, natural textures, high fidelity",
    "cyberpunk": "cyberpunk atmosphere, neon lights, futuristic details, cinematic mood",
}

SIZE_PRESETS = {
    "square": "1024x1024",
    "portrait": "1024x1536",
    "landscape": "1536x1024",
}


def fail(message: str, code: int = 1):
    print(message, file=sys.stderr)
    raise SystemExit(code)


def env_any(names: list[str], required: bool = True) -> str:
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    if required:
        fail(f"Missing environment variable: one of {', '.join(names)}")
    return ""


def normalize_base_url(url: str) -> str:
    return url.rstrip("/")


def auth_headers(api_key: str) -> dict:
    return {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
        "User-Agent": "grok-image-api-skill/1.1.1",
    }


def slugify(text: str, limit: int = 48) -> str:
    text = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff]+", "-", text).strip("-")
    return (text[:limit] or "image").strip("-")


def default_output_path(prefix: str, size: str | None = None) -> Path:
    root = Path.cwd() / "output" / "grok-images"
    stamp = datetime.now().strftime("%Y-%m-%d/%H%M%S")
    root = root / stamp
    root.mkdir(parents=True, exist_ok=True)
    name = slugify(prefix)
    suffix = f"-{size}" if size else ""
    return root / f"{name}{suffix}.png"


def friendly_http_error(e: error.HTTPError) -> str:
    body = e.read().decode("utf-8", errors="replace")
    tips = []
    if e.code in (401, 403):
        tips.append("Check whether the API key is valid and active.")
    elif e.code == 404:
        tips.append("Check the base URL and ensure the endpoint path is correct.")
    elif e.code == 413:
        tips.append("The uploaded image may be too large; try compressing it first.")
    elif e.code >= 500:
        tips.append("The service may be temporarily unavailable; retry later.")
    detail = f"HTTP {e.code}: {body}"
    if tips:
        detail += "\n" + " ".join(tips)
    return detail


def http_json(url: str, payload: dict, headers: dict) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(url, data=data, method="POST")
    for k, v in headers.items():
        req.add_header(k, v)
    req.add_header("Content-Type", "application/json")
    try:
        with request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as e:
        fail(friendly_http_error(e))


def encode_multipart(fields, files):
    boundary = f"----OpenClaw{uuid.uuid4().hex}"
    body = bytearray()
    for name, value in fields.items():
        body.extend(f"--{boundary}\r\n".encode())
        body.extend(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode())
        body.extend(str(value).encode())
        body.extend(b"\r\n")
    for name, path in files.items():
        if not path:
            continue
        p = Path(path)
        if not p.is_file():
            fail(f"Input file not found: {p}")
        ctype = mimetypes.guess_type(p.name)[0] or "application/octet-stream"
        body.extend(f"--{boundary}\r\n".encode())
        body.extend(f'Content-Disposition: form-data; name="{name}"; filename="{p.name}"\r\n'.encode())
        body.extend(f"Content-Type: {ctype}\r\n\r\n".encode())
        body.extend(p.read_bytes())
        body.extend(b"\r\n")
    body.extend(f"--{boundary}--\r\n".encode())
    return boundary, bytes(body)


def http_multipart(url: str, fields: dict, files: dict, headers: dict) -> dict:
    boundary, data = encode_multipart(fields, files)
    req = request.Request(url, data=data, method="POST")
    for k, v in headers.items():
        req.add_header(k, v)
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    try:
        with request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as e:
        fail(friendly_http_error(e))


def first_data_item(payload: dict) -> dict:
    data = payload.get("data") or []
    if not data:
        fail(f"No image data in response: {json.dumps(payload, ensure_ascii=False)[:1000]}")
    return data[0]


def download_to(url: str, out_path: Path) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    req = request.Request(url, headers={"User-Agent": "grok-image-api-skill/1.1.1"})
    with request.urlopen(req) as resp:
        data = resp.read()
        content_type = resp.headers.get("Content-Type", "")
    if out_path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
        if "jpeg" in content_type or url.lower().endswith((".jpg", ".jpeg")):
            out_path = out_path.with_suffix(".jpg")
        elif "webp" in content_type or url.lower().endswith(".webp"):
            out_path = out_path.with_suffix(".webp")
        else:
            out_path = out_path.with_suffix(".png")
    out_path.write_bytes(data)
    return out_path


def save_result(item: dict, out_path: str | None, prefix: str, size: str | None, download_url: bool = True):
    path = Path(out_path) if out_path else default_output_path(prefix, size)
    if item.get("b64_json"):
        raw = base64.b64decode(item["b64_json"])
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
            path = path.with_suffix(".png")
        path.write_bytes(raw)
        print(str(path))
        return
    if item.get("url"):
        if download_url:
            final_path = download_to(item["url"], path)
            print(str(final_path))
        else:
            print(item["url"])
        return
    print(json.dumps(item, ensure_ascii=False, indent=2))


def resolve_size(args):
    if getattr(args, "preset_size", None):
        return SIZE_PRESETS[args.preset_size]
    return getattr(args, "size", None) or "1024x1024"


def apply_style(prompt: str, style: str | None):
    if not style:
        return prompt
    return f"{prompt}, {STYLE_PRESETS[style]}"


def load_base_and_key():
    base = normalize_base_url(env_any(["IMAGE_API_BASE_URL", "GROK_IMAGE_BASE_URL"]))
    api_key = env_any(["IMAGE_API_KEY", "GROK_IMAGE_API_KEY"])
    return base, api_key


def cmd_probe(args):
    base, api_key = load_base_and_key()
    req = request.Request(base + "/images/generations", method="OPTIONS")
    for k, v in auth_headers(api_key).items():
        req.add_header(k, v)
    try:
        with request.urlopen(req) as resp:
            print(f"Probe OK: HTTP {resp.status}")
    except Exception as e:
        print(f"Probe finished with: {e}")


def cmd_generate(args):
    base, api_key = load_base_and_key()
    size = resolve_size(args)
    prompt = apply_style(args.prompt, args.style)
    payload = {"prompt": prompt, "n": args.n, "size": size}
    if args.model:
        payload["model"] = args.model
    for extra in args.extra:
        key, value = extra.split("=", 1)
        payload[key] = value
    result = http_json(base + "/images/generations", payload, auth_headers(api_key))
    save_result(first_data_item(result), args.out, args.prompt, size, download_url=not args.keep_url)


def cmd_edit(args):
    base, api_key = load_base_and_key()
    size = resolve_size(args) if (getattr(args, "preset_size", None) or args.size) else None
    prompt = apply_style(args.prompt, args.style)
    fields = {"prompt": prompt}
    if args.model:
        fields["model"] = args.model
    if size:
        fields["size"] = size
    if args.n:
        fields["n"] = args.n
    for extra in args.extra:
        key, value = extra.split("=", 1)
        fields[key] = value
    files = {"image": args.image, "mask": args.mask}
    result = http_multipart(base + "/images/edits", fields, files, auth_headers(api_key))
    save_result(first_data_item(result), args.out, args.prompt, size, download_url=not args.keep_url)


def add_common_image_args(parser, include_image=False):
    if include_image:
        parser.add_argument("--image", required=True)
        parser.add_argument("--mask")
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--model")
    parser.add_argument("--size")
    parser.add_argument("--preset-size", choices=sorted(SIZE_PRESETS.keys()))
    parser.add_argument("--style", choices=sorted(STYLE_PRESETS.keys()))
    parser.add_argument("--n", type=int, default=1)
    parser.add_argument("--out")
    parser.add_argument("--keep-url", action="store_true")
    parser.add_argument("--extra", action="append", default=[])


def build_parser():
    p = argparse.ArgumentParser(description="Call OpenAI-compatible image generation/edit APIs")
    sub = p.add_subparsers(dest="cmd", required=True)

    probe = sub.add_parser("probe")
    probe.set_defaults(func=cmd_probe)

    gen = sub.add_parser("generate")
    add_common_image_args(gen)
    gen.set_defaults(func=cmd_generate)

    edit = sub.add_parser("edit")
    add_common_image_args(edit, include_image=True)
    edit.set_defaults(func=cmd_edit)
    return p


if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)
