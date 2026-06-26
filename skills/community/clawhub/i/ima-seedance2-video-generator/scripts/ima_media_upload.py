"""
IMA Media Upload Module
Version: 1.0.0 (Production Environment Only)

Handles image, video, and audio upload to IMA OSS (imapi.liveme.com).
Two-step process: get presigned URL → upload bytes.

Current in 1.0.0: Production environment only
Current in 1.0.0: Parallel upload support (max 3 concurrent uploads)
"""

import hashlib
import json
import mimetypes
import os
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import List, Tuple

import requests

from ima_constants import APP_ID, APP_KEY, DEFAULT_IM_BASE_URL
from ima_logger import get_logger

logger = get_logger()

# Maximum concurrent uploads (to avoid overwhelming the server)
MAX_CONCURRENT_UPLOADS = 3

FILE_TYPE_MAP = {
    "image": "picture",
    "picture": "picture",
    "video": "video",
    "audio": "audio",
}

CONTENT_TYPE_MAP = {
    # Images
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
    "gif": "image/gif",
    "webp": "image/webp",
    "bmp": "image/bmp",
    # Videos
    "mp4": "video/mp4",
    "avi": "video/x-msvideo",
    "mov": "video/quicktime",
    "mkv": "video/x-matroska",
    "webm": "video/webm",
    "flv": "video/x-flv",
    # Audio
    "mp3": "audio/mpeg",
    "wav": "audio/wav",
    "ogg": "audio/ogg",
    "m4a": "audio/mp4",
    "aac": "audio/aac",
    "flac": "audio/flac",
}

def _gen_sign() -> tuple[str, str, str]:
    """Generate per-request (sign, timestamp, nonce) for IM authentication."""
    nonce = uuid.uuid4().hex[:21]
    ts = str(int(time.time()))
    raw = f"{APP_ID}|{APP_KEY}|{ts}|{nonce}"
    sign = hashlib.sha1(raw.encode()).hexdigest().upper()
    return sign, ts, nonce


def detect_upload_spec(source: str, media_type: str | None = None) -> tuple[str, str, str]:
    """Detect upload f_type, file suffix, and content type for any supported media."""
    ext = Path(source).suffix.lstrip(".").lower()

    if media_type:
        f_type = FILE_TYPE_MAP.get(media_type, "picture")
    elif ext in {"jpg", "jpeg", "png", "gif", "webp", "bmp"}:
        f_type = "picture"
    elif ext in {"mp4", "avi", "mov", "mkv", "webm", "flv"}:
        f_type = "video"
    elif ext in {"mp3", "wav", "ogg", "m4a", "aac", "flac"}:
        f_type = "audio"
    else:
        mime = mimetypes.guess_type(source)[0]
        if mime and mime.startswith("video/"):
            f_type = "video"
        elif mime and mime.startswith("audio/"):
            f_type = "audio"
        else:
            f_type = "picture"

    if not ext:
        ext = {"picture": "jpeg", "video": "mp4", "audio": "mp3"}[f_type]

    content_type = CONTENT_TYPE_MAP.get(ext)
    if not content_type:
        content_type = mimetypes.guess_type(source)[0] or "application/octet-stream"

    return f_type, ext, content_type

def get_upload_token(api_key: str, suffix: str,
                     content_type: str, im_base_url: str = DEFAULT_IM_BASE_URL,
                     f_type: str = "picture") -> dict:
    """
    Step 1: Get presigned upload URL from IM platform (imapi.liveme.com).
    
    **Security Note**: This function sends your IMA API key to imapi.liveme.com,
    which is IMA Studio's dedicated image upload service (separate from the main API).
    
    Why the API key is sent here:
    - imapi.liveme.com is owned and operated by IMA Studio
    - The upload service authenticates requests using the same IMA API key
    - This allows secure, authenticated image uploads without separate credentials
    - Images are stored in IMA's OSS infrastructure and returned as CDN URLs
    
    The two-domain architecture separates concerns:
    - api.imastudio.com: Video generation API (task orchestration)
    - imapi.liveme.com: Media storage API (large file uploads)
    
    See SECURITY.md § "Network Endpoints Used" for full disclosure.
    
    Args:
        api_key: IMA API key (used as both appUid and cmimToken for authentication)
        suffix: File extension (e.g., "jpg", "png")
        content_type: MIME type (e.g., "image/jpeg")
        im_base_url: IM upload service URL (default: https://imapi.liveme.com)
    
    Returns: 
        dict with keys:
        - "ful": Presigned PUT URL for uploading raw bytes
        - "fdl": CDN download URL for the uploaded file
    
    Raises:
        RuntimeError: If upload token request fails
    """
    sign, ts, nonce = _gen_sign()
    
    # Production environment endpoint
    endpoint = "/api/rest/oss/getuploadtoken"
    logger.info("Using PRODUCTION environment upload endpoint: /api/rest/oss/getuploadtoken")
    
    url = f"{im_base_url}{endpoint}"
    params = {
        "appUid": api_key,
        "appId": APP_ID,
        "appKey": APP_KEY,
        "cmimToken": api_key,
        "sign": sign,
        "timestamp": ts,
        "nonce": nonce,
        "fService": "privite",
        "fType": f_type,
        "fSuffix": suffix,
        "fContentType": content_type,
    }
    
    logger.info(f"Getting upload token: suffix={suffix}, fType={f_type}, url={url}")
    
    try:
        resp = requests.get(url, params=params, timeout=30)
        
        # Parse JSON response (don't check HTTP status first!)
        try:
            data = resp.json()
        except ValueError as json_err:
            logger.error(f"Upload token API returned non-JSON response: "
                        f"HTTP {resp.status_code}, body={resp.text[:200]}")
            raise RuntimeError(
                f"Upload token API returned non-JSON response (HTTP {resp.status_code})"
            ) from json_err
        
        # Check business code (0 or 200 = success)
        code = data.get("code")
        if code in (0, 200):
            return data.get("data", {})
        
        # Business error
        message = data.get("message") or "Unknown error"
        error_msg = f"Get upload token failed: code={code}, msg={message}"
        logger.error(error_msg)
        raise RuntimeError(error_msg)
        
    except requests.RequestException as e:
        logger.error(f"Failed to get upload token: {e}")
        raise RuntimeError(f"Failed to get upload token: {e}")

def upload_to_oss(image_bytes: bytes, content_type: str, ful: str) -> None:
    """Step 2: PUT image bytes to the presigned OSS URL."""
    logger.info(f"Uploading {len(image_bytes)} bytes to OSS...")
    
    try:
        resp = requests.put(ful, data=image_bytes, 
                           headers={"Content-Type": content_type}, timeout=60)
        resp.raise_for_status()
        logger.info("Upload successful")
    except requests.RequestException as e:
        logger.error(f"Upload failed: {e}")
        raise RuntimeError(f"Upload failed: {e}")

def is_remote_url(source: str) -> bool:
    """Return True when source is a remote HTTP(S) URL."""
    return source.startswith("https://") or source.startswith("http://")

def normalize_input_media(raw_inputs: list) -> list[str]:
    """
    Normalize CLI media-input values to a strict string array.

    Accepts:
    - space-separated args: a b c
    - comma-separated token: a,b,c
    - JSON array token: ["a","b","c"]
    """
    normalized: list[str] = []
    for token in raw_inputs or []:
        if isinstance(token, list):
            normalized.extend(normalize_input_media(token))
            continue
        if token is None:
            continue
        item = token.strip()
        if not item:
            continue

        if item.startswith("[") and item.endswith("]"):
            try:
                arr = json.loads(item)
                if isinstance(arr, list):
                    normalized.extend(
                        [str(v).strip() for v in arr if isinstance(v, str) and str(v).strip()]
                    )
                    continue
            except json.JSONDecodeError:
                pass

        if "," in item:
            normalized.extend([v.strip() for v in item.split(",") if v.strip()])
        else:
            normalized.append(item)
    return normalized

def prepare_media_url(source: str | bytes, api_key: str,
                      im_base_url: str = DEFAULT_IM_BASE_URL,
                      media_type: str | None = None) -> str:
    """
    Convert media reference to a public URL string.

    - If source is already HTTP(S) URL → return as-is
    - If source is local file/bytes → upload to OSS first
    """
    if isinstance(source, str) and is_remote_url(source):
        logger.info(f"Using URL directly: {source[:50]}...")
        return source

    if not api_key:
        raise RuntimeError("Local media upload requires IMA API key (--api-key)")

    if isinstance(source, str):
        if not os.path.isfile(source):
            raise RuntimeError(f"Media file not found: {source}")

        f_type, ext, content_type = detect_upload_spec(source, media_type=media_type)
        with open(source, "rb") as f:
            file_bytes = f.read()
        logger.info(f"Read local file: {source} ({len(file_bytes)} bytes, f_type={f_type})")
    else:
        f_type = FILE_TYPE_MAP.get(media_type or "image", "picture")
        ext = {"picture": "jpeg", "video": "mp4", "audio": "mp3"}[f_type]
        content_type = CONTENT_TYPE_MAP[ext]
        file_bytes = source
        logger.info(f"Using raw bytes ({len(file_bytes)} bytes, f_type={f_type})")

    token_data = get_upload_token(api_key, ext, content_type, im_base_url, f_type=f_type)
    ful = token_data.get("ful")
    fdl = token_data.get("fdl")

    if not ful or not fdl:
        raise RuntimeError("Upload token missing 'ful' or 'fdl' field")

    upload_to_oss(file_bytes, content_type, ful)
    logger.info(f"Media uploaded: {fdl[:50]}...")
    return fdl

def _upload_single_media(source: str | bytes, api_key: str,
                         im_base_url: str, index: int) -> Tuple[int, str]:
    """
    Helper for parallel upload: upload single media item and return (index, url).
    
    Args:
        source: File path, URL, or bytes
        api_key: IMA API key
        im_base_url: Upload service base URL
        index: Position in original list (for ordering)
    
    Returns:
        Tuple of (index, url)
    
    Raises:
        Exception: If upload fails
    """
    try:
        url = prepare_media_url(source, api_key, im_base_url)
        return (index, url)
    except Exception as e:
        logger.error(f"Failed to upload media #{index + 1}: {e}")
        raise RuntimeError(f"Media #{index + 1} upload failed: {e}") from e

def prepare_media_urls_parallel(sources: List[str | bytes], api_key: str,
                                im_base_url: str = DEFAULT_IM_BASE_URL,
                                max_workers: int = MAX_CONCURRENT_UPLOADS) -> List[str]:
    """
    Convert multiple media references to URLs in parallel.
    
    This function uploads local files concurrently (up to max_workers=3 at once).
    
    Args:
        sources: List of file paths, URLs, or bytes
        api_key: IMA API key
        im_base_url: Upload service base URL
        max_workers: Maximum concurrent uploads (default: 3)
    
    Returns:
        List of URLs in the same order as sources
    
    Raises:
        RuntimeError: If any upload fails
    
    Example:
        sources = ["img1.jpg", "img2.jpg", "img3.jpg"]
        urls = prepare_media_urls_parallel(sources, api_key)
        # Uploads 3 media items in parallel instead of sequentially
    """
    if not sources:
        return []
    
    # Quick path: single item
    if len(sources) == 1:
        return [prepare_media_url(sources[0], api_key, im_base_url)]
    
    # Check if all are already URLs (no upload needed)
    all_remote = all(
        isinstance(src, str) and is_remote_url(src) 
        for src in sources
    )
    
    if all_remote:
        logger.info(f"All {len(sources)} media items are remote URLs, no upload needed")
        return list(sources)
    
    # Parallel upload
    logger.info(f"Uploading {len(sources)} media items in parallel (max {max_workers} concurrent)...")
    
    results = {}
    errors = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all uploads
        future_to_index = {
            executor.submit(_upload_single_media, src, api_key, im_base_url, i): i
            for i, src in enumerate(sources)
        }
        
        # Collect results as they complete
        for future in as_completed(future_to_index):
            index = future_to_index[future]
            try:
                result_index, url = future.result()
                results[result_index] = url
                logger.info(f"Media #{result_index + 1}/{len(sources)} uploaded successfully")
            except Exception as e:
                errors.append(f"Media #{index + 1}: {str(e)}")
    
    # Check for errors
    if errors:
        error_msg = "Parallel upload failed:\n" + "\n".join(errors)
        logger.error(error_msg)
        raise RuntimeError(error_msg)
    
    # Return URLs in original order
    urls = [results[i] for i in range(len(sources))]
    logger.info(f"Successfully uploaded {len(urls)} media items in parallel")
    return urls
