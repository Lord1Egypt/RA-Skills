from __future__ import annotations

import hashlib
import mimetypes
import os
import re
import secrets
import stat
import time
import unicodedata
import zipfile
from pathlib import Path
from typing import Any

from .common import (
    ALLOWED_EXTENSIONS, DEFAULT_MAX_ARCHIVE_ENTRIES, DEFAULT_MAX_ARCHIVE_UNPACK,
    DEFAULT_MAX_COMPRESSION_RATIO, DEFAULT_MIN_SAFE_EPUB_BYTES, DEFAULT_BATCH_CONFIRM_BOOKS,
    DEFAULT_BATCH_CONFIRM_BYTES, NotFound,
    PocketBookError, UnsafeOperation, _commit_temp_without_overwrite,
    _private_open_exclusive, env_bytes, env_int,
)
from .models import book_summary

def _zip_member_basename(name: str) -> str:
    raw = str(name or "").replace("\\", "/")
    if not raw or raw.startswith("/") or re.match(r"^[A-Za-z]:/", raw):
        raise UnsafeOperation("Archive contains an absolute or empty path")
    parts = [part for part in raw.split("/") if part not in ("", ".")]
    if not parts or any(part == ".." for part in parts):
        raise UnsafeOperation("Archive contains path traversal")
    if any(any(ord(ch) < 32 or ord(ch) == 127 for ch in part) for part in parts):
        raise UnsafeOperation("Archive contains control characters in a filename")
    return sanitize_filename(parts[-1])

def _zip_info_is_symlink(info: zipfile.ZipInfo) -> bool:
    mode = (info.external_attr >> 16) & 0xFFFF
    return bool(mode and stat.S_ISLNK(mode))

def _zip_info_is_unsafe_special(info: zipfile.ZipInfo) -> bool:
    mode = (info.external_attr >> 16) & 0xFFFF
    file_type = stat.S_IFMT(mode) if mode else 0
    return bool(file_type and file_type not in {stat.S_IFREG, stat.S_IFDIR})

def _validate_zip_common(zf: zipfile.ZipFile) -> dict[str, Any]:
    infos = zf.infolist()
    max_entries = env_int("POCKETBOOK_MAX_ARCHIVE_ENTRIES", DEFAULT_MAX_ARCHIVE_ENTRIES)
    if len(infos) > max_entries:
        raise UnsafeOperation(f"Archive contains too many entries ({len(infos)} > {max_entries})")
    total_unpacked = 0
    total_compressed = 0
    for info in infos:
        _zip_member_basename(info.filename)
        if _zip_info_is_symlink(info) or _zip_info_is_unsafe_special(info):
            raise UnsafeOperation("Archive contains a symbolic link or special file")
        if info.flag_bits & 0x1:
            raise UnsafeOperation("Encrypted ZIP entries are not supported")
        if info.is_dir():
            continue
        total_unpacked += int(info.file_size)
        total_compressed += int(info.compress_size)
    max_unpacked = env_bytes("POCKETBOOK_MAX_ARCHIVE_UNPACK_MB", DEFAULT_MAX_ARCHIVE_UNPACK)
    if total_unpacked > max_unpacked:
        raise UnsafeOperation(f"Archive expands beyond configured limit ({max_unpacked // (1024*1024)} MiB)")
    ratio = (total_unpacked / max(1, total_compressed)) if total_unpacked else 1.0
    max_ratio = env_int("POCKETBOOK_MAX_ARCHIVE_RATIO", DEFAULT_MAX_COMPRESSION_RATIO)
    if total_unpacked >= 10 * 1024 * 1024 and ratio > max_ratio:
        raise UnsafeOperation(f"Archive compression ratio is suspicious ({ratio:.1f}x > {max_ratio}x)")
    return {"entries": len(infos), "expandedBytes": total_unpacked, "compressionRatio": ratio}

def _zip_is_epub(zf: zipfile.ZipFile) -> bool:
    try:
        mimetype = zf.getinfo("mimetype")
        container = zf.getinfo("META-INF/container.xml")
    except KeyError:
        return False
    if any(info.is_dir() or _zip_info_is_symlink(info) for info in (mimetype, container)):
        return False
    if mimetype.file_size > 128 or container.file_size <= 0 or container.file_size > 1024 * 1024:
        return False
    try:
        if zf.read(mimetype).strip() != b"application/epub+zip":
            return False
        head = zf.read(container)[:4096].lstrip(b"\xef\xbb\xbf\x00 \t\r\n")
        return b"container" in head.lower()
    except (OSError, RuntimeError, zipfile.BadZipFile):
        return False

def _fictionbook_root_bytes(head: bytes) -> bool:
    data = head[:256 * 1024]
    upper = data.upper()
    if b"<!DOCTYPE" in upper or b"<!ENTITY" in upper:
        return False
    if data.startswith(b"\xef\xbb\xbf"):
        data = data[3:]
    data = data.lstrip(b" \t\r\n")
    decl = re.match(br"<\?xml(?:.|\r|\n)*?\?>", data, re.IGNORECASE)
    if decl:
        data = data[decl.end():].lstrip(b" \t\r\n")
    # Permit a small run of leading XML comments, but nothing executable.
    for _ in range(8):
        if not data.startswith(b"<!--"):
            break
        end = data.find(b"-->")
        if end < 0:
            return False
        data = data[end + 3:].lstrip(b" \t\r\n")
    return re.match(br"<(?:[A-Za-z_][\w.-]*:)?FictionBook(?=[\s/>])", data, re.IGNORECASE) is not None

def is_fb2_xml(path: Path) -> bool:
    """Conservatively recognize a FictionBook root without parsing XML/entities."""
    try:
        with path.open("rb") as fh:
            head = fh.read(256 * 1024)
    except OSError:
        return False
    return _fictionbook_root_bytes(head)

def _validate_native_fb2_zip(zf: zipfile.ZipFile) -> dict[str, Any]:
    infos = [i for i in zf.infolist() if not i.is_dir()]
    if len(infos) != 1:
        raise UnsafeOperation("Native .fb2.zip must contain exactly one FB2 file")
    info = infos[0]
    safe_name = _zip_member_basename(info.filename)
    if not safe_name.casefold().endswith(".fb2"):
        raise UnsafeOperation("Native .fb2.zip does not contain an FB2 file")
    if _zip_info_is_symlink(info) or (info.flag_bits & 0x1):
        raise UnsafeOperation("Native .fb2.zip contains an unsafe entry")
    max_unpacked = env_bytes("POCKETBOOK_MAX_ARCHIVE_UNPACK_MB", DEFAULT_MAX_ARCHIVE_UNPACK)
    if info.file_size > max_unpacked:
        raise UnsafeOperation("Native .fb2.zip expands beyond configured limit")
    ratio = info.file_size / max(1, info.compress_size)
    if info.file_size >= 10 * 1024 * 1024 and ratio > env_int("POCKETBOOK_MAX_ARCHIVE_RATIO", DEFAULT_MAX_COMPRESSION_RATIO):
        raise UnsafeOperation("Native .fb2.zip compression ratio is suspicious")
    try:
        with zf.open(info, "r") as fh:
            head = fh.read(256 * 1024)
    except (OSError, RuntimeError, zipfile.BadZipFile) as exc:
        raise UnsafeOperation("Cannot inspect native .fb2.zip") from exc
    if not _fictionbook_root_bytes(head):
        raise UnsafeOperation("Native .fb2.zip does not contain recognizable FictionBook XML")
    return {"name": safe_name, "bytes": int(info.file_size)}

def canonical_upload_name(path: Path, remote_name: str | None = None) -> str:
    name = sanitize_filename(remote_name or path.name)
    if name.casefold().endswith(".xml") and is_fb2_xml(path):
        return sanitize_filename(Path(name).stem + ".fb2")
    return name

def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    fd = os.open(path, flags)
    try:
        st = os.fstat(fd)
        if not stat.S_ISREG(st.st_mode):
            raise UnsafeOperation("Attachment is not a regular file")
        with os.fdopen(fd, "rb", closefd=False) as fh:
            while True:
                chunk = fh.read(1024 * 1024)
                if not chunk:
                    break
                h.update(chunk)
    finally:
        os.close(fd)
    return h.hexdigest()

def _inbound_roots() -> list[Path]:
    roots: list[Path] = []
    media = os.environ.get("OPENCLAW_MEDIA_DIR", "").strip()
    if media:
        roots.append((Path(media).expanduser() / "inbound").resolve())
    workspace = os.environ.get("OPENCLAW_WORKSPACE_DIR", "").strip()
    if workspace:
        roots.append((Path(workspace).expanduser() / "media" / "inbound").resolve())
    state = os.environ.get("OPENCLAW_STATE_DIR", "").strip()
    if state:
        roots.append((Path(state).expanduser() / "media" / "inbound").resolve())
    roots.append((Path.cwd() / "media" / "inbound").resolve())
    out: list[Path] = []
    seen: set[str] = set()
    for root in roots:
        key = str(root)
        if key not in seen:
            seen.add(key)
            out.append(root)
    return out

def resolve_inbound_attachment(name: str | None = None, within_seconds: int = 1800, roots: list[Path] | None = None) -> dict[str, Any]:
    now = time.time()
    wanted = sanitize_filename(name) if name else None
    candidates: list[Path] = []
    for root in (roots or _inbound_roots()):
        if not root.exists() or not root.is_dir():
            continue
        try:
            iterator = root.rglob("*")
            for path in iterator:
                try:
                    if not path.is_file():
                        continue
                    age = now - path.stat().st_mtime
                    if age < -60 or age > max(1, within_seconds):
                        continue
                    if wanted and path.name != wanted:
                        continue
                    lower = path.name.casefold()
                    ebookish = supported_filename(path.name) or lower.endswith(".zip") or (lower.endswith(".xml") and is_fb2_xml(path))
                    if ebookish:
                        candidates.append(path.resolve())
                except OSError:
                    continue
        except OSError:
            continue
    # De-duplicate staged/state copies only when content is byte-identical.
    # Same-name/same-size files may still be different books.
    unique: dict[tuple[str, int, str], Path] = {}
    for path in sorted(candidates, key=lambda q: -q.stat().st_mtime):
        key = (path.name, path.stat().st_size, _sha256_file(path))
        unique.setdefault(key, path)
    items = list(unique.values())
    if not items:
        raise NotFound("No recent inbound ebook attachment found")
    if len(items) > 1:
        return {
            "ok": False, "ambiguous": True, "count": len(items),
            "candidates": [{"filename": q.name, "bytes": q.stat().st_size, "modified": int(q.stat().st_mtime)} for q in sorted(items, key=lambda q: q.stat().st_mtime, reverse=True)[:10]],
        }
    path = items[0]
    inspected = inspect_upload_input(path)
    return {"ok": True, "path": str(path), "filename": path.name, "bytes": path.stat().st_size, "preflightItem": inspected}

def ensure_inbound_path(path: Path, roots: list[Path] | None = None) -> Path:
    resolved = path.expanduser().resolve()
    if not resolved.is_file():
        raise NotFound(f"Inbound file not found: {resolved}")
    allowed = False
    for root in (roots or _inbound_roots()):
        try:
            resolved.relative_to(root.expanduser().resolve())
            allowed = True
            break
        except ValueError:
            continue
    if not allowed:
        raise UnsafeOperation("upload-inbound accepts files only from OpenClaw inbound media directories")
    return resolved

def compact_upload_preflight(plan: dict[str, Any]) -> dict[str, Any]:
    return {
        "inputs": int(plan.get("inputs") or 0),
        "books": int(plan.get("books") or 0),
        "inputBytes": int(plan.get("inputBytes") or 0),
        "estimatedBookBytes": int(plan.get("estimatedBookBytes") or 0),
        "requiresConfirmation": bool(plan.get("requiresConfirmation")),
        "confirmationReasons": list(plan.get("confirmationReasons") or []),
        "thresholds": dict(plan.get("thresholds") or {}),
        "files": [
            {
                "filename": Path(str(item.get("path") or item.get("filename") or "attachment")).name,
                "books": int(item.get("bookCount") or 0),
                "bytes": int(item.get("bookBytes") or item.get("inputBytes") or 0),
            }
            for item in (plan.get("items") or [])
            if isinstance(item, dict)
        ],
    }

def inspect_upload_input(path: Path) -> dict[str, Any]:
    path = path.expanduser()
    if not path.is_absolute():
        path = Path.cwd() / path
    try:
        st = path.lstat()
    except FileNotFoundError as exc:
        raise NotFound(f"Upload file not found: {path}") from exc
    if stat.S_ISLNK(st.st_mode) or not stat.S_ISREG(st.st_mode):
        raise UnsafeOperation("Upload input must be a regular non-symlink file")
    path = path.absolute()
    input_size = st.st_size
    lower = path.name.casefold()
    is_zip = zipfile.is_zipfile(path)
    if lower.endswith(".epub") and not is_zip:
        raise UnsafeOperation("EPUB is not a valid ZIP container")
    if lower.endswith(".fb2.zip") and not is_zip:
        raise UnsafeOperation(".fb2.zip is not a valid ZIP archive")
    if is_zip:
        try:
            with zipfile.ZipFile(path, "r") as zf:
                common = _validate_zip_common(zf)
                if lower.endswith(".epub"):
                    if not _zip_is_epub(zf):
                        raise UnsafeOperation("EPUB is missing a valid mimetype or META-INF/container.xml")
                    return {
                        "path": str(path), "filename": path.name, "kind": "epub",
                        "action": "direct", "inputBytes": input_size, "bookBytes": input_size,
                        "bookCount": 1, "books": [{"name": sanitize_filename(path.name), "bytes": input_size}],
                    }
                if lower.endswith(".fb2.zip"):
                    _validate_native_fb2_zip(zf)
                    return {
                        "path": str(path), "filename": path.name, "kind": "fb2_zip",
                        "action": "direct", "inputBytes": input_size, "bookBytes": input_size,
                        "bookCount": 1, "books": [{"name": sanitize_filename(path.name), "bytes": input_size}],
                    }
                infos = zf.infolist()
                max_entries = env_int("POCKETBOOK_MAX_ARCHIVE_ENTRIES", DEFAULT_MAX_ARCHIVE_ENTRIES)
                if len(infos) > max_entries:
                    raise UnsafeOperation(f"Archive contains too many entries ({len(infos)} > {max_entries})")
                total_unpacked = 0
                total_compressed = 0
                books: list[dict[str, Any]] = []
                seen_names: set[str] = set()
                for info in infos:
                    if info.is_dir():
                        continue
                    safe_name = _zip_member_basename(info.filename)
                    if _zip_info_is_symlink(info):
                        raise UnsafeOperation("Archive contains a symbolic link")
                    if info.flag_bits & 0x1:
                        raise UnsafeOperation("Encrypted ZIP entries are not supported")
                    total_unpacked += int(info.file_size)
                    total_compressed += int(info.compress_size)
                    aux_stem = Path(safe_name).stem.casefold().strip(" ._-()[]")
                    obvious_aux = aux_stem in {"readme", "license", "licence", "copying", "manifest"}
                    if supported_filename(safe_name) and not obvious_aux:
                        collision_key = unicodedata.normalize("NFC", safe_name).casefold()
                        if collision_key in seen_names:
                            raise UnsafeOperation(f"Archive contains duplicate ebook filename: {safe_name}")
                        seen_names.add(collision_key)
                        books.append({"member": info.filename, "name": safe_name, "bytes": int(info.file_size)})
                max_unpacked = env_bytes("POCKETBOOK_MAX_ARCHIVE_UNPACK_MB", DEFAULT_MAX_ARCHIVE_UNPACK)
                if total_unpacked > max_unpacked:
                    raise UnsafeOperation(f"Archive expands beyond configured limit ({max_unpacked // (1024*1024)} MiB)")
                ratio = (total_unpacked / max(1, total_compressed)) if total_unpacked else 1.0
                max_ratio = env_int("POCKETBOOK_MAX_ARCHIVE_RATIO", DEFAULT_MAX_COMPRESSION_RATIO)
                if total_unpacked >= 10 * 1024 * 1024 and ratio > max_ratio:
                    raise UnsafeOperation(f"Archive compression ratio is suspicious ({ratio:.1f}x > {max_ratio}x)")
                if not books:
                    raise UnsafeOperation("ZIP archive contains no supported ebook files")
                return {
                    "path": str(path), "filename": path.name, "kind": "transport_zip",
                    "action": "extract", "inputBytes": input_size, "bookBytes": sum(x["bytes"] for x in books),
                    "expandedBytes": total_unpacked, "compressionRatio": round(ratio, 2),
                    "entries": len(infos), "ignoredEntries": max(0, len([i for i in infos if not i.is_dir()]) - len(books)),
                    "bookCount": len(books), "books": books,
                }
        except zipfile.BadZipFile as exc:
            raise UnsafeOperation("Invalid ZIP archive") from exc
    if lower.endswith(".xml") and is_fb2_xml(path):
        inner_name = canonical_upload_name(path)
        archive_name = sanitize_filename(inner_name + ".zip")
        return {
            "path": str(path), "filename": path.name, "kind": "fb2_xml",
            "action": "wrap_fb2_zip", "inputBytes": input_size, "bookBytes": input_size,
            "bookCount": 1, "books": [{"name": archive_name, "bytes": input_size}],
            "uploadName": archive_name, "innerName": inner_name,
            "reason": "telegram_xml_fb2_ios_sync_workaround",
        }
    if not supported_filename(path.name):
        raise UnsafeOperation(f"Unsupported ebook file type: {path.name}")
    warnings: list[str] = []
    if lower.endswith(".epub"):
        warnings.append("epub_container_signature_not_detected")
    return {
        "path": str(path), "filename": path.name, "kind": "ebook",
        "action": "direct", "inputBytes": input_size, "bookBytes": input_size,
        "bookCount": 1, "books": [{"name": sanitize_filename(path.name), "bytes": input_size}],
        **({"warnings": warnings} if warnings else {}),
    }

def preflight_upload(paths: list[Path]) -> dict[str, Any]:
    if not paths:
        raise PocketBookError("At least one upload input is required")
    items = [inspect_upload_input(path) for path in paths]
    seen_book_names: set[str] = set()
    for item in items:
        for book in item.get("books", []):
            name = sanitize_filename(str(book.get("name") or ""))
            key = unicodedata.normalize("NFC", name).casefold()
            if key in seen_book_names:
                raise UnsafeOperation(f"Batch contains duplicate output filename: {name}")
            seen_book_names.add(key)
    books = sum(int(item["bookCount"]) for item in items)
    input_bytes = sum(int(item["inputBytes"]) for item in items)
    book_bytes = sum(int(item["bookBytes"]) for item in items)
    book_limit = env_int("POCKETBOOK_BATCH_CONFIRM_BOOKS", DEFAULT_BATCH_CONFIRM_BOOKS)
    byte_limit = env_bytes("POCKETBOOK_BATCH_CONFIRM_MB", DEFAULT_BATCH_CONFIRM_BYTES)
    reasons = []
    if books > book_limit:
        reasons.append("book_count")
    if book_bytes > byte_limit:
        reasons.append("total_bytes")
    return {
        "ok": True, "inputs": len(paths), "books": books, "inputBytes": input_bytes,
        "estimatedBookBytes": book_bytes, "requiresConfirmation": bool(reasons),
        "confirmationReasons": reasons, "thresholds": {"books": book_limit, "bytes": byte_limit},
        "items": items,
    }

def materialize_upload_inputs(paths: list[Path], output_dir: Path) -> dict[str, Any]:
    plan = preflight_upload(paths)
    output_dir = output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    materialized: list[str] = []
    extracted: list[str] = []
    for item in plan["items"]:
        source = Path(item["path"])
        if item["action"] == "direct":
            materialized.append(str(source))
            continue
        if item["action"] == "wrap_fb2_zip":
            target = (output_dir / str(item["uploadName"])).resolve()
            if target.parent != output_dir:
                raise UnsafeOperation("Unsafe FB2 ZIP output path")
            if target.exists():
                raise UnsafeOperation(f"Refusing to overwrite prepared file: {target.name}")
            inner_name = sanitize_filename(str(item["innerName"]))
            part = target.with_name(target.name + f".part.{os.getpid()}.{secrets.token_hex(4)}")
            try:
                with _private_open_exclusive(part) as raw:
                    with zipfile.ZipFile(raw, "w", compression=zipfile.ZIP_STORED) as zf:
                        zf.write(source, arcname=inner_name)
                    raw.flush(); os.fsync(raw.fileno())
                with zipfile.ZipFile(part, "r") as zf:
                    infos = zf.infolist()
                    if len(infos) != 1 or infos[0].filename != inner_name or infos[0].file_size != source.stat().st_size:
                        raise UnsafeOperation("Prepared FB2 ZIP verification failed")
                    with zf.open(infos[0], "r") as fh, source.open("rb") as src:
                        while True:
                            a = fh.read(1024 * 1024); b = src.read(1024 * 1024)
                            if a != b:
                                raise UnsafeOperation("Prepared FB2 ZIP does not preserve original bytes")
                            if not a:
                                break
                _commit_temp_without_overwrite(part, target)
                os.chmod(target, 0o600)
            finally:
                try: part.unlink()
                except FileNotFoundError: pass
            materialized.append(str(target))
            extracted.append(str(target))
            continue
        with zipfile.ZipFile(source, "r") as zf:
            by_name = {info.filename: info for info in zf.infolist()}
            for book in item["books"]:
                info = by_name.get(book["member"])
                if info is None:
                    raise UnsafeOperation("Archive changed between preflight and extraction")
                safe_name = _zip_member_basename(info.filename)
                target = (output_dir / safe_name).resolve()
                if target.parent != output_dir:
                    raise UnsafeOperation("Unsafe extracted ebook path")
                if target.exists():
                    raise UnsafeOperation(f"Refusing to overwrite extracted file: {safe_name}")
                part = target.with_name(target.name + f".part.{os.getpid()}.{secrets.token_hex(4)}")
                written = 0
                try:
                    with zf.open(info, "r") as src, _private_open_exclusive(part) as dst:
                        while True:
                            chunk = src.read(1024 * 1024)
                            if not chunk:
                                break
                            written += len(chunk)
                            if written > int(book["bytes"]):
                                raise UnsafeOperation("Archive entry expanded beyond declared size")
                            dst.write(chunk)
                        dst.flush(); os.fsync(dst.fileno())
                    if written != int(book["bytes"]):
                        raise UnsafeOperation("Archive entry size changed during extraction")
                    _commit_temp_without_overwrite(part, target)
                    os.chmod(target, 0o600)
                finally:
                    try: part.unlink()
                    except FileNotFoundError: pass
                materialized.append(str(target))
                extracted.append(str(target))
    return {"ok": True, "books": len(materialized), "paths": materialized, "extracted": extracted, "preflight": plan}

def package_files(paths: list[Path], output: Path) -> dict[str, Any]:
    if not paths:
        raise PocketBookError("At least one file is required for packaging")
    resolved: list[Path] = []
    names: set[str] = set()
    for raw in paths:
        path = raw.expanduser().resolve()
        try:
            st = path.lstat()
        except FileNotFoundError as exc:
            raise NotFound(f"Local file not found: {raw}") from exc
        if stat.S_ISLNK(st.st_mode) or not stat.S_ISREG(st.st_mode):
            raise UnsafeOperation("Package input must be a regular non-symlink file")
        name = sanitize_filename(path.name)
        key = unicodedata.normalize("NFC", name).casefold()
        if key in names:
            raise UnsafeOperation(f"Duplicate archive filename: {name}")
        names.add(key)
        resolved.append(path)
    output = output.expanduser().resolve()
    if output.suffix.casefold() != ".zip":
        raise UnsafeOperation("Chat/package output must use .zip")
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        raise UnsafeOperation("Refusing to overwrite an existing package")
    tmp = output.with_name(output.name + f".tmp.{os.getpid()}.{secrets.token_hex(4)}")
    try:
        with _private_open_exclusive(tmp) as raw:
            with zipfile.ZipFile(raw, "w", compression=zipfile.ZIP_STORED, allowZip64=True) as zf:
                for path in resolved:
                    zf.write(path, arcname=sanitize_filename(path.name))
            raw.flush()
            os.fsync(raw.fileno())
        _commit_temp_without_overwrite(tmp, output)
        os.chmod(output, 0o600)
    finally:
        try:
            tmp.unlink()
        except FileNotFoundError:
            pass
    return {"ok": True, "path": str(output), "filename": output.name, "bytes": output.stat().st_size, "files": len(resolved)}

def expected_cloud_format(name: str) -> str | None:
    lower = name.casefold()
    if lower.endswith(".fb2.zip"):
        return "fb2.zip"
    if lower.endswith(".epub"):
        return "epub"
    if lower.endswith(".fb2"):
        return "fb2"
    if lower.endswith(".pdf"):
        return "pdf"
    if lower.endswith(".djvu"):
        return "djvu"
    return None

def verify_uploaded_record(
    book: dict[str, Any], expected_name: str, expected_bytes: int, *, expected_fast_hash: str | None = None
) -> dict[str, Any]:
    summary = book_summary(book)
    remote_hash = str(book.get("fast_hash") or "")
    remote_name = str(book.get("name") or "")
    remote_bytes = book.get("bytes")
    remote_format = str(book.get("format") or "").casefold()
    expected_format = expected_cloud_format(expected_name)
    if expected_fast_hash and remote_hash != expected_fast_hash:
        raise PocketBookError("Upload verification failed: Cloud fast_hash differs from upload response")
    if not remote_name or remote_name != expected_name:
        raise PocketBookError("Upload verification failed: Cloud filename differs from the requested filename")
    if not isinstance(remote_bytes, int) or remote_bytes != expected_bytes:
        raise PocketBookError("Upload verification failed: Cloud file size differs from the uploaded file")
    if expected_format and remote_format != expected_format:
        raise PocketBookError("Upload verification failed: Cloud format differs from the uploaded file")
    if remote_format == "epub" and remote_bytes < DEFAULT_MIN_SAFE_EPUB_BYTES:
        raise PocketBookError("Upload verification failed: Cloud indexed an unsafe sub-4-KiB EPUB")
    return summary

def sanitize_filename(name: str) -> str:
    name = unicodedata.normalize("NFC", Path(str(name)).name)
    name = "".join(ch for ch in name if ord(ch) >= 32 and ch not in "\x7f")
    name = name.replace("/", "_").replace("\\", "_").strip(" .")
    if not name:
        raise UnsafeOperation("Unsafe empty filename")
    if len(name) > 180:
        suffix = "".join(Path(name).suffixes)[-24:]
        base = name[: max(1, 180 - len(suffix))]
        name = base + suffix
    return name

def supported_filename(name: str) -> bool:
    lower = name.casefold()
    return any(lower.endswith(ext) for ext in ALLOWED_EXTENSIONS)

def guess_mime(name: str) -> str:
    lower = name.casefold()
    if lower.endswith(".epub"): return "application/epub+zip"
    if lower.endswith(".fb2"): return "application/x-fictionbook+xml"
    if lower.endswith(".fb2.zip"): return "application/zip"
    if lower.endswith(".pdf"): return "application/pdf"
    return mimetypes.guess_type(name)[0] or "application/octet-stream"

__all__ = ['_zip_member_basename', '_zip_info_is_symlink', '_zip_info_is_unsafe_special', '_validate_zip_common', '_zip_is_epub', '_fictionbook_root_bytes', 'is_fb2_xml', '_validate_native_fb2_zip', 'canonical_upload_name', '_sha256_file', '_inbound_roots', 'resolve_inbound_attachment', 'ensure_inbound_path', 'compact_upload_preflight', 'inspect_upload_input', 'preflight_upload', 'materialize_upload_inputs', 'package_files', 'expected_cloud_format', 'verify_uploaded_record', 'sanitize_filename', 'supported_filename', 'guess_mime']
