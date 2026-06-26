"""
Media Watcher
─────────────
Scans ~/.openclaw/media/inbound for new images dropped by the WhatsApp bridge,
classifies them by caption/filename keywords, dedupes by content hash, and
returns structured data.

Architecture:
  Python returns *data*. It does NOT call any LLM and does NOT deliver messages.
  Image classification beyond keyword matching is the agent's job — the agent
  layer (whichever model OpenClaw is configured with) reads the image directly
  using its native vision capability and calls back into tools.py to log
  receipts or save snack schedules.

  scan_and_process() returns a structured result dict listing:
    - receipts:        keyword-classified receipt images, agent should parse
    - snacks:          keyword-classified snack images, agent should parse
    - unclassified:    images with no caption/keyword match, agent should look
    - skipped:         images explicitly excluded (screenshots, selfies)
"""

from __future__ import annotations

import fcntl
import hashlib
import json
import os
import tempfile
from datetime import datetime
from typing import Any, Dict, List

from core.keychain_secrets import load_google_secrets

# Best-effort credential warm-up. Tests stub this; production may no-op.
try:
    load_google_secrets()
except Exception:
    pass

# Resolve skill root: features/dining/media_watcher.py → ../../
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

MEDIA_DIR        = os.path.expanduser("~/.openclaw/media/inbound")
STATE_FILE       = os.path.join(SKILL_DIR, "household", "media_watcher_state.json")
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".heic"}
MAX_IMAGE_BYTES  = 20 * 1024 * 1024  # 20 MB hard cap
MAX_PROCESSED_HASHES = 200           # bounded ring buffer to keep state file small


# ─── State ────────────────────────────────────────────────────────────────────

def load_state() -> Dict[str, Any]:
    """Read state file with a shared lock; return defaults if missing or corrupt."""
    if not os.path.exists(STATE_FILE):
        return {"processed": [], "last_run_month": ""}
    try:
        with open(STATE_FILE, "r") as f:
            fcntl.flock(f, fcntl.LOCK_SH)
            try:
                data = json.load(f)
            finally:
                fcntl.flock(f, fcntl.LOCK_UN)
        data.setdefault("processed", [])
        data.setdefault("last_run_month", "")
        return data
    except (json.JSONDecodeError, OSError):
        return {"processed": [], "last_run_month": ""}


def save_state(state: Dict[str, Any]) -> None:
    """Atomic write: tempfile in same dir → fsync → os.replace."""
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    dir_path = os.path.dirname(STATE_FILE)
    fd, tmp_path = tempfile.mkstemp(prefix=".media_state.", suffix=".tmp", dir=dir_path)
    try:
        with os.fdopen(fd, "w") as tmp:
            json.dump(state, tmp, indent=2)
            tmp.flush()
            os.fsync(tmp.fileno())
        os.replace(tmp_path, STATE_FILE)
    except Exception:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


def file_hash(path: str) -> str:
    """Deterministic MD5 of file bytes — used for image dedup."""
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


# ─── Caption sidecar parsing ─────────────────────────────────────────────────

def get_caption(image_path: str) -> str:
    """Look for caption sidecar files written by the WhatsApp bridge."""
    base = os.path.splitext(image_path)[0]
    for candidate in (
        base + ".txt", base + ".json", base + ".meta.json",
        image_path + ".txt", image_path + ".json", image_path + ".meta.json",
    ):
        if not os.path.exists(candidate):
            continue
        try:
            with open(candidate, "r") as f:
                content = f.read().strip()
        except OSError:
            continue
        try:
            data = json.loads(content)
            return (data.get("caption") or data.get("body")
                    or data.get("text") or "").strip()
        except (json.JSONDecodeError, AttributeError):
            return content
    return ""


# ─── Caption + filename classifier (no LLM) ──────────────────────────────────

_RECEIPT_TRIGGERS = (
    "receipt", "bill", "check", "invoice",
    "restaurant", "dinner", "lunch", "breakfast", "ate at",
    "we went", "food",
)
_SNACK_TRIGGERS = (
    "snack", "morning snack", "afternoon snack", "school snack",
)
_SKIP_TRIGGERS = ("screenshot", "selfie", "profile")


def classify_image(image_path: str) -> str:
    """
    Caption/filename keyword classifier. Returns one of:
      'receipt', 'snack', 'skip', 'unclassified'
    The agent inspects 'unclassified' images directly using its vision.
    """
    filename = os.path.basename(image_path).lower()
    caption  = get_caption(image_path).lower()
    combined = filename + " " + caption

    if any(t in caption for t in _SKIP_TRIGGERS) or "screenshot" in filename:
        return "skip"

    if any(t in combined for t in _RECEIPT_TRIGGERS):
        return "receipt"

    if any(t in combined for t in _SNACK_TRIGGERS):
        return "snack"

    return "unclassified"


# ─── Snack month gate ─────────────────────────────────────────────────────────

def should_skip_snacks_this_month() -> bool:
    """
    Skip snack-photo processing if the current month's schedule is already
    sufficiently populated. Best-effort — never raises.
    """
    try:
        from features.school.snack_manager import SnackManager
        mgr = SnackManager(SKILL_DIR)
    except Exception:
        return False

    now = datetime.now()
    current_month = now.strftime("%Y-%m")

    state = load_state()
    if state.get("last_run_month") == current_month:
        return True

    prefix = current_month + "-"
    schedule = getattr(mgr, "schedule", {}) or {}
    month_entries = {k: v for k, v in schedule.items() if k.startswith(prefix)}
    has_morning   = sum(1 for v in month_entries.values() if v.get("morning"))
    has_afternoon = sum(1 for v in month_entries.values() if v.get("afternoon"))

    if has_morning >= 10 and has_afternoon >= 10:
        state["last_run_month"] = current_month
        save_state(state)
        return True
    return False


# ─── Reminders (data-only) ───────────────────────────────────────────────────

def get_pending_rating_reminders() -> List[Dict[str, Any]]:
    """Return pending rating reminders as a list of dicts. Agent delivers them."""
    try:
        from features.dining.restaurant_tracker import get_pending_reminders
        return get_pending_reminders() or []
    except Exception:
        return []


def send_rating_reminders() -> List[Dict[str, Any]]:
    """
    Compatibility shim. Returns the pending reminders without sending anything;
    the agent handles delivery.
    """
    return get_pending_rating_reminders()


# ─── Main scan ────────────────────────────────────────────────────────────────

def scan_and_process() -> Dict[str, Any]:
    """
    Scan MEDIA_DIR for new images, classify by caption/filename, and return a
    structured result dict for the agent to act on. The agent reads each image
    using its native vision capability and calls tools.py to persist data.
    Never raises — top-level errors are reported in the result.
    """
    result: Dict[str, Any] = {
        "status": "ok",
        "scanned": 0,
        "new_images": 0,
        "receipts": [],
        "snacks": [],
        "unclassified": [],
        "skipped": [],
        "errors": [],
    }

    if not os.path.exists(MEDIA_DIR):
        result["status"] = "no_media_dir"
        return result

    try:
        result["pending_reminders"] = send_rating_reminders() or []
    except Exception as e:  # noqa: BLE001
        result["errors"].append(f"reminders: {e}")
        result["pending_reminders"] = []

    state = load_state()
    processed = set(state.get("processed", []))
    new_hashes: List[str] = []

    images: List[tuple] = []
    try:
        for fname in os.listdir(MEDIA_DIR):
            if os.path.splitext(fname)[1].lower() in IMAGE_EXTENSIONS:
                full_path = os.path.join(MEDIA_DIR, fname)
                try:
                    images.append((os.path.getmtime(full_path), full_path))
                except OSError:
                    continue
    except OSError as e:
        result["status"] = "scan_failed"
        result["errors"].append(f"listdir: {e}")
        return result

    images.sort()
    result["scanned"] = len(images)

    skip_snacks = should_skip_snacks_this_month()

    for _, image_path in images:
        try:
            try:
                if os.path.getsize(image_path) > MAX_IMAGE_BYTES:
                    result["skipped"].append(
                        {"file": os.path.basename(image_path), "reason": "too_large"}
                    )
                    continue
            except OSError:
                continue

            fhash = file_hash(image_path)
            if fhash in processed:
                continue

            new_hashes.append(fhash)
            kind = classify_image(image_path)
            entry = {
                "file": os.path.basename(image_path),
                "path": image_path,
                "caption": get_caption(image_path),
            }

            if kind == "receipt":
                result["receipts"].append(entry)
            elif kind == "snack":
                if not skip_snacks:
                    result["snacks"].append(entry)
                else:
                    result["skipped"].append(
                        {"file": entry["file"], "reason": "snack_month_full"}
                    )
            elif kind == "skip":
                result["skipped"].append({"file": entry["file"], "reason": "skip_keyword"})
            else:
                result["unclassified"].append(entry)

        except Exception as e:  # noqa: BLE001
            result["errors"].append(f"{os.path.basename(image_path)}: {e}")

    if new_hashes:
        state["processed"] = (list(processed) + new_hashes)[-MAX_PROCESSED_HASHES:]

    try:
        save_state(state)
    except Exception as e:  # noqa: BLE001
        result["errors"].append(f"save_state: {e}")

    result["new_images"] = len(new_hashes)
    return result


# ─── CLI entry point ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    try:
        out = scan_and_process()
    except Exception as e:  # noqa: BLE001
        out = {"status": "crashed", "error": str(e)}
    print(json.dumps(out, indent=2, default=str))
