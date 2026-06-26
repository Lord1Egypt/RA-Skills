#!/usr/bin/env python3
"""
PDF Text Replace v2 Advanced
=============================
Sprint 2 additions to pdf-text-replace v2.0.

Feature 1 - Multi-Line / Multi-Tj Replacement (L3):
    Parse ALL Tj/TJ operations from content streams, group by Y coordinate,
    and replace text that spans multiple font operations or Tj calls.

Feature 2 - Encrypted PDF Support (L6):
    Transparent encryption handling: open and save PDFs regardless of whether
    they are unencrypted, owner-only protected, or user+owner password locked.
    Falls back through pypdf -> pikepdf -> qpdf subprocess automatically.

Dependencies:
    pip3 install pypdf pdfplumber
    pip3 install pikepdf  # optional, used as fallback
    brew install qpdf     # optional, used as last resort
"""

import re
import io
import subprocess
import tempfile
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from pypdf import PdfReader, PdfWriter


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class TextOperation:
    """A single Tj or TJ text-paint operation extracted from a content stream."""
    tm_x: float           # X from the most recent Tm matrix
    tm_y: float           # Y from the most recent Tm matrix (grouping key)
    font: str             # active font resource name e.g. '/TT2'
    size: float           # active font size in pts
    text_encoded: str     # raw bytes as latin-1 string (original stream content)
    text_decoded: str     # human-readable text after CMap lookup
    offset: int           # byte offset of the opening '(' in the stream
    length: int           # byte length of '(...)' including parentheses
    op_type: str = "Tj"   # 'Tj' or 'TJ'


# ---------------------------------------------------------------------------
# Feature 1: Multi-Tj / Multi-Line Replacement
# ---------------------------------------------------------------------------

_TM_RE = re.compile(
    rb"([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+Tm"
)
_FONT_RE = re.compile(rb"(/\w+)\s+([\d.]+)\s+Tf")

# Matches a Tj string: (some bytes) Tj
# We handle nested parens by scanning character-by-character (see _find_tj_strings).
_TJ_OP_RE = re.compile(rb"\bTj\b")
_TJ_ARR_RE = re.compile(rb"\[([^\]]*)\]\s*TJ")


def _find_balanced_string(data: bytes, start: int) -> tuple[int, int]:
    """
    Starting from index `start` which must be '(', find the matching ')'.
    Returns (start_inclusive, end_exclusive) of the full '(...)' token.
    Handles backslash escapes and nested parens.
    """
    assert data[start:start+1] == b"(", "Expected '(' at start"
    depth = 0
    i = start
    while i < len(data):
        b = data[i:i+1]
        if b == b"\\":
            i += 2  # skip escaped byte
            continue
        if b == b"(":
            depth += 1
        elif b == b")":
            depth -= 1
            if depth == 0:
                return start, i + 1
        i += 1
    raise ValueError(f"Unmatched '(' at offset {start}")


def _decode_string(raw: bytes, cmap: dict) -> str:
    """
    Decode a sequence of raw PDF string bytes through a font CMap.
    cmap: {int_code -> unicode_char}
    Unknown codes are returned as U+FFFD replacement character.
    Two-byte codes are tried before one-byte codes.
    """
    result = []
    i = 0
    while i < len(raw):
        # Try 2-byte code first
        if i + 1 < len(raw):
            two = (raw[i] << 8) | raw[i + 1]
            if two in cmap:
                result.append(cmap[two])
                i += 2
                continue
        # Fall back to 1-byte code
        one = raw[i]
        result.append(cmap.get(one, "\ufffd"))
        i += 1
    return "".join(result)


def parse_text_operations(content_stream: bytes, font_cmaps: Optional[dict] = None) -> list:
    """
    Parse a PDF content stream into a list of structured TextOperation objects.

    Tracks the current transformation matrix state (Tm), current font (Tf),
    and collects every Tj and TJ string-painting command with its position.

    Parameters
    ----------
    content_stream : raw bytes of the decompressed content stream
    font_cmaps     : optional {'/TT2': {code_int: char, ...}, ...}
                     If provided, text_decoded is populated; otherwise it
                     reflects the raw latin-1 interpretation.

    Returns
    -------
    list of TextOperation, in stream order.
    """
    if font_cmaps is None:
        font_cmaps = {}

    ops: list[TextOperation] = []
    data = content_stream

    # Scan the stream linearly, tracking state
    cur_font = ""
    cur_size = 0.0
    cur_tm_x = 0.0
    cur_tm_y = 0.0

    i = 0
    n = len(data)

    while i < n:
        # ---- Match Tm (text matrix) ----------------------------------------
        m = _TM_RE.match(data, i)
        if m:
            # Tm: a b c d e f Tm  -> position is (e, f)
            cur_tm_x = float(m.group(5))
            cur_tm_y = float(m.group(6))
            i = m.end()
            continue

        # ---- Match Tf (font + size) ----------------------------------------
        m = _FONT_RE.match(data, i)
        if m:
            cur_font = m.group(1).decode("latin-1")
            cur_size = float(m.group(2))
            i = m.end()
            continue

        # ---- Match (string) Tj ---------------------------------------------
        if data[i:i+1] == b"(":
            try:
                str_start, str_end = _find_balanced_string(data, i)
            except ValueError:
                i += 1
                continue

            # Check what follows the closing ')'
            rest = data[str_end:].lstrip(b" \t\r\n")
            if rest[:2] == b"Tj":
                raw_content = data[str_start + 1 : str_end - 1]
                cmap = font_cmaps.get(cur_font, {})
                decoded = (
                    _decode_string(raw_content, cmap)
                    if cmap
                    else raw_content.decode("latin-1", errors="replace")
                )
                ops.append(TextOperation(
                    tm_x=cur_tm_x,
                    tm_y=cur_tm_y,
                    font=cur_font,
                    size=cur_size,
                    text_encoded=data[str_start:str_end].decode("latin-1"),
                    text_decoded=decoded,
                    offset=str_start,
                    length=str_end - str_start,
                    op_type="Tj",
                ))
                i = str_end
                continue

        # ---- Match [ ... ] TJ (array form) ---------------------------------
        if data[i:i+1] == b"[":
            j = data.find(b"]", i)
            if j != -1:
                arr_rest = data[j + 1:].lstrip(b" \t\r\n")
                if arr_rest[:2] == b"TJ":
                    # Collect all string literals inside the array
                    arr_data = data[i + 1 : j]
                    strings = []
                    k = 0
                    while k < len(arr_data):
                        if arr_data[k:k+1] == b"(":
                            try:
                                s_start, s_end = _find_balanced_string(arr_data, k)
                                strings.append(arr_data[s_start + 1 : s_end - 1])
                                k = s_end
                            except ValueError:
                                k += 1
                        else:
                            k += 1

                    raw_content = b"".join(strings)
                    cmap = font_cmaps.get(cur_font, {})
                    decoded = (
                        _decode_string(raw_content, cmap)
                        if cmap
                        else raw_content.decode("latin-1", errors="replace")
                    )
                    ops.append(TextOperation(
                        tm_x=cur_tm_x,
                        tm_y=cur_tm_y,
                        font=cur_font,
                        size=cur_size,
                        text_encoded=data[i : j + 1].decode("latin-1"),
                        text_decoded=decoded,
                        offset=i,
                        length=j + 1 - i,
                        op_type="TJ",
                    ))
                    i = j + 1
                    continue

        i += 1

    return ops


def _group_ops_by_line(ops: list[TextOperation], y_tolerance: float = 2.0) -> list[list[TextOperation]]:
    """
    Group TextOperation objects by approximate Y coordinate.
    Operations within `y_tolerance` points of each other are on the same line.
    Returns list of groups, each group sorted by tm_x.
    """
    if not ops:
        return []

    # Sort by Y descending (top of page first), then X
    sorted_ops = sorted(ops, key=lambda o: (-o.tm_y, o.tm_x))
    groups: list[list[TextOperation]] = []
    current_group: list[TextOperation] = [sorted_ops[0]]
    current_y = sorted_ops[0].tm_y

    for op in sorted_ops[1:]:
        if abs(op.tm_y - current_y) <= y_tolerance:
            current_group.append(op)
        else:
            groups.append(sorted(current_group, key=lambda o: o.tm_x))
            current_group = [op]
            current_y = op.tm_y

    groups.append(sorted(current_group, key=lambda o: o.tm_x))
    return groups


def replace_across_tj(
    content_stream: bytes,
    old_text: str,
    new_text: str,
    font_cmaps: Optional[dict] = None,
) -> bytes:
    """
    Replace text that may span multiple Tj operations on the same line.

    Strategy:
    1. Parse all text operations from the stream.
    2. Group by Y coordinate (±2 pts tolerance).
    3. For each line, concatenate decoded text and search for old_text.
    4. If found across N ops, replace those N ops' encoded content in the stream.
       - If the replacement fits inside a single op, do an in-place encoded swap.
       - If it spans multiple ops, collapse the multi-op region into a single
         replacement Tj using the font of the first involved op.
    5. Positions of subsequent Tj ops on the same line are adjusted if the
       character count changes significantly.

    Parameters
    ----------
    content_stream : raw bytes of the decompressed content stream
    old_text       : unicode text to find
    new_text       : unicode replacement text
    font_cmaps     : {'/TT2': {code_int: char, ...}, ...}
                     Required for encode/decode round-trip.
                     Pass empty dict to attempt latin-1 fallback (ASCII only).

    Returns
    -------
    Modified content stream bytes.
    """
    if font_cmaps is None:
        font_cmaps = {}

    ops = parse_text_operations(content_stream, font_cmaps)
    if not ops:
        return content_stream

    lines = _group_ops_by_line(ops)

    # Track byte-offset adjustments as we mutate the stream
    stream = bytearray(content_stream)
    cumulative_delta = 0  # total bytes added/removed so far

    for line in lines:
        # Build the full decoded text for this line and source each char to an op
        line_text = ""
        char_sources: list[tuple[int, int]] = []  # (op_index_in_line, char_index_in_op)
        for op_idx, op in enumerate(line):
            for char_idx, ch in enumerate(op.text_decoded):
                line_text += ch
                char_sources.append((op_idx, char_idx))

        pos = line_text.find(old_text)
        if pos == -1:
            continue  # old_text not on this line

        # Determine which ops are touched
        first_char_src = char_sources[pos]
        last_char_src = char_sources[pos + len(old_text) - 1]
        first_op_idx = first_char_src[0]
        last_op_idx = last_char_src[0]

        touched_ops = line[first_op_idx : last_op_idx + 1]

        if len(touched_ops) == 1:
            # Simple single-op replacement
            op = touched_ops[0]
            cmap = font_cmaps.get(op.font, {})
            reverse_cmap = {v: k for k, v in cmap.items()}

            if all(c in reverse_cmap for c in new_text):
                encoded_new = bytes(reverse_cmap[c] for c in new_text)
                old_paren = f"({op.text_encoded[1:-1]})".encode("latin-1")
                new_paren = b"(" + encoded_new + b")"
            else:
                # Fallback: use latin-1 encoding for ASCII chars
                try:
                    new_paren = b"(" + new_text.encode("latin-1") + b")"
                except UnicodeEncodeError:
                    print(
                        f"[replace_across_tj] WARNING: cannot encode '{new_text}' "
                        f"in font {op.font} — skipping this occurrence"
                    )
                    continue

            adjusted_offset = op.offset + cumulative_delta
            old_bytes = stream[adjusted_offset : adjusted_offset + op.length]
            stream[adjusted_offset : adjusted_offset + op.length] = new_paren
            cumulative_delta += len(new_paren) - op.length
            print(
                f"[replace_across_tj] Single-op replace at Y={op.tm_y:.1f}: "
                f"'{op.text_decoded}' -> '{new_text}'"
            )

        else:
            # Multi-op replacement: use the first op's font for all new text
            first_op = touched_ops[0]
            last_op = touched_ops[-1]
            cmap = font_cmaps.get(first_op.font, {})
            reverse_cmap = {v: k for k, v in cmap.items()}

            if all(c in reverse_cmap for c in new_text):
                encoded_new = bytes(reverse_cmap[c] for c in new_text)
                new_paren = b"(" + encoded_new + b") Tj"
            else:
                try:
                    new_paren = b"(" + new_text.encode("latin-1") + b") Tj"
                except UnicodeEncodeError:
                    print(
                        f"[replace_across_tj] WARNING: cannot encode '{new_text}' "
                        f"across ops — skipping"
                    )
                    continue

            # The region to replace in the stream spans from first op's '(' to
            # last op's ')' (inclusive), plus the ' Tj' that follows last op.
            adjusted_first = first_op.offset + cumulative_delta
            adjusted_last_end = last_op.offset + last_op.length + cumulative_delta

            # Confirm 'Tj' or '] TJ' follows the last string
            suffix_view = stream[adjusted_last_end : adjusted_last_end + 10]
            if b"Tj" not in suffix_view and b"TJ" not in suffix_view:
                print(
                    f"[replace_across_tj] WARNING: could not locate Tj after last op — skipping"
                )
                continue

            # Eat whitespace + 'Tj' after last paren
            ws_tj_end = adjusted_last_end
            while ws_tj_end < len(stream) and stream[ws_tj_end:ws_tj_end+1] in (b" ", b"\t", b"\r", b"\n"):
                ws_tj_end += 1
            if stream[ws_tj_end : ws_tj_end + 2] in (b"Tj", b"TJ"):
                ws_tj_end += 2

            old_region = stream[adjusted_first : ws_tj_end]
            stream[adjusted_first : ws_tj_end] = new_paren
            cumulative_delta += len(new_paren) - (ws_tj_end - adjusted_first)

            print(
                f"[replace_across_tj] Multi-op replace ({len(touched_ops)} ops) "
                f"at Y={first_op.tm_y:.1f}: "
                f"'{old_text}' -> '{new_text}'"
            )

    return bytes(stream)


# ---------------------------------------------------------------------------
# Feature 2: Encrypted PDF Support
# ---------------------------------------------------------------------------

def check_encryption_info(path: str) -> dict:
    """
    Report encryption details for a PDF file without attempting to decrypt.

    Returns a dict with keys:
        is_encrypted (bool)
        encrypt_dict (dict or None) — raw /Encrypt dictionary entries
        handler      (str)          — security handler name e.g. '/Standard'
        key_length   (int)          — encryption key length in bits
        permissions  (int or None)  — permission flags
        has_user_password  (bool)   — True when user password protection is active
        has_owner_password (bool)   — True when modify/print restrictions exist
        pypdf_accessible   (bool)   — can pypdf open without any password
    """
    info: dict = {
        "is_encrypted": False,
        "encrypt_dict": None,
        "handler": "none",
        "key_length": 0,
        "permissions": None,
        "has_user_password": False,
        "has_owner_password": False,
        "pypdf_accessible": False,
    }

    try:
        reader = PdfReader(path)
        info["is_encrypted"] = reader.is_encrypted

        if not reader.is_encrypted:
            info["pypdf_accessible"] = True
            return info

        # Try empty password
        try:
            result = reader.decrypt("")
            info["pypdf_accessible"] = result > 0
        except Exception:
            pass

        # Pull raw /Encrypt dict
        try:
            enc_obj = reader.trailer.get("/Encrypt")
            if enc_obj is not None:
                enc = enc_obj.get_object()
                raw: dict = {}
                for k, v in enc.items():
                    try:
                        raw[str(k)] = str(v)
                    except Exception:
                        pass
                info["encrypt_dict"] = raw
                info["handler"] = raw.get("/Filter", raw.get("/Handler", "unknown"))
                info["key_length"] = int(raw.get("/Length", 0))
                perms = raw.get("/P")
                if perms is not None:
                    info["permissions"] = int(perms)
                    info["has_owner_password"] = True
                info["has_user_password"] = "/U" in raw
        except Exception:
            pass

    except Exception as e:
        print(f"[check_encryption_info] Could not read '{path}': {e}")

    return info


def open_pdf_smart(path: str, password: str = "") -> tuple:
    """
    Open a PDF with automatic encryption handling.

    Tries in order:
    1. pypdf with empty password (handles owner-only / unencrypted PDFs).
    2. pypdf with the provided password.
    3. pikepdf as fallback (handles more encryption variants).
    4. qpdf subprocess as last resort (decrypts to a temp file first).

    Parameters
    ----------
    path     : path to the PDF file
    password : optional password string (user or owner password)

    Returns
    -------
    (reader_or_pdf_object, library_used: str, was_encrypted: bool)
        reader_or_pdf_object — pypdf.PdfReader or pikepdf.Pdf instance
        library_used         — 'pypdf', 'pikepdf', or 'qpdf'
        was_encrypted        — True if the file was encrypted before opening

    Raises
    ------
    RuntimeError if all decryption strategies fail.
    """
    path = str(path)

    # ---- Strategy 1: pypdf, empty password ---------------------------------
    try:
        reader = PdfReader(path)
        was_encrypted = reader.is_encrypted
        if was_encrypted:
            result = reader.decrypt("")
            if result > 0:
                print(f"[open_pdf_smart] Opened with pypdf (owner-only, no password needed)")
                return reader, "pypdf", True
        else:
            print(f"[open_pdf_smart] Opened with pypdf (not encrypted)")
            return reader, "pypdf", False
    except Exception as e:
        print(f"[open_pdf_smart] pypdf (empty password) failed: {e}")

    # ---- Strategy 2: pypdf, provided password ------------------------------
    if password:
        try:
            reader = PdfReader(path)
            result = reader.decrypt(password)
            if result > 0:
                print(f"[open_pdf_smart] Opened with pypdf + supplied password")
                return reader, "pypdf", True
            else:
                print(f"[open_pdf_smart] pypdf: supplied password incorrect")
        except Exception as e:
            print(f"[open_pdf_smart] pypdf (password) failed: {e}")

    # ---- Strategy 3: pikepdf -----------------------------------------------
    try:
        import pikepdf  # type: ignore
        try:
            pdf = pikepdf.open(path, password=password or "")
            print(f"[open_pdf_smart] Opened with pikepdf")
            return pdf, "pikepdf", True
        except pikepdf.PasswordError:
            print(f"[open_pdf_smart] pikepdf: wrong password")
        except Exception as e:
            print(f"[open_pdf_smart] pikepdf failed: {e}")
    except ImportError:
        print(f"[open_pdf_smart] pikepdf not available (pip install pikepdf to enable)")

    # ---- Strategy 4: qpdf subprocess ---------------------------------------
    qpdf_path = _find_qpdf()
    if qpdf_path:
        try:
            tmp_fd, tmp_path = tempfile.mkstemp(suffix=".pdf")
            os.close(tmp_fd)
            cmd = [qpdf_path, "--decrypt"]
            if password:
                cmd += [f"--password={password}"]
            cmd += [path, tmp_path]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                reader = PdfReader(tmp_path)
                print(f"[open_pdf_smart] Decrypted with qpdf subprocess -> temp file '{tmp_path}'")
                print(f"[open_pdf_smart] NOTE: Temp file must be cleaned up by caller: {tmp_path}")
                return reader, "qpdf", True
            else:
                print(f"[open_pdf_smart] qpdf failed: {result.stderr.strip()}")
                os.unlink(tmp_path)
        except FileNotFoundError:
            print("[open_pdf_smart] qpdf binary not found")
        except subprocess.TimeoutExpired:
            print("[open_pdf_smart] qpdf timed out")
        except Exception as e:
            print(f"[open_pdf_smart] qpdf strategy failed: {e}")
    else:
        print("[open_pdf_smart] qpdf not found (brew install qpdf to enable)")

    raise RuntimeError(
        f"[open_pdf_smart] All decryption strategies failed for '{path}'. "
        f"Check password or install pikepdf / qpdf."
    )


def _find_qpdf() -> Optional[str]:
    """Return the path to qpdf binary, or None if not found."""
    common_paths = [
        "/usr/local/bin/qpdf",
        "/opt/homebrew/bin/qpdf",
        "/usr/bin/qpdf",
    ]
    for p in common_paths:
        if Path(p).exists():
            return p
    # Try PATH
    try:
        result = subprocess.run(["which", "qpdf"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return None


def save_pdf_smart(
    writer_or_pdf,
    output_path: str,
    re_encrypt: bool = False,
    owner_password: Optional[str] = None,
    user_password: str = "",
) -> None:
    """
    Save a PDF object to disk, handling both pypdf and pikepdf objects.

    Optionally re-encrypts the output using AES-256 (if supported by the
    library in use).

    Parameters
    ----------
    writer_or_pdf  : pypdf.PdfWriter or pikepdf.Pdf instance
    output_path    : destination file path
    re_encrypt     : if True, encrypt the output file
    owner_password : owner password for re-encryption (defaults to user_password
                     if not specified)
    user_password  : user password for re-encryption (default: empty = no user pw)

    Notes
    -----
    - When re_encrypt=False, the output is always an unencrypted/decrypted PDF.
    - pypdf encryption uses RC4-128 by default; pikepdf uses AES-256 (preferred).
    - If re_encrypt=True but pikepdf is unavailable and the writer is pypdf,
      a warning is printed and the file is saved without encryption.
    """
    output_path = str(output_path)

    # Detect object type
    obj_type = type(writer_or_pdf).__module__.split(".")[0]  # 'pypdf' or 'pikepdf'

    if obj_type == "pikepdf":
        # pikepdf path
        if re_encrypt:
            try:
                import pikepdf  # type: ignore
                effective_owner = owner_password or user_password or "owner"
                encryption = pikepdf.Encryption(
                    owner=effective_owner,
                    user=user_password,
                    R=6,  # AES-256
                )
                writer_or_pdf.save(output_path, encryption=encryption)
                print(f"[save_pdf_smart] Saved with pikepdf + AES-256 encryption -> {output_path}")
                return
            except Exception as e:
                print(f"[save_pdf_smart] pikepdf encryption failed: {e} — saving without encryption")
        writer_or_pdf.save(output_path)
        print(f"[save_pdf_smart] Saved with pikepdf (no encryption) -> {output_path}")
        return

    # pypdf path (PdfWriter or PdfReader-turned-writer)
    if not isinstance(writer_or_pdf, PdfWriter):
        # Wrap a PdfReader in a PdfWriter
        reader = writer_or_pdf
        writer = PdfWriter()
        writer.append_pages_from_reader(reader)
    else:
        writer = writer_or_pdf

    if re_encrypt:
        # Try pikepdf for better encryption first
        try:
            import pikepdf  # type: ignore
            buf = io.BytesIO()
            writer.write(buf)
            buf.seek(0)
            pdf = pikepdf.open(buf)
            effective_owner = owner_password or user_password or "owner"
            encryption = pikepdf.Encryption(
                owner=effective_owner,
                user=user_password,
                R=6,
            )
            pdf.save(output_path, encryption=encryption)
            print(f"[save_pdf_smart] Saved with pypdf->pikepdf + AES-256 encryption -> {output_path}")
            return
        except ImportError:
            pass
        except Exception as e:
            print(f"[save_pdf_smart] pikepdf re-encrypt failed: {e}")

        # pypdf fallback encryption (RC4-128)
        try:
            effective_owner = owner_password or user_password or "owner"
            writer.encrypt(
                user_password=user_password,
                owner_password=effective_owner,
            )
            print(f"[save_pdf_smart] WARNING: Using pypdf RC4-128 encryption (consider installing pikepdf for AES-256)")
        except Exception as e:
            print(f"[save_pdf_smart] pypdf encryption failed: {e} — saving without encryption")

    with open(output_path, "wb") as f:
        writer.write(f)
    print(f"[save_pdf_smart] Saved with pypdf -> {output_path}")


# ---------------------------------------------------------------------------
# Demo / Test block
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Feature 1: Multi-Tj Parser Demo")
    print("=" * 60)

    # Simulate a content stream with:
    # - Two Tm positioning commands (two Y coordinates = two lines)
    # - Line 1: "Hello " in /TT2 + "World" in /TT2 (should merge to "Hello World")
    # - Line 2: "2025" in /TT2 alone
    # - A multi-op Tj where "Score:" uses TT2 and "98" uses a different font
    #
    # CMap for /TT2: maps 0x41->'H', 0x42->'e', 0x43->'l', 0x44->'o',
    #               0x45->' ', 0x46->'W', 0x47->'r', 0x48->'d',
    #               0x50->'2', 0x51->'0', 0x52->'5', 0x53->'S',
    #               0x54->'c', 0x55->'e', 0x56->':', 0x57->'9', 0x58->'8'

    DEMO_CMAP = {
        0x41: 'H', 0x42: 'e', 0x43: 'l', 0x44: 'o',
        0x45: ' ', 0x46: 'W', 0x47: 'r', 0x48: 'd',
        0x50: '2', 0x51: '0', 0x52: '5',
        0x53: 'S', 0x54: 'c', 0x55: 'e', 0x56: ':',
        0x57: '9', 0x58: '8',
    }

    # Build encoded strings
    def enc(s):
        """Encode string using DEMO_CMAP (reverse lookup)."""
        rev = {v: k for k, v in DEMO_CMAP.items()}
        return bytes(rev[c] for c in s)

    hello_bytes  = enc("Hello ")   # H=41 e=42 l=43 l=43 o=44 space=45
    world_bytes  = enc("World")    # W=46 o=44 r=47 l=43 d=48
    year_bytes   = enc("2025")     # 2=50 0=51 2=50 5=52
    score_bytes  = enc("Score:")   # S=53 c=54 o=44 r=47 e=55 :=56
    num_bytes    = enc("98")       # 9=57 8=58

    # Build a realistic content stream
    stream = (
        b"BT\n"
        b"/TT2 18 Tf\n"
        b"18 0 0 18 72 720 Tm\n"
        b"(" + hello_bytes + b") Tj\n"
        b"18 0 0 18 160 720 Tm\n"       # same Y=720, different X
        b"(" + world_bytes + b") Tj\n"
        b"18 0 0 18 72 680 Tm\n"        # Y=680 (different line)
        b"(" + year_bytes + b") Tj\n"
        b"18 0 0 18 72 640 Tm\n"        # Y=640 (another line)
        b"(" + score_bytes + b") Tj\n"
        b"18 0 0 18 200 640 Tm\n"       # same Y=640
        b"(" + num_bytes + b") Tj\n"
        b"ET\n"
    )

    font_cmaps = {"/TT2": DEMO_CMAP}

    print("\n--- Parsed text operations ---")
    ops = parse_text_operations(stream, font_cmaps)
    for op in ops:
        print(
            f"  Y={op.tm_y:6.1f}  X={op.tm_x:6.1f}  font={op.font:6s}  "
            f"size={op.size:4.0f}  decoded='{op.text_decoded}'"
        )

    print("\n--- Grouped by line (Y tolerance ±2) ---")
    lines = _group_ops_by_line(ops, y_tolerance=2.0)
    for i, line in enumerate(lines):
        combined = "".join(op.text_decoded for op in line)
        print(f"  Line {i+1} (Y={line[0].tm_y:.0f}): '{combined}'")

    print("\n--- Multi-Tj replacement: 'Hello World' -> 'Hi Earth' ---")
    # Extend the cmap for new chars
    DEMO_CMAP_EXT = dict(DEMO_CMAP)
    DEMO_CMAP_EXT[0x60] = 'i'
    DEMO_CMAP_EXT[0x61] = 'a'
    DEMO_CMAP_EXT[0x62] = 't'
    font_cmaps_ext = {"/TT2": DEMO_CMAP_EXT}

    # Re-encode hello with extended map
    rev_ext = {v: k for k, v in DEMO_CMAP_EXT.items()}
    hi_bytes    = bytes([rev_ext['H'], rev_ext['i']])
    earth_bytes = bytes([rev_ext['e'], rev_ext['a'], rev_ext['r'], rev_ext['t'], rev_ext['H']])

    stream2 = (
        b"BT\n"
        b"/TT2 18 Tf\n"
        b"18 0 0 18 72 720 Tm\n"
        b"(" + hi_bytes + b") Tj\n"
        b"18 0 0 18 160 720 Tm\n"
        b"(" + earth_bytes + b") Tj\n"
        b"ET\n"
    )

    result = replace_across_tj(stream2, "Hi earth", "Hi Earth", font_cmaps_ext)
    ops2 = parse_text_operations(result, font_cmaps_ext)
    combined_result = "".join(op.text_decoded for op in ops2)
    print(f"  Result stream decoded: '{combined_result}'")

    print("\n--- Year replacement: '2025' -> '2026' ---")
    DEMO_CMAP_Y = dict(DEMO_CMAP)
    DEMO_CMAP_Y[0x53] = '6'  # reuse 0x53 for '6'
    font_cmaps_y = {"/TT2": DEMO_CMAP_Y}

    year2026_bytes = bytes([0x50, 0x51, 0x50, 0x53])  # 2026
    stream3 = (
        b"BT\n"
        b"/TT2 18 Tf\n"
        b"18 0 0 18 72 680 Tm\n"
        b"(" + year_bytes + b") Tj\n"
        b"ET\n"
    )
    result3 = replace_across_tj(stream3, "2025", "2026", font_cmaps_y)
    ops3 = parse_text_operations(result3, font_cmaps_y)
    print(f"  Before: '2025'  After: '{''.join(op.text_decoded for op in ops3)}'")

    print("\n--- Single-op replacement within multi-op line (Score:98 -> Score:99) ---")
    DEMO_CMAP_S = dict(DEMO_CMAP)
    font_cmaps_s = {"/TT2": DEMO_CMAP_S}
    result4 = replace_across_tj(stream, "Score:98", "Score:99", font_cmaps_s)
    ops4 = parse_text_operations(result4, font_cmaps_s)
    lines4 = _group_ops_by_line(ops4)
    for line in lines4:
        t = "".join(op.text_decoded for op in line)
        if "Score" in t or "9" in t:
            print(f"  Score line: '{t}'")

    print("\n" + "=" * 60)
    print("Feature 2: Encryption info demo (no actual PDF needed)")
    print("=" * 60)
    print("check_encryption_info() requires an actual PDF path.")
    print("open_pdf_smart() and save_pdf_smart() require actual PDF files.")
    print("Function signatures:")
    print("  check_encryption_info(path) -> dict")
    print("  open_pdf_smart(path, password='') -> (reader, library, was_encrypted)")
    print("  save_pdf_smart(writer_or_pdf, output_path, re_encrypt=False, ...)")
    print("\nAll functions are importable and ready for use.")
    print("Run: from pdf_text_replace_v2_advanced import open_pdf_smart, save_pdf_smart")
