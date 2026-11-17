#!/usr/bin/env python3
"""
Phosor AI CLI Client — single-file, stdlib-only.

Usage:
    python3 phosor_client.py <command> [options]
    python3 phosor_client.py --help

Environment:
    PHOSOR_API_KEY  — API key for authentication (required for most commands)
    PHOSOR_BASE_URL — Optional compatibility setting; must be https://phosor.ai
"""

import argparse
import json
import os
import re
import sys
import time
import uuid
import hashlib
import tempfile
from http.client import HTTPException
if os.name == "nt":
    import msvcrt
else:
    import fcntl
from contextlib import contextmanager, redirect_stderr
import io
from pathlib import Path
from urllib.parse import quote, urlsplit
from urllib.request import Request, build_opener, HTTPRedirectHandler
from urllib.error import HTTPError, URLError

def _decode_response(raw):
    value = json.loads(raw) if raw else {}
    if not isinstance(value, dict):
        raise ValueError("Unexpected response type")
    return value


def _valid_stream_chunk(chunk):
    choices = chunk.get("choices", [])
    if not isinstance(choices, list):
        return False
    for choice in choices:
        if not isinstance(choice, dict):
            return False
        if choice.get("finish_reason") is not None and not isinstance(choice["finish_reason"], str):
            return False
        delta = choice.get("delta") or {}
        if not isinstance(delta, dict):
            return False
        for key in ("content", "reasoning_content"):
            if delta.get(key) is not None and not isinstance(delta[key], str):
                return False
        calls = delta.get("tool_calls") or []
        if not isinstance(calls, list):
            return False
        for call in calls:
            if not isinstance(call, dict) or type(call.get("index", 0)) is not int:
                return False
            function = call.get("function") or {}
            if not isinstance(function, dict):
                return False
            if any(function.get(key) is not None and not isinstance(function[key], str)
                   for key in ("name", "arguments")):
                return False
    return True


class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise HTTPError(req.full_url, code, "Redirect refused", headers, fp)


def urlopen(request, timeout=120):
    """Only send requests to the official HTTPS service; never follow redirects."""
    target = request.full_url if isinstance(request, Request) else request
    parts = urlsplit(target)
    if (parts.scheme != "https" or parts.hostname != "phosor.ai"
            or parts.port not in (None, 443) or parts.username or parts.password):
        _error_out("Only https://phosor.ai is supported")
    return build_opener(_NoRedirect()).open(request, timeout=timeout)


def _http_error(error):
    """Keep diagnostic identifiers without echoing untrusted response bodies."""
    headers = error.headers or {}
    hints = {400: "Check request parameters", 401: "Check the API key",
             402: "Insufficient credits", 403: "Access denied",
             404: "Resource not found", 429: "Request limit reached",
             503: "Service temporarily unavailable"}
    out = {"http_status": error.code,
           "message": hints.get(error.code, "Request failed")}
    for header, key in (("Retry-After", "retry_after"),
                        ("X-Reject-Reason", "reject_reason"),
                        ("X-Request-ID", "request_id")):
        value = headers.get(header)
        if value and re.fullmatch(r"[A-Za-z0-9_.:, +/\-]{1,160}", value):
            out[key] = value
    try:
        body = json.loads(error.read())
        code = body.get("code") or body.get("error")
        if isinstance(code, dict):
            code = code.get("code")
        allowed = {"SYSTEM_UPGRADING", "maintenance", "invalid_request",
                   "invalid_api_key", "insufficient_credits", "email_not_verified",
                   "rate_limited", "capacity_busy", "service_unavailable"}
        if isinstance(code, str) and code in allowed:
            out["code"] = code
    except (ValueError, AttributeError, TypeError, OSError, HTTPException):
        pass
    print(json.dumps({"error": out}), file=sys.stderr)
    raise SystemExit(1)


VERSION = "1.4.1"   # keep equal to the VERSION file shipped in this package
DEFAULT_BASE_URL = "https://phosor.ai"
WORKSPACE_DIR = Path.home() / ".openclaw" / "workspace"
PENDING_FILE = WORKSPACE_DIR / "phosor-pending.json"

# Fields forwarded verbatim to /api/v1/inference/submit.
_SUBMIT_FIELDS = (
    "width", "height", "num_frames", "frames_per_second", "seed",
    "negative_prompt", "image_url", "image_urls", "audio_url", "video_url",
    "lora_id", "lora_scale", "loras",
    "num_inference_steps", "guidance_scale", "model",
    "num_images", "strength", "output_format",
    # MiniMax H3 (duration-based, not frame-based)
    "duration", "resolution_tier", "aspect_ratio", "end_image_url", "avoid_model_limitations",
    "unrestricted_enhancement",
    "reference_image_urls", "reference_video_urls", "reference_audio_urls",
    "use_ref_video_audio",
    # What each reference asset is, in the same order as the *_urls arrays.
    # Optional but recommended for Ref2VA: uploaded files are stored under
    # generated ids, so without this the model cannot tell which picture shows
    # which character named in your prompt. Keep your prompt as you wrote it —
    # the platform does the binding for you.
    "reference_image_labels", "reference_video_labels", "reference_audio_labels",
    # Qwen3-TTS (takes `text`, not `prompt`)
    "text", "speaker", "language", "temperature", "top_p", "top_k", "repetition_penalty",
)

# Fields accepted by POST /api/v1/chat/completions. The endpoint rejects any other
# field with 400 invalid_request, so the client never forwards anything outside this list.
_CHAT_FIELDS = (
    "model", "messages", "max_tokens", "temperature", "top_p", "stop", "stream",
    "stream_options", "response_format", "tools", "tool_choice", "enable_thinking",
    "seed", "presence_penalty", "frequency_penalty", "n", "user",
)
CHAT_MODEL = "qwen3.8-27b"
CHAT_MAX_IMAGES = 2
CHAT_MAX_IMAGE_BYTES = 4 * 1024 * 1024

MODELS = {
    "models": {
        "qwen-image/v2511/image-edit": {
            "id": "qwen-image/v2511/image-edit", "name": "Qwen Image Edit",
            "type": "image-edit", "input": {
                "prompt": {"type": "string", "required": True},
                "image_urls": {"type": "array", "required": True}},
            "note": "Use --image-urls with a JSON array of uploaded image keys or public URLs."
        },
        "minimax/h3/text-to-image": {
            "id": "minimax/h3/text-to-image", "name": "MiniMax H3 Image",
            "type": "text-to-image", "input": {"prompt": {"required": True}},
            "resolutions": [[1024, 1024], [1536, 1536], [2048, 2048], [3072, 3072], [4096, 4096]],
            "note": "One image. Square presets shown; consult the model reference for all supported sizes. Formats: png, jpeg, webp."
        },
        "minimax/h3/reference-to-video/turbo": {
            "id": "minimax/h3/reference-to-video/turbo", "name": "MiniMax H3 Reference-to-Video Turbo",
            "type": "reference-to-video",
            "billing": "per output second PLUS per reference input",
            "note": "MiniMax H3 Turbo; output 480p $0.006/s, 768p $0.012/s; first 5 images free, then $0.0025 each; audio free.",
        },
        "wan/v2.2-a14b/text-to-video": {
            "id": "wan/v2.2-a14b/text-to-video",
            "name": "Wan 2.2 Text-to-Video 14B",
            "type": "text-to-video",
            "input": {
                "prompt": {"type": "string", "required": True, "description": "Input and processing limits depend on the model"},
                "negative_prompt": {"type": "string", "required": False, "default": ""},
                "width": {"type": "integer", "required": False, "default": 854},
                "height": {"type": "integer", "required": False, "default": 480},
                "num_frames": {"type": "integer", "required": False, "default": 81},
                "frames_per_second": {"type": "integer", "required": False, "default": 16, "min": 4, "max": 30},
                "num_inference_steps": {"type": "integer", "required": False, "description": "Consult the selected model contract for sampling controls"},
                "guidance_scale": {"type": "number", "required": False, "description": "Consult the selected model contract for sampling controls"},
                "seed": {"type": "integer", "required": False, "default": None},
                "lora_id": {"type": "string", "required": False},
                "loras": {"type": "array", "required": False, "description": "Multiple LoRAs: [{\"lora_id\": \"...\", \"lora_scale\": 1.0}]"},
                "lora_scale": {"type": "number", "required": False, "default": 1.0, "min": 0.0, "max": 1.0},
            },
            "resolutions": {
                "480p_landscape": {"width": 854, "height": 480, "max_frames": 161},
                "480p_portrait": {"width": 480, "height": 854, "max_frames": 161},
                "720p_landscape": {"width": 1280, "height": 720, "max_frames": 161},
                "720p_portrait": {"width": 720, "height": 1280, "max_frames": 161},
                "1080p_landscape": {"width": 1920, "height": 1080, "max_frames": 81},
                "1080p_portrait": {"width": 1080, "height": 1920, "max_frames": 81},
            },
        },
        "wan/v2.2-a14b/image-to-video": {
            "id": "wan/v2.2-a14b/image-to-video",
            "name": "Wan 2.2 Image-to-Video 14B",
            "type": "image-to-video",
            "input": {
                "prompt": {"type": "string", "required": True, "description": "Input and processing limits depend on the model"},
                "image_url": {"type": "string", "required": True, "description": "S3 key from upload-image"},
                "negative_prompt": {"type": "string", "required": False, "default": ""},
                "width": {"type": "integer", "required": False, "default": 854},
                "height": {"type": "integer", "required": False, "default": 480},
                "num_frames": {"type": "integer", "required": False, "default": 81},
                "frames_per_second": {"type": "integer", "required": False, "default": 16, "min": 4, "max": 30},
                "num_inference_steps": {"type": "integer", "required": False, "description": "Consult the selected model contract for sampling controls"},
                "guidance_scale": {"type": "number", "required": False, "description": "Consult the selected model contract for sampling controls"},
                "seed": {"type": "integer", "required": False, "default": None},
                "lora_id": {"type": "string", "required": False},
                "loras": {"type": "array", "required": False, "description": "Multiple LoRAs: [{\"lora_id\": \"...\", \"lora_scale\": 1.0}]"},
                "lora_scale": {"type": "number", "required": False, "default": 1.0, "min": 0.0, "max": 1.0},
            },
            "resolutions": {
                "480p_landscape": {"width": 854, "height": 480, "max_frames": 161},
                "480p_portrait": {"width": 480, "height": 854, "max_frames": 161},
                "720p_landscape": {"width": 1280, "height": 720, "max_frames": 161},
                "720p_portrait": {"width": 720, "height": 1280, "max_frames": 161},
                "1080p_landscape": {"width": 1920, "height": 1080, "max_frames": 81},
                "1080p_portrait": {"width": 1080, "height": 1920, "max_frames": 81},
            },
        },
        "wan/v2.2-a14b/speech-to-video": {
            "id": "wan/v2.2-a14b/speech-to-video",
            "name": "Wan 2.2 Speech-to-Video 14B",
            "type": "speech-to-video",
            "input": {
                "prompt": {"type": "string", "required": True, "description": "Input and processing limits depend on the model"},
                "image_url": {"type": "string", "required": True, "description": "S3 key from upload-image (reference face image)"},
                "audio_url": {"type": "string", "required": True, "description": "URL to audio file (WAV/MP3)"},
                "negative_prompt": {"type": "string", "required": False, "default": ""},
                "width": {"type": "integer", "required": False, "default": 854},
                "height": {"type": "integer", "required": False, "default": 480},
                "num_frames": {"type": "integer", "required": False, "default": 81},
                "frames_per_second": {"type": "integer", "required": False, "default": 16, "min": 4, "max": 30},
                "num_inference_steps": {"type": "integer", "required": False, "description": "Consult the selected model contract for sampling controls"},
                "guidance_scale": {"type": "number", "required": False, "description": "Consult the selected model contract for sampling controls"},
                "seed": {"type": "integer", "required": False, "default": None},
            },
            "resolutions": {
                "480p_landscape": {"width": 854, "height": 480, "max_frames": 161},
                "480p_portrait": {"width": 480, "height": 854, "max_frames": 161},
                "512p_square": {"width": 512, "height": 512, "max_frames": 161},
                "720p_landscape": {"width": 1280, "height": 720, "max_frames": 161},
                "720p_portrait": {"width": 720, "height": 1280, "max_frames": 161},
            },
        },
        "wan/v2.2-a14b/animate": {
            "id": "wan/v2.2-a14b/animate",
            "name": "Wan 2.2 Animate 14B",
            "type": "animate",
            "input": {
                "prompt": {"type": "string", "required": True, "description": "Input and processing limits depend on the model"},
                "image_url": {"type": "string", "required": True, "description": "S3 key from upload-image (reference character image)"},
                "video_url": {"type": "string", "required": True, "description": "URL to motion/pose reference video"},
                "negative_prompt": {"type": "string", "required": False, "default": ""},
                "width": {"type": "integer", "required": False, "default": 854},
                "height": {"type": "integer", "required": False, "default": 480},
                "num_frames": {"type": "integer", "required": False, "default": 81},
                "frames_per_second": {"type": "integer", "required": False, "default": 16, "min": 4, "max": 30},
                "num_inference_steps": {"type": "integer", "required": False, "description": "Consult the selected model contract for sampling controls"},
                "guidance_scale": {"type": "number", "required": False, "description": "Consult the selected model contract for sampling controls"},
                "seed": {"type": "integer", "required": False, "default": None},
            },
            "resolutions": {
                "480p_landscape": {"width": 854, "height": 480, "max_frames": 161},
                "480p_portrait": {"width": 480, "height": 854, "max_frames": 161},
                "512p_square": {"width": 512, "height": 512, "max_frames": 161},
                "720p_landscape": {"width": 1280, "height": 720, "max_frames": 161},
                "720p_portrait": {"width": 720, "height": 1280, "max_frames": 161},
            },
        },
        "qwen-image/v2512/text-to-image": {
            "id": "qwen-image/v2512/text-to-image",
            "name": "Qwen Image 2512 Text-to-Image",
            "type": "text-to-image",
            "input": {
                "prompt": {"type": "string", "required": True, "description": "Input and processing limits depend on the model"},
                "negative_prompt": {"type": "string", "required": False, "default": ""},
                "width": {"type": "integer", "required": False, "default": 1024},
                "height": {"type": "integer", "required": False, "default": 1024},
                "num_images": {"type": "integer", "required": False, "default": 1, "min": 1, "max": 4},
                "num_inference_steps": {"type": "integer", "required": False, "default": 20, "min": 1, "max": 40},
                "guidance_scale": {"type": "number", "required": False, "default": 7.5, "min": 1.0, "max": 20.0},
                "seed": {"type": "integer", "required": False, "default": None},
                "output_format": {"type": "string", "required": False, "default": "png", "enum": ["png", "jpeg"]},
                "lora_id": {"type": "string", "required": False},
                "lora_scale": {"type": "number", "required": False, "default": 1.0, "min": 0.0, "max": 1.0},
            },
            "resolutions": {
                "512x512": {"width": 512, "height": 512},
                "1024x1024": {"width": 1024, "height": 1024},
                "1024x768": {"width": 1024, "height": 768},
                "768x1024": {"width": 768, "height": 1024},
                "1280x768": {"width": 1280, "height": 768},
                "768x1280": {"width": 768, "height": 1280},
            },
        },
        "qwen-image/v2512/text-to-image/lora": {
            "id": "qwen-image/v2512/text-to-image/lora",
            "name": "Qwen Image 2512 Text-to-Image with LoRA",
            "type": "text-to-image",
            "input": {
                "prompt": {"type": "string", "required": True, "description": "Input and processing limits depend on the model"},
                "negative_prompt": {"type": "string", "required": False, "default": ""},
                "width": {"type": "integer", "required": False, "default": 1024},
                "height": {"type": "integer", "required": False, "default": 1024},
                "num_images": {"type": "integer", "required": False, "default": 1, "min": 1, "max": 4},
                "num_inference_steps": {"type": "integer", "required": False, "default": 20, "min": 1, "max": 40},
                "guidance_scale": {"type": "number", "required": False, "default": 7.5, "min": 1.0, "max": 20.0},
                "seed": {"type": "integer", "required": False, "default": None},
                "output_format": {"type": "string", "required": False, "default": "png", "enum": ["png", "jpeg"]},
                "lora_id": {"type": "string", "required": True},
                "lora_scale": {"type": "number", "required": False, "default": 1.0, "min": 0.0, "max": 1.0},
            },
            "resolutions": {
                "512x512": {"width": 512, "height": 512},
                "1024x1024": {"width": 1024, "height": 1024},
                "1024x768": {"width": 1024, "height": 768},
                "768x1024": {"width": 768, "height": 1024},
                "1280x768": {"width": 1280, "height": 768},
                "768x1280": {"width": 768, "height": 1280},
            },
        },
        "z-image/turbo/text-to-image": {
            "id": "z-image/turbo/text-to-image",
            "name": "Z-Image Turbo Text-to-Image",
            "type": "text-to-image",
            "input": {
                "prompt": {"type": "string", "required": True, "description": "Input and processing limits depend on the model"},
                "negative_prompt": {"type": "string", "required": False, "default": ""},
                "width": {"type": "integer", "required": False, "default": 1024},
                "height": {"type": "integer", "required": False, "default": 1024},
                "num_images": {"type": "integer", "required": False, "default": 1, "min": 1, "max": 4},
                "num_inference_steps": {"type": "integer", "required": False, "default": 4, "min": 1, "max": 4},
                "guidance_scale": {"type": "number", "required": False, "default": 1.0, "min": 1.0, "max": 20.0},
                "seed": {"type": "integer", "required": False, "default": None},
                "output_format": {"type": "string", "required": False, "default": "png", "enum": ["png", "jpeg"]},
                "lora_id": {"type": "string", "required": False},
                "lora_scale": {"type": "number", "required": False, "default": 1.0, "min": 0.0, "max": 1.0},
            },
            "resolutions": {
                "512x512": {"width": 512, "height": 512},
                "1024x1024": {"width": 1024, "height": 1024},
                "1024x768": {"width": 1024, "height": 768},
                "768x1024": {"width": 768, "height": 1024},
                "1280x768": {"width": 1280, "height": 768},
                "768x1280": {"width": 768, "height": 1280},
            },
        },
        "z-image/turbo/text-to-image/lora": {
            "id": "z-image/turbo/text-to-image/lora",
            "name": "Z-Image Turbo Text-to-Image with LoRA",
            "type": "text-to-image",
            "input": {
                "prompt": {"type": "string", "required": True, "description": "Input and processing limits depend on the model"},
                "negative_prompt": {"type": "string", "required": False, "default": ""},
                "width": {"type": "integer", "required": False, "default": 1024},
                "height": {"type": "integer", "required": False, "default": 1024},
                "num_images": {"type": "integer", "required": False, "default": 1, "min": 1, "max": 4},
                "num_inference_steps": {"type": "integer", "required": False, "default": 4, "min": 1, "max": 4},
                "guidance_scale": {"type": "number", "required": False, "default": 1.0, "min": 1.0, "max": 20.0},
                "seed": {"type": "integer", "required": False, "default": None},
                "output_format": {"type": "string", "required": False, "default": "png", "enum": ["png", "jpeg"]},
                "lora_id": {"type": "string", "required": True},
                "lora_scale": {"type": "number", "required": False, "default": 1.0, "min": 0.0, "max": 1.0},
            },
            "resolutions": {
                "512x512": {"width": 512, "height": 512},
                "1024x1024": {"width": 1024, "height": 1024},
                "1024x768": {"width": 1024, "height": 768},
                "768x1024": {"width": 768, "height": 1024},
                "1280x768": {"width": 1280, "height": 768},
                "768x1280": {"width": 768, "height": 1280},
            },
        },
        "z-image/turbo/image-to-image": {
            "id": "z-image/turbo/image-to-image",
            "name": "Z-Image Turbo Image-to-Image",
            "type": "image-to-image",
            "input": {
                "prompt": {"type": "string", "required": True, "description": "Input and processing limits depend on the model"},
                "image_url": {"type": "string", "required": True, "description": "S3 key from upload-image"},
                "negative_prompt": {"type": "string", "required": False, "default": ""},
                "width": {"type": "integer", "required": False, "default": 1024},
                "height": {"type": "integer", "required": False, "default": 1024},
                "num_images": {"type": "integer", "required": False, "default": 1, "min": 1, "max": 4},
                "strength": {"type": "number", "required": False, "default": 0.7, "min": 0.0, "max": 1.0},
                "num_inference_steps": {"type": "integer", "required": False, "default": 4, "min": 1, "max": 4},
                "guidance_scale": {"type": "number", "required": False, "default": 1.0, "min": 1.0, "max": 20.0},
                "seed": {"type": "integer", "required": False, "default": None},
                "output_format": {"type": "string", "required": False, "default": "png", "enum": ["png", "jpeg"]},
                "lora_id": {"type": "string", "required": False},
                "lora_scale": {"type": "number", "required": False, "default": 1.0, "min": 0.0, "max": 1.0},
            },
            "resolutions": {
                "512x512": {"width": 512, "height": 512},
                "1024x1024": {"width": 1024, "height": 1024},
                "1024x768": {"width": 1024, "height": 768},
                "768x1024": {"width": 768, "height": 1024},
                "1280x768": {"width": 1280, "height": 768},
                "768x1280": {"width": 768, "height": 1280},
            },
        },
        "z-image/turbo/image-to-image/lora": {
            "id": "z-image/turbo/image-to-image/lora",
            "name": "Z-Image Turbo Image-to-Image with LoRA",
            "type": "image-to-image",
            "input": {
                "prompt": {"type": "string", "required": True, "description": "Input and processing limits depend on the model"},
                "image_url": {"type": "string", "required": True, "description": "S3 key from upload-image"},
                "negative_prompt": {"type": "string", "required": False, "default": ""},
                "width": {"type": "integer", "required": False, "default": 1024},
                "height": {"type": "integer", "required": False, "default": 1024},
                "num_images": {"type": "integer", "required": False, "default": 1, "min": 1, "max": 4},
                "strength": {"type": "number", "required": False, "default": 0.7, "min": 0.0, "max": 1.0},
                "num_inference_steps": {"type": "integer", "required": False, "default": 4, "min": 1, "max": 4},
                "guidance_scale": {"type": "number", "required": False, "default": 1.0, "min": 1.0, "max": 20.0},
                "seed": {"type": "integer", "required": False, "default": None},
                "output_format": {"type": "string", "required": False, "default": "png", "enum": ["png", "jpeg"]},
                "lora_id": {"type": "string", "required": True},
                "lora_scale": {"type": "number", "required": False, "default": 1.0, "min": 0.0, "max": 1.0},
            },
            "resolutions": {
                "512x512": {"width": 512, "height": 512},
                "1024x1024": {"width": 1024, "height": 1024},
                "1024x768": {"width": 1024, "height": 768},
                "768x1024": {"width": 768, "height": 1024},
                "1280x768": {"width": 1280, "height": 768},
                "768x1280": {"width": 768, "height": 1280},
            },
        },
        "minimax/h3/text-to-video": {
            "id": "minimax/h3/text-to-video",
            "name": "MiniMax H3 Text-to-Video",
            "type": "text-to-video",
            "billing": "per output second",
            "note": "Duration-based. Ignores num_frames / frames_per_second; output FPS is fixed at 24.",
            "input": {
                "prompt": {"type": "string", "required": True},
                "resolution_tier": {"type": "string", "required": False, "default": "480p", "enum": ["480p", "768p"]},
                "aspect_ratio": {"type": "string", "required": False, "default": "16:9", "enum": ["16:9", "4:3", "1:1", "3:4", "9:16"]},
                "duration": {"type": "number", "required": False, "default": 5, "min": 4, "max": 15},
                "seed": {"type": "integer", "required": False, "default": None},
            },
            "frame_sizes": {
                "480p": {"16:9": [832, 480], "4:3": [640, 480], "1:1": [480, 480], "3:4": [480, 640], "9:16": [480, 832]},
                "768p": {"16:9": [1344, 768], "4:3": [1024, 768], "1:1": [768, 768], "3:4": [768, 1024], "9:16": [768, 1344]},
            },
        },
        "minimax/h3/image-to-video": {
            "id": "minimax/h3/image-to-video",
            "name": "MiniMax H3 Image-to-Video",
            "type": "image-to-video",
            "billing": "per output second",
            "input": {
                "prompt": {"type": "string", "required": True},
                "image_url": {"type": "string", "required": True, "description": "S3 key from upload-image"},
                "end_image_url": {"type": "string", "required": False, "description": "Optional closing frame"},
                "resolution_tier": {"type": "string", "required": False, "default": "480p", "enum": ["480p", "768p"]},
                "aspect_ratio": {"type": "string", "required": False, "default": "16:9", "enum": ["16:9", "4:3", "1:1", "3:4", "9:16"]},
                "duration": {"type": "number", "required": False, "default": 5, "min": 4, "max": 15},
                "seed": {"type": "integer", "required": False, "default": None},
            },
        },
        "minimax/h3/text-to-video/turbo": {
            "id": "minimax/h3/text-to-video/turbo", "name": "MiniMax H3 Text-to-Video Turbo",
            "type": "text-to-video", "billing": "per output second",
            "note": "MiniMax H3 Turbo; 480p $0.006/s, 768p $0.012/s.",
        },
        "minimax/h3/image-to-video/turbo": {
            "id": "minimax/h3/image-to-video/turbo", "name": "MiniMax H3 Image-to-Video Turbo",
            "type": "image-to-video", "billing": "per output second",
            "note": "MiniMax H3 Turbo; 480p $0.006/s, 768p $0.012/s.",
        },
        "minimax/h3/reference-to-video": {
            "id": "minimax/h3/reference-to-video",
            "name": "MiniMax H3 Reference-to-Video (Ref2VA)",
            "type": "reference-to-video",
            "billing": "per output second PLUS per reference input - see pricing.minimax_h3_ref2va",
            "note": "Refer to references positionally in the prompt as <Picture 1>, <Picture 2>, ...",
            "input": {
                "prompt": {"type": "string", "required": True},
                "reference_image_urls": {"type": "array", "required": False},
                "reference_video_urls": {"type": "array", "required": False},
                "reference_audio_urls": {"type": "array", "required": False},
                "use_ref_video_audio": {"type": "boolean", "required": False, "default": False},
                "resolution_tier": {"type": "string", "required": False, "default": "480p", "enum": ["480p", "768p"]},
                "aspect_ratio": {"type": "string", "required": False, "default": "16:9", "enum": ["16:9", "4:3", "1:1", "3:4", "9:16"]},
                "duration": {"type": "number", "required": False, "default": 5, "min": 4, "max": 15},
                "seed": {"type": "integer", "required": False, "default": None},
            },
            "requires": "at least one of reference_image_urls / reference_video_urls",
            "reference_limits": {
                "480p": {"max_images": 5, "max_images_if_images_only": 9, "max_videos": 3, "max_audios": 3},
                "768p": {"max_images": 5, "max_images_if_images_only": 9, "max_videos": 3, "max_audios": 3},
                "max_reference_video_total_seconds": 15.1,
                "max_reference_video_fps": 24,
                "max_reference_audio_seconds": 10.0,
                "max_reference_image_edge": 2048,
                "max_reference_image_aspect_ratio": 4.0,
            },
        },
        "wan/v2.2-a14b/text-to-video/turbo": {
            "id": "wan/v2.2-a14b/text-to-video/turbo",
            "name": "Wan 2.2 Text-to-Video 14B (turbo)",
            "type": "text-to-video",
            "note": "Ignores num_inference_steps / guidance_scale. 1080p allows 153 frames (standard caps at 81).",
        },
        "wan/v2.2-a14b/image-to-video/turbo": {
            "id": "wan/v2.2-a14b/image-to-video/turbo",
            "name": "Wan 2.2 Image-to-Video 14B (turbo)",
            "type": "image-to-video",
            "note": "Ignores num_inference_steps / guidance_scale.",
        },
        "ltx-video/v2.3/image-audio-to-video": {
            "id": "ltx-video/v2.3/image-audio-to-video",
            "name": "LTX Video 2.3 Image and Optional Audio to Video",
            "type": "image-audio-to-video",
            "input": {
                "prompt": {"type": "string", "required": True},
                "image_url": {"type": "string", "required": True},
                "audio_url": {"type": "string", "required": False},
                "num_frames": {"type": "integer", "required": False, "default": 121},
                "frames_per_second": {"type": "integer", "required": False, "default": 24},
            },
            "note": "Per frame: 480p USD 0.0008, 720p USD 0.0012. No Wan frame alignment. 1080p quote needs confirmation. See references/api.md.",
        },
        "openai/gpt-image-2/text-to-image": {
            "id": "openai/gpt-image-2/text-to-image",
            "name": "GPT Image 2 Text-to-Image",
            "type": "text-to-image",
            "note": ("Sizes: 1024x1024 | 1920x1072 / 1072x1920 (1080p) | 2560x1440 / 1440x2560 (2K); "
                     "other sizes are rejected with 400. Always returns exactly 1 image "
                     "(num_images ignored); also ignores num_inference_steps / guidance_scale / output_format."),
            "input": {
                "prompt": {"type": "string", "required": True},
                "width": {"type": "integer", "required": False, "default": 1024},
                "height": {"type": "integer", "required": False, "default": 1024},
                "seed": {"type": "integer", "required": False},
            },
            # Mirrors the gateway's accepted resolution list for this model; a size that is
            # not listed here is rejected with 400. 1536x1024 / 1024x1536 are intentionally
            # absent: the provider honours them inconsistently and may silently return a
            # different size. 4K is not open yet. 1080 is not a multiple of 16 (the provider
            # requires multiples of 16), hence 1072.
            "resolutions": [[1024, 1024], [1920, 1072], [1072, 1920], [2560, 1440], [1440, 2560]],
        },
        "flux2/dev/text-to-image": {
            "id": "flux2/dev/text-to-image",
            "name": "FLUX.2-dev Text-to-Image",
            "type": "text-to-image",
            "note": "Own resolution whitelist; always returns exactly 1 image (num_images and steps are ignored).",
            "input": {
                "prompt": {"type": "string", "required": True},
                "width": {"type": "integer", "required": False, "default": 1024},
                "height": {"type": "integer", "required": False, "default": 1024},
                "seed": {"type": "integer", "required": False},
            },
            "resolutions": [[2048, 1536], [1536, 2048], [2048, 1152], [1152, 2048], [2048, 2048], [1024, 1024]],
        },
        "flux2/dev/image-edit": {
            "id": "flux2/dev/image-edit",
            "name": "FLUX.2-dev Image Edit",
            "type": "image-edit",
            "note": "Always returns exactly 1 image.",
            "input": {
                "prompt": {"type": "string", "required": True},
                "image_url": {"type": "string", "required": True},
                "width": {"type": "integer", "required": False, "default": 1024},
                "height": {"type": "integer", "required": False, "default": 1024},
            },
            "resolutions": [[2048, 1536], [1536, 2048], [2048, 1152], [1152, 2048], [2048, 2048], [1024, 1024]],
        },
        "qwen3-tts/text-to-speech/1.7b": {
            "id": "qwen3-tts/text-to-speech/1.7b",
            "name": "Qwen3-TTS CustomVoice",
            "type": "text-to-speech",
            "note": "Keys off `text`, NOT `prompt`. Use the submit-tts command.",
            "input": {
                "text": {"type": "string", "required": True, "max_length": 500},
                "speaker": {"type": "string", "required": False, "default": "Sohee"},
                "language": {"type": "string", "required": False, "default": "Chinese"},
                "seed": {"type": "integer", "required": False, "description": "-1 = random"},
                "temperature": {"type": "number", "required": False, "default": 0.9, "min": 0.0, "max": 2.0},
                "top_p": {"type": "number", "required": False, "default": 1.0},
                "top_k": {"type": "integer", "required": False, "default": 50, "min": 1, "max": 200},
                "repetition_penalty": {"type": "number", "required": False, "default": 1.05, "min": 1.0, "max": 2.0},
            },
        },
    },
    "llm": {
        "qwen3.8-27b": {
            "id": "qwen3.8-27b", "name": "Qwen3.8 27B", "type": "llm",
            "endpoint": "POST /api/v1/chat/completions (OpenAI-compatible, synchronous or streaming)",
            "input": "text + up to 2 images per request (https or data:image/png|jpeg|webp;base64, <= 4 MB each)",
            "context_window": "48K tokens", "max_tokens": {"default": 1024, "min": 1, "max": 8192},
            "features": ["streaming", "json_mode", "tool_calling", "enable_thinking (default off)"],
            "billing": "per token: USD 0.2125 / 1M input, USD 1.275 / 1M output (2.125 / 12.75 credits)",
            "rate_limit": "60 requests/min per API key",
        },
    },
    "frame_alignment": {
        "formula": "valid_frames = 1 + 4*k where k >= 1",
        "examples": [5, 9, 13, 17, 21, 25, 29, 33, 37, 41, 45, 49, 53, 57, 61, 65, 69, 73, 77, 81],
    },
    "pricing": {
        "inference": {
            "480p": {"per_frame_usd": 0.0009375, "per_frame_credits": 0.009375},
            "720p": {"per_frame_usd": 0.001875, "per_frame_credits": 0.01875},
            "1080p": {"per_frame_usd": 0.0025, "per_frame_credits": 0.025},
        },
        "s2v": {
            "480p": {"per_frame_usd": 0.0009375, "per_frame_credits": 0.009375},
            "512p": {"per_frame_usd": 0.0013125, "per_frame_credits": 0.013125},
            "720p": {"per_frame_usd": 0.001875, "per_frame_credits": 0.01875},
        },
        "animate": {
            "480p": {"per_frame_usd": 0.00125, "per_frame_credits": 0.0125},
            "512p": {"per_frame_usd": 0.00175, "per_frame_credits": 0.0175},
            "720p": {"per_frame_usd": 0.0025, "per_frame_credits": 0.025},
        },
        "lora_multiplier": 1.2,
        "minimax_h3": {
            "480p": {"per_second_usd": 0.0045, "per_second_credits": 0.045},
            "768p": {"per_second_usd": 0.012, "per_second_credits": 0.12},
        },
        "minimax_h3_ref2va": {
            "formula": "duration * base_rate + max(0, images - 5) * 0.0075 + ref_video_seconds * base_rate  (audio free)",
            "480p": {"base_per_second_usd": 0.0045, "reference_video_per_second_usd": 0.0045},
            "768p": {"base_per_second_usd": 0.012, "reference_video_per_second_usd": 0.012},
            "reference_image_usd": 0.0075,
            "reference_image_free_count": 5,
            "reference_audio_usd": 0.0,
            "note": "Same base rate as plain H3 T2V/I2V since 2026-09-10.",
        },
        "minimax_h3_turbo": {
            "480p": {"per_second_usd": 0.006, "per_second_credits": 0.06},
            "768p": {"per_second_usd": 0.012, "per_second_credits": 0.12},
        },
        "minimax_h3_ref2va_turbo": {
            "formula": "duration * turbo_base_rate + max(0, images - 5) * 0.0025 + ref_video_seconds * turbo_base_rate (audio free)",
            "480p": {"base_per_second_usd": 0.006, "reference_video_per_second_usd": 0.006},
            "768p": {"base_per_second_usd": 0.012, "reference_video_per_second_usd": 0.012},
            "reference_image_usd": 0.0025, "reference_image_free_count": 5, "reference_audio_usd": 0.0,
        },
        "audio": {"qwen_tts_per_char_usd": 3e-05, "min_charge_usd": 0.003},
        "image": {
            "gpt_image_2_t2i": {"per_image_usd": 0.03, "per_image_credits": 0.3},
            "flux2_t2i": {"per_image_usd": 0.006, "per_image_credits": 0.06},
            "flux2_image_edit": {"per_image_usd": 0.012, "per_image_credits": 0.12},
            "qwen": {"per_image_usd": 0.015, "per_image_credits": 0.15},
            "qwen_lora": {"per_image_usd": 0.018, "per_image_credits": 0.18},
            "qwen_image_edit": {"per_image_usd": 0.003, "per_image_credits": 0.03},
            "qwen_image_edit_turbo": {"per_image_usd": 0.005, "per_image_credits": 0.05},
            "z_turbo": {"per_image_usd": 0.0025, "per_image_credits": 0.025},
            "z_turbo_lora": {"per_image_usd": 0.003, "per_image_credits": 0.03},
        },
        "credits_per_usd": 10,
        "note": "Model API prices: GET /api/v1/pricing/config. Image Studio prices: studio-pricing. Static estimates may change.",
    },
    "limits": {
        "max_loras_per_user": 20,
        "max_api_keys_per_user": 10,
        # Enforced against the COMBINED size of high_noise + low_noise, not per file:
        # exceeding it returns HTTP 413 "LoRA files too large (N MB). Maximum allowed: 2048 MB."
        "max_lora_upload_total_mb": 2048,
        "uploaded_lora_expiry_days": 1,
        "saved_lora_expiry_days": 7,
        "max_image_file_size_mb": 20,
        "rate_limit_requests_per_minute": 1000,
    },
}


# ─── Image Studio catalog ──────────────────────────────────────────────────
# Image Studio is a separate product surface (e-commerce product/model photography,
# not the video/LoRA pipeline above) reached through the SAME gateway + API key,
# under the `/api/v1/image-studio` prefix. All endpoints are async: POST returns
# {request_id, status:"pending"}, poll GET /jobs/{request_id} until status is "done"/"error"/"cancelled".
# Image-generation endpoints are billed per successful output image; the
# analyze endpoints use a fixed model and a daily free quota before billing kicks in.
# Real-time prices: call `studio-pricing` (GET /pricing) — do not hardcode from here.
IMAGE_STUDIO = {
    "base_path": "/api/v1/image-studio",
    "billing": {
        "generation": "Flat per-image credit rate (same for every generation endpoint below), returned live by GET /pricing as `per_image_credits`. Partial success (e.g. 3 of 5 images generated) is billed only for the successes; the rest is auto-refunded.",
        "analyze": "First `analyze_daily_free_quota` analyze calls per user per day are free (shared across agent/product/model analyze); beyond that, `per_analyze_credits` per call (from GET /pricing).",
    },
    "endpoints": {
        # ── Analyze (freemium, shared quota) ──
        "agent/analyze":            {"method": "POST", "path": "/agent/analyze", "billing": "analyze", "fields": {"image_url": "required", "prompt": "optional", "language": "optional, default zh"}},
        "product/analyze":          {"method": "POST", "path": "/product/analyze", "billing": "analyze", "fields": {"image_url": "required", "prompt": "optional", "language": "optional, default zh"}},
        "model/analyze":            {"method": "POST", "path": "/model/analyze", "billing": "analyze", "fields": {"image_url": "required", "prompt": "optional", "language": "optional, default zh"}},
        "product/reference/analyze": {"method": "POST", "path": "/product/reference/analyze", "billing": "free", "fields": {"source_type": "optional: web_url|image_url, default web_url", "url": "required if source_type=web_url", "image_url": "required if source_type=image_url", "prompt": "optional"}},
        # ── Product image generation ──
        "product/suite":            {"method": "POST", "path": "/product/suite", "billing": "generation", "model_selectable": True, "fields": {"product_image_url": "required", "layout_types": "optional list[str]", "count_per_type": "optional int, default 1", "custom_suggestions": "optional list", "product_info": "optional str", "same_style_reference": "optional dict", "brand_config": "optional dict", "aspect_ratio": "optional: 1:1|3:4|4:3|9:16|16:9", "gen_language": "optional", "model": "optional"}},
        "product/scene-compose":    {"method": "POST", "path": "/product/scene-compose", "billing": "generation", "model_selectable": True, "fields": {"composite_image_url": "required", "reference_image_url": "required", "similarity": "optional, default strong", "prompt": "optional", "count": "optional int 1-20, default 2", "aspect_ratio": "optional", "model": "optional"}},
        "product/scene-variation":  {"method": "POST", "path": "/product/scene-variation", "billing": "generation", "model_selectable": True, "fields": {"product_image_url": "required", "count": "optional int 1-20, default 2", "style": "optional: smart|realistic|minimal|studio|outdoor|lifestyle", "scene_description": "optional", "aspect_ratio": "optional", "model": "optional"}},
        "product/remove-bg":        {"method": "POST", "path": "/product/remove-bg", "billing": "generation", "model_selectable": True, "fields": {"image_url": "required", "count": "optional int, max 20, default 1", "aspect_ratio": "optional", "model": "optional"}},
        "product/replace":          {"method": "POST", "path": "/product/replace", "billing": "generation", "model_selectable": True, "fields": {"image_url": "required (scene)", "new_product_url": "optional (product to composite in)", "count": "optional int 1-4, default 1", "prompt": "optional", "model": "optional"}},
        "product/inpaint":          {"method": "POST", "path": "/product/inpaint", "billing": "generation", "model_selectable": True, "fields": {"image_url": "required", "mask_url": "required", "prompt": "optional fill description", "aspect_ratio": "optional", "count": "optional int, max 20", "model": "optional"}},
        "product/erase":            {"method": "POST", "path": "/product/erase", "billing": "generation", "model_selectable": True, "fields": {"image_url": "required", "mask_url": "required", "prompt": "optional removal note", "aspect_ratio": "optional", "count": "optional int, max 20", "model": "optional"}},
        "product/handheld":         {"method": "POST", "path": "/product/handheld", "billing": "generation", "model_selectable": True, "fields": {"image_url": "required", "pose_id": "optional: front_single_lift|side_single_grip|both_hands_cup|usage_scene|gift_display|outdoor_handheld", "prompt": "optional override", "aspect_ratio": "optional", "count": "optional int, max 20", "model": "optional"}},
        "product/translate":        {"method": "POST", "path": "/product/translate", "billing": "generation", "model_selectable": True, "fields": {"image_url": "required", "source_lang": "optional, default auto", "target_langs": "optional list[str], default [en] — one output image per language", "aspect_ratio": "optional, default source (keep input size)", "model": "optional"}},
        "product/outpaint":         {"method": "POST", "path": "/product/outpaint", "billing": "generation", "model_selectable": True, "fields": {"image_url": "required", "expand": "optional dict {top,bottom,left,right} in px, default all 0", "prompt": "optional expansion note", "model": "optional"}},
        "product/recolor":          {"method": "POST", "path": "/product/recolor", "billing": "generation", "model_selectable": True, "fields": {"image_url": "required", "target_color": "optional", "region": "optional, default the product", "prompt": "optional", "aspect_ratio": "optional", "count": "optional int, max 20", "model": "optional"}},
        "product/enhance":          {"method": "POST", "path": "/product/enhance", "billing": "generation", "model_selectable": True, "fields": {"image_url": "required", "enhance_type": "optional: smart|product|color|pattern|hands", "prompt": "optional", "aspect_ratio": "optional", "model": "optional"}},
        "product/upscale":          {"method": "POST", "path": "/product/upscale", "billing": "generation", "model_selectable": True, "fields": {"image_url": "required", "prompt": "optional", "model": "optional"}},
        # ── Model (clothing/photography) image generation ──
        "model/clothing-suite":     {"method": "POST", "path": "/model/clothing-suite", "billing": "generation", "model_selectable": True, "fields": {"clothing_image_urls": "required list[str], up to 5 used", "main_image_types": "optional dict {model_shot|grass_shot|selling_point|size_chart: count}", "aplus_types": "optional dict {standard_aplus|mobile_aplus|basic_aplus|custom_ratio: count}", "product_info": "optional", "brand_config": "optional dict", "same_style_reference": "optional dict", "aspect_ratio": "optional, default 3:4", "gen_language": "optional", "model": "optional"}},
        "model/real-model-swap":    {"method": "POST", "path": "/model/real-model-swap", "billing": "generation", "model_selectable": True, "fields": {"garment_image_urls": "required list[str]", "count": "optional int 1-20, default 2", "model_attrs": "optional dict {gender,age_group,ethnicity,skin_tone,hair_color}", "scene_id": "optional", "aspect_ratio": "optional", "model": "optional"}},
        "model/mannequin-swap":     {"method": "POST", "path": "/model/mannequin-swap", "billing": "generation", "model_selectable": True, "fields": {"garment_image_urls": "required list[str]", "count": "optional int 1-20, default 2", "model_attrs": "optional dict", "expression": "optional, default smile", "custom_prompt": "optional, max 500 chars", "aspect_ratio": "optional", "model": "optional"}},
        "model/model-scene-swap":   {"method": "POST", "path": "/model/model-scene-swap", "billing": "generation", "model_selectable": True, "fields": {"source_image_urls": "required list[str]", "count": "optional int 1-20, default 2", "scene_id": "optional", "scene_description": "optional", "scene_image_url": "optional (image-to-image scene reference)", "aspect_ratio": "optional", "model": "optional"}},
        "model/ai-outfit":          {"method": "POST", "path": "/model/ai-outfit", "billing": "generation", "model_selectable": True, "fields": {"clothing_image_urls": "required list[str], first 2 used", "count": "optional int 1-20, default 2", "model_attrs": "optional dict — REQUIRED for accurate results, not inferred from image alone", "aspect_ratio": "optional", "model": "optional"}},
        "model/pose-variation":     {"method": "POST", "path": "/model/pose-variation", "billing": "generation", "model_selectable": True, "fields": {"source_image_urls": "required list[str]", "pose_ids": "optional list[str], up to 3", "custom_pose_url": "optional reference pose image", "count": "optional int, per-pose count, default 1", "aspect_ratio": "optional", "model": "optional"}},
        "model/ai-wearable":        {"method": "POST", "path": "/model/ai-wearable", "billing": "generation", "model_selectable": True, "fields": {"accessory_image_url": "required", "count": "optional int 1-20, default 2", "wearable_type": "optional, default accessory", "model_attrs": "optional dict", "aspect_ratio": "optional", "model": "optional"}},
        # ── Job / account ──
        "jobs":                     {"method": "GET", "path": "/jobs/{request_id}", "billing": "free"},
        "cancel":                   {"method": "POST", "path": "/jobs/{request_id}/cancel", "billing": "free"},
        "pricing":                  {"method": "GET", "path": "/pricing", "billing": "free"},
        "my-works":                 {"method": "GET", "path": "/my-works", "billing": "free", "fields": {"task_type": "optional filter", "date_from": "optional YYYY-MM-DD", "date_to": "optional YYYY-MM-DD", "limit": "optional 1-100, default 20", "offset": "optional, default 0"}},
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


def _parse_json_arg(raw, flag_name, expected_type):
    """Parse a --flag JSON string argument; None passes through untouched."""
    if raw is None:
        return None
    try:
        value = json.loads(raw)
    except json.JSONDecodeError:
        _error_out(f"{flag_name} must be valid JSON")
    if not isinstance(value, expected_type):
        _error_out(f"{flag_name} must be a JSON {expected_type}")
    return value


def _chat_image_part(ref):
    """Turn an https URL, a data URL, or a local image path into an image_url part."""
    if ref.startswith(("https://", "data:image/")):
        return {"type": "image_url", "image_url": {"url": ref}}
    path = Path(ref)
    if not path.is_file():
        _error_out(f"--image must be an https:// URL, a data:image URL, or an existing file: {ref}")
    mime = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
            ".webp": "image/webp"}.get(path.suffix.lower())
    if not mime:
        _error_out(f"Unsupported image type {path.suffix!r}; use PNG, JPEG or WebP")
    data = path.read_bytes()
    if len(data) > CHAT_MAX_IMAGE_BYTES:
        _error_out(f"{ref} is larger than 4 MB")
    import base64
    return {"type": "image_url",
            "image_url": {"url": f"data:{mime};base64,{base64.b64encode(data).decode()}"}}


# ─── PhosorClient ──────────────────────────────────────────────────────────

class PhosorClient:
    """Core API wrapper — stdlib-only HTTP via urllib."""

    def __init__(self, base_url=None, api_key=None):
        resolved = (base_url or os.environ.get("PHOSOR_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
        if resolved != DEFAULT_BASE_URL:
            _error_out("Only https://phosor.ai is supported")
        self.base_url = resolved
        self.api_key = api_key or self._resolve_api_key()

    @staticmethod
    def _resolve_api_key():
        key = os.environ.get("PHOSOR_API_KEY")
        if key:
            return key.strip()
        # Fallback: try reading from TOOLS.md in workspace
        tools_md = WORKSPACE_DIR / "TOOLS.md"
        if tools_md.exists():
            for line in tools_md.read_text().splitlines():
                if "PHOSOR_API_KEY" in line and "=" in line:
                    candidate = line.split("=", 1)[1].strip().strip('"').strip("'")
                    # Basic validation: reject suspiciously long or malformed keys
                    if candidate and len(candidate) <= 256 and re.match(r'^[A-Za-z0-9_\-\.]+$', candidate):
                        return candidate
        return None

    def _request(self, method, path, json_data=None, params=None, raise_http=False):
        """Make an authenticated HTTP request. Returns parsed JSON.

        With `raise_http=True` an HTTPError is re-raised instead of going through
        `_error_out` and exiting -- for callers that branch on the status code
        (check_key reports 401/403 as "invalid" rather than printing an error and
        exiting). Defaults to False; every other caller keeps its behaviour.
        """
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
                return _decode_response(raw)
        except HTTPError as e:
            if raise_http:
                raise
            _http_error(e)
        except (URLError, OSError, UnicodeError, ValueError, HTTPException):
            _error_out("Request failed or response was invalid; submission acceptance may be unknown. Check history before resubmitting")

    @staticmethod
    def _sanitize_filename(name):
        """Remove characters unsafe for Content-Disposition filename."""
        return re.sub(r'["\r\n\\]', '_', name)

    def _send_files(self, path, files, fields=None, max_bytes=None):
        """Build multipart data on disk and send bounded chunks."""
        boundary = "----PhosorBoundary" + uuid.uuid4().hex
        try:
            total = sum(Path(file).stat().st_size for _, file in files)
            if max_bytes is not None and total > max_bytes:
                _error_out("Upload exceeds the supported total file size")
            with tempfile.TemporaryFile() as body:
                copied = 0
                for field, file in files:
                    file = Path(file)
                    filename = self._sanitize_filename(file.name)
                    content_type = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp"}.get(file.suffix.lower(), "application/octet-stream")
                    body.write((f'--{boundary}\r\nContent-Disposition: form-data; name="{field}"; '
                                f'filename="{filename}"\r\nContent-Type: {content_type}\r\n\r\n').encode())
                    with file.open("rb") as source:
                        while True:
                            chunk = source.read(1024 * 1024)
                            if not chunk:
                                break
                            copied += len(chunk)
                            if max_bytes is not None and copied > max_bytes:
                                _error_out("Upload exceeds the supported total file size")
                            body.write(chunk)
                    body.write(b"\r\n")
                for name, value in (fields or {}).items():
                    body.write((f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"'
                                f'\r\n\r\n{value}\r\n').encode())
                body.write(f"--{boundary}--\r\n".encode())
                length = body.tell()
                body.seek(0)
                headers = {"Content-Type": "multipart/form-data; boundary=" + boundary,
                           "Content-Length": str(length)}
                if self.api_key:
                    headers["X-API-Key"] = self.api_key
                request = Request(self.base_url + path,
                                  data=iter(lambda: body.read(1024 * 1024), b""),
                                  headers=headers, method="POST")
                with urlopen(request, timeout=600) as response:
                    return _decode_response(response.read().decode("utf-8"))
        except HTTPError as error:
            _http_error(error)
        except (OSError, URLError, ValueError, UnicodeError, HTTPException):
            _error_out("Upload failed; check files and query task history before retrying")

    def _upload_multipart(self, path, file_path, field_name="image"):
        return self._send_files(path, [(field_name, file_path)])

    # ── Inference ───────────────────────────────────────────────────────────

    def check_key(self):
        """Validate the API key using an authenticated, read-only request."""
        return self._request("GET", "/api/v1/loras", params={"limit": 1}, raise_http=True)

    def submit(self, prompt, **kwargs):
        """Submit an inference job (T2V, I2V, T2I, or I2I)."""
        payload = {"prompt": prompt}
        for k in _SUBMIT_FIELDS:
            if kwargs.get(k) is not None:
                payload[k] = kwargs[k]
        if str(payload.get("model", "")).startswith("minimax/h3/") and payload.get("model") != "minimax/h3/text-to-image":
            if "negative_prompt" in payload:
                raise ValueError("H3 does not support negative_prompt; describe constraints in prompt")
            if type(payload.get("avoid_model_limitations", False)) is not bool:
                raise ValueError("avoid_model_limitations must be a boolean")
            if type(payload.get("unrestricted_enhancement", False)) is not bool:
                raise ValueError("unrestricted_enhancement must be a boolean")
            for field in ("num_inference_steps", "guidance_scale", "lora_id", "lora_scale", "loras"):
                payload.pop(field, None)
        if payload.get("model") == "minimax/h3/text-to-image":
            unsupported = set(payload) - {"prompt", "model", "width", "height", "seed", "output_format"}
            if unsupported:
                raise ValueError("H3 Image does not support: " + ", ".join(sorted(unsupported)))
        return self._request("POST", "/api/v1/inference/submit", json_data=payload)

    def submit_tts(self, text, **kwargs):
        """Submit a Qwen3-TTS job.

        Same endpoint as submit(), but TTS keys off `text` rather than `prompt` —
        sending a prompt here produces nothing.
        """
        payload = {"model": kwargs.pop("model", None) or "qwen3-tts/text-to-speech/1.7b",
                   "text": text}
        for k in ("speaker", "language", "seed", "temperature", "top_p", "top_k",
                  "repetition_penalty"):
            if kwargs.get(k) is not None:
                payload[k] = kwargs[k]
        return self._request("POST", "/api/v1/inference/submit", json_data=payload)

    def chat(self, body, on_delta=None):
        """POST /api/v1/chat/completions (OpenAI-compatible).

        Non-streaming: returns the parsed response.
        Streaming (body["stream"] is True): reads the SSE stream, calls
        on_delta(kind, text) for each "content" / "reasoning" fragment, and returns
        an assembled response with the same shape as a non-streaming one,
        including the final `usage` (with `credits_charged`).
        """
        payload = {k: v for k, v in body.items() if k in _CHAT_FIELDS and v is not None}
        if not body.get("stream"):
            return self._request("POST", "/api/v1/chat/completions", json_data=payload)

        headers = {"Content-Type": "application/json", "Accept": "text/event-stream"}
        if self.api_key:
            headers["X-API-Key"] = self.api_key
        req = Request(f"{self.base_url}/api/v1/chat/completions",
                      data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
        out = {"id": None, "object": "chat.completion", "model": payload.get("model"),
               "choices": [{"index": 0, "message": {"role": "assistant", "content": ""},
                            "finish_reason": None}],
               "usage": None, "stream_complete": False}
        msg = out["choices"][0]["message"]
        reasoning, tool_calls = [], {}
        try:
            with urlopen(req, timeout=600) as resp:
                for raw in resp:
                    line = raw.decode("utf-8", errors="replace").strip()
                    if not line.startswith("data:"):
                        continue
                    data = line[5:].strip()
                    if data == "[DONE]":
                        out["stream_complete"] = bool(out["choices"][0]["finish_reason"])
                        if not out["stream_complete"]:
                            out["error"] = {"message": "Stream ended without a completion reason"}
                        break
                    try:
                        chunk = json.loads(data)
                    except json.JSONDecodeError:
                        out["error"] = {"message": "Invalid stream data"}
                        break
                    if not isinstance(chunk, dict):
                        out["error"] = {"message": "Invalid stream event"}
                        break
                    if "error" in chunk:
                        out["error"] = {"message": "Stream failed"}
                        continue
                    out["id"] = chunk.get("id") or out["id"]
                    if chunk.get("usage"):
                        out["usage"] = chunk["usage"]
                    if not _valid_stream_chunk(chunk):
                        out["error"] = {"message": "Invalid stream event fields"}
                        break
                    for ch in chunk.get("choices") or []:
                        delta = ch.get("delta") or {}
                        if delta.get("reasoning_content"):
                            reasoning.append(delta["reasoning_content"])
                            if on_delta:
                                on_delta("reasoning", delta["reasoning_content"])
                        if delta.get("content"):
                            msg["content"] += delta["content"]
                            if on_delta:
                                on_delta("content", delta["content"])
                        for tc in delta.get("tool_calls") or []:
                            slot = tool_calls.setdefault(tc.get("index", 0), {
                                "id": None, "type": "function",
                                "function": {"name": "", "arguments": ""}})
                            slot["id"] = tc.get("id") or slot["id"]
                            fn = tc.get("function") or {}
                            slot["function"]["name"] += fn.get("name") or ""
                            slot["function"]["arguments"] += fn.get("arguments") or ""
                        if ch.get("finish_reason"):
                            out["choices"][0]["finish_reason"] = ch["finish_reason"]
        except HTTPError as e:
            _http_error(e)
        except (URLError, OSError, UnicodeError, ValueError, HTTPException):
            _error_out("Request failed or response was invalid; submission acceptance may be unknown. Check history before resubmitting")
        if reasoning:
            msg["reasoning_content"] = "".join(reasoning)
        if tool_calls:
            msg["tool_calls"] = [tool_calls[i] for i in sorted(tool_calls)]
        return out

    def status(self, request_id):
        """Get job status."""
        return self._request("GET", f"/api/v1/inference/status/{request_id}")

    def result(self, request_id):
        """Get job result (video URL or image URL)."""
        return self._request("GET", f"/api/v1/inference/result/{request_id}")

    def history(self, limit=50):
        """Get job history for authenticated user."""
        return self._request("GET", "/api/v1/inference/history", params={"limit": limit})

    # ── Storage: Image ──────────────────────────────────────────────────────

    def upload_image(self, file_path):
        """Upload a local image file for I2V."""
        return self._upload_multipart("/api/v1/storage/image/upload", file_path, field_name="image")

    def import_image(self, url, filename=None):
        """Import an image from a remote URL."""
        payload = {"url": url}
        if filename:
            payload["filename"] = filename
        return self._request("POST", "/api/v1/storage/image/import", json_data=payload)

    # ── Storage: LoRA ───────────────────────────────────────────────────────

    def upload_lora(self, high_noise_path, low_noise_path, name=None):
        """Upload two LoRA files with bounded memory and a combined size limit."""
        return self._send_files("/api/v1/storage/lora/upload",
                                [("high_noise_file", high_noise_path), ("low_noise_file", low_noise_path)],
                                {"name": name} if name else None,
                                max_bytes=2048 * 1024 * 1024)

    def import_lora(self, high_noise_url, low_noise_url=None, name=None):
        """Import a LoRA model from remote URLs (HTTPS .safetensors).
        Video LoRA: two files (high_noise_url + low_noise_url).
        Image LoRA: single file (high_noise_url only).
        """
        payload = {
            "high_noise_url": high_noise_url,
        }
        if low_noise_url:
            payload["low_noise_url"] = low_noise_url
        if name:
            payload["name"] = name
        return self._request("POST", "/api/v1/storage/lora/import", json_data=payload)

    def list_models(self):
        """List available models."""
        return self._request("GET", "/api/v1/models")

    # ── LoRA Management ─────────────────────────────────────────────────────

    def loras(self, limit=50, offset=0):
        """List LoRA models."""
        return self._request("GET", "/api/v1/loras", params={"limit": limit, "offset": offset})

    def lora_status(self, lora_id):
        """Get LoRA upload/import status."""
        return self._request("GET", f"/api/v1/loras/{lora_id}/status")

    def save_lora(self, lora_id, name=None):
        """Activate a LoRA, extending its expiry to 7 days (status: trained → ready).

        `trained` is just the wire value for "finished processing" - it is set for
        uploaded and imported LoRAs alike.
        """
        payload = {}
        if name:
            payload["name"] = name
        return self._request("POST", f"/api/v1/loras/{lora_id}/save", json_data=payload)

    def delete_lora(self, lora_id):
        """Delete a LoRA model (soft delete)."""
        return self._request("DELETE", f"/api/v1/loras/{lora_id}")

    # ── Utility ─────────────────────────────────────────────────────────────

    # ── Image Studio (product/model photography — separate product surface) ──

    IMAGE_STUDIO_PREFIX = "/api/v1/image-studio"

    def studio_call(self, method, path, json_data=None, params=None):
        """Generic Image Studio call for any endpoint in IMAGE_STUDIO['endpoints'].
        `path` is relative to /api/v1/image-studio, e.g. '/product/remove-bg'."""
        if not path.startswith("/"):
            path = "/" + path
        return self._request(method.upper(), f"{self.IMAGE_STUDIO_PREFIX}{path}", json_data=json_data, params=params)

    def studio_analyze(self, target, image_url, prompt=None, url=None, language=None):
        """target: 'agent' | 'product' | 'model' | 'reference'."""
        path_map = {
            "agent": "/agent/analyze",
            "product": "/product/analyze",
            "model": "/model/analyze",
            "reference": "/product/reference/analyze",
        }
        if target not in path_map:
            _error_out(f"--target must be one of {list(path_map)}")
        payload = {}
        if target == "reference":
            payload["source_type"] = "image_url" if image_url else "web_url"
            if image_url:
                payload["image_url"] = image_url
            if url:
                payload["url"] = url
        else:
            if image_url:
                payload["image_url"] = image_url
        if prompt:
            payload["prompt"] = prompt
        if language:
            payload["language"] = language
        return self.studio_call("POST", path_map[target], json_data=payload)

    def studio_suite(self, product_image_url, layout_types=None, count_per_type=None,
                      custom_suggestions=None, product_info=None, aspect_ratio=None,
                      gen_language=None, model=None, same_style_reference=None,
                      layout_template_ids=None, layout_random_count=None, image_urls=None):
        payload = {"product_image_url": product_image_url}
        if image_urls:
            payload["image_urls"] = image_urls
        if layout_types:
            payload["layout_types"] = layout_types
        if count_per_type is not None:
            payload["count_per_type"] = count_per_type
        if custom_suggestions:
            payload["custom_suggestions"] = custom_suggestions
        # Select layouts by their public template IDs.
        if layout_template_ids:
            payload["layout_template_ids"] = layout_template_ids
        if layout_random_count:
            payload["layout_random_count"] = layout_random_count
        if product_info:
            payload["product_info"] = product_info
        if aspect_ratio:
            payload["aspect_ratio"] = aspect_ratio
        if gen_language:
            payload["gen_language"] = gen_language
        if model:
            payload["model"] = model
        if same_style_reference:
            payload["same_style_reference"] = same_style_reference
        return self.studio_call("POST", "/product/suite", json_data=payload)

    def studio_layouts(self, module="product", type_filter=None):
        """List public layout templates; no authentication is needed."""
        path = f"/asset-library/image-studio/references/layouts/{module}/templates.json"
        try:
            with urlopen(Request(self.base_url + path, headers={"Accept": "application/json"}), timeout=60) as resp:
                data = json.loads(resp.read())
            if not isinstance(data, list) or any(not isinstance(t, dict) for t in data):
                raise ValueError("Invalid layout response")
            return [t for t in data if t.get("type") == type_filter] if type_filter else data
        except HTTPError as exc:
            _http_error(exc)
        except (URLError, ValueError, OSError, HTTPException):
            _error_out("Could not fetch layout templates")

    def layout_templates_to_suggestions(self, template_ids, module="product"):
        """Expand chosen layout template ids into custom_suggestions entries, exactly
        how the UI sends a manual template selection to /product/suite."""
        LABELS = {"selling_point": "Selling point", "aplus": "Premium A+", "white_bg": "White background",
                  "scene": "Scene", "closeup": "Close-up", "size_chart": "Size chart"}
        tpls = {t.get("id"): t for t in self.studio_layouts(module)}
        cs = []
        for tid in template_ids:
            t = tpls.get(tid)
            if not t:
                _error_out(f"layout template id not found in {module} library: {tid}")
            cs.append({"id": tid, "label": LABELS.get(t.get("type"), t.get("type") or "Image"),
                       "desc": t.get("layout_prompt"), "layout_prompt": t.get("layout_prompt"),
                       "template_file": t.get("file"), "template_name": t.get("name"),
                       "type": "layout_composite", "width": 1024, "height": 1024})
        return cs

    def studio_clothing_suite(self, clothing_image_urls, main_image_types=None, aplus_types=None,
                               product_info=None, brand_config=None, aspect_ratio=None,
                               gen_language=None, model=None, same_style_reference=None):
        payload = {"clothing_image_urls": clothing_image_urls}
        if main_image_types:
            payload["main_image_types"] = main_image_types
        if aplus_types:
            payload["aplus_types"] = aplus_types
        if product_info:
            payload["product_info"] = product_info
        if brand_config:
            payload["brand_config"] = brand_config
        if aspect_ratio:
            payload["aspect_ratio"] = aspect_ratio
        if gen_language:
            payload["gen_language"] = gen_language
        if model:
            payload["model"] = model
        if same_style_reference:
            payload["same_style_reference"] = same_style_reference
        return self.studio_call("POST", "/model/clothing-suite", json_data=payload)

    def studio_cancel(self, request_id):
        """Cancel a running Image Studio generation.

        Billing follows how far each image got, not how many you receive:
        images still queued are refunded, images already generating are charged
        (they cannot be stopped), images already delivered bill once through the
        normal path. The response reports the split as refunded_queued /
        charged_running / already_done, and the task then polls as
        status "cancelled" - not an error.
        """
        return self.studio_call("POST", f"/jobs/{request_id}/cancel")

    def studio_status(self, request_id):
        """Poll an Image Studio job.

        The async key is `request_id`, same name as inference but a **separate id
        space** - an Image Studio id is not valid on /api/v1/inference/status/...
        """
        return self.studio_call("GET", f"/jobs/{request_id}")

    def studio_pricing(self):
        """Live Image Studio pricing — always the source of truth over any static table."""
        return self.studio_call("GET", "/pricing")

    def studio_my_works(self, task_type=None, limit=20, offset=0):
        params = {"limit": limit, "offset": offset}
        if task_type:
            params["task_type"] = task_type
        return self.studio_call("GET", "/my-works", params=params)


# ─── PendingManager ────────────────────────────────────────────────────────

class PendingManager:
    """Track jobs in credential-scoped files; legacy files require explicit import."""

    def __init__(self, path=None):
        self.path = Path(path) if path else PENDING_FILE


    def _load(self):
        if self.path.exists():
            try:
                data = json.loads(self.path.read_text())
                if not isinstance(data, dict) or any(not isinstance(v, dict) for v in data.values()):
                    raise ValueError("Invalid task records")
                return data
            except (ValueError, OSError):
                _error_out("Cannot read pending task records; preserve the file for recovery")
        return {}

    def _save(self, data):
        fd, temporary = tempfile.mkstemp(prefix=self.path.name + ".", dir=str(self.path.parent))
        try:
            with os.fdopen(fd, "w") as handle:
                json.dump(data, handle, indent=2, default=str)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, self.path)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)

    @contextmanager
    def _locked(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(str(self.path) + ".lock", "a+b") as handle:
            if os.name == "nt":
                handle.seek(0, os.SEEK_END)
                if handle.tell() == 0:
                    handle.write(b"0")
                    handle.flush()
                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_LOCK, 1)
            else:
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            try:
                yield
            finally:
                if os.name == "nt":
                    handle.seek(0)
                    msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    fcntl.flock(handle.fileno(), fcntl.LOCK_UN)

    def add(self, request_id, job_type, metadata=None):
        with self._locked():
            data = self._load()
            data[request_id] = {
                "job_type": job_type,
                "submitted_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                **(metadata or {}),
            }
            self._save(data)

    def remove(self, request_id):
        with self._locked():
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
            job_type = meta.get("job_type", "inference")
            try:
                with redirect_stderr(io.StringIO()):
                    if job_type == "image-studio":
                        st = client.studio_status(rid)
                    else:
                        st = client.status(rid)
                results[rid] = st
                status_val = st.get("status") or st.get("job_status") or ""
                if str(status_val).upper() in ("COMPLETED", "FAILED", "NOT_FOUND", "DONE", "ERROR", "CANCELLED", "CANCELED"):
                    to_remove.append(rid)
            except (SystemExit, OSError, ValueError):
                results[rid] = {"error": "Failed to poll"}

        for rid in to_remove:
            try:
                with redirect_stderr(io.StringIO()):
                    self.remove(rid)
            except (OSError, ValueError, SystemExit):
                results[rid]["tracking_error"] = "Could not save task state"

        errors = sum(1 for v in results.values() if v.get("error") or v.get("tracking_error"))
        return {"polled": len(data), "completed": len(to_remove), "errors": errors, "results": results}


def _track_accepted(pending, request_id, job_type, metadata):
    """Local bookkeeping must never hide an accepted request's identifier."""
    try:
        with redirect_stderr(io.StringIO()):
            pending.add(request_id, job_type, metadata)
    except (OSError, ValueError, SystemExit):
        print(json.dumps({"warning": "Task accepted but local tracking failed. Save the request_id; do not resubmit.",
                          "request_id": request_id}), file=sys.stderr)


# ─── CLI ────────────────────────────────────────────────────────────────────

def build_parser():
    parser = argparse.ArgumentParser(
        prog="phosor_client",
        description="Phosor AI CLI — generate videos and images, bring your own LoRAs, manage models",
    )
    parser.add_argument("--version", action="version", version=f"phosor-client {VERSION}")
    parser.add_argument("--base-url", default=None, help="Compatibility option; only https://phosor.ai is accepted")
    parser.add_argument("--api-key", default=None, help="API key override")

    sub = parser.add_subparsers(dest="command", help="Available commands")

    # ── check-key ───────────────────────────────────────────────────────
    sub.add_parser("check-key", help="Validate API key")

    # ── submit ──────────────────────────────────────────────────────────
    p = sub.add_parser("submit", help="Submit inference job (T2V, I2V, T2I, or I2I)")
    p.add_argument("prompt", help="Text prompt")
    p.add_argument("--width", type=int, default=None)
    p.add_argument("--height", type=int, default=None)
    p.add_argument("--num-frames", type=int, default=None)
    p.add_argument("--fps", type=int, default=None, dest="frames_per_second")
    p.add_argument("--steps", type=int, default=None, dest="num_inference_steps",
                   help="Inference steps where supported; defaults depend on the model")
    p.add_argument("--guidance", type=float, default=None, dest="guidance_scale",
                   help="Guidance scale where supported; limits depend on the selected model")
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--negative-prompt", default=None)
    p.add_argument("--image-url", default=None, help="S3 key for I2V/I2I/S2V/Animate (from upload-image)")
    p.add_argument("--image-urls", default=None, help="JSON array of uploaded image keys or public HTTPS URLs")
    for kind in ("image", "video", "audio"):
        p.add_argument("--reference-" + kind + "-labels", default=None,
                       help="JSON array of labels in reference URL order")
    p.add_argument("--audio-url", default=None, help="Audio URL for S2V (speech-to-video)")
    p.add_argument("--video-url", default=None, help="Video URL for Animate (motion reference)")
    p.add_argument("--lora-id", default=None)
    p.add_argument("--lora-scale", type=float, default=None)
    p.add_argument("--loras", default=None,
                   help='Multiple LoRAs as JSON: \'[{"lora_id":"...","lora_scale":1.0}]\'')
    p.add_argument("--model", default=None)
    p.add_argument("--num-images", type=int, default=None, dest="num_images",
                   help="Number of images to generate, 1-4 (image models only)")
    p.add_argument("--strength", type=float, default=None,
                   help="Transformation strength 0.0-1.0 (image-to-image only)")
    p.add_argument("--output-format", default=None, dest="output_format",
                   choices=["png", "jpeg", "webp"], help="Output format (image models only)")

    # MiniMax H3 — duration-based, ignores width/height/num_frames/fps (output is fixed 24fps)
    p.add_argument("--avoid-model-limitations", action="store_true", default=None,
                   help="H3: allow model-limit adaptation during mandatory prompt processing (default off)")
    p.add_argument("--unrestricted-enhancement", action="store_true", default=None,
                   help="H3: run prompt processing on an open model that does not refuse mature themes (default off)")
    p.add_argument("--duration", type=float, default=None,
                   help="Output length in seconds, 4-15 (MiniMax H3; billed per output second)")
    p.add_argument("--resolution-tier", default=None, dest="resolution_tier",
                   choices=["480p", "768p"], help="MiniMax H3 resolution tier (default 480p)")
    p.add_argument("--aspect", default=None, dest="aspect_ratio",
                   choices=["16:9", "4:3", "1:1", "3:4", "9:16"],
                   help="MiniMax H3 aspect ratio (default 16:9)")
    p.add_argument("--end-image-url", default=None, dest="end_image_url",
                   help="Optional ending frame for minimax/h3/image-to-video")
    p.add_argument("--reference-image-urls", default=None, dest="reference_image_urls",
                   help="Comma-separated reference images for minimax/h3/reference-to-video")
    p.add_argument("--reference-video-urls", default=None, dest="reference_video_urls",
                   help="Comma-separated reference videos for minimax/h3/reference-to-video")
    p.add_argument("--reference-audio-urls", default=None, dest="reference_audio_urls",
                   help="Comma-separated reference audio for minimax/h3/reference-to-video")
    p.add_argument("--use-ref-video-audio", action="store_true", default=None,
                   dest="use_ref_video_audio",
                   help="Also feed each reference video's own soundtrack as an audio reference")

    # ── status ──────────────────────────────────────────────────────────
    p = sub.add_parser("status", help="Get job status")
    p.add_argument("request_id", help="Job request ID")

    # ── result ──────────────────────────────────────────────────────────
    p = sub.add_parser("result", help="Get job result (video or image URL)")
    p.add_argument("request_id", help="Job request ID")

    # ── poll ────────────────────────────────────────────────────────────
    sub.add_parser("poll", help="Poll all pending jobs")

    # ── list ────────────────────────────────────────────────────────────
    sub.add_parser("list", help="List pending jobs (local tracking)")
    sub.add_parser("pending-sources", help="List saved task files available for explicit import")
    p = sub.add_parser("import-pending", help="Import a saved task file after verifying task access with the current key")
    p.add_argument("file", help="Path reported by pending-sources")

    # ── history ─────────────────────────────────────────────────────────
    p = sub.add_parser("history", help="Get job history")
    p.add_argument("--limit", type=int, default=50)

    # ── upload-image ────────────────────────────────────────────────────
    p = sub.add_parser("upload-image", help="Upload local image for I2V or I2I")
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
    p = sub.add_parser("import-lora", help="Import LoRA from HTTPS URLs (video: 2 files, image: 1 file)")
    p.add_argument("high_noise_url", help="HTTPS URL to .safetensors (single file for image LoRA, high_noise for video)")
    p.add_argument("low_noise_url", nargs="?", default=None, help="HTTPS URL to low_noise .safetensors (video LoRA only)")
    p.add_argument("--name", default=None, help="LoRA model name")

    # ── submit-tts ──────────────────────────────────────────────────────
    p = sub.add_parser("submit-tts", help="Submit a text-to-speech job (Qwen3-TTS)")
    p.add_argument("text", help="Text to synthesize (max 500 characters)")
    p.add_argument("--speaker", default=None, help="Preset voice (default Sohee)")
    p.add_argument("--language", default=None, help="Language tag (default Chinese)")
    p.add_argument("--seed", type=int, default=None, help="-1 = random")
    p.add_argument("--temperature", type=float, default=None, help="0.0-2.0 (default 0.9)")
    p.add_argument("--top-p", type=float, default=None, dest="top_p", help="(0.0, 1.0] (default 1.0)")
    p.add_argument("--top-k", type=int, default=None, dest="top_k", help="1-200 (default 50)")
    p.add_argument("--repetition-penalty", type=float, default=None, dest="repetition_penalty",
                   help="1.0-2.0 (default 1.05)")
    p.add_argument("--model", default=None, help="Override the TTS model id")

    # ── chat ───────────────────────────────────────────────────────────
    p = sub.add_parser("chat", help="Chat with the Qwen3.8 27B LLM (OpenAI-compatible /api/v1/chat/completions)")
    p.add_argument("prompt", nargs="?", default=None, help="User message (omit when using --messages)")
    p.add_argument("--system", default=None, help="System message")
    p.add_argument("--messages", default=None,
                   help="Full OpenAI messages array as JSON, or @file.json; replaces prompt/--system")
    p.add_argument("--image", action="append", default=None,
                   help="Image for the user message: https URL, data URL or local PNG/JPEG/WebP file (max 2, 4 MB each)")
    p.add_argument("--model", default=CHAT_MODEL, help=f"Model id (default {CHAT_MODEL})")
    p.add_argument("--max-tokens", type=int, default=None, dest="max_tokens", help="1-8192 (server default 1024)")
    p.add_argument("--temperature", type=float, default=None)
    p.add_argument("--top-p", type=float, default=None, dest="top_p")
    p.add_argument("--stop", action="append", default=None, help="Stop sequence (repeat up to 4 times)")
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--json-mode", action="store_true", default=False, help='Set response_format {"type": "json_object"}')
    p.add_argument("--tools", default=None, help="OpenAI tools array as JSON, or @file.json")
    p.add_argument("--tool-choice", default=None, dest="tool_choice", help='"auto", "none", "required" or a JSON object')
    p.add_argument("--thinking", action="store_true", default=False, help="Set enable_thinking=true (reasoning returned in reasoning_content)")
    p.add_argument("--stream", action="store_true", default=False,
                   help="Stream the answer: text goes to stderr as it arrives, the assembled JSON to stdout")

    # ── models ─────────────────────────────────────────────────────────
    sub.add_parser("models", help="List available models")

    # ── save-lora ───────────────────────────────────────────────────────
    p = sub.add_parser("save-lora", help="Activate a LoRA, extending expiry to 7 days (trained → ready)")
    p.add_argument("lora_id", help="LoRA model UUID")
    p.add_argument("--name", default=None)

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

    # ── Image Studio (separate product surface: product/model photography) ──

    sub.add_parser("studio-features", help="List Image Studio endpoints, fields, and billing model")
    sub.add_parser("studio-pricing", help="Get live Image Studio pricing (source of truth over any static table)")

    p = sub.add_parser("studio-analyze", help="AI-analyze a product/garment image or reference URL (freemium)")
    p.add_argument("--target", required=True, choices=["agent", "product", "model", "reference"],
                   help="agent=general Agent-image analysis, product=product suite, model=clothing suite, reference=analyze a reference URL/image")
    p.add_argument("--image-url", default=None, help="S3 key or URL of the image to analyze")
    p.add_argument("--url", default=None, help="Reference product page URL (only for --target reference with a web_url source)")
    p.add_argument("--prompt", default=None, help="Optional free-text hint for the analysis")
    p.add_argument("--language", default=None, choices=["zh", "en"])

    p = sub.add_parser("studio-suite", help="Generate a product image suite (POST /product/suite)")
    p.add_argument("--image-url", required=True, dest="product_image_url", help="Product image S3 key/URL")
    p.add_argument("--layout-types", default=None, help="Comma-separated layout type ids")
    p.add_argument("--count-per-type", type=int, default=None)
    p.add_argument("--custom-suggestions", default=None, help="JSON array")
    p.add_argument("--product-info", default=None, help="Free-text product description/facts")
    p.add_argument("--aspect-ratio", default=None, choices=["1:1", "3:4", "4:3", "9:16", "16:9"])
    p.add_argument("--gen-language", default=None)
    p.add_argument("--model", default=None)
    p.add_argument("--same-style-reference", default=None, help="JSON object (from studio-analyze --target reference)")
    p.add_argument("--template-ids", default=None, help="Comma-separated layout template ids (from studio-layouts) — sent as custom_suggestions like the UI's manual template pick")
    p.add_argument("--layout-template-ids", default=None, help="Comma-separated layout template IDs (recommended over --template-ids)")
    p.add_argument("--layout-random-count", type=int, default=None, help="Randomly select N layout templates (no manual IDs)")
    p.add_argument("--image-urls", dest="suite_image_urls", default=None, help="Comma-separated extra product view S3 URLs (multi-view input)")

    p = sub.add_parser("studio-layouts", help="List the layout template library (static asset; query, then select via studio-suite --template-ids)")
    p.add_argument("--module", default="product", choices=["product", "clothing"])
    p.add_argument("--type", dest="type_filter", default=None, help="Filter by type: selling_point, aplus, white_bg, scene, closeup, size_chart …")

    p = sub.add_parser("studio-clothing-suite", help="Generate a model/clothing image suite (POST /model/clothing-suite)")
    p.add_argument("--image-urls", required=True, dest="clothing_image_urls", help="Comma-separated garment image S3 keys/URLs (up to 5 used)")
    p.add_argument("--main-image-types", default=None, help='JSON object, e.g. \'{"model_shot":2,"selling_point":1}\'')
    p.add_argument("--aplus-types", default=None, help='JSON object, e.g. \'{"standard_aplus":1}\'')
    p.add_argument("--product-info", default=None)
    p.add_argument("--brand-config", default=None, help="JSON object")
    p.add_argument("--aspect-ratio", default=None, help="Default 3:4")
    p.add_argument("--gen-language", default=None)
    p.add_argument("--model", default=None)
    p.add_argument("--same-style-reference", default=None, help="JSON object")

    p = sub.add_parser("studio-cancel", help="Cancel a running Image Studio generation (queued images refunded, generating ones charged)")
    p.add_argument("request_id", help="Image Studio request_id (UUID)")

    p = sub.add_parser("studio-status", help="Get Image Studio job status (separate id space; key is request_id)")
    p.add_argument("request_id", help="Image Studio request_id (UUID)")

    p = sub.add_parser("studio-my-works", help="List past Image Studio generations")
    p.add_argument("--task-type", default=None)
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--offset", type=int, default=0)

    p = sub.add_parser("studio-call", help="Generic Image Studio call — any endpoint from `studio-features` not covered by a dedicated command "
                                            "(remove-bg, replace, inpaint, erase, handheld, translate, outpaint, recolor, enhance, upscale, "
                                            "scene-compose, scene-variation, real-model-swap, mannequin-swap, model-scene-swap, ai-outfit, pose-variation, ai-wearable)")
    p.add_argument("method", choices=["GET", "POST", "PUT", "DELETE", "PATCH"])
    p.add_argument("path", help="Path relative to /api/v1/image-studio, e.g. /product/remove-bg")
    p.add_argument("--json", dest="json_body", default=None, help="JSON request body")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    client = PhosorClient(base_url=args.base_url, api_key=args.api_key)
    scope = hashlib.sha256((client.base_url + "\0" + (client.api_key or "anonymous")).encode()).hexdigest()
    pending = PendingManager(WORKSPACE_DIR / ("phosor-pending-" + scope + ".json"))

    cmd = args.command

    # ── Offline commands ────────────────────────────────────────────────

    if cmd == "models":
        _json_out(MODELS)

    if cmd == "studio-features":
        _json_out(IMAGE_STUDIO)

    if cmd == "pending-sources":
        files = sorted(WORKSPACE_DIR.glob("phosor-pending*.json"))
        _json_out({"sources": [str(p) for p in files], "note": "Import explicitly after switching keys; source files are preserved."})

    if cmd == "import-pending":
        source = Path(args.file).expanduser().resolve()
        if source.parent != WORKSPACE_DIR.resolve() or not source.name.startswith("phosor-pending") or source.suffix != ".json":
            _error_out("Choose a file reported by pending-sources")
        records = PendingManager(source)._load()
        imported, rejected = [], []
        for rid, meta in records.items():
            try:
                with redirect_stderr(io.StringIO()):
                    response = client.studio_status(rid) if meta.get("job_type") == "image-studio" else client.status(rid)
                status = str(response.get("status") or response.get("job_status") or "").upper()
                if response.get("error") or not status or status == "NOT_FOUND":
                    rejected.append(rid)
                    continue
                pending.add(rid, meta.get("job_type", "inference"), meta)
                imported.append(rid)
            except (SystemExit, OSError, ValueError):
                rejected.append(rid)
        print(json.dumps({"imported": imported, "rejected": rejected, "source_preserved": True}, indent=2))
        raise SystemExit(1 if rejected else 0)

    if cmd == "list":
        _json_out(pending.list_pending())

    # ── Commands requiring API key ──────────────────────────────────────

    if cmd == "check-key":
        if not client.api_key:
            _error_out("PHOSOR_API_KEY not set")
        # 401/403 must be reported as "invalid" -- the whole point of check-key is a
        # one-line verdict on the key, not a traceback.
        try:
            resp = client.check_key()
        except HTTPError as e:
            if e.code in (401, 403):
                _json_out({"status": "invalid", "http": e.code,
                           "hint": "PHOSOR_API_KEY is missing, wrong, or revoked."})
                return
            _http_error(e)
        _json_out({"status": "valid", "loras_total": resp.get("total", resp.get("count"))})

    if cmd == "submit":
        kwargs = {}
        for k in _SUBMIT_FIELDS:
            if k == "loras":
                continue  # parsed from its own JSON string just below
            v = getattr(args, k, None)
            if v is not None:
                kwargs[k] = v
        # reference_*_urls arrive as comma-separated strings; the API wants arrays
        for k in ("reference_image_urls", "reference_video_urls", "reference_audio_urls"):
            if isinstance(kwargs.get(k), str):
                raw = kwargs[k]
                kwargs[k] = (_parse_json_arg(raw, "--" + k.replace("_", "-"), list)
                             if raw.lstrip().startswith("[") else
                             [u.strip() for u in raw.split(",") if u.strip()])
                if not all(isinstance(u, str) and u.strip() for u in kwargs[k]):
                    _error_out(k + " must contain nonempty strings")

        for field in ("image_urls", "reference_image_labels", "reference_video_labels", "reference_audio_labels"):
            if field in kwargs:
                kwargs[field] = _parse_json_arg(kwargs[field], "--" + field.replace("_", "-"), list)
                if not all(isinstance(v, str) and v.strip() for v in kwargs[field]):
                    _error_out(field + " must contain nonempty strings")
                if field.endswith("_labels"):
                    urls = kwargs.get(field.replace("_labels", "_urls"), [])
                    if len(kwargs[field]) != len(urls):
                        _error_out(field + " must match the reference URL count")

        # Parse --loras JSON string
        loras_str = getattr(args, "loras", None)
        if loras_str:
            try:
                kwargs["loras"] = _parse_json_arg(loras_str, "--loras", list)
            except json.JSONDecodeError:
                _error_out("--loras must be valid JSON array, e.g. '[{\"lora_id\":\"...\",\"lora_scale\":1.0}]'")
        try:
            resp = client.submit(args.prompt, **kwargs)
        except ValueError as exc:
            _error_out(str(exc))
        # Auto-track pending — detect job type from model
        rid = resp.get("request_id") or resp.get("requested_id")
        if rid:
            _model = kwargs.get("model", "")
            _IMAGE_MODEL_PREFIXES = ("qwen-image/", "z-image/", "openai/gpt-image-2/", "flux2/")
            if _model == "minimax/h3/text-to-image" or any(_model.startswith(p) for p in _IMAGE_MODEL_PREFIXES):
                job_type = "i2i" if "image-to-image" in _model else "t2i"
            elif "speech-to-video" in _model:
                job_type = "s2v"
            elif "animate" in _model:
                job_type = "animate"
            else:
                job_type = "i2v" if kwargs.get("image_url") else "t2v"
            _track_accepted(pending, rid, job_type, {"prompt": args.prompt[:80]})
        _json_out(resp)

    if cmd == "submit-tts":
        kw = {k: getattr(args, k, None) for k in
              ("speaker", "language", "seed", "temperature", "top_p", "top_k",
               "repetition_penalty", "model")}
        resp = client.submit_tts(args.text, **kw)
        rid = resp.get("request_id")
        if rid:
            _track_accepted(pending, rid, "inference", {"text": args.text[:80]})
        _json_out(resp)

    if cmd == "chat":
        if not client.api_key:
            _error_out("PHOSOR_API_KEY not set")

        def _json_or_file(raw, flag, kind):
            if raw is None:
                return None
            if raw.startswith("@"):
                try:
                    raw = Path(raw[1:]).read_text(encoding="utf-8")
                except OSError as e:
                    _error_out(f"{flag}: cannot read file: {e}")
            return _parse_json_arg(raw, flag, kind)

        messages = _json_or_file(args.messages, "--messages", list)
        if messages is None:
            if not args.prompt:
                _error_out("Give a prompt or --messages")
            messages = []
            if args.system:
                messages.append({"role": "system", "content": args.system})
            if args.image:
                if len(args.image) > CHAT_MAX_IMAGES:
                    _error_out(f"At most {CHAT_MAX_IMAGES} images per request")
                content = [{"type": "text", "text": args.prompt}] + [_chat_image_part(i) for i in args.image]
            else:
                content = args.prompt
            messages.append({"role": "user", "content": content})
        elif args.prompt or args.system or args.image:
            _error_out("--messages replaces prompt, --system and --image; pass one or the other")
        if args.stop and len(args.stop) > 4:
            _error_out("At most 4 --stop sequences")
        tool_choice = args.tool_choice
        if tool_choice and tool_choice.strip().startswith("{"):
            tool_choice = _parse_json_arg(tool_choice, "--tool-choice", dict)
        body = {
            "model": args.model, "messages": messages, "max_tokens": args.max_tokens,
            "temperature": args.temperature, "top_p": args.top_p, "seed": args.seed,
            "stop": (args.stop[0] if args.stop and len(args.stop) == 1 else args.stop),
            "response_format": {"type": "json_object"} if args.json_mode else None,
            "tools": _json_or_file(args.tools, "--tools", list), "tool_choice": tool_choice,
            "enable_thinking": True if args.thinking else None,
            "stream": True if args.stream else None,
        }

        def _echo(kind, text):
            sys.stderr.write(text)
            sys.stderr.flush()

        resp = client.chat(body, on_delta=_echo if args.stream else None)
        if args.stream:
            sys.stderr.write("\n")
        if args.stream and (not resp.get("stream_complete") or resp.get("error")):
            print(json.dumps(resp, indent=2))
            raise SystemExit(1)
        _json_out(resp)

    if cmd == "status":
        _json_out(client.status(args.request_id))

    if cmd == "result":
        _json_out(client.result(args.request_id))

    if cmd == "poll":
        result = pending.poll_all(client)
        print(json.dumps(result, indent=2))
        raise SystemExit(1 if result["errors"] else 0)

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

    if cmd == "save-lora":
        _json_out(client.save_lora(args.lora_id, name=args.name))

    if cmd == "loras":
        _json_out(client.loras(limit=args.limit, offset=args.offset))

    if cmd == "lora-status":
        _json_out(client.lora_status(args.lora_id))

    if cmd == "delete-lora":
        _json_out(client.delete_lora(args.lora_id))

    # ── Utility ─────────────────────────────────────────────────────────

    # ── Image Studio (separate product surface) ──────────────────────────

    if cmd == "studio-pricing":
        _json_out(client.studio_pricing())

    if cmd == "studio-analyze":
        resp = client.studio_analyze(
            args.target, image_url=args.image_url, prompt=args.prompt,
            url=args.url, language=args.language,
        )
        if resp.get("request_id"):
            _track_accepted(pending, resp["request_id"], "image-studio", {"feature": "analyze"})
        _json_out(resp)

    if cmd == "studio-layouts":
        tpls = client.studio_layouts(args.module, type_filter=args.type_filter)
        _json_out([{"id": t.get("id"), "name": t.get("name"), "name_en": t.get("name_en"),
                    "type": t.get("type"), "platform": t.get("platform"),
                    "random_safe": t.get("random_safe"), "file": t.get("file")} for t in tpls])
        return

    if cmd == "studio-suite":
        layout_types = [t.strip() for t in args.layout_types.split(",") if t.strip()] if args.layout_types else None
        custom_suggestions = _parse_json_arg(args.custom_suggestions, "--custom-suggestions", list) or []
        if getattr(args, "template_ids", None):
            ids = [x.strip() for x in args.template_ids.split(",") if x.strip()]
            custom_suggestions = custom_suggestions + client.layout_templates_to_suggestions(ids)
        custom_suggestions = custom_suggestions or None
        same_style_reference = _parse_json_arg(args.same_style_reference, "--same-style-reference", dict)
        layout_template_ids = [x.strip() for x in args.layout_template_ids.split(",") if x.strip()] if getattr(args, "layout_template_ids", None) else None
        suite_image_urls = [u.strip() for u in args.suite_image_urls.split(",") if u.strip()] if getattr(args, "suite_image_urls", None) else None
        resp = client.studio_suite(
            args.product_image_url, layout_types=layout_types, count_per_type=args.count_per_type,
            custom_suggestions=custom_suggestions, product_info=args.product_info,
            aspect_ratio=args.aspect_ratio, gen_language=args.gen_language, model=args.model,
            same_style_reference=same_style_reference,
            layout_template_ids=layout_template_ids,
            layout_random_count=getattr(args, "layout_random_count", None),
            image_urls=suite_image_urls,
        )
        jid = resp.get("request_id")   # the server returns request_id (job_id is never set)
        if jid:
            _track_accepted(pending, jid, "image-studio", {"feature": "product/suite"})
        _json_out(resp)

    if cmd == "studio-clothing-suite":
        clothing_image_urls = [u.strip() for u in args.clothing_image_urls.split(",") if u.strip()]
        main_image_types = _parse_json_arg(args.main_image_types, "--main-image-types", dict)
        aplus_types = _parse_json_arg(args.aplus_types, "--aplus-types", dict)
        brand_config = _parse_json_arg(args.brand_config, "--brand-config", dict)
        same_style_reference = _parse_json_arg(args.same_style_reference, "--same-style-reference", dict)
        resp = client.studio_clothing_suite(
            clothing_image_urls, main_image_types=main_image_types, aplus_types=aplus_types,
            product_info=args.product_info, brand_config=brand_config, aspect_ratio=args.aspect_ratio,
            gen_language=args.gen_language, model=args.model, same_style_reference=same_style_reference,
        )
        jid = resp.get("request_id")   # the server returns request_id (job_id is never set)
        if jid:
            _track_accepted(pending, jid, "image-studio", {"feature": "model/clothing-suite"})
        _json_out(resp)

    if cmd == "studio-status":
        _json_out(client.studio_status(args.request_id))

    if cmd == "studio-cancel":
        _json_out(client.studio_cancel(args.request_id))

    if cmd == "studio-my-works":
        _json_out(client.studio_my_works(task_type=args.task_type, limit=args.limit, offset=args.offset))

    if cmd == "studio-call":
        body = _parse_json_arg(args.json_body, "--json", (dict, list))
        resp = client.studio_call(args.method, args.path, json_data=body)
        jid = resp.get("request_id") if isinstance(resp, dict) else None
        if jid:
            _track_accepted(pending, jid, "image-studio", {"feature": args.path.strip("/")})
        _json_out(resp)


if __name__ == "__main__":
    main()
