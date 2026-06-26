# Copyright (c) 2025 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
PaddleOCR Document Parsing Library

Adapted for local Triton Inference Server deployment.
Compatible with: /v2/models/layout-parsing/infer
"""

import base64
import json
import logging
import os
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urlparse, unquote

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


def _get_env(key: str, *fallback_keys: str) -> str:
    """Get environment variable with fallback keys."""
    value = os.getenv(key, "").strip()
    if value:
        return value
    for fallback in fallback_keys:
        value = os.getenv(fallback, "").strip()
        if value:
            logger.debug(f"Using fallback env var: {fallback}")
            return value
    return ""


def get_config() -> tuple[str, str, str, str]:
    """
    Get API URL and optional Basic Auth credentials from environment.

    Returns:
        tuple of (api_url, token, basic_auth_user, basic_auth_password)
        — token, basic_auth_user, basic_auth_password may be empty strings

    Raises:
        ValueError: If API URL is not configured
    """
    api_url = _get_env("PADDLEOCR_DOC_PARSING_API_URL")
    # Token is optional for local Triton; won't raise if missing
    token = _get_env("PADDLEOCR_ACCESS_TOKEN")
    # Basic Auth credentials for nginx/proxy authentication (optional)
    basic_auth_user = _get_env("PADDLEOCR_BASIC_AUTH_USER")
    basic_auth_password = _get_env("PADDLEOCR_BASIC_AUTH_PASSWORD")

    if not api_url:
        raise ValueError(
            "PADDLEOCR_DOC_PARSING_API_URL not configured. "
            "Set it to your Triton endpoint, e.g.: "
            "http://10.0.133.33:8020/v2/models/layout-parsing/infer"
        )

    # Ensure scheme is present
    if not api_url.startswith(("http://", "https://")):
        api_url = f"http://{api_url}"

    return api_url, token, basic_auth_user, basic_auth_password


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


def _load_file_as_base64(file_path: str) -> str:
    """Load local file and encode as base64."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    return base64.b64encode(path.read_bytes()).decode("utf-8")


# =============================================================================
# API Request  (Triton Inference Server format)
# =============================================================================


def _make_api_request(
    api_url: str,
    token: str,
    params: dict,
    basic_auth_user: str = "",
    basic_auth_password: str = "",
) -> dict:
    """
    Make request to local Triton Inference Server.

    Triton expects:
        POST /v2/models/layout-parsing/infer
        {
            "inputs": [{
                "name": "input",
                "shape": [1, 1],
                "datatype": "BYTES",
                "data": ["<JSON string of actual params>"]
            }],
            "outputs": [{"name": "output"}]
        }

    Triton responds:
        {
            "outputs": [{
                "name": "output",
                "datatype": "BYTES",
                "shape": [1, 1],
                "data": ["<JSON string of actual result>"]
            }]
        }

    The inner JSON string has the same structure as the official cloud API:
        {"logId": "...", "errorCode": 0, "errorMsg": "Success", "result": {...}}
    """
    # Wrap params into Triton request format
    triton_payload = {
        "inputs": [
            {
                "name": "input",
                "shape": [1, 1],
                "datatype": "BYTES",
                "data": [json.dumps(params, ensure_ascii=False)],
            }
        ],
        "outputs": [{"name": "output"}],
    }

    headers = {"Content-Type": "application/json"}
    # Only add token Authorization header if token is provided
    if token:
        headers["Authorization"] = f"token {token}"

    # Basic Auth for nginx/proxy layer (equivalent to curl -u user:password)
    auth = (basic_auth_user, basic_auth_password) if basic_auth_user else None

    timeout = float(os.getenv("PADDLEOCR_DOC_PARSING_TIMEOUT", str(DEFAULT_TIMEOUT)))

    try:
        with httpx.Client(timeout=timeout) as client:
            resp = client.post(api_url, json=triton_payload, headers=headers, auth=auth)
    except httpx.TimeoutException:
        raise RuntimeError(f"API request timed out after {timeout}s")
    except httpx.RequestError as e:
        raise RuntimeError(f"API request failed: {e}")

    # Handle HTTP errors
    if resp.status_code != 200:
        error_detail = (resp.text[:200] or "No response body").strip()
        if resp.status_code == 403:
            raise RuntimeError(f"Authentication failed (403): {error_detail}")
        elif resp.status_code >= 500:
            raise RuntimeError(f"API service error ({resp.status_code}): {error_detail}")
        else:
            raise RuntimeError(f"API error ({resp.status_code}): {error_detail}")

    # Parse Triton outer response
    try:
        triton_resp = resp.json()
    except Exception:
        raise RuntimeError(f"Invalid JSON response: {resp.text[:200]}")

    # Extract inner result from outputs[0].data[0]
    try:
        raw_data_str = triton_resp["outputs"][0]["data"][0]
    except (KeyError, IndexError, TypeError) as e:
        raise RuntimeError(f"Unexpected Triton response structure: {e}. Response: {str(triton_resp)[:200]}")

    # Parse inner JSON string
    try:
        result = json.loads(raw_data_str)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Failed to parse inner result JSON: {e}")

    # Check API-level error code (same as official cloud API)
    if result.get("errorCode", 0) != 0:
        raise RuntimeError(f"API error: {result.get('errorMsg', 'Unknown error')}")

    return result


# =============================================================================
# Main API
# =============================================================================


def parse_document(
    file_path: Optional[str] = None,
    file_url: Optional[str] = None,
    file_type: Optional[int] = None,
    **options,
) -> dict[str, Any]:
    """
    Parse document with local PaddleOCR Triton service.

    Args:
        file_path: Local file path
        file_url: URL to file (passed directly to the service)
        file_type: Optional file type override (0=PDF, 1=Image)
        **options: Additional API options (e.g. visualize, useDocUnwarping)

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
    # Validate input
    if not file_path and not file_url:
        return _error("INPUT_ERROR", "file_path or file_url required")
    if file_type is not None and file_type not in (FILE_TYPE_PDF, FILE_TYPE_IMAGE):
        return _error("INPUT_ERROR", "file_type must be 0 (PDF) or 1 (Image)")

    # Get config
    try:
        api_url, token, basic_auth_user, basic_auth_password = get_config()
    except ValueError as e:
        return _error("CONFIG_ERROR", str(e))

    # Build request params (inner payload, same fields as official API)
    try:
        resolved_file_type: Optional[int] = None
        if file_url:
            params = {"file": file_url}
            resolved_file_type = file_type
        else:
            resolved_file_type = (
                file_type if file_type is not None else _detect_file_type(file_path)
            )
            params = {
                "file": _load_file_as_base64(file_path),
            }

        params.update(options)
        if resolved_file_type is not None:
            params["fileType"] = resolved_file_type
        elif file_url:
            params.pop("fileType", None)

    except (ValueError, FileNotFoundError) as e:
        return _error("INPUT_ERROR", str(e))

    # Call API
    try:
        result = _make_api_request(
            api_url, token, params,
            basic_auth_user=basic_auth_user,
            basic_auth_password=basic_auth_password,
        )
    except RuntimeError as e:
        return _error("API_ERROR", str(e))

    # Extract text — inner JSON structure is identical to official cloud API
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


def _extract_text(result) -> str:
    """Extract text from document parsing result (works for both Triton and cloud API)."""
    if not isinstance(result, dict):
        raise ValueError(
            "Invalid response schema: top-level response must be an object"
        )

    raw_result = result.get("result")
    if not isinstance(raw_result, dict):
        raise ValueError("Invalid response schema: missing result object")

    pages = raw_result.get("layoutParsingResults")
    if not isinstance(pages, list):
        raise ValueError(
            "Invalid response schema: result.layoutParsingResults must be an array"
        )

    texts = []
    for i, page in enumerate(pages):
        if not isinstance(page, dict):
            raise ValueError(
                f"Invalid response schema: result.layoutParsingResults[{i}] must be an object"
            )

        markdown = page.get("markdown")
        if not isinstance(markdown, dict):
            raise ValueError(
                f"Invalid response schema: result.layoutParsingResults[{i}].markdown must be an object"
            )

        text = markdown.get("text")
        if not isinstance(text, str):
            raise ValueError(
                f"Invalid response schema: result.layoutParsingResults[{i}].markdown.text must be a string"
            )
        texts.append(text)

    return "\n\n".join(texts)


def _error(code: str, message: str) -> dict:
    """Create error response."""
    return {
        "ok": False,
        "text": "",
        "result": None,
        "error": {"code": code, "message": message},
    }