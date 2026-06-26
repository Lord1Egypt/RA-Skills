#!/usr/bin/env python3
"""MoPNG API client for OpenClaw - Image processing via mopng.cn"""

import argparse
import ipaddress
import json
import mimetypes
import os
import struct
import sys
import time
import uuid
from pathlib import Path
from urllib import error, request, parse

BASE_URL = "https://mo-api.mopng.cn"
UPSCALE_URL = "https://mo-api.mopng.cn"
ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
MAX_BYTES = 25 * 1024 * 1024
MAX_DIMENSION = 12000
MAX_PROMPT_CHARS = 8000

# Remote image URL passed as --input: only https, host must be under MoPNG or MOPNG_EXTRA_ALLOWED_IMAGE_HOSTS.
_USER_URL_SUFFIX = "mopng.cn"
_FORBIDDEN_RESULT_HOSTS = frozenset(
    {
        "localhost",
        "127.0.0.1",
        "0.0.0.0",  # nosec B104 — blocklisted hostname for SSRF checks, not socket bind
        "::1",
        "169.254.169.254",
        "metadata.google.internal",
    }
)


def _workspace_root() -> Path:
    env_root = os.getenv("OPENCLAW_WORKSPACE")
    return Path(env_root).resolve() if env_root else Path.cwd().resolve()


def _ensure_within(path: Path, root: Path, label: str) -> None:
    try:
        path.relative_to(root)
    except ValueError:
        raise ValueError(f"{label} must be inside workspace: {root}")


def _is_remote_image_ref(s: str) -> bool:
    t = s.strip().lower()
    return t.startswith("https://") or t.startswith("http://")


def _extra_allowed_user_image_hosts() -> frozenset[str]:
    raw = os.environ.get("MOPNG_EXTRA_ALLOWED_IMAGE_HOSTS", "")
    return frozenset(h.strip().lower() for h in raw.split(",") if h.strip())


def _host_matches_user_allowlist(host: str) -> bool:
    h = host.lower().rstrip(".")
    if not h:
        return False
    if h == _USER_URL_SUFFIX or h.endswith("." + _USER_URL_SUFFIX):
        return True
    for entry in _extra_allowed_user_image_hosts():
        e = entry.rstrip(".").lower()
        if not e:
            continue
        if e.startswith("."):
            suf = e[1:]
            if h == suf or h.endswith("." + suf):
                return True
        elif h == e or h.endswith("." + e):
            return True
    return False


def _validate_user_image_url(url: str) -> None:
    """Restrict user-supplied image URLs (SSRF mitigation for URLs forwarded to MoPNG)."""
    u = url.strip()
    p = parse.urlparse(u)
    if p.scheme.lower() != "https":
        raise ValueError("Remote image input must use https:// (http is not allowed).")
    if not p.hostname:
        raise ValueError("Remote image URL must include a valid hostname.")
    if p.username is not None or p.password is not None:
        raise ValueError("URLs with embedded credentials are not allowed.")
    host = p.hostname
    if not _host_matches_user_allowlist(host):
        raise ValueError(
            "Remote image URL host is not allowed. "
            f"Use a hostname under {_USER_URL_SUFFIX}, or set MOPNG_EXTRA_ALLOWED_IMAGE_HOSTS "
            "(comma-separated hosts or suffixes such as .cdn.example.com)."
        )


def _host_is_ssrf_risk(host: str) -> bool:
    hn = host.lower().strip(".")
    if not hn:
        return True
    if hn in _FORBIDDEN_RESULT_HOSTS:
        return True
    if hn.endswith(".local") or hn.endswith(".localhost"):
        return True
    for candidate in (hn, hn.strip("[]")):
        try:
            ip = ipaddress.ip_address(candidate)
            return bool(
                ip.is_private
                or ip.is_loopback
                or ip.is_multicast
                or ip.is_reserved
                or ip.is_link_local
            )
        except ValueError:
            continue
    return False


def _validate_result_download_url(url: str) -> None:
    """Validate URLs returned by MoPNG before downloading (HTTPS + no obvious SSRF targets)."""
    u = url.strip()
    p = parse.urlparse(u)
    if p.scheme.lower() != "https":
        raise ValueError("Download URL must use https.")
    if not p.hostname:
        raise ValueError("Download URL must include a hostname.")
    if p.username is not None or p.password is not None:
        raise ValueError("Download URL with credentials is not allowed.")
    if _host_is_ssrf_risk(p.hostname):
        raise ValueError("Download URL host is not allowed.")


def _validate_prompt_field(text: str, name: str) -> str:
    s = text.strip()
    if not s:
        raise ValueError(f"{name} cannot be empty.")
    if len(s) > MAX_PROMPT_CHARS:
        raise ValueError(f"{name} must be at most {MAX_PROMPT_CHARS} characters.")
    return s


def _validate_optional_prompt_field(text: str | None, name: str) -> str | None:
    if text is None or not str(text).strip():
        return None
    return _validate_prompt_field(str(text), name)


def _resolve_input_image_url(args, in_path: Path, api_key: str) -> str:
    if _is_remote_image_ref(str(args.input)):
        return str(args.input).strip()
    return _upload_image(in_path, api_key)


def _detect_image_format(data: bytes) -> str | None:
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if data.startswith(b"\xff\xd8\xff"):
        return "jpeg"
    if len(data) >= 12 and data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "webp"
    return None


def _jpeg_dimensions(data: bytes) -> tuple[int, int]:
    i = 2
    while i + 9 < len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        i += 2

        if marker in {0xD8, 0xD9, 0x01} or 0xD0 <= marker <= 0xD7:
            continue

        if i + 2 > len(data):
            break
        seg_len = struct.unpack(">H", data[i : i + 2])[0]
        if seg_len < 2 or i + seg_len > len(data):
            break

        if marker in {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}:
            if i + 7 > len(data):
                break
            height = struct.unpack(">H", data[i + 3 : i + 5])[0]
            width = struct.unpack(">H", data[i + 5 : i + 7])[0]
            return width, height

        i += seg_len

    raise ValueError("Could not parse JPEG dimensions")


def _image_dimensions(fmt: str, data: bytes) -> tuple[int, int]:
    if fmt == "png":
        if len(data) < 24:
            raise ValueError("Invalid PNG")
        width = struct.unpack(">I", data[16:20])[0]
        height = struct.unpack(">I", data[20:24])[0]
        return width, height

    if fmt == "jpeg":
        return _jpeg_dimensions(data)

    if fmt == "webp":
        if len(data) < 30:
            raise ValueError("Invalid WEBP")
        chunk = data[12:16]
        if chunk == b"VP8X":
            width = 1 + int.from_bytes(data[24:27], "little")
            height = 1 + int.from_bytes(data[27:30], "little")
            return width, height
        if chunk == b"VP8 ":
            start = data.find(b"\x9d\x01\x2a", 20)
            if start == -1 or start + 7 > len(data):
                raise ValueError("Invalid WEBP VP8")
            width = struct.unpack("<H", data[start + 3 : start + 5])[0] & 0x3FFF
            height = struct.unpack("<H", data[start + 5 : start + 7])[0] & 0x3FFF
            return width, height
        if chunk == b"VP8L":
            if len(data) < 25 or data[20] != 0x2F:
                raise ValueError("Invalid WEBP VP8L")
            b0, b1, b2, b3 = data[21], data[22], data[23], data[24]
            width = 1 + (((b1 & 0x3F) << 8) | b0)
            height = 1 + (((b3 & 0x0F) << 10) | (b2 << 2) | ((b1 & 0xC0) >> 6))
            return width, height
        raise ValueError("Unsupported WEBP chunk")

    raise ValueError(f"Unsupported format: {fmt}")


def _validate_input_image(path: Path) -> bytes:
    if path.suffix.lower() not in ALLOWED_EXTENSIONS:
        allowed = ", ".join(sorted(ALLOWED_EXTENSIONS))
        raise ValueError(f"Input extension not allowed. Allowed: {allowed}")

    size = path.stat().st_size
    if size > MAX_BYTES:
        raise ValueError("Input too large (>25MB)")

    data = path.read_bytes()
    fmt = _detect_image_format(data)
    if fmt is None:
        raise ValueError("Input is not a supported image (png/jpg/jpeg/webp)")

    ext = path.suffix.lower()
    if ext in {".jpg", ".jpeg"} and fmt != "jpeg":
        raise ValueError("File extension/content mismatch")
    if ext == ".png" and fmt != "png":
        raise ValueError("File extension/content mismatch")
    if ext == ".webp" and fmt != "webp":
        raise ValueError("File extension/content mismatch")

    width, height = _image_dimensions(fmt, data)
    if width <= 0 or height <= 0:
        raise ValueError("Invalid image dimensions")
    if width > MAX_DIMENSION or height > MAX_DIMENSION:
        raise ValueError(f"Image dimensions too large (>{MAX_DIMENSION}px)")

    return data


def _api_request(method: str, endpoint: str, api_key: str, data: dict | None = None,
                 files: dict | None = None, timeout: int = 90, base_url: str = BASE_URL) -> dict:
    """Make API request with proper auth"""
    url = f"{base_url}{endpoint}"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    if files:
        # Multipart form data
        boundary = f"----OpenClaw{uuid.uuid4().hex}"
        body = bytearray()
        
        for k, v in (data or {}).items():
            body.extend(f"--{boundary}\r\n".encode())
            body.extend(f'Content-Disposition: form-data; name="{k}"\r\n\r\n'.encode())
            body.extend(str(v).encode())
            body.extend(b"\r\n")
        
        for field_name, (file_path, file_data) in files.items():
            mime = mimetypes.guess_type(str(file_path))[0] or "application/octet-stream"
            body.extend(f"--{boundary}\r\n".encode())
            body.extend(
                f'Content-Disposition: form-data; name="{field_name}"; filename="{file_path.name}"\r\n'.encode()
            )
            body.extend(f"Content-Type: {mime}\r\n\r\n".encode())
            body.extend(file_data)
            body.extend(b"\r\n")
        
        body.extend(f"--{boundary}--\r\n".encode())
        headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"
        req = request.Request(url, method=method, data=bytes(body), headers=headers)
    elif data:
        # JSON data
        body = json.dumps(data).encode()
        headers["Content-Type"] = "application/json"
        req = request.Request(url, method=method, data=body, headers=headers)
    else:
        req = request.Request(url, method=method, headers=headers)
    
    try:
        with request.urlopen(req, timeout=timeout) as resp:  # nosec B310 — URL is fixed API host + path
            return json.loads(resp.read().decode())
    except error.HTTPError as e:
        body = e.read().decode("utf-8", "ignore")
        try:
            parsed = json.loads(body)
            raise RuntimeError(f"API error: {parsed.get('message', body)}")
        except json.JSONDecodeError:
            raise RuntimeError(f"HTTP {e.code}: {body}")


def _upload_image(image_path: Path, api_key: str) -> str:
    """Upload local image and return signed URL"""
    data = image_path.read_bytes()
    files = {"file": (image_path, data)}
    resp = _api_request("POST", "/api/v1/images/upload", api_key, files=files)
    if resp.get("code") != 0:
        raise RuntimeError(f"Upload failed: {resp.get('message', 'unknown error')}")
    return resp["data"].get("signed_url") or resp["data"].get("signedUrl")


def _poll_task(endpoint: str, task_id: str, api_key: str, max_retries: int = 60, interval: int = 2, base_url: str = BASE_URL) -> dict:
    """Poll async task until complete or failed"""
    for i in range(max_retries):
        resp = _api_request("GET", f"{endpoint}/{task_id}", api_key, base_url=base_url)
        data = resp.get("data", {})
        status = data.get("status", "unknown")
        
        if status == "completed":
            return data
        elif status == "failed":
            raise RuntimeError(f"Task failed: {data.get('message', 'unknown error')}")
        
        time.sleep(interval)
    
    raise RuntimeError("Task polling timeout")


def _download_image(url: str, output_path: Path) -> None:
    """Download image from URL to local path"""
    _validate_result_download_url(url)
    req = request.Request(url, method="GET")
    with request.urlopen(req, timeout=60) as resp:  # nosec B310 — URL validated in _validate_result_download_url
        output_path.write_bytes(resp.read())


def cmd_remove_bg(args, api_key: str, workspace: Path, safe_output_root: Path) -> int:
    """Remove background from image"""
    in_path, out_path = _prepare_paths(args, workspace, safe_output_root)
    
    image_url = _resolve_input_image_url(args, in_path, api_key)
    
    data = {
        "image_url": image_url,
        "output_format": args.output_format,
        "return_mask": args.return_mask,
        "only_mask": args.only_mask,
        "async_mode": args.async_mode
    }
    
    resp = _api_request("POST", "/api/v1/open/image/remove-bg", api_key, data=data)
    if resp.get("code") != 0:
        print(f"Task failed: {resp.get('message', 'unknown')}", file=sys.stderr)
        return 1
    result = resp.get("data") or {}

    if args.async_mode and result.get("status") in ("pending", "processing"):
        task_id = result.get("task_id")
        print(f"Task {task_id} is {result.get('status')}, polling...")
        result = _poll_task("/api/v1/open/image/tasks", task_id, api_key)
    
    if result.get("status") != "completed":
        print(f"Task failed: {result.get('message', 'unknown')}", file=sys.stderr)
        return 1
    
    # Download result
    image_url = result.get("result", {}).get("imageUrl") or result.get("result", {}).get("image_url")
    if not image_url:
        print("No result image URL", file=sys.stderr)
        return 1
    
    _download_image(image_url, out_path)
    _print_result(out_path)
    return 0


def cmd_upscale(args, api_key: str, workspace: Path, safe_output_root: Path) -> int:
    """Upscale image"""
    in_path, out_path = _prepare_paths(args, workspace, safe_output_root)

    image_url = _resolve_input_image_url(args, in_path, api_key)

    # Use camelCase for this endpoint
    data = {
        "imageUrl": image_url,
        "scale": args.scale,
        "tileSize": args.tile_size,
        "tilePad": args.tile_pad,
        "outputFormat": args.output_format,
        "asyncMode": args.async_mode
    }

    resp = _api_request("POST", "/api/v1/ai/tools/upscale/photo", api_key, data=data, base_url=UPSCALE_URL)
    if resp.get("code") != 0:
        print(f"Task failed: {resp.get('message', 'unknown')}", file=sys.stderr)
        return 1
    result = resp.get("data") or {}

    if args.async_mode and result.get("status") in ("pending", "processing"):
        task_id = result.get("taskId") or result.get("task_id")
        print(f"Task {task_id} is {result.get('status')}, polling...")
        result = _poll_task("/api/v1/ai/tools/tasks", task_id, api_key, base_url=UPSCALE_URL)

    if result.get("status") != "completed":
        print(f"Task failed: {result.get('message', 'unknown')}", file=sys.stderr)
        return 1

    # Handle camelCase result.imageUrl
    image_url = result.get("result", {}).get("imageUrl") or result.get("result", {}).get("image_url")
    if not image_url:
        print("No result image URL", file=sys.stderr)
        return 1

    _download_image(image_url, out_path)
    _print_result(out_path)
    return 0


def cmd_outpainting(args, api_key: str, workspace: Path, safe_output_root: Path) -> int:
    """Outpainting - expand image"""
    in_path, out_path = _prepare_paths(args, workspace, safe_output_root)
    
    image_url = _resolve_input_image_url(args, in_path, api_key)
    
    data = {
        "provider": "aliyun",
        "model_id": "wanx-outpaint",
        "image_url": image_url,
        "direction": args.direction,
        "expand_ratio": args.expand_ratio,
        "angle": args.angle,
        "output_ratio": args.output_ratio,
        "best_quality": args.best_quality
    }
    
    resp = _api_request("POST", "/api/v1/open/image/outpainting", api_key, data=data)
    if resp.get("code") != 0:
        print(f"Task failed: {resp.get('message', 'unknown')}", file=sys.stderr)
        return 1
    result = resp.get("data") or {}

    # Sync: immediate URL
    out_image_url = result.get("image_url")
    if out_image_url:
        _download_image(out_image_url, out_path)
        _print_result(out_path)
        return 0

    # Async: same generations poll as translation / t2i (POST returns task_id + pending)
    job_id = result.get("job_id") or result.get("task_id") or result.get("jobId")
    if result.get("status") in ("pending", "processing") and not job_id:
        print("No task ID for async outpainting", file=sys.stderr)
        return 1

    if job_id:
        if result.get("status") == "failed":
            print(f"Task failed: {result.get('message', 'unknown')}", file=sys.stderr)
            return 1
        if result.get("status") != "completed":
            print(f"Job {job_id} submitted, polling...")
            result = _poll_task(
                "/api/v1/open/ai/generations", job_id, api_key, max_retries=120, interval=3
            )

    if result.get("status") == "failed":
        print(f"Task failed: {result.get('message', 'unknown')}", file=sys.stderr)
        return 1

    if result.get("status") not in ("completed", None):
        print(f"Task failed: {result.get('message', 'unknown')}", file=sys.stderr)
        return 1

    result_data = result.get("result", {}) or {}
    images = result_data.get("images", [])
    if not images:
        u = result_data.get("imageUrl") or result_data.get("image_url")
        if u:
            images = [{"url": u}]
    if not images:
        results = result.get("results", [])
        if results:
            images = [{"url": r.get("url")} for r in results if r.get("url")]

    if not images:
        print("No result image URL", file=sys.stderr)
        return 1

    _download_image(images[0]["url"], out_path)
    _print_result(out_path)
    return 0


def cmd_translation(args, api_key: str, workspace: Path, safe_output_root: Path) -> int:
    """Translate image text"""
    in_path, out_path = _prepare_paths(args, workspace, safe_output_root)
    
    image_url = _resolve_input_image_url(args, in_path, api_key)
    
    data = {
        "provider": "aliyun",
        "model_id": "qwen-mt-image",
        "image_url": image_url,
        "source_language": args.source_language,
        "target_language": args.target_language,
        "domain_hint": args.domain_hint,
        "sensitive_word_filter": args.sensitive_word_filter,
        "term_intervention": args.term_intervention
    }
    
    resp = _api_request("POST", "/api/v1/open/image/translation", api_key, data=data)
    if resp.get("code") != 0:
        print(f"Task failed: {resp.get('message', 'unknown')}", file=sys.stderr)
        return 1
    result = resp.get("data") or {}

    # Sync response: immediate image URL
    image_url = result.get("image_url")
    if image_url:
        _download_image(image_url, out_path)
        _print_result(out_path)
        return 0

    # Async: poll unified generations task endpoint (not /api/v1/open/image/translation/{task_id})
    job_id = result.get("job_id") or result.get("task_id") or result.get("jobId")
    if result.get("status") in ("pending", "processing") and not job_id:
        print("No job ID for async translation task", file=sys.stderr)
        return 1

    if job_id:
        if result.get("status") == "failed":
            print(f"Task failed: {result.get('message', 'unknown')}", file=sys.stderr)
            return 1
        if result.get("status") != "completed":
            print(f"Job {job_id} submitted, polling...")
            result = _poll_task(
                "/api/v1/open/ai/generations", job_id, api_key, max_retries=120, interval=3
            )

    if result.get("status") == "failed":
        print(f"Task failed: {result.get('message', 'unknown')}", file=sys.stderr)
        return 1

    if result.get("status") not in ("completed", None):
        print(f"Task failed: {result.get('message', 'unknown')}", file=sys.stderr)
        return 1

    result_data = result.get("result", {})
    images = result_data.get("images", [])
    if not images:
        u = result_data.get("imageUrl") or result_data.get("image_url")
        if u:
            images = [{"url": u}]
    if not images:
        results = result.get("results", [])
        if results:
            images = [{"url": r.get("url")} for r in results if r.get("url")]

    if not images:
        print("No result image URL", file=sys.stderr)
        return 1

    _download_image(images[0]["url"], out_path)
    _print_result(out_path)
    return 0


def cmd_text_to_image(args, api_key: str, workspace: Path, safe_output_root: Path) -> int:
    """Generate image from text"""
    out_path = _prepare_output_path(args.output, workspace, safe_output_root)
    prompt = _validate_prompt_field(args.prompt, "prompt")
    neg = _validate_optional_prompt_field(getattr(args, "negative_prompt", None), "negative prompt")
    
    data = {
        "type": "text_to_image",
        "model": args.model,
        "prompt": prompt,
        "sensitive_word_filter": not getattr(args, "no_sensitive_word_filter", False),
    }
    
    if neg:
        data["negative_prompt"] = neg
    if args.width:
        data["width"] = args.width
    if args.height:
        data["height"] = args.height
    if args.n:
        data["n"] = args.n
    
    resp = _api_request("POST", "/api/v1/open/ai/generations", api_key, data=data)
    result = resp.get("data", {})
    
    job_id = result.get("job_id") or result.get("task_id") or result.get("jobId")
    if not job_id:
        print("No job ID returned", file=sys.stderr)
        return 1
    
    # Poll for completion
    print(f"Job {job_id} submitted, polling...")
    result = _poll_task("/api/v1/open/ai/generations", job_id, api_key, max_retries=120, interval=3)
    
    if result.get("status") != "completed":
        print(f"Task failed: {result.get('message', 'unknown')}", file=sys.stderr)
        return 1
    
    # Get result images - handle both camelCase and snake_case
    result_data = result.get("result", {})
    images = result_data.get("images", [])
    if not images:
        image_url = result_data.get("imageUrl") or result_data.get("image_url")
        if image_url:
            images = [{"url": image_url}]

    # Also check for camelCase 'results' array
    if not images:
        results = result.get("results", [])
        if results:
            images = [{"url": r.get("url")} for r in results if r.get("url")]

    if not images:
        print("No result images", file=sys.stderr)
        return 1
    
    # Download first image
    _download_image(images[0]["url"], out_path)
    _print_result(out_path)
    
    # Download additional images if any
    for i, img in enumerate(images[1:], 1):
        extra_path = out_path.parent / f"{out_path.stem}_{i}{out_path.suffix}"
        _download_image(img["url"], extra_path)
        _print_result(extra_path)
    
    return 0


def cmd_image_to_image(args, api_key: str, workspace: Path, safe_output_root: Path) -> int:
    """Generate image from image"""
    in_path, out_path = _prepare_paths(args, workspace, safe_output_root)
    reference_image = _resolve_input_image_url(args, in_path, api_key)
    prompt = _validate_prompt_field(args.prompt, "prompt")
    neg = _validate_optional_prompt_field(getattr(args, "negative_prompt", None), "negative prompt")
    
    data = {
        "type": "image_to_image",
        "model": args.model,
        "prompt": prompt,
        "referenceImage": reference_image,
        "sensitive_word_filter": not getattr(args, "no_sensitive_word_filter", False),
    }
    
    if neg:
        data["negative_prompt"] = neg
    if args.strength is not None:
        data["strength"] = args.strength
    if args.width:
        data["width"] = args.width
    if args.height:
        data["height"] = args.height
    
    resp = _api_request("POST", "/api/v1/open/ai/generations", api_key, data=data)
    result = resp.get("data", {})
    
    job_id = result.get("job_id") or result.get("task_id") or result.get("jobId")
    if not job_id:
        print("No job ID returned", file=sys.stderr)
        return 1
    
    # Poll for completion
    print(f"Job {job_id} submitted, polling...")
    result = _poll_task("/api/v1/open/ai/generations", job_id, api_key, max_retries=120, interval=3)
    
    if result.get("status") != "completed":
        print(f"Task failed: {result.get('message', 'unknown')}", file=sys.stderr)
        return 1
    
    # Get result images - handle both camelCase and snake_case
    result_data = result.get("result", {})
    images = result_data.get("images", [])
    if not images:
        image_url = result_data.get("imageUrl") or result_data.get("image_url")
        if image_url:
            images = [{"url": image_url}]

    # Also check for camelCase 'results' array
    if not images:
        results = result.get("results", [])
        if results:
            images = [{"url": r.get("url")} for r in results if r.get("url")]

    if not images:
        print("No result images", file=sys.stderr)
        return 1
    
    # Download first image
    _download_image(images[0]["url"], out_path)
    _print_result(out_path)
    
    return 0


def cmd_list_models(args, api_key: str) -> int:
    """List available AI models"""
    endpoint = "/api/v1/open/ai/models"
    if args.type:
        endpoint += f"?type={args.type}"
    
    resp = _api_request("GET", endpoint, api_key)
    models = resp.get("data", {}).get("models", [])
    
    print(f"Available models ({len(models)} total):")
    print("-" * 60)
    for m in models:
        print(f"  Model: {m.get('model')}")
        print(f"  Type: {m.get('type')}")
        print(f"  Provider: {m.get('provider')}")
        print(f"  Description: {m.get('description', 'N/A')}")
        print("-" * 60)
    
    return 0


def _prepare_paths(args, workspace: Path, safe_output_root: Path) -> tuple[Path, Path]:
    """Prepare input and output paths"""
    input_str = args.input
    
    # Handle input
    if _is_remote_image_ref(input_str):
        url = input_str.strip()
        _validate_user_image_url(url)
        in_path = Path(url)
    else:
        try:
            in_path = Path(input_str).expanduser().resolve(strict=True)
        except FileNotFoundError:
            print(f"Input file not found: {input_str}", file=sys.stderr)
            raise SystemExit(2)
        
        if not in_path.is_file():
            print(f"Input is not a file: {in_path}", file=sys.stderr)
            raise SystemExit(2)
        
        _ensure_within(in_path, workspace, "input path")
        _validate_input_image(in_path)
    
    out_path = _prepare_output_path(args.output, workspace, safe_output_root)
    return in_path, out_path


def _prepare_output_path(output_str: str, workspace: Path, safe_output_root: Path) -> Path:
    """Prepare output path (always under safe_output_root)."""
    raw = Path(output_str).expanduser()
    safe = safe_output_root.resolve()
    if raw.is_absolute():
        out_path = raw.resolve()
    else:
        candidate_ws = (workspace / raw).resolve()
        try:
            candidate_ws.relative_to(safe)
            out_path = candidate_ws
        except ValueError:
            out_path = (safe / raw).resolve()

    _ensure_within(out_path, safe_output_root, "output path")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    
    return out_path


def _print_result(out_path: Path) -> None:
    """Print result with MEDIA tag"""
    print(f"Saved: {out_path}")
    try:
        rel = out_path.relative_to(Path.cwd())
        print(f"MEDIA: ./{rel}")
    except ValueError:
        print(f"MEDIA: {out_path}")


def main() -> int:
    p = argparse.ArgumentParser(description="MoPNG API client for image processing")
    sub = p.add_subparsers(dest="command", required=True)
    
    # Common args
    def add_common(cmd):
        cmd.add_argument("--input", "-i", required=True, help="Input image path or URL")
        cmd.add_argument("--output", "-o", required=True, help="Output image path")
    
    def add_output_format(cmd):
        cmd.add_argument("--output-format", default="png", choices=["png", "jpg"], help="Output format")
    
    def add_async(cmd):
        cmd.add_argument("--async-mode", action="store_true", help="Use async mode with polling")
    
    # remove-bg
    cmd_bg = sub.add_parser("remove-bg", help="Remove background from image")
    add_common(cmd_bg)
    add_output_format(cmd_bg)
    add_async(cmd_bg)
    cmd_bg.add_argument("--return-mask", action="store_true", help="Return mask")
    cmd_bg.add_argument("--only-mask", action="store_true", help="Return only mask")
    
    # upscale
    cmd_up = sub.add_parser("upscale", help="Upscale image")
    add_common(cmd_up)
    add_output_format(cmd_up)
    add_async(cmd_up)
    cmd_up.add_argument("--scale", type=int, default=2, choices=[2, 4], help="Scale factor")
    cmd_up.add_argument("--tile-size", type=int, default=0, help="Tile size")
    cmd_up.add_argument("--tile-pad", type=int, default=10, help="Tile padding")
    
    # outpainting
    cmd_op = sub.add_parser("outpainting", help="Expand image with outpainting")
    add_common(cmd_op)
    cmd_op.add_argument("--direction", default="all", choices=["all", "up", "down", "left", "right"], help="Expand direction")
    cmd_op.add_argument("--expand-ratio", type=float, default=0.5, help="Expand ratio (0.1-1.0)")
    cmd_op.add_argument("--angle", type=int, default=0, help="Rotation angle")
    cmd_op.add_argument("--output-ratio", help="Output ratio")
    cmd_op.add_argument("--best-quality", action="store_true", help="Best quality")
    
    # translation
    cmd_tr = sub.add_parser("translation", help="Translate image text")
    add_common(cmd_tr)
    cmd_tr.add_argument("--source-language", default="auto", help="Source language")
    cmd_tr.add_argument("--target-language", required=True, help="Target language (e.g., en, zh, ja, ko)")
    cmd_tr.add_argument("--domain-hint", help="Domain hint")
    cmd_tr.add_argument("--sensitive-word-filter", action="store_true", help="Enable sensitive word filter")
    cmd_tr.add_argument("--term-intervention", help="Term intervention")
    
    # text-to-image
    cmd_t2i = sub.add_parser("text-to-image", help="Generate image from text")
    cmd_t2i.add_argument("--prompt", "-p", required=True, help="Text prompt")
    cmd_t2i.add_argument("--output", "-o", required=True, help="Output image path")
    cmd_t2i.add_argument("--model", default="wanx-v2.5", help="Model name")
    cmd_t2i.add_argument("--negative-prompt", help="Negative prompt")
    cmd_t2i.add_argument("--width", type=int, help="Image width")
    cmd_t2i.add_argument("--height", type=int, help="Image height")
    cmd_t2i.add_argument("--n", type=int, help="Number of images")
    cmd_t2i.add_argument(
        "--no-sensitive-word-filter",
        action="store_true",
        help="Disable server-side sensitive word filtering (default: filtering on)",
    )
    
    # image-to-image
    cmd_i2i = sub.add_parser("image-to-image", help="Generate image from image")
    add_common(cmd_i2i)
    cmd_i2i.add_argument("--prompt", "-p", required=True, help="Edit prompt")
    cmd_i2i.add_argument("--model", default="wanx-v2.5", help="Model name")
    cmd_i2i.add_argument("--negative-prompt", help="Negative prompt")
    cmd_i2i.add_argument("--strength", type=float, help="Edit strength")
    cmd_i2i.add_argument("--width", type=int, help="Image width")
    cmd_i2i.add_argument("--height", type=int, help="Image height")
    cmd_i2i.add_argument(
        "--no-sensitive-word-filter",
        action="store_true",
        help="Disable server-side sensitive word filtering (default: filtering on)",
    )
    
    # list-models
    cmd_lm = sub.add_parser("list-models", help="List available models")
    cmd_lm.add_argument("--type", choices=["text_to_image", "image_to_image", "image_edit"], help="Filter by type")
    
    args = p.parse_args()
    
    # Get API key
    api_key = os.getenv("MOPNG_API_KEY")
    if not api_key:
        print("Missing MOPNG_API_KEY environment variable", file=sys.stderr)
        return 2
    
    # Setup paths
    workspace = _workspace_root()
    safe_output_root = workspace / "outputs" / "mopng-api"
    
    # Dispatch
    try:
        if args.command == "remove-bg":
            return cmd_remove_bg(args, api_key, workspace, safe_output_root)
        elif args.command == "upscale":
            return cmd_upscale(args, api_key, workspace, safe_output_root)
        elif args.command == "outpainting":
            return cmd_outpainting(args, api_key, workspace, safe_output_root)
        elif args.command == "translation":
            return cmd_translation(args, api_key, workspace, safe_output_root)
        elif args.command == "text-to-image":
            return cmd_text_to_image(args, api_key, workspace, safe_output_root)
        elif args.command == "image-to-image":
            return cmd_image_to_image(args, api_key, workspace, safe_output_root)
        elif args.command == "list-models":
            return cmd_list_models(args, api_key)
        else:
            print(f"Unknown command: {args.command}", file=sys.stderr)
            return 2
    except ValueError as e:
        print(str(e), file=sys.stderr)
        print(f"Input must be an allowed image inside {workspace}.", file=sys.stderr)
        print(f"Output must be under {safe_output_root}.", file=sys.stderr)
        return 2
    except RuntimeError as e:
        print(str(e), file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
