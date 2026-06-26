"""Shared utilities for Poe Connector: authentication, error handling, file encoding."""

import sys
import io
import base64
import mimetypes
import time
import json
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

try:
    import openai
except ImportError:
    print("Error: openai package not installed. Run: pip install openai", file=sys.stderr)
    sys.exit(1)

POE_BASE_URL = "https://api.poe.com/v1"

MIME_MAP = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".webp": "image/webp",
    ".svg": "image/svg+xml",
    ".pdf": "application/pdf",
    ".mp3": "audio/mp3",
    ".wav": "audio/wav",
    ".mp4": "video/mp4",
    ".webm": "video/webm",
}

MAX_RETRIES = 3
INITIAL_BACKOFF_S = 0.5

_config_cache: dict | None = None
SKILL_ROOT = Path(__file__).resolve().parent.parent


def load_config() -> dict:
    """Load poe_config.json from the skill root. Returns empty dict on failure."""
    global _config_cache
    if _config_cache is not None:
        return _config_cache

    config_path = SKILL_ROOT / "poe_config.json"
    if config_path.exists():
        try:
            _config_cache = json.loads(config_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            _config_cache = {}
    else:
        _config_cache = {}
    return _config_cache


def get_default_model(task_type: str) -> str | None:
    """Get the default model for a task type (chat/image/video/audio)."""
    cfg = load_config()
    return cfg.get("defaults", {}).get(task_type)


def get_available_models(task_type: str) -> list[str]:
    """Get the configured model list for a task type."""
    cfg = load_config()
    return cfg.get("models", {}).get(task_type, [])


def get_chat_options() -> dict:
    """Get default chat options (stream, max_tokens, temperature)."""
    cfg = load_config()
    return cfg.get("chat_options", {})


def _load_key_from_openclaw_json() -> str | None:
    """Try to read POE_API_KEY from ~/.openclaw/openclaw.json."""
    config_path = Path.home() / ".openclaw" / "openclaw.json"
    if not config_path.exists():
        return None
    try:
        raw = config_path.read_text(encoding="utf-8").lstrip("\ufeff")
        cfg = json.loads(raw)
        return (
            cfg.get("skills", {})
            .get("entries", {})
            .get("poe-connector", {})
            .get("env", {})
            .get("POE_API_KEY")
        )
    except (json.JSONDecodeError, OSError):
        return None


def get_client() -> openai.OpenAI:
    """Create an OpenAI client configured for the Poe API."""
    api_key = _load_key_from_openclaw_json()
    if not api_key:
        print(
            "Error: POE_API_KEY is not configured.\n"
            "Get your key at https://poe.com/api/keys, then add it to:\n"
            "\n"
            "  ~/.openclaw/openclaw.json\n"
            '  { "skills": { "entries": { "poe-connector": { "env": { "POE_API_KEY": "your-key" } } } } }',
            file=sys.stderr,
        )
        sys.exit(1)
    return openai.OpenAI(api_key=api_key, base_url=POE_BASE_URL)


def encode_file(file_path: str) -> dict:
    """Encode a local file as a base64 data-URL content block for the messages API.

    Returns an OpenAI-compatible content block (image_url or file type).
    """
    p = Path(file_path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    suffix = p.suffix.lower()
    mime = MIME_MAP.get(suffix) or mimetypes.guess_type(file_path)[0] or "application/octet-stream"
    b64 = base64.b64encode(p.read_bytes()).decode("utf-8")
    data_url = f"data:{mime};base64,{b64}"

    if mime.startswith("image/"):
        return {"type": "image_url", "image_url": {"url": data_url}}
    else:
        return {"type": "file", "file": {"filename": p.name, "file_data": data_url}}


def build_file_messages(text: str, file_paths: list[str]) -> list[dict]:
    """Build a multimodal user message with text and attached files."""
    content: list[dict] = [{"type": "text", "text": text}]
    for fp in file_paths:
        content.append(encode_file(fp))
    return [{"role": "user", "content": content}]


def handle_api_error(e: openai.APIError) -> None:
    """Print a user-friendly error message for known Poe API errors."""
    code = getattr(e, "status_code", None)
    messages = {
        401: "Authentication failed — check your POE_API_KEY.",
        402: "Insufficient credits — purchase add-on points at https://poe.com/api/keys",
        403: "Permission denied — this model or action is not allowed.",
        404: "Model not found — run poe_models.py --list to see available models.",
        408: "Request timed out — the model took too long to respond. Try again.",
        413: "Request too large — reduce the input size (tokens exceed context window).",
        429: "Rate limit hit (500 rpm). Retrying with backoff...",
        500: "Provider error — the upstream model had an issue. Try again shortly.",
        502: "Upstream error — the model backend is temporarily unavailable.",
        529: "Service overloaded — transient traffic spike. Retry shortly.",
    }
    msg = messages.get(code, f"API error (HTTP {code}): {e}")
    print(f"Error: {msg}", file=sys.stderr)


def retry_on_rate_limit(func, *args, **kwargs):
    """Call *func* with automatic retry on 429 rate-limit errors."""
    backoff = INITIAL_BACKOFF_S
    for attempt in range(MAX_RETRIES + 1):
        try:
            return func(*args, **kwargs)
        except openai.RateLimitError:
            if attempt == MAX_RETRIES:
                print("Error: Rate limit exceeded after maximum retries.", file=sys.stderr)
                sys.exit(1)
            wait = backoff * (2 ** attempt)
            print(f"Rate limited. Retrying in {wait:.1f}s... (attempt {attempt + 1}/{MAX_RETRIES})", file=sys.stderr)
            time.sleep(wait)
        except openai.APIError as e:
            handle_api_error(e)
            sys.exit(1)


def parse_extra_body(raw: str | None) -> dict | None:
    """Parse a JSON string into a dict for extra_body, or return None."""
    if not raw:
        return None
    try:
        return json.loads(raw.lstrip("\ufeff").strip())
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON for --extra: {e}", file=sys.stderr)
        sys.exit(1)
