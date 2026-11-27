"""
docx_attachments.py — Gmail .docx attachment text extraction for homebase

Generic across any feature that reads Gmail messages (school, bills, ...),
exactly like pdf_attachments.py alongside it.

WHY THIS EXISTS. homebase extracted PDFs and images and nothing else, so a
Word attachment matched neither collector and vanished without a log line:
`pdf_text` came back "" and `image_paths` [], and the runner reported success.

Observed 2026-09-23. "October Newsletter 2026" from the school was a
378 KB .docx behind a 454-character cover note. The cover note mentioned a
snack sign-up, so the school runner announced the snack sign-up and nothing
else. Inside the file, unread: Parent-Teacher Conferences on Oct 23, pumpkin
decorating Oct 26, Harvest party Oct 30 and two classmate birthdays. Same
shape as the `none`-bucket and `has:attachment` silent drops — the run looked
clean from the outside, which is what makes this class of bug expensive.

Text is folded into the SAME `pdf_text` field the school runner already
reads. extract.md tells the model to read `body`, `pdf_text` and
`image_paths`; a fourth key would arrive in the payload and be ignored,
because nothing in the prompt mentions it. Widening an existing field the
prompt already trusts is what makes this fix prompt-free.

PURE STDLIB ON PURPOSE. python-docx is not in the venv, and a dependency
added for one newsletter a month is a dependency that breaks a 6am run on
some future reinstall. A .docx is a zip holding word/document.xml, and that
is enough to read one.

A legacy .doc is NOT a zip and cannot be read this way. It is logged rather
than dropped, because the thing worth fixing about the incident above was the
silence, not only the format.
"""

from __future__ import annotations

import base64
import html
import io
import logging
import re
import zipfile
from typing import Dict, List

logger = logging.getLogger(__name__)

DOCX_MIME = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
DOC_MIME = "application/msword"


def _xml_to_text(xml: str) -> str:
    """Flatten WordprocessingML to plain text, keeping line and cell breaks.

    Order matters: the structural tags have to become whitespace BEFORE the
    blanket tag strip, or every paragraph in the document runs together into
    one line and the dates inside a table lose the rows that separate them.
    """
    xml = re.sub(r"<w:tab\b[^>]*/>", "\t", xml)
    xml = re.sub(r"<w:br\b[^>]*/>", "\n", xml)
    xml = xml.replace("</w:tc>", "\t")   # table cell
    xml = xml.replace("</w:tr>", "\n")   # table row
    xml = xml.replace("</w:p>", "\n")    # paragraph
    text = re.sub(r"<[^>]+>", "", xml)
    text = html.unescape(text)

    lines = [re.sub(r"[ \t]+", " ", ln).strip() for ln in text.split("\n")]
    out: List[str] = []
    for ln in lines:
        if ln or (out and out[-1]):
            out.append(ln)
    return "\n".join(out).strip()


# A real school newsletter's document.xml is well under 1 MB. The cap stops a
# small, highly compressed attachment from inflating to gigabytes in memory;
# fetching doesn't mark mail processed, so one such email would otherwise kill
# every retry.
MAX_DOCUMENT_XML_BYTES = 20 * 1024 * 1024


def extract_docx_text_from_bytes(docx_bytes: bytes) -> str:
    """Extract plain text from raw .docx bytes using stdlib zipfile."""
    try:
        with zipfile.ZipFile(io.BytesIO(docx_bytes)) as z:
            info = z.getinfo("word/document.xml")
            if info.file_size > MAX_DOCUMENT_XML_BYTES:
                logger.warning(f"[docx_extract] document.xml claims {info.file_size} bytes; skipped")
                return ""
            with z.open(info) as f:
                raw = f.read(MAX_DOCUMENT_XML_BYTES + 1)
            if len(raw) > MAX_DOCUMENT_XML_BYTES:
                logger.warning("[docx_extract] document.xml inflates past the cap; skipped")
                return ""
            xml = raw.decode("utf-8", errors="replace")
    except Exception as exc:
        logger.warning(f"[docx_extract] could not open .docx: {exc}")
        return ""
    try:
        return _xml_to_text(xml)
    except Exception as exc:
        logger.warning(f"[docx_extract] could not flatten document.xml: {exc}")
        return ""


def _collect_docx_parts(payload: Dict, out: list) -> None:
    """Recursively collect Word parts from a Gmail message payload.

    Matches on filename as well as MIME type: senders that attach through a
    phone or a scanner routinely label a .docx application/octet-stream, and
    a MIME-only match would drop those exactly as silently as before.
    """
    mime = (payload.get("mimeType") or "").lower()
    filename = (payload.get("filename") or "").lower()

    if mime == DOCX_MIME or filename.endswith(".docx"):
        out.append(payload)
    elif mime == DOC_MIME or filename.endswith(".doc"):
        # Not a zip; stdlib cannot read it. Say so rather than drop it.
        logger.warning(
            f"[docx_extract] legacy .doc attachment cannot be read: {filename or '(unnamed)'}"
        )
    else:
        for part in payload.get("parts") or []:
            _collect_docx_parts(part, out)


def extract_docx_attachments(msg_id: str, payload: Dict) -> List[str]:
    """Download and extract text from every .docx attachment in a message.

    Walks the payload directly instead of trusting a has_* flag computed
    elsewhere: the flag is what a silent drop looks like when it is wrong,
    and the walk costs nothing when there is no Word file to find.
    """
    from core import gmail

    parts: list = []
    _collect_docx_parts(payload, parts)

    texts: List[str] = []
    for part in parts:
        body = part.get("body", {}) or {}
        attachment_id = body.get("attachmentId")
        inline_data = body.get("data")

        try:
            if attachment_id:
                raw = gmail.get_attachment(msg_id, attachment_id)
                if not raw:
                    continue
            elif inline_data:
                raw = base64.urlsafe_b64decode(inline_data)
            else:
                continue

            text = extract_docx_text_from_bytes(raw)
            if text:
                texts.append(text)
            else:
                logger.warning(
                    f"[docx_extract] {part.get('filename') or '(unnamed)'} produced no text"
                )
        except Exception as exc:
            logger.warning(f"[docx_extract] {part.get('filename') or '(unnamed)'}: {exc}")
            continue

    return texts
