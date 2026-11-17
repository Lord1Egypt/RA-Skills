from __future__ import annotations

import json
import os
import re
import shutil
import stat
import tempfile
import time
import unicodedata
import zipfile
from pathlib import Path
from typing import Any

from .api import PocketBookClient
from .common import (AuthRequired, AmbiguousBook, DownloadError, NotFound,
                     PocketBookError, UnsafeOperation, DEFAULT_BATCH_CONFIRM_BOOKS,
                     DEFAULT_BATCH_CONFIRM_BYTES, _commit_temp_without_overwrite,
                     env_bytes, env_int, safe_untrusted_text)
from .state import FileLock, _account_fingerprint, _private_json_write, _read_private_bytes
from .formats import (compact_upload_preflight, ensure_inbound_path, materialize_upload_inputs,
                      package_files, preflight_upload, sanitize_filename)
from .models import (book_summary, display_author, display_title, normalize_text, phonetic_title_candidates,
                     resolve_book, search_books)
from .transport import download_book

DELETE_CONFIRM_TTL = 15 * 60

_DELETE_CONFIRM_PHRASES = {
    "да",
    "да удали",
    "да, удали",
    "да удаляй",
    "да, удаляй",
    "удали",
    "удаляй",
    "подтверждаю",
    "подтверждаю удаление",
    "подтвердить удаление",
    "yes",
    "yes delete",
    "yes, delete",
    "yes delete it",
    "yes, delete it",
    "delete",
    "delete it",
    "confirm",
    "confirm deletion",
}

def _delete_pending_path(client: PocketBookClient) -> Path:
    return client.store.path.with_name("delete-pending.json")

def _delete_lock_path(client: PocketBookClient) -> Path:
    p = _delete_pending_path(client)
    return p.with_name(p.name + ".lock")

def _load_delete_request(path: Path) -> dict[str, Any] | None:
    """Load the sole account-bound pending delete request. Old schemas stay inert."""
    encoded = _read_private_bytes(path, 64 * 1024, label="Pending PocketBook deletion state")
    if encoded is None:
        return None
    try:
        raw = json.loads(encoded.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise UnsafeOperation("Pending PocketBook deletion state is invalid") from exc
    if not isinstance(raw, dict):
        raise UnsafeOperation("Pending PocketBook deletion state is invalid")
    if int(raw.get("schema") or 0) != 4:
        return None
    record = raw.get("request")
    if not isinstance(record, dict):
        return None
    required = ("created_at", "expires_at", "fast_hash", "account_fingerprint")
    if any(key not in record for key in required):
        raise UnsafeOperation("Pending PocketBook deletion state is incomplete")
    if not isinstance(record.get("created_at"), int) or not isinstance(record.get("expires_at"), int):
        raise UnsafeOperation("Pending PocketBook deletion timestamps are invalid")
    if not isinstance(record.get("fast_hash"), str) or not isinstance(record.get("account_fingerprint"), str):
        raise UnsafeOperation("Pending PocketBook deletion identity is invalid")
    return record

def _save_delete_request(path: Path, record: dict[str, Any] | None) -> None:
    if record is None:
        try:
            path.unlink()
        except FileNotFoundError:
            pass
        return
    _private_json_write(path, {"schema": 4, "request": record})

def _normalize_delete_confirmation(value: str) -> str:
    text = unicodedata.normalize("NFKC", str(value or "")).strip().casefold()
    text = re.sub(r"[.!?]+$", "", text).strip()
    text = re.sub(r"\s+", " ", text)
    return text

def _delete_confirmation_is_explicit(value: str) -> bool:
    return _normalize_delete_confirmation(value) in _DELETE_CONFIRM_PHRASES

def prepare_delete(client: PocketBookClient, query: str) -> dict[str, Any]:
    """Prepare exactly one delete without exposing a confirmation secret.

    A new prepare replaces every older pending request. This intentionally
    prevents stale conversation history from retaining an actionable delete.
    """
    book = resolve_book(client.books(), query)
    summary = book_summary(book)
    fast_hash = str(book.get("fast_hash") or "")
    if not fast_hash:
        raise NotFound("PocketBook book has no fast_hash; cannot delete")
    account_fingerprint = _account_fingerprint(client.session)
    if not account_fingerprint:
        raise AuthRequired("PocketBook account identity is incomplete; authenticate again")
    now = int(time.time())
    record = {
        "created_at": now,
        "expires_at": now + DELETE_CONFIRM_TTL,
        "fast_hash": fast_hash,
        "id": str(book.get("id") or ""),
        "account_fingerprint": account_fingerprint,
        "book": summary,
    }
    path = _delete_pending_path(client)
    with FileLock(_delete_lock_path(client)):
        _save_delete_request(path, record)
    return {
        "ok": True,
        "prepared": True,
        "expiresInSeconds": DELETE_CONFIRM_TTL,
        "book": summary,
        "requiresSeparateUserConfirmation": True,
        "confirmationMode": "next_message_plain_text",
    }

def confirm_delete(client: PocketBookClient, confirmation_text: str) -> dict[str, Any]:
    """Confirm the sole pending delete using the user's *current* plain text.

    Expected control-flow misses are returned as non-destructive JSON results,
    not exceptions. In particular, legacy six-hex-character confirmation codes
    are inert so stale model history cannot generate either a deletion or an
    OpenClaw `Exec failed` warning.
    """
    raw = str(confirmation_text or "").strip()
    if re.fullmatch(r"[A-Fa-f0-9]{6}", raw):
        return {
            "ok": False,
            "deleted": False,
            "ignored": True,
            "reason": "legacy_confirmation_code_is_inert",
        }
    if not _delete_confirmation_is_explicit(raw):
        return {
            "ok": False,
            "deleted": False,
            "ignored": True,
            "reason": "explicit_next_message_confirmation_required",
        }

    path = _delete_pending_path(client)
    with FileLock(_delete_lock_path(client)):
        record = _load_delete_request(path)
        if record is None:
            # Remove any legacy/stale schema while remaining non-destructive.
            _save_delete_request(path, None)
            return {
                "ok": False,
                "deleted": False,
                "ignored": True,
                "reason": "no_active_delete_request",
            }
        if int(record.get("expires_at") or 0) < int(time.time()):
            _save_delete_request(path, None)
            return {
                "ok": False,
                "deleted": False,
                "ignored": True,
                "reason": "delete_confirmation_expired",
            }
        latest_session = client.store.load()
        current_fingerprint = _account_fingerprint(latest_session or client.session)
        if not current_fingerprint or current_fingerprint != str(record.get("account_fingerprint") or ""):
            _save_delete_request(path, None)
            return {
                "ok": False,
                "deleted": False,
                "ignored": True,
                "reason": "delete_account_changed",
            }
        client.session = latest_session or client.session
        # Consume before the destructive API call. Confirmation is one-shot even
        # if PocketBook returns a misleading/transient response afterward.
        _save_delete_request(path, None)

    fast_hash = str(record.get("fast_hash") or "")
    original_id = str(record.get("id") or "")
    books = client.books()
    matches = [b for b in books if str(b.get("fast_hash") or "") == fast_hash]
    if original_id:
        matches = [b for b in matches if str(b.get("id") or "") == original_id]
    if len(matches) != 1:
        raise UnsafeOperation("Pending book no longer resolves to exactly one unchanged PocketBook item")
    result = client.delete(matches[0])
    return {
        **result,
        "book": book_summary(matches[0]),
        "confirmationConsumed": True,
        "confirmationMode": "next_message_plain_text",
    }

def cancel_delete(client: PocketBookClient, _legacy_value: str | None = None) -> dict[str, Any]:
    path = _delete_pending_path(client)
    with FileLock(_delete_lock_path(client)):
        record = _load_delete_request(path)
        _save_delete_request(path, None)
    return {
        "ok": True,
        "cancelled": record is not None,
        "reason": "cancelled" if record is not None else "no_pending_request",
    }

def download_many(client: PocketBookClient, queries: list[str], output_dir: Path, archive: Path | None = None, *, confirmed: bool = False) -> dict[str, Any]:
    plan = preflight_download(client, queries)
    if plan.get("requiresConfirmation") and not confirmed:
        return {
            "ok": False,
            "requiresConfirmation": True,
            "preflight": plan,
            "message": "Batch download requires separate confirmation before transfer",
        }
    books = client.books()
    resolved: list[dict[str, Any]] = []
    seen: set[str] = set()
    # Resolve every query before writing any file. One ambiguous query means zero
    # side effects, which is much nicer than a half-downloaded batch.
    for query in queries:
        book = resolve_book(books, query)
        key = str(book.get("fast_hash") or book.get("id") or "")
        if key and key in seen:
            continue
        if key:
            seen.add(key)
        resolved.append(book)
    results: list[dict[str, Any]] = []
    files: list[Path] = []
    for book in resolved:
        summary = book_summary(book)
        try:
            item = download_book(book, output_dir)
            path = Path(item["path"])
            files.append(path)
            results.append({"book": summary, "status": "downloaded", "file": item["filename"], "bytes": item["bytes"]})
        except PocketBookError as exc:
            results.append({"book": summary, "status": "failed", "error": str(exc)})
    archive_info = None
    if archive is not None and files:
        archive_info = package_files(files, archive)
    failures = sum(1 for r in results if r["status"] == "failed")
    return {"ok": failures == 0, "requested": len(queries), "resolved": len(resolved), "downloaded": len(files), "failed": failures, "results": results, "archive": archive_info}

def upload_inbound(client: PocketBookClient, path: Path, roots: list[Path] | None = None, *, confirmed: bool = False) -> dict[str, Any]:
    source = ensure_inbound_path(path, roots)
    plan = preflight_upload([source])
    if plan.get("requiresConfirmation") and not confirmed:
        return {
            "ok": False,
            "requiresConfirmation": True,
            "preflight": plan,
            "message": "Inbound upload requires separate confirmation before transfer",
        }

    workdir = Path(tempfile.mkdtemp(prefix="pocketbook-cloud-upload-"))
    prepared: dict[str, Any] | None = None
    try:
        prepared = materialize_upload_inputs([source], workdir)
        paths = [Path(x) for x in prepared["paths"]]
        result = upload_many(client, paths, confirmed=True)
        generated = [Path(x) for x in prepared.get("extracted", [])]
        out: dict[str, Any] = {
            "ok": bool(result.get("ok")),
            "requiresConfirmation": False,
            "source": {"path": str(source), "filename": source.name, "bytes": source.stat().st_size},
            "preflight": plan,
            "upload": result,
        }
        if result.get("ok"):
            for item in generated:
                try:
                    item.unlink()
                except FileNotFoundError:
                    pass
            shutil.rmtree(workdir, ignore_errors=True)
            out["cleanup"] = {"temporaryPreparedFilesRemoved": True}
        else:
            if generated:
                out["diagnosticTempDir"] = str(workdir)
                out["preparedFiles"] = [str(x) for x in generated if x.exists()]
            else:
                shutil.rmtree(workdir, ignore_errors=True)
        return out
    except Exception:
        # Keep generated diagnostic material only when preparation already created it.
        generated = [Path(x) for x in (prepared or {}).get("extracted", [])]
        if not any(x.exists() for x in generated):
            shutil.rmtree(workdir, ignore_errors=True)
        raise

def upload_inbound_many(client: PocketBookClient, paths: list[Path], roots: list[Path] | None = None, *, confirmed: bool = False) -> dict[str, Any]:
    if not paths:
        raise PocketBookError("At least one inbound ebook attachment is required")

    # Validate every source before the first network mutation. De-duplicate an
    # accidentally repeated MediaPath while preserving user order.
    sources: list[Path] = []
    seen: set[str] = set()
    for raw in paths:
        source = ensure_inbound_path(raw, roots)
        key = str(source)
        if key in seen:
            continue
        seen.add(key)
        sources.append(source)

    plan = preflight_upload(sources)
    compact_plan = compact_upload_preflight(plan)
    if plan.get("requiresConfirmation") and not confirmed:
        return {
            "ok": False,
            "requiresConfirmation": True,
            "preflight": compact_plan,
            "message": "Inbound batch requires separate confirmation before transfer",
        }

    workdir = Path(tempfile.mkdtemp(prefix="pocketbook-cloud-batch-"))
    prepared: dict[str, Any] | None = None
    try:
        prepared = materialize_upload_inputs(sources, workdir)
        upload_paths = [Path(x) for x in prepared["paths"]]
        result = upload_many(client, upload_paths, confirmed=True)
        generated = [Path(x) for x in prepared.get("extracted", [])]

        files: list[dict[str, Any]] = []
        for item in result.get("results", []):
            if not isinstance(item, dict):
                continue
            nested = item.get("result") if isinstance(item.get("result"), dict) else {}
            filename = str(nested.get("name") or Path(str(item.get("path") or "attachment")).name)
            row: dict[str, Any] = {"filename": filename, "status": str(item.get("status") or "unknown")}
            if row["status"] == "failed":
                row["error"] = str(item.get("error") or "upload failed")[:300]
            elif row["status"] == "accepted_unverified":
                row["warning"] = str(nested.get("warning") or "accepted but not verified")[:200]
            files.append(row)

        out: dict[str, Any] = {
            "ok": bool(result.get("ok")),
            "requiresConfirmation": False,
            "inputs": len(sources),
            "books": len(upload_paths),
            "inputBytes": int(plan.get("inputBytes") or 0),
            "estimatedBookBytes": int(plan.get("estimatedBookBytes") or 0),
            "uploaded": int(result.get("uploaded") or 0),
            "acceptedUnverified": int(result.get("acceptedUnverified") or 0),
            "failed": int(result.get("failed") or 0),
            "files": files,
        }
        if result.get("ok"):
            for item in generated:
                try:
                    item.unlink()
                except FileNotFoundError:
                    pass
            shutil.rmtree(workdir, ignore_errors=True)
            out["cleanup"] = {"temporaryPreparedFilesRemoved": True}
        else:
            if any(item.exists() for item in generated):
                out["diagnosticTempDir"] = str(workdir)
            else:
                shutil.rmtree(workdir, ignore_errors=True)
        return out
    except Exception:
        generated = [Path(x) for x in (prepared or {}).get("extracted", [])]
        if not any(item.exists() for item in generated):
            shutil.rmtree(workdir, ignore_errors=True)
        raise

def preflight_download(client: PocketBookClient, queries: list[str]) -> dict[str, Any]:
    if not queries:
        raise PocketBookError("At least one book query is required")
    books = client.books()
    resolved: list[dict[str, Any]] = []
    seen: set[str] = set()
    for query in queries:
        book = resolve_book(books, query)
        key = str(book.get("fast_hash") or book.get("id") or "")
        if key and key in seen:
            continue
        if key:
            seen.add(key)
        resolved.append(book)
    summaries = [book_summary(book) for book in resolved]
    known = [int(s["bytes"]) for s in summaries if isinstance(s.get("bytes"), int)]
    total = sum(known)
    unknown = len(summaries) - len(known)
    book_limit = env_int("POCKETBOOK_BATCH_CONFIRM_BOOKS", DEFAULT_BATCH_CONFIRM_BOOKS)
    byte_limit = env_bytes("POCKETBOOK_BATCH_CONFIRM_MB", DEFAULT_BATCH_CONFIRM_BYTES)
    reasons = []
    if len(summaries) > book_limit:
        reasons.append("book_count")
    if total > byte_limit:
        reasons.append("known_total_bytes")
    return {
        "ok": True, "requested": len(queries), "books": len(summaries), "knownBytes": total,
        "unknownSizeBooks": unknown, "requiresConfirmation": bool(reasons),
        "confirmationReasons": reasons, "thresholds": {"books": book_limit, "bytes": byte_limit},
        "items": summaries,
    }

def upload_many(client: PocketBookClient, paths: list[Path], *, confirmed: bool = False) -> dict[str, Any]:
    # Validate the entire local batch before the first network mutation.
    plan = preflight_upload(paths)
    if plan.get("requiresConfirmation") and not confirmed:
        return {
            "ok": False,
            "requiresConfirmation": True,
            "preflight": compact_upload_preflight(plan),
            "message": "Batch upload requires separate confirmation before transfer",
        }
    results: list[dict[str, Any]] = []
    for path in paths:
        try:
            result = client.upload(path)
            status = "uploaded" if result.get("verified") else "accepted_unverified"
            results.append({"path": str(path), "status": status, "result": result})
        except PocketBookError as exc:
            results.append({"path": str(path), "status": "failed", "error": safe_untrusted_text(exc, 300)})
    failures = sum(1 for r in results if r["status"] == "failed")
    unverified = sum(1 for r in results if r["status"] == "accepted_unverified")
    uploaded = sum(1 for r in results if r["status"] == "uploaded")
    return {
        "ok": failures == 0 and unverified == 0,
        "requiresConfirmation": False,
        "total": len(paths),
        "uploaded": uploaded,
        "acceptedUnverified": unverified,
        "failed": failures,
        "results": results,
    }

def _equivalent_outer_zip_pair(books: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]] | None:
    """Return (raw, outer_zip) only for an exact filename X / X.zip pair.

    This is deliberately narrow. Content equality is verified separately before
    collapsing ambiguity.
    """
    if len(books) != 2:
        return None
    a, b = books
    an = str(a.get('name') or '')
    bn = str(b.get('name') or '')
    if bn == an + '.zip':
        return a, b
    if an == bn + '.zip':
        return b, a
    return None

def _download_equivalent_packaging(client: PocketBookClient, candidates: list[dict[str, Any]], work_dir: Path) -> tuple[dict[str, Any], dict[str, Any]] | None:
    """Collapse raw+outer-ZIP ambiguity only after byte-for-byte verification.

    Returns the raw book and its already-downloaded result when the ZIP contains
    exactly that raw file unchanged. Otherwise returns None.
    """
    pair = _equivalent_outer_zip_pair(candidates)
    if pair is None:
        return None
    raw_book, zip_book = pair
    raw_name = str(raw_book.get('name') or '')
    # Metadata must also agree, otherwise treat them as separate editions.
    if normalize_text(display_title(raw_book)) != normalize_text(display_title(zip_book)):
        return None
    if normalize_text(display_author(raw_book)) != normalize_text(display_author(zip_book)):
        return None
    compare_dir = (work_dir / '.compare').resolve()
    compare_dir.mkdir(parents=True, exist_ok=True)
    raw_dl = download_book(raw_book, compare_dir)
    zip_dl = download_book(zip_book, compare_dir)
    raw_path = Path(raw_dl['path']).resolve()
    zip_path = Path(zip_dl['path']).resolve()
    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            infos = [i for i in zf.infolist() if not i.is_dir()]
            if len(infos) != 1 or infos[0].filename != raw_name:
                return None
            with raw_path.open('rb') as src, zf.open(infos[0], 'r') as inner:
                while True:
                    a = src.read(1024 * 1024)
                    b = inner.read(1024 * 1024)
                    if a != b:
                        return None
                    if not a:
                        break
        return raw_book, raw_dl
    finally:
        try:
            zip_path.unlink()
        except OSError:
            pass

def resolve_book_for_chat_download(client: PocketBookClient, query: str, work_dir: Path) -> tuple[dict[str, Any], dict[str, Any] | None]:
    books = client.books()
    candidates: list[dict[str, Any]] = []
    try:
        return resolve_book(books, query), None
    except AmbiguousBook:
        scored = search_books(books, query)
        if scored:
            top = scored[0][0]
            candidates = [b for score, b in scored if score == top]
    except NotFound:
        candidates = phonetic_title_candidates(books, query)
    if len(candidates) == 1:
        return candidates[0], None
    if len(candidates) > 1:
        collapsed = _download_equivalent_packaging(client, candidates, work_dir)
        if collapsed is not None:
            return collapsed
        raise AmbiguousBook(query, [book_summary(b) | {'matchScore': 70} for b in candidates[:8]])
    raise NotFound(f"Book not found: {query}")

def _media_roots() -> list[Path]:
    roots: list[Path] = []
    explicit = os.environ.get("OPENCLAW_MEDIA_DIR", "").strip()
    if explicit:
        roots.append(Path(explicit).expanduser().resolve())
    workspace = os.environ.get("OPENCLAW_WORKSPACE_DIR", "").strip()
    if workspace:
        roots.append((Path(workspace).expanduser() / "media").resolve())
    state = os.environ.get("OPENCLAW_STATE_DIR", "").strip()
    if state:
        roots.append((Path(state).expanduser() / "media").resolve())
    roots.append((Path.cwd() / "media").resolve())
    out: list[Path] = []
    seen: set[str] = set()
    for root in roots:
        key = str(root)
        if key not in seen:
            seen.add(key)
            out.append(root)
    return out

def _default_chat_media_dir() -> Path:
    return _media_roots()[0] / "pocketbook-cloud"

def download_for_chat(client: PocketBookClient, query: str, media_dir: Path | None = None) -> dict[str, Any]:
    """Prepare one genuine ZIP attachment without exposing the signed source URL."""
    media_dir = (media_dir or _default_chat_media_dir()).expanduser().resolve()
    allowed = False
    for root in _media_roots():
        try:
            media_dir.relative_to(root)
            allowed = True
            break
        except ValueError:
            continue
    if not allowed:
        raise UnsafeOperation("Chat media output must stay under an OpenClaw runtime media directory")
    media_dir.mkdir(parents=True, exist_ok=True)
    work_dir = media_dir / ".work"
    work_dir.mkdir(parents=True, exist_ok=True)
    book, downloaded = resolve_book_for_chat_download(client, query, work_dir)
    if downloaded is None:
        downloaded = download_book(book, work_dir)
    original = Path(downloaded["path"]).resolve()
    safe_stem = sanitize_filename(original.name)
    archive = (media_dir / (safe_stem + ".zip")).resolve()
    if archive.parent != media_dir:
        raise UnsafeOperation("Unsafe chat archive path")
    if archive.exists():
        marker = str(book.get("fast_hash") or book.get("id") or "copy")[:8]
        archive = media_dir / f"{safe_stem} [{marker}].zip"
        n = 2
        while archive.exists():
            archive = media_dir / f"{safe_stem} [{marker}-{n}].zip"
            n += 1
    packaged = package_files([original], archive)
    # Stream both sides. Never load an ebook into model/process memory just to verify packaging.
    with zipfile.ZipFile(archive, "r") as zf:
        infos = zf.infolist()
        if len(infos) != 1 or infos[0].filename != original.name:
            raise UnsafeOperation("Chat package verification failed")
        with original.open("rb") as src, zf.open(infos[0], "r") as inner:
            while True:
                a = src.read(1024 * 1024)
                b = inner.read(1024 * 1024)
                if a != b:
                    raise UnsafeOperation("Chat package changed ebook bytes")
                if not a:
                    break
    try:
        original.unlink()
        if original.parent != work_dir:
            try:
                original.parent.rmdir()
            except OSError:
                pass
        try:
            work_dir.rmdir()
        except OSError:
            pass
    except OSError:
        pass
    # The ZIP intentionally remains until the channel reports successful delivery.
    return {
        "ok": True,
        "book": book_summary(book),
        "attachment": packaged,
        "mediaPath": str(archive),
        "mediaDirective": "MEDIA:" + str(archive),
        "originalFilename": downloaded["filename"],
        "originalBytes": downloaded["bytes"],
        "packaged": True,
        "deliveryPending": True,
        "reason": "openclaw_local_ebook_mime_workaround",
    }

def backup_library(client: PocketBookClient, output_dir: Path) -> dict[str, Any]:
    books = client.books()
    results: list[dict[str, Any]] = []
    for book in books:
        summary = book_summary(book)
        if summary.get("drm") or summary.get("lcp") or not book.get("link"):
            results.append({"book": summary, "status": "skipped", "reason": "not_downloadable"})
            continue
        try:
            result = download_book(book, output_dir)
        except DownloadError as first:
            if not first.retryable:
                results.append({"book": summary, "status": "failed", "error": safe_untrusted_text(first, 300)})
                continue
            try:
                fresh = client.books()
                fast_hash = str(book.get("fast_hash") or "")
                current = next((x for x in fresh if fast_hash and str(x.get("fast_hash") or "") == fast_hash), None)
                if current is None:
                    raise NotFound("Book disappeared while refreshing its download link")
                time.sleep(0.25)
                result = download_book(current, output_dir)
            except DownloadError as second:
                if second.status == 404:
                    results.append({"book": summary, "status": "unavailable", "reason": "source_not_found"})
                    continue
                results.append({"book": summary, "status": "failed", "error": safe_untrusted_text(second, 300)})
                continue
            except PocketBookError as second:
                results.append({"book": summary, "status": "failed", "error": safe_untrusted_text(second, 300)})
                continue
        except PocketBookError as exc:
            results.append({"book": summary, "status": "failed", "error": safe_untrusted_text(exc, 300)})
            continue
        results.append({"book": summary, "status": "downloaded", "file": result["filename"], "bytes": result["bytes"]})
    downloaded = sum(1 for x in results if x["status"] == "downloaded")
    skipped = sum(1 for x in results if x["status"] == "skipped")
    unavailable = sum(1 for x in results if x["status"] == "unavailable")
    failed = sum(1 for x in results if x["status"] == "failed")
    complete = downloaded == len(books)
    return {
        "ok": failed == 0, "complete": complete, "total": len(books),
        "downloaded": downloaded, "skipped": skipped, "unavailable": unavailable,
        "failed": failed, "results": results,
    }

__all__ = ['_delete_pending_path', '_delete_lock_path', '_load_delete_request', '_save_delete_request', '_normalize_delete_confirmation', '_delete_confirmation_is_explicit', 'prepare_delete', 'confirm_delete', 'cancel_delete', 'download_many', 'upload_inbound', 'upload_inbound_many', 'preflight_download', 'upload_many', '_equivalent_outer_zip_pair', '_download_equivalent_packaging', 'resolve_book_for_chat_download', '_media_roots', '_default_chat_media_dir', 'download_for_chat', 'DELETE_CONFIRM_TTL', 'backup_library']
