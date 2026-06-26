"""
GLM-4.6V Caption Tool
Generate captions for images, videos, and files with Zhipu GLM-4.6V models.

Official API docs (https://docs.bigmodel.cn/api-reference/模型-api/对话补全):
Vision model enum: glm-4.6v, autoglm-phone, glm-4.6v-flash, glm-4.6v-flashx, glm-4v-flash, glm-4.1v-thinking-flashx, glm-4.1v-thinking-flash

- file_url cannot mix with image_url or video_url in the same request
- Images: URL or Base64, ≤5MB each, ≤6000×6000px, only jpg/png/jpeg
- GLM-4.6V/GLM-4.6V-Flash/GLM-4.6V-FlashX/GLM-4.1v-thinking series: ≤50 images
- GLM-4V-Flash: ≤1 image, NO Base64 (URL only)
- Videos: URL or local path (mp4/mkv/mov) — local paths are auto-tunneled via cloudflare
  - GLM-4.6V series: ≤200MB
- Files: URL or local path (pdf/txt/docx/jsonl/xlsx/pptx) — local paths are auto-tunneled via cloudflare
  - Up to 50 files
"""

import os
import json
import base64
import argparse
import sys
from pathlib import Path
from typing import List, Optional, Dict, Any

import requests

# ---------------------------------------------------------------------------
# Make tunnel_server importable when running as a script
# ---------------------------------------------------------------------------
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

DEFAULT_MODEL = "glm-5v-turbo"
DEFAULT_PROMPT = "请详细描述这张图片的内容"
DEFAULT_RESPONSE_FORMAT = "json_object"
API_BASE_URL = "https://open.bigmodel.cn/api/coding/paas/v4/chat/completions"

# Model max_tokens limits (per official docs)
MODEL_MAX_TOKENS = {
    "glm-4.6v": {"default": 16384, "max": 32768},
    "glm-4.6v-flash": {"default": 16384, "max": 32768},
    "glm-4.6v-flashx": {"default": 16384, "max": 32768},
}

# Officially supported image formats only (per Zhipu API docs)
SUPPORTED_IMAGE_EXTS = {".jpg", ".jpeg", ".png"}
IMAGE_MIME_TYPES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
}

# Image constraints per official docs
MAX_IMAGE_SIZE_MB = 5
MAX_IMAGE_PIXELS = 6000 * 6000  # 36 megapixels

# Max images per model (per official docs)
MODEL_IMAGE_LIMITS = {
    "glm-4.6v": 50,
    "glm-4.6v-flash": 50,
    "glm-4.6v-flashx": 50,
}

# Models that do NOT support Base64 (URL only)
NO_BASE64_MODELS = {"glm-4v-flash"}


def validate_local_image(image_path: str) -> str:
    """Validate local image against official API constraints.

    Returns error message if validation fails, empty string if OK.
    """
    path = Path(image_path)
    if not path.exists():
        return f"Image not found: {image_path}"

    # Check format
    ext = path.suffix.lower()
    if ext not in SUPPORTED_IMAGE_EXTS:
        return (
            f"Unsupported image format '{ext}'. "
            f"Only {', '.join(sorted(SUPPORTED_IMAGE_EXTS))} are supported by the Zhipu API."
        )

    # Check file size (≤5MB)
    size_bytes = path.stat().st_size
    max_bytes = MAX_IMAGE_SIZE_MB * 1024 * 1024
    if size_bytes > max_bytes:
        return (
            f"Image too large: {size_bytes / 1024 / 1024:.1f}MB "
            f"(max {MAX_IMAGE_SIZE_MB}MB). "
            f"Consider resizing or compressing the image."
        )

    return ""


def load_image_as_data_url(image_path: str) -> str:
    """Convert a local image file to data URL format.

    Validates format and size before encoding.
    """
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    ext = path.suffix.lower()
    if ext not in SUPPORTED_IMAGE_EXTS:
        raise ValueError(
            f"Unsupported image format '{ext}'. "
            f"Only {', '.join(sorted(SUPPORTED_IMAGE_EXTS))} are supported by the Zhipu API."
        )

    # Check file size
    size_bytes = path.stat().st_size
    max_bytes = MAX_IMAGE_SIZE_MB * 1024 * 1024
    if size_bytes > max_bytes:
        raise ValueError(
            f"Image too large: {size_bytes / 1024 / 1024:.1f}MB "
            f"(max {MAX_IMAGE_SIZE_MB}MB). "
            f"Consider resizing or compressing the image."
        )

    mime_type = IMAGE_MIME_TYPES[ext]
    with open(path, "rb") as f:
        img_data = base64.b64encode(f.read()).decode()

    return f"data:{mime_type};base64,{img_data}"


def process_image(image_input: str) -> str:
    """
    Process an image input into a usable image_url.

    Supports: URL, local path (→ data URL), data URL (pass-through), base64:xxx
    """
    image_input = image_input.strip()

    if image_input.startswith("data:"):
        return image_input

    if image_input.startswith("base64:"):
        return f"data:image/jpeg;base64,{image_input[7:]}"

    if image_input.startswith("http://") or image_input.startswith("https://"):
        return image_input

    return load_image_as_data_url(image_input)


def build_content(
    images: Optional[List[str]] = None,
    videos: Optional[List[str]] = None,
    files: Optional[List[str]] = None,
    prompt: str = DEFAULT_PROMPT,
) -> List[Dict[str, Any]]:
    """Build the multimodal content array for the API request."""
    content = []

    if images:
        for img in images:
            content.append(
                {
                    "type": "image_url",
                    "image_url": {"url": process_image(img)},
                }
            )
    elif videos:
        for vid in videos:
            content.append(
                {
                    "type": "video_url",
                    "video_url": {"url": vid.strip()},
                }
            )
    elif files:
        for f in files:
            content.append(
                {
                    "type": "file_url",
                    "file_url": {"url": f.strip()},
                }
            )

    content.append({"type": "text", "text": prompt})
    return content


def _is_url(s: str) -> bool:
    return s.strip().startswith(("http://", "https://"))


def _has_local_paths(items: Optional[List[str]]) -> bool:
    """Check whether any item in the list is a local path (not a URL)."""
    if not items:
        return False
    return any(not _is_url(item) for item in items)


def _resolve_to_urls(items: List[str], tunnel) -> List[str]:
    """Replace local paths with tunnel URLs; pass URLs through unchanged."""
    return [tunnel.get_url(item) if not _is_url(item) else item for item in items]


def caption(
    images: Optional[List[str]] = None,
    videos: Optional[List[str]] = None,
    files: Optional[List[str]] = None,
    prompt: str = DEFAULT_PROMPT,
    api_key: Optional[str] = None,
    model: str = DEFAULT_MODEL,
    temperature: float = 0.8,
    top_p: float = 0.6,
    max_tokens: int = 2048,
    thinking: bool = False,
    stream: bool = False,
    response_format: Optional[str] = None,
    sys_prompt: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Generate captions for images, videos, or documents using GLM-4.6V.

    Args:
        images: Image URLs, local paths, or base64 strings
        videos: Video URLs or local paths (auto-tunneled if local)
        files: File URLs or local paths (auto-tunneled if local)
        prompt: Prompt for the model
        api_key: ZhiPu API Key (defaults to ZHIPU_API_KEY env var)
        model: Model name (default: glm-5v-turbo)
        temperature: Sampling temperature (default: 0.8)
        top_p: Nucleus sampling (default: 0.6)
        max_tokens: Max output tokens (max 32768)
        thinking: Enable thinking/reasoning mode
        stream: Whether to use streaming output
        response_format: Structured output mode (currently supports json_object)
        sys_prompt: Optional system prompt, recommended for defining JSON shape

    Returns:
        Dict with success, caption, and usage fields
    """
    if not api_key:
        api_key = os.environ.get("ZHIPU_API_KEY")

    if not api_key:
        return {
            "success": False,
            "error": (
                "ZHIPU_API_KEY not configured. "
                "Get your API key at: https://bigmodel.cn/usercenter/proj-mgmt/apikeys. "
                "未配置 ZHIPU_API_KEY，请在上述链接获取并配置。"
            ),
        }

    if response_format and response_format != DEFAULT_RESPONSE_FORMAT:
        return {
            "success": False,
            "error": f"Unsupported response_format '{response_format}'. Supported value: {DEFAULT_RESPONSE_FORMAT}.",
        }

    # Validate max_tokens against model limits
    model_key = model.lower()
    model_limits = MODEL_MAX_TOKENS.get(model_key)
    if model_limits and max_tokens > model_limits["max"]:
        return {
            "success": False,
            "error": f"max_tokens {max_tokens} exceeds model '{model}' limit of {model_limits['max']}.",
        }

    # Validate image count against model limits
    if images:
        model_key = model.lower()
        max_images = MODEL_IMAGE_LIMITS.get(model_key, 50)
        if len(images) > max_images:
            return {
                "success": False,
                "error": (
                    f"Too many images: {len(images)} (max {max_images} for model '{model}'). "
                    f"Official limits: GLM-4.6V/GLM-4.6V-Flash/GLM-4.6V-FlashX/GLM-4.1v-thinking ≤50, GLM-4V-Flash ≤1."
                ),
            }

        # GLM-4V-Flash does not support Base64 encoding
        if model_key in NO_BASE64_MODELS:
            for img in images:
                img_stripped = img.strip()
                if not (
                    img_stripped.startswith("http://")
                    or img_stripped.startswith("https://")
                ):
                    return {
                        "success": False,
                        "error": (
                            f"Model '{model}' does not support Base64 or local file inputs. "
                            f"Please provide image URLs only."
                        ),
                    }

    # NOTE: videos and files now accept local paths — they are auto-tunneled
    # in main() before this function is called.  By the time we get here all
    # entries should already be URLs.

    content = build_content(images=images, videos=videos, files=files, prompt=prompt)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    messages: List[Dict[str, Any]] = []
    if sys_prompt:
        messages.append({"role": "system", "content": sys_prompt})
    messages.append({"role": "user", "content": content})

    payload: Dict[str, Any] = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "top_p": top_p,
        "max_tokens": max_tokens,
        "stream": stream,
    }

    if thinking:
        payload["thinking"] = {"type": "enabled"}

    if response_format == DEFAULT_RESPONSE_FORMAT:
        payload["response_format"] = {"type": response_format}

    response = requests.post(
        API_BASE_URL, headers=headers, json=payload, stream=stream, timeout=120
    )

    if response.status_code == 401 or response.status_code == 403:
        try:
            error_data = response.json()
            error_msg = error_data.get("error", {}).get("message", str(error_data))
        except Exception:
            error_msg = response.text
        return {
            "success": False,
            "error": (
                f"API authentication failed: {error_msg}. "
                "Please check your ZHIPU_API_KEY at: https://bigmodel.cn/usercenter/proj-mgmt/apikeys. "
                "认证失败，请检查或更新你的 ZHIPU_API_KEY。"
            ),
            "status_code": response.status_code,
        }

    if response.status_code != 200:
        try:
            error_data = response.json()
        except Exception:
            error_data = response.text
        return {
            "success": False,
            "error": f"API request failed: {response.status_code} - {error_data}",
            "status_code": response.status_code,
        }

    if stream:
        full_content = ""
        for line in response.iter_lines():
            if not line:
                continue
            line = line.decode("utf-8")
            if line.startswith("data: "):
                data = line[6:]
                if data == "[DONE]":
                    break
                try:
                    chunk = json.loads(data)
                    delta = chunk.get("choices", [{}])[0].get("delta", {})
                    if "content" in delta:
                        full_content += delta["content"]
                        print(delta["content"], end="", flush=True)
                except json.JSONDecodeError:
                    continue
        print()
        return {"success": True, "caption": full_content}

    result = response.json()
    caption_text = ""
    finish_reason = ""
    if result.get("choices"):
        caption_text = result["choices"][0].get("message", {}).get("content", "")
        finish_reason = result["choices"][0].get("finish_reason", "")

    out = {
        "success": True,
        "caption": caption_text,
        "usage": result.get("usage", {}),
    }
    if finish_reason == "sensitive":
        out["warning"] = "Content blocked by safety review (finish_reason: sensitive)"
    return out


def main():
    parser = argparse.ArgumentParser(
        description="Generate captions for images, videos, and documents using GLM-4.6V"
    )

    # Input groups (mutually exclusive — API limitation)
    input_group = parser.add_argument_group("Input (pick one)")
    input_group.add_argument(
        "--images",
        "-i",
        nargs="+",
        help="Image paths or URLs (supports multiple, base64 OK)",
    )
    input_group.add_argument(
        "--videos", "-v", nargs="+", help="Video paths or URLs (mp4/mkv/mov)"
    )
    input_group.add_argument(
        "--files",
        "-f",
        nargs="+",
        help="Document paths or URLs (pdf/docx/txt/xlsx/pptx/jsonl)",
    )

    # Model parameters (defaults per GLM-4.6V official spec)
    parser.add_argument("--prompt", "-p", default=DEFAULT_PROMPT, help="Custom prompt")
    parser.add_argument(
        "--model",
        "-m",
        default=DEFAULT_MODEL,
        help="Model name (default: glm-5v-turbo)",
    )
    parser.add_argument(
        "--temperature",
        "-t",
        type=float,
        default=0.8,
        help="Sampling temperature 0-1 (default: 0.8)",
    )
    parser.add_argument(
        "--top-p",
        type=float,
        default=0.6,
        help="Nucleus sampling 0.01-1.0 (default: 0.6)",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=None,
        help="Max output tokens (default: model's default, max 32768)",
    )
    parser.add_argument(
        "--thinking", action="store_true", help="Enable thinking/reasoning mode"
    )
    parser.add_argument(
        "--response-format",
        nargs="?",
        const=DEFAULT_RESPONSE_FORMAT,
        default=None,
        choices=[DEFAULT_RESPONSE_FORMAT],
        help=(
            "Enable structured output mode. If the flag is present without a value, "
            f"it defaults to '{DEFAULT_RESPONSE_FORMAT}'."
        ),
    )
    parser.add_argument(
        "--sys-prompt",
        help=(
            "Optional system prompt inserted before the user message. "
            "Recommended for defining the expected JSON schema when using structured output."
        ),
    )

    # Output options
    parser.add_argument("--output", "-o", help="Save result JSON to file")
    parser.add_argument(
        "--pretty", action="store_true", help="Pretty-print JSON output"
    )
    parser.add_argument("--stream", action="store_true", help="Enable streaming output")

    args = parser.parse_args()

    # Validate: exactly one input type required
    input_count = sum(1 for x in [args.images, args.videos, args.files] if x)
    if input_count == 0:
        parser.error("Must provide one of: --images, --videos, --files")
    if input_count > 1:
        parser.error(
            "--images, --videos, and --files are mutually exclusive (files cannot mix with images/videos)"
        )

    # Resolve default max_tokens from MODEL_MAX_TOKENS table
    resolved_max_tokens = args.max_tokens
    if resolved_max_tokens is None:
        model_key = args.model.lower()
        model_limits = MODEL_MAX_TOKENS.get(model_key)
        resolved_max_tokens = model_limits["default"] if model_limits else 4096

    # ------------------------------------------------------------------
    # Auto-tunnel: if --videos or --files contain local paths, spin up a
    # temporary HTTP server + cloudflare quick tunnel so the GLM-V API
    # can fetch them over HTTPS.
    # ------------------------------------------------------------------
    items_needing_tunnel = []
    target_attr = None  # "videos" or "files"

    if args.videos and _has_local_paths(args.videos):
        items_needing_tunnel = [v for v in args.videos if not _is_url(v)]
        target_attr = "videos"
    elif args.files and _has_local_paths(args.files):
        items_needing_tunnel = [f for f in args.files if not _is_url(f)]
        target_attr = "files"

    if items_needing_tunnel:
        from tunnel_server import LocalTunnel

        print(
            f"[tunnel] Exposing {len(items_needing_tunnel)} local file(s) via cloudflare tunnel...",
            file=sys.stderr,
        )
        try:
            with LocalTunnel(items_needing_tunnel) as tunnel:
                print(f"[tunnel] Public URL: {tunnel.tunnel_url}", file=sys.stderr)

                # Replace local paths with tunnel URLs
                if target_attr == "videos":
                    args.videos = _resolve_to_urls(args.videos, tunnel)
                elif target_attr == "files":
                    args.files = _resolve_to_urls(args.files, tunnel)

                result = _run_caption(args, resolved_max_tokens)
        except FileNotFoundError as e:
            result = {"success": False, "error": str(e)}
        except Exception as e:
            result = {"success": False, "error": f"Tunnel setup failed: {e}"}
    else:
        # No tunneling needed (all URLs, or images which use base64)
        result = _run_caption(args, resolved_max_tokens)

    # Output result
    if args.stream:
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"\nResult saved to: {args.output}", file=sys.stderr)
        return

    indent = 2 if args.pretty else None
    print(json.dumps(result, ensure_ascii=False, indent=indent))

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\nResult saved to: {args.output}", file=sys.stderr)


def _run_caption(args, resolved_max_tokens: int) -> Dict[str, Any]:
    """Thin wrapper around caption() that maps argparse args to kwargs."""
    try:
        return caption(
            images=args.images,
            videos=args.videos,
            files=args.files,
            prompt=args.prompt,
            model=args.model,
            temperature=args.temperature,
            top_p=args.top_p,
            max_tokens=resolved_max_tokens,
            thinking=args.thinking,
            stream=args.stream,
            response_format=args.response_format,
            sys_prompt=args.sys_prompt,
        )
    except Exception as e:
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    main()
