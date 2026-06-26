#!/usr/bin/env python3
"""
Phosor AI CLI Client — single-file, stdlib-only.

Usage:
    python3 phosor_client.py <command> [options]
    python3 phosor_client.py --help

Environment:
    PHOSOR_API_KEY  — API key for authentication (required for most commands)
    PHOSOR_BASE_URL — Base URL override (default: https://phosor.ai)
"""

import argparse
import json
import os
import re
import sys
import time
import uuid
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

VERSION = "1.0.0"
DEFAULT_BASE_URL = "https://phosor.ai"
WORKSPACE_DIR = Path.home() / ".openclaw" / "workspace"
PENDING_FILE = WORKSPACE_DIR / "phosor-pending.json"

MODELS = {
    "models": {
        "wan/2.2-14b/text-to-video": {
            "id": "wan/2.2-14b/text-to-video",
            "name": "Wan 2.2 Text-to-Video 14B",
            "type": "text-to-video",
            "input": {
                "prompt": {"type": "string", "required": True},
                "negative_prompt": {"type": "string", "required": False, "default": ""},
                "width": {"type": "integer", "required": False, "default": 854},
                "height": {"type": "integer", "required": False, "default": 480},
                "num_frames": {"type": "integer", "required": False, "default": 81},
                "frames_per_second": {"type": "integer", "required": False, "default": 16, "min": 4, "max": 30},
                "num_inference_steps": {"type": "integer", "required": False, "default": 4, "min": 4, "max": 4},
                "guidance_scale": {"type": "number", "required": False, "default": 1.0, "min": 1.0, "max": 3.5},
                "seed": {"type": "integer", "required": False, "default": None},
                "lora_id": {"type": "string", "required": False},
                "lora_scale": {"type": "number", "required": False, "default": 1.0, "min": 0.0, "max": 2.0},
            },
            "resolutions": {
                "480p_landscape": {"width": 854, "height": 480, "max_frames": 161},
                "480p_portrait": {"width": 480, "height": 854, "max_frames": 161},
                "720p_landscape": {"width": 1280, "height": 720, "max_frames": 161},
                "720p_portrait": {"width": 720, "height": 1280, "max_frames": 161},
                "1080p_landscape": {"width": 1920, "height": 1080, "max_frames": 153},
                "1080p_portrait": {"width": 1080, "height": 1920, "max_frames": 153},
            },
        },
        "wan/2.2-14b/image-to-video": {
            "id": "wan/2.2-14b/image-to-video",
            "name": "Wan 2.2 Image-to-Video 14B",
            "type": "image-to-video",
            "input": {
                "prompt": {"type": "string", "required": True},
                "image_url": {"type": "string", "required": True, "description": "S3 key from upload-image"},
                "negative_prompt": {"type": "string", "required": False, "default": ""},
                "width": {"type": "integer", "required": False, "default": 854},
                "height": {"type": "integer", "required": False, "default": 480},
                "num_frames": {"type": "integer", "required": False, "default": 81},
                "frames_per_second": {"type": "integer", "required": False, "default": 16, "min": 4, "max": 30},
                "num_inference_steps": {"type": "integer", "required": False, "default": 4, "min": 4, "max": 4},
                "guidance_scale": {"type": "number", "required": False, "default": 1.0, "min": 1.0, "max": 3.5},
                "seed": {"type": "integer", "required": False, "default": None},
                "lora_id": {"type": "string", "required": False},
                "lora_scale": {"type": "number", "required": False, "default": 1.0, "min": 0.0, "max": 2.0},
            },
            "resolutions": {
                "480p_landscape": {"width": 854, "height": 480, "max_frames": 161},
                "480p_portrait": {"width": 480, "height": 854, "max_frames": 161},
                "720p_landscape": {"width": 1280, "height": 720, "max_frames": 161},
                "720p_portrait": {"width": 720, "height": 1280, "max_frames": 161},
                "1080p_landscape": {"width": 1920, "height": 1080, "max_frames": 153},
                "1080p_portrait": {"width": 1080, "height": 1920, "max_frames": 153},
            },
        },
    },
    "frame_alignment": {
        "formula": "valid_frames = 1 + 4*k where k >= 1",
        "examples": [5, 9, 13, 17, 21, 25, 29, 33, 37, 41, 45, 49, 53, 57, 61, 65, 69, 73, 77, 81],
    },
    "pricing": {
        "inference": {
            "480p": {"per_frame_usd": 0.0002, "per_frame_credits": 0.002},
            "720p": {"per_frame_usd": 0.0006, "per_frame_credits": 0.006},
            "1080p": {"per_frame_usd": 0.0012, "per_frame_credits": 0.012},
        },
        "lora_multiplier": 1.25,
        "credits_per_usd": 10,
    },
    "quotas": {
        "max_loras_per_user": 20,
        "max_lora_size_mb": 2048,
        "max_api_keys_per_user": 10,
        "uploaded_lora_expiry_days": 1,
        "rate_limit_requests_per_minute": 1000,
    },
}


# ─── Helpers ────────────────────────────────────────────────────────────────

def _json_out(data):
    """Print JSON to stdout and exit 0."""
    print(json.dumps(data, indent=2, default=str))
    sys.exit(0)


def _error_out(message, code=1):
    """Print error JSON to stderr and exit non-zero."""
    print(json.dumps({"error": message}, indent=2), file=sys.stderr)
    sys.exit(code)


# ─── PhosorClient ──────────────────────────────────────────────────────────

class PhosorClient:
    """Core API wrapper — stdlib-only HTTP via urllib."""

    def __init__(self, base_url=None, api_key=None):
        resolved = (base_url or os.environ.get("PHOSOR_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
        if not resolved.startswith("https://"):
            _error_out(f"Base URL must use HTTPS: {resolved}")
        self.base_url = resolved
        self.api_key = api_key or self._resolve_api_key()

    @staticmethod
    def _resolve_api_key():
        key = os.environ.get("PHOSOR_API_KEY")
        if key:
            return key.strip()
        return None

    def _request(self, method, path, json_data=None, params=None):
        """Make an authenticated HTTP request. Returns parsed JSON."""
        url = f"{self.base_url}{path}"
        if params:
            qs = "&".join(f"{quote(str(k), safe='')}={quote(str(v), safe='')}"
                          for k, v in params.items() if v is not None)
            if qs:
                url = f"{url}?{qs}"

        body = None
        if json_data is not None:
            body = json.dumps(json_data).encode("utf-8")

        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["X-API-Key"] = self.api_key

        req = Request(url, data=body, headers=headers, method=method)

        try:
            with urlopen(req, timeout=120) as resp:
                raw = resp.read().decode("utf-8")
                return json.loads(raw) if raw else {}
        except HTTPError as e:
            raw = e.read().decode("utf-8", errors="replace")
            try:
                detail = json.loads(raw)
            except Exception:
                detail = {"raw": raw}
            _error_out(f"HTTP {e.code}: {detail}")
        except URLError as e:
            _error_out(f"Connection error: {e.reason}")

    @staticmethod
    def _sanitize_filename(name):
        """Remove characters unsafe for Content-Disposition filename."""
        return re.sub(r'["\r\n\\]', '_', name)

    def _upload_multipart(self, path, file_path, field_name="file"):
        """Upload a file via multipart/form-data (stdlib-only)."""
        boundary = f"----PhosorBoundary{uuid.uuid4().hex}"
        file_path = Path(file_path)
        filename = self._sanitize_filename(file_path.name)

        ext = file_path.suffix.lower()
        ct_map = {
            ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
            ".png": "image/png", ".webp": "image/webp",
            ".safetensors": "application/octet-stream",
        }
        content_type = ct_map.get(ext, "application/octet-stream")

        file_data = file_path.read_bytes()

        body_parts = []
        body_parts.append(f"--{boundary}\r\n".encode())
        body_parts.append(
            f'Content-Disposition: form-data; name="{field_name}"; filename="{filename}"\r\n'
            f"Content-Type: {content_type}\r\n\r\n".encode()
        )
        body_parts.append(file_data)
        body_parts.append(f"\r\n--{boundary}--\r\n".encode())

        body = b"".join(body_parts)

        url = f"{self.base_url}{path}"
        headers = {
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        }
        if self.api_key:
            headers["X-API-Key"] = self.api_key

        req = Request(url, data=body, headers=headers, method="POST")

        try:
            with urlopen(req, timeout=300) as resp:
                raw = resp.read().decode("utf-8")
                return json.loads(raw) if raw else {}
        except HTTPError as e:
            raw = e.read().decode("utf-8", errors="replace")
            try:
                detail = json.loads(raw)
            except Exception:
                detail = {"raw": raw}
            _error_out(f"HTTP {e.code}: {detail}")
        except URLError as e:
            _error_out(f"Connection error: {e.reason}")

    # ── Inference ───────────────────────────────────────────────────────────

    def check_key(self):
        """Validate the API key by calling a read-only endpoint."""
        return self._request("GET", "/api/v1/models")

    def submit(self, prompt, **kwargs):
        """Submit an inference job (T2V or I2V)."""
        payload = {"prompt": prompt}
        for k in ("width", "height", "num_frames", "frames_per_second", "seed",
                   "negative_prompt", "image_url", "lora_id", "lora_scale", "loras",
                   "num_inference_steps", "guidance_scale", "model"):
            if kwargs.get(k) is not None:
                payload[k] = kwargs[k]
        return self._request("POST", "/api/v1/inference/submit", json_data=payload)

    def status(self, request_id):
        """Get job status."""
        return self._request("GET", f"/api/v1/inference/status/{request_id}")

    def result(self, request_id):
        """Get job result (video URL)."""
        return self._request("GET", f"/api/v1/inference/result/{request_id}")

    def history(self, limit=50):
        """Get job history for authenticated user."""
        return self._request("GET", "/api/v1/inference/history", params={"limit": limit})

    # ── Storage: Image ──────────────────────────────────────────────────────

    def upload_image(self, file_path):
        """Upload a local image file for I2V."""
        return self._upload_multipart("/api/v1/storage/image/upload", file_path, field_name="file")

    def import_image(self, url, filename=None):
        """Import an image from a remote URL."""
        payload = {"url": url}
        if filename:
            payload["filename"] = filename
        return self._request("POST", "/api/v1/storage/image/import", json_data=payload)

    # ── Storage: LoRA ───────────────────────────────────────────────────────

    def upload_lora(self, high_noise_path, low_noise_path, name=None):
        """Upload a LoRA model (two .safetensors files: high_noise + low_noise)."""
        boundary = f"----PhosorBoundary{uuid.uuid4().hex}"
        high_path = Path(high_noise_path)
        low_path = Path(low_noise_path)

        body_parts = []
        for field, fpath in [("high_noise_file", high_path), ("low_noise_file", low_path)]:
            safe_name = self._sanitize_filename(fpath.name)
            body_parts.append(f"--{boundary}\r\n".encode())
            body_parts.append(
                f'Content-Disposition: form-data; name="{field}"; filename="{safe_name}"\r\n'
                f"Content-Type: application/octet-stream\r\n\r\n".encode()
            )
            body_parts.append(fpath.read_bytes())
            body_parts.append(b"\r\n")

        if name:
            safe_val = re.sub(r'[\r\n]', ' ', name)
            body_parts.append(f"--{boundary}\r\n".encode())
            body_parts.append(
                f'Content-Disposition: form-data; name="name"\r\n\r\n{safe_val}\r\n'.encode()
            )

        body_parts.append(f"--{boundary}--\r\n".encode())
        body = b"".join(body_parts)

        url = f"{self.base_url}/api/v1/storage/lora/upload"
        headers = {"Content-Type": f"multipart/form-data; boundary={boundary}"}
        if self.api_key:
            headers["X-API-Key"] = self.api_key

        req = Request(url, data=body, headers=headers, method="POST")
        try:
            with urlopen(req, timeout=600) as resp:
                raw = resp.read().decode("utf-8")
                return json.loads(raw) if raw else {}
        except HTTPError as e:
            raw = e.read().decode("utf-8", errors="replace")
            try:
                detail = json.loads(raw)
            except Exception:
                detail = {"raw": raw}
            _error_out(f"HTTP {e.code}: {detail}")
        except URLError as e:
            _error_out(f"Connection error: {e.reason}")

    def import_lora(self, high_noise_url, low_noise_url, name=None):
        """Import a LoRA model from two remote URLs (HTTPS .safetensors)."""
        payload = {
            "high_noise_url": high_noise_url,
            "low_noise_url": low_noise_url,
        }
        if name:
            payload["name"] = name
        return self._request("POST", "/api/v1/storage/lora/import", json_data=payload)

    # ── LoRA Management ─────────────────────────────────────────────────────

    def loras(self, limit=50, offset=0):
        """List LoRA models."""
        return self._request("GET", "/api/v1/loras", params={"limit": limit, "offset": offset})

    def lora_status(self, lora_id):
        """Get LoRA upload/import status."""
        return self._request("GET", f"/api/v1/loras/{lora_id}/status")

    def delete_lora(self, lora_id):
        """Delete a LoRA model (soft delete)."""
        return self._request("DELETE", f"/api/v1/loras/{lora_id}")

    # ── Models ──────────────────────────────────────────────────────────────

    def list_models(self):
        """List available models."""
        return self._request("GET", "/api/v1/models")

    # ── Utility ─────────────────────────────────────────────────────────────

    def quotas(self):
        """Get quota usage and limits."""
        return self._request("GET", "/api/v1/training/quotas")


# ─── PendingManager ────────────────────────────────────────────────────────

class PendingManager:
    """Track pending jobs locally at ~/.openclaw/workspace/phosor-pending.json."""

    def __init__(self, path=None):
        self.path = Path(path) if path else PENDING_FILE
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _load(self):
        if self.path.exists():
            try:
                return json.loads(self.path.read_text())
            except (json.JSONDecodeError, OSError):
                return {}
        return {}

    def _save(self, data):
        self.path.write_text(json.dumps(data, indent=2, default=str))

    def add(self, request_id, job_type, metadata=None):
        data = self._load()
        data[request_id] = {
            "job_type": job_type,
            "submitted_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            **(metadata or {}),
        }
        self._save(data)

    def remove(self, request_id):
        data = self._load()
        data.pop(request_id, None)
        self._save(data)

    def list_pending(self):
        return self._load()

    def poll_all(self, client):
        """Poll all pending jobs, remove completed/failed, return results."""
        data = self._load()
        results = {}
        to_remove = []

        for rid, meta in data.items():
            try:
                st = client.status(rid)
                results[rid] = st
                status_val = st.get("status") or ""
                if status_val.upper() in ("COMPLETED", "FAILED", "NOT_FOUND"):
                    to_remove.append(rid)
            except SystemExit:
                results[rid] = {"error": "Failed to poll"}

        for rid in to_remove:
            self.remove(rid)

        return {"polled": len(data), "completed": len(to_remove), "results": results}


# ─── CLI ────────────────────────────────────────────────────────────────────

def build_parser():
    parser = argparse.ArgumentParser(
        prog="phosor_client",
        description="Phosor AI CLI — generate videos with optional custom LoRA styles",
    )
    parser.add_argument("--version", action="version", version=f"phosor-client {VERSION}")
    parser.add_argument("--base-url", default=None, help="API base URL override")
    parser.add_argument("--api-key", default=None, help="API key override")

    sub = parser.add_subparsers(dest="command", help="Available commands")

    # ── check-key ───────────────────────────────────────────────────────
    sub.add_parser("check-key", help="Validate API key")

    # ── submit ──────────────────────────────────────────────────────────
    p = sub.add_parser("submit", help="Submit inference job (T2V or I2V)")
    p.add_argument("prompt", help="Text prompt")
    p.add_argument("--width", type=int, default=None)
    p.add_argument("--height", type=int, default=None)
    p.add_argument("--num-frames", type=int, default=None)
    p.add_argument("--fps", type=int, default=None, dest="frames_per_second")
    p.add_argument("--steps", type=int, default=None, dest="num_inference_steps",
                   help="Inference steps (default 4)")
    p.add_argument("--guidance", type=float, default=None, dest="guidance_scale",
                   help="Guidance scale (1.0-3.5, default 1.0)")
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--negative-prompt", default=None)
    p.add_argument("--image-url", default=None, help="S3 key for I2V (from upload-image)")
    p.add_argument("--lora-id", default=None)
    p.add_argument("--lora-scale", type=float, default=None)
    p.add_argument("--loras", default=None,
                   help='Multiple LoRAs as JSON: \'[{"lora_id":"...","lora_scale":1.0}]\'')
    p.add_argument("--model", default=None)

    # ── status ──────────────────────────────────────────────────────────
    p = sub.add_parser("status", help="Get job status")
    p.add_argument("request_id", help="Job request ID")

    # ── result ──────────────────────────────────────────────────────────
    p = sub.add_parser("result", help="Get job result (video URL)")
    p.add_argument("request_id", help="Job request ID")

    # ── poll ────────────────────────────────────────────────────────────
    sub.add_parser("poll", help="Poll all pending jobs")

    # ── list ────────────────────────────────────────────────────────────
    sub.add_parser("list", help="List pending jobs (local tracking)")

    # ── history ─────────────────────────────────────────────────────────
    p = sub.add_parser("history", help="Get job history")
    p.add_argument("--limit", type=int, default=50)

    # ── upload-image ────────────────────────────────────────────────────
    p = sub.add_parser("upload-image", help="Upload local image for I2V")
    p.add_argument("file", help="Path to image file (JPEG, PNG, WebP)")

    # ── import-image ────────────────────────────────────────────────────
    p = sub.add_parser("import-image", help="Import image from URL")
    p.add_argument("url", help="Public image URL")
    p.add_argument("--filename", default=None)

    # ── upload-lora ─────────────────────────────────────────────────────
    p = sub.add_parser("upload-lora", help="Upload LoRA model (two .safetensors files)")
    p.add_argument("high_noise_file", help="Path to high_noise .safetensors file")
    p.add_argument("low_noise_file", help="Path to low_noise .safetensors file")
    p.add_argument("--name", default=None, help="LoRA model name")

    # ── import-lora ──────────────────────────────────────────────────────
    p = sub.add_parser("import-lora", help="Import LoRA from two HTTPS URLs")
    p.add_argument("high_noise_url", help="HTTPS URL to high_noise .safetensors")
    p.add_argument("low_noise_url", help="HTTPS URL to low_noise .safetensors")
    p.add_argument("--name", default=None, help="LoRA model name")

    # ── loras ───────────────────────────────────────────────────────────
    p = sub.add_parser("loras", help="List LoRA models")
    p.add_argument("--limit", type=int, default=50)
    p.add_argument("--offset", type=int, default=0)

    # ── lora-status ─────────────────────────────────────────────────────
    p = sub.add_parser("lora-status", help="Get LoRA upload/import status")
    p.add_argument("lora_id", help="LoRA model UUID")

    # ── delete-lora ─────────────────────────────────────────────────────
    p = sub.add_parser("delete-lora", help="Delete a LoRA model")
    p.add_argument("lora_id", help="LoRA model UUID")

    # ── models ─────────────────────────────────────────────────────────
    sub.add_parser("models", help="List available models")

    # ── quotas ──────────────────────────────────────────────────────────
    sub.add_parser("quotas", help="Get quota usage and limits")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    client = PhosorClient(base_url=args.base_url, api_key=args.api_key)
    pending = PendingManager()

    cmd = args.command

    # ── Offline commands ────────────────────────────────────────────────

    if cmd == "list":
        _json_out(pending.list_pending())

    # ── Commands requiring API key ──────────────────────────────────────

    if cmd == "check-key":
        if not client.api_key:
            _error_out("PHOSOR_API_KEY not set")
        resp = client.check_key()
        _json_out({"status": "valid", "models": resp})

    if cmd == "submit":
        kwargs = {}
        for k in ("width", "height", "num_frames", "frames_per_second", "seed",
                   "negative_prompt", "image_url", "lora_id", "lora_scale",
                   "num_inference_steps", "guidance_scale", "model"):
            v = getattr(args, k, None)
            if v is not None:
                kwargs[k] = v
        loras_str = getattr(args, "loras", None)
        if loras_str:
            try:
                kwargs["loras"] = json.loads(loras_str)
            except json.JSONDecodeError:
                _error_out("--loras must be valid JSON array, e.g. '[{\"lora_id\":\"...\",\"lora_scale\":1.0}]'")
        resp = client.submit(args.prompt, **kwargs)
        rid = resp.get("request_id") or resp.get("requested_id")
        if rid:
            job_type = "i2v" if kwargs.get("image_url") else "t2v"
            pending.add(rid, job_type, {"prompt": args.prompt[:80]})
        _json_out(resp)

    if cmd == "status":
        _json_out(client.status(args.request_id))

    if cmd == "result":
        _json_out(client.result(args.request_id))

    if cmd == "poll":
        _json_out(pending.poll_all(client))

    if cmd == "history":
        _json_out(client.history(limit=args.limit))

    # ── Storage ─────────────────────────────────────────────────────────

    if cmd == "upload-image":
        _json_out(client.upload_image(args.file))

    if cmd == "import-image":
        _json_out(client.import_image(args.url, filename=args.filename))

    if cmd == "upload-lora":
        _json_out(client.upload_lora(args.high_noise_file, args.low_noise_file, name=args.name))

    if cmd == "import-lora":
        _json_out(client.import_lora(args.high_noise_url, args.low_noise_url, name=args.name))

    # ── LoRA Management ─────────────────────────────────────────────────

    if cmd == "loras":
        _json_out(client.loras(limit=args.limit, offset=args.offset))

    if cmd == "lora-status":
        _json_out(client.lora_status(args.lora_id))

    if cmd == "delete-lora":
        _json_out(client.delete_lora(args.lora_id))

    # ── Models & Utility ────────────────────────────────────────────────

    if cmd == "models":
        _json_out(client.list_models())

    if cmd == "quotas":
        _json_out(client.quotas())


if __name__ == "__main__":
    main()
