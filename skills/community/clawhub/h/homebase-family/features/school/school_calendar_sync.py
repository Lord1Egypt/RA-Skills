"""
school_calendar_sync.py — School Email Attachment Extraction Utility

Refactored: LLM logic removed. This script now focuses on extracting text from
PDF attachments and downloading inline images to provide raw data to the
OpenClaw agent.
"""

from __future__ import annotations

import base64
import logging
import os
import re
import time
from typing import Dict, List

logger = logging.getLogger(__name__)


# ─── Image Extraction ────────────────────────────────────────────────────────

def _collect_image_parts(payload: Dict, out: list) -> None:
    """Recursively collect image/* parts from a Gmail message payload."""
    mime = payload.get("mimeType", "")
    if mime.startswith("image/"):
        out.append(payload)
    elif mime.startswith("multipart/"):
        for part in payload.get("parts", []):
            _collect_image_parts(part, out)


def _mime_to_ext(mime: str) -> str:
    """Map image MIME type to file extension."""
    mapping = {
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "image/gif": ".gif",
        "image/webp": ".webp",
        "image/bmp": ".bmp",
    }
    return mapping.get(mime.lower(), ".jpg")


def download_image_attachments(
    msg_id: str, payload: Dict, save_dir: str
) -> List[str]:
    """Download all image attachments from a Gmail message and save to disk.

    Returns list of absolute file paths for saved images.

    Took a Gmail `service` as its first argument until 2026-09-07; downloads
    now go through core.gmail and the `gog` CLI. The MIME walk is unchanged
    because gog returns Google's own payload shape.
    """
    from core import gmail
    image_parts: list = []
    _collect_image_parts(payload, image_parts)

    os.makedirs(save_dir, exist_ok=True)
    paths: List[str] = []

    for idx, part in enumerate(image_parts):
        filename = part.get("filename", "")
        mime = part.get("mimeType", "image/jpeg")
        ext = _mime_to_ext(mime)

        if filename:
            safe_name = re.sub(r'[^\w.\-]', '_', filename)
        else:
            safe_name = f"inline_{idx}{ext}"
        save_name = f"{msg_id}_{idx}_{safe_name}"
        save_path = os.path.join(save_dir, save_name)

        body = part.get("body", {})
        attachment_id = body.get("attachmentId")
        inline_data = body.get("data")

        try:
            if attachment_id:
                img_bytes = gmail.get_attachment(msg_id, attachment_id)
                if not img_bytes:
                    continue
            elif inline_data:
                img_bytes = base64.urlsafe_b64decode(inline_data)
            else:
                continue

            with open(save_path, "wb") as f:
                f.write(img_bytes)
            paths.append(os.path.abspath(save_path))
        except Exception:
            continue

    return paths


def cleanup_old_attachments(save_dir: str, max_age_days: int = 7) -> None:
    """Remove attachment files older than max_age_days."""
    if not os.path.isdir(save_dir):
        return
    cutoff = time.time() - (max_age_days * 86400)
    for fname in os.listdir(save_dir):
        fpath = os.path.join(save_dir, fname)
        try:
            if os.path.isfile(fpath) and os.path.getmtime(fpath) < cutoff:
                os.unlink(fpath)
        except OSError:
            pass
