"""
school_calendar_sync.py — School Email PDF Extraction Utility

Refactored: LLM logic removed. This script now focuses on extracting text from 
PDF attachments to provide raw data to the OpenClaw agent.
"""

from __future__ import annotations

import base64
import io
import logging
import re
from typing import Dict, List

logger = logging.getLogger(__name__)


# ─── PDF Extraction ───────────────────────────────────────────────────────────

def extract_pdf_text_from_bytes(pdf_bytes: bytes) -> str:
    """Extract plain text from raw PDF bytes using pypdf."""
    try:
        from pypdf import PdfReader  # type: ignore
        reader = PdfReader(io.BytesIO(pdf_bytes))
        pages = []
        for page in reader.pages:
            text = page.extract_text() or ""
            if text.strip():
                pages.append(text)
        return "\n".join(pages)
    except Exception as exc:
        logger.warning(f"[pdf_extract] pypdf failed: {exc}")
        return ""


def _collect_pdf_parts(payload: Dict, out: list) -> None:
    """Recursively collect application/pdf parts from a Gmail message payload."""
    mime = payload.get("mimeType", "")
    if mime == "application/pdf":
        out.append(payload)
    elif mime.startswith("multipart/"):
        for part in payload.get("parts", []):
            _collect_pdf_parts(part, out)


def extract_pdf_attachments(service, msg_id: str, payload: Dict) -> List[str]:
    """Download and extract text from all PDF attachments in a Gmail message."""
    pdf_parts: list = []
    _collect_pdf_parts(payload, pdf_parts)

    texts: List[str] = []
    for part in pdf_parts:
        filename = part.get("filename", "attachment.pdf")
        body = part.get("body", {})
        attachment_id = body.get("attachmentId")
        inline_data = body.get("data")

        try:
            if attachment_id:
                att = service.users().messages().attachments().get(
                    userId="me", messageId=msg_id, id=attachment_id
                ).execute()
                pdf_bytes = base64.urlsafe_b64decode(att["data"])
            elif inline_data:
                pdf_bytes = base64.urlsafe_b64decode(inline_data)
            else:
                continue

            text = extract_pdf_text_from_bytes(pdf_bytes)
            if text:
                texts.append(text)
        except Exception:
            continue

    return texts
