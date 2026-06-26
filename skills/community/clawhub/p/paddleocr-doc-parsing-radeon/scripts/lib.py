"""
PaddleOCR Document Parsing Library — AMD Radeon Cloud Edition

API wrapper for PaddleOCR document parsing, configured for the
AMD Radeon Cloud free PaddleOCR-VL 1.5 endpoint.
"""

import logging
import math
import os
from typing import Any, Optional
from urllib.parse import unquote, urlparse

import httpx

logger = logging.getLogger(__name__)

# =============================================================================
# Constants
# =============================================================================

DEFAULT_TIMEOUT = 600  # seconds (10 minutes)
FILE_TYPE_PDF = 0
FILE_TYPE_IMAGE = 1
IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".tif", ".webp")


# =============================================================================
# Environment
# =============================================================================


def _get_env(key: str) -> str:
    """Get environment variable, defaulting to empty string with whitespace stripped."""
    return os.getenv(key, "").strip()


def _http_timeout_from_env(env_key: str, default_seconds: float) -> float:
    """
    Read HTTP client timeout in seconds from the environment.

    Returns a positive finite float. If the variable is missing, empty,
    unparsable, non-finite, or not greater than zero, logs a warning and uses the
    default_seconds argument value.
    """
    raw = os.getenv(env_key)
    if raw is None:
        return float(default_seconds)
    stripped = raw.strip()
    if not stripped:
        return float(default_seconds)
    try:
        timeout = float(stripped)
    except (ValueError, TypeError):
        logger.warning(
            "Invalid %s value %r; using default %ss",
            env_key,
            raw,
            default_seconds,
        )
        return float(default_seconds)
    if not math.isfinite(timeout) or timeout <= 0:
        logger.warning(
            "%s must be a finite number > 0 (got %r); using default %ss",
            env_key,
            raw,
            default_seconds,
        )
        return float(default_seconds)
    return timeout


def get_config() -> str:
    """
    Get API URL from environment.

    Requires PADDLEOCR_DOC_PARSING_API_URL to be set to the
    AMD Radeon Cloud endpoint URL.

    Returns:
        api_url string

    Raises:
        ValueError: If env var is missing or URL path is invalid
    """
    api_url = _get_env("PADDLEOCR_DOC_PARSING_API_URL")

    if not api_url:
        raise ValueError(
            "PADDLEOCR_DOC_PARSING_API_URL not configured. "
            "Set it to your AMD Radeon Cloud endpoint, e.g. "
            "PADDLEOCR_DOC_PARSING_API_URL=http://host:port/layout-parsing"
        )

    if not api_url.startswith(("http://", "https://")):
        api_url = f"http://{api_url}"

    api_path = urlparse(api_url).path.rstrip("/")
    if not api_path.endswith("/layout-parsing"):
        raise ValueError(
            "PADDLEOCR_DOC_PARSING_API_URL must be a full endpoint ending with "
            "/layout-parsing."
        )

    return api_url


# =============================================================================
# File Utilities
# =============================================================================


def _detect_file_type(path_or_url: str) -> int:
    """Detect file type: 0=PDF, 1=Image."""
    path = path_or_url.lower()
    if path.startswith(("http://", "https://")):
        path = unquote(urlparse(path).path)

    if path.endswith(".pdf"):
        return FILE_TYPE_PDF
    elif path.endswith(IMAGE_EXTENSIONS):
        return FILE_TYPE_IMAGE
    else:
        raise ValueError(f"Unsupported file format: {path_or_url}")


# =============================================================================
# API Request
# =============================================================================


def _make_api_request(api_url: str, params: dict[str, Any]) -> dict[str, Any]:
    """
    Make PaddleOCR document parsing API request.

    Args:
        api_url: API endpoint URL
        params: Request parameters

    Returns:
        API response dict

    Raises:
        RuntimeError: On API errors
    """
    headers = {
        "Content-Type": "application/json",
        "Client-Platform": "official-skill",
    }

    timeout = _http_timeout_from_env(
        "PADDLEOCR_DOC_PARSING_TIMEOUT", float(DEFAULT_TIMEOUT)
    )

    try:
        with httpx.Client(timeout=timeout) as client:
            try:
                resp = client.post(api_url, json=params, headers=headers)
            except TypeError as e:
                raise RuntimeError(
                    "Request parameters cannot be JSON-encoded; use only JSON-serializable "
                    f"option values ({e})"
                ) from e
    except httpx.TimeoutException:
        raise RuntimeError(f"API request timed out after {timeout}s")
    except httpx.RequestError as e:
        raise RuntimeError(f"API request failed: {e}")

    if resp.status_code != 200:
        error_detail = ""
        try:
            error_body = resp.json()
            if isinstance(error_body, dict):
                error_detail = str(error_body.get("errorMsg", "")).strip()
        except Exception:
            pass

        if not error_detail:
            error_detail = (resp.text[:200] or "No response body").strip()

        if resp.status_code == 403:
            raise RuntimeError(f"Authentication failed (403): {error_detail}")
        elif resp.status_code == 429:
            raise RuntimeError(f"API rate limit exceeded (429): {error_detail}")
        elif resp.status_code >= 500:
            raise RuntimeError(
                f"API service error ({resp.status_code}): {error_detail}"
            )
        else:
            raise RuntimeError(f"API error ({resp.status_code}): {error_detail}")

    try:
        result = resp.json()
    except Exception:
        raise RuntimeError(f"Invalid JSON response: {resp.text[:200]}")

    if not isinstance(result, dict):
        raise RuntimeError(
            f"Unexpected JSON shape (expected object): {resp.text[:200]}"
        )

    if result.get("errorCode", 0) != 0:
        msg = result.get("errorMsg", "Unknown error")
        raise RuntimeError(f"API error: {msg}")

    return result


# =============================================================================
# Main API
# =============================================================================


def parse_document(
    file_data: Optional[str] = None,
    file_source: Optional[str] = None,
    file_type: Optional[int] = None,
    **options: Any,
) -> dict[str, Any]:
    """
    Parse document with PaddleOCR.

    Args:
        file_data: Base64-encoded file content (provided by caller)
        file_source: Original file path or URL (used for file type detection)
        file_type: Optional file type override (0=PDF, 1=Image)
        **options: Additional API options

    Returns:
        {
            "ok": True,
            "text": "extracted text...",
            "result": { raw API result },
            "error": None
        }
        or on error:
        {
            "ok": False,
            "text": "",
            "result": None,
            "error": {"code": "...", "message": "..."}
        }
    """
    if file_data is not None and not isinstance(file_data, str):
        return _error("INPUT_ERROR", "file_data must be a string or None")

    if not file_data:
        return _error("INPUT_ERROR", "file_data (base64-encoded) required")
    if file_type is not None and file_type not in (FILE_TYPE_PDF, FILE_TYPE_IMAGE):
        return _error("INPUT_ERROR", "file_type must be 0 (PDF) or 1 (Image)")

    try:
        api_url = get_config()
    except ValueError as e:
        return _error("CONFIG_ERROR", str(e))

    # Build request params
    try:
        resolved_file_type: Optional[int] = None
        if file_source:
            try:
                resolved_file_type = _detect_file_type(file_source)
            except ValueError:
                pass
        if file_type is not None:
            resolved_file_type = file_type

        params = {"file": file_data}
        params["visualize"] = (
            False  # reduce response payload; callers can override via options
        )
        params.update(options)
        if resolved_file_type is not None:
            params["fileType"] = resolved_file_type
        else:
            params.pop("fileType", None)

    except ValueError as e:
        return _error("INPUT_ERROR", str(e))

    try:
        result = _make_api_request(api_url, params)
    except RuntimeError as e:
        return _error("API_ERROR", str(e))

    try:
        text = _extract_text(result)
    except ValueError as e:
        return _error("API_ERROR", str(e))

    return {
        "ok": True,
        "text": text,
        "result": result,
        "error": None,
    }


def _extract_text(result: dict[str, Any]) -> str:
    """Extract text from document parsing result."""
    if not isinstance(result, dict):
        raise ValueError("Invalid API response: top-level response must be an object")

    raw_result = result.get("result")
    if not isinstance(raw_result, dict):
        raise ValueError("Invalid API response: missing 'result' object")

    pages = raw_result.get("layoutParsingResults")
    if not isinstance(pages, list):
        raise ValueError(
            "Invalid API response: result.layoutParsingResults must be an array"
        )

    texts = []
    for i, page in enumerate(pages):
        if not isinstance(page, dict):
            raise ValueError(
                f"Invalid API response: result.layoutParsingResults[{i}] must be an object"
            )

        markdown = page.get("markdown")
        if not isinstance(markdown, dict):
            raise ValueError(
                f"Invalid API response: result.layoutParsingResults[{i}].markdown must be an object"
            )

        text = markdown.get("text")
        if not isinstance(text, str):
            raise ValueError(
                f"Invalid API response: result.layoutParsingResults[{i}].markdown.text must be a string"
            )
        texts.append(text)

    return "\n\n".join(texts)


def _error(code: str, message: str) -> dict[str, Any]:
    """Create error response."""
    return {
        "ok": False,
        "text": "",
        "result": None,
        "error": {"code": code, "message": message},
    }
