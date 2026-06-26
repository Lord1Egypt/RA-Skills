#!/usr/bin/env python3
"""Shared helpers for Pocketbook ledger scripts."""

from __future__ import annotations

import json
import os
import time
import uuid
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import date, datetime, time as dt_time, timedelta
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path
from typing import Any, Callable
from zoneinfo import ZoneInfo

DEFAULT_TIMEZONE = "Asia/Shanghai"
DEFAULT_CURRENCY = "CNY"
DEFAULT_DATA_DIR = Path.home() / ".openclaw" / "pocketbook" / "default"
LEDGER_FILENAME = "ledger.jsonl"
MARKDOWN_FILENAME = "personal_finance.md"
PROFILE_FILENAME = "profile.json"
LOCK_FILENAME = ".ledger.lock"
LOCK_STALE_SECONDS = 120.0
ENTRY_TYPES = {"expense", "income", "refund", "transfer"}
EVENT_TYPES = {"create", "update", "revert"}
UNKNOWN_VALUE = "unknown"
TRACKED_COMPLETION_FIELDS = ("category", "payment_method", "account")
PROFILE_ALIAS_FIELDS = {
    "entry_type",
    "category",
    "payment_method",
    "account",
    "merchant",
    "currency",
    "timezone",
}
PROFILE_DEFAULT_FIELDS = {"currency", "timezone", "payment_method", "account"}
PROFILE_MANAGED_FIELDS = PROFILE_ALIAS_FIELDS | PROFILE_DEFAULT_FIELDS
MUTABLE_FIELDS = {
    "amount",
    "occurred_at",
    "category",
    "payment_method",
    "account",
    "merchant",
    "note",
    "status",
    "needs_review",
    "inferred_fields",
    "confidence",
    "currency",
    "entry_type",
}
TWOPLACES = Decimal("0.01")


class LedgerError(RuntimeError):
    """Raised when a ledger operation cannot be completed."""


@dataclass
class Summary:
    entry_count: int
    expense_total: Decimal
    income_total: Decimal
    refund_total: Decimal
    transfer_total: Decimal
    net_outflow: Decimal


def ensure_data_dir(data_dir: str | Path | None) -> Path:
    raw = data_dir or os.environ.get("POCKETBOOK_DATA_DIR")
    resolved = Path(raw).expanduser() if raw else DEFAULT_DATA_DIR
    resolved.mkdir(parents=True, exist_ok=True)
    return resolved


def ledger_path(data_dir: str | Path | None) -> Path:
    return ensure_data_dir(data_dir) / LEDGER_FILENAME


def markdown_path(data_dir: str | Path | None) -> Path:
    return ensure_data_dir(data_dir) / MARKDOWN_FILENAME


def profile_path(data_dir: str | Path | None) -> Path:
    return ensure_data_dir(data_dir) / PROFILE_FILENAME


def now_local(timezone_name: str = DEFAULT_TIMEZONE) -> datetime:
    return datetime.now(ZoneInfo(timezone_name))


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def parse_amount(value: Any) -> Decimal:
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError) as exc:
        raise LedgerError(f"Invalid amount: {value!r}") from exc
    if amount <= 0:
        raise LedgerError("Amount must be greater than zero.")
    return amount.quantize(TWOPLACES, rounding=ROUND_HALF_UP)


def coerce_decimal(value: Any) -> Decimal:
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError) as exc:
        raise LedgerError(f"Invalid decimal amount: {value!r}") from exc
    return amount.quantize(TWOPLACES, rounding=ROUND_HALF_UP)


def decimal_to_str(value: Decimal | str | int | float) -> str:
    if not isinstance(value, Decimal):
        value = coerce_decimal(value)
    return str(value.quantize(TWOPLACES, rounding=ROUND_HALF_UP))


def normalize_string(value: Any, fallback: str = UNKNOWN_VALUE) -> str:
    if value is None:
        return fallback
    text = str(value).strip()
    return text or fallback


def normalize_optional_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def normalize_confidence(value: Any) -> dict[str, float]:
    if value in (None, ""):
        return {}
    if not isinstance(value, dict):
        raise LedgerError("confidence must be an object.")
    normalized: dict[str, float] = {}
    for key, raw in value.items():
        try:
            normalized[str(key)] = float(raw)
        except (TypeError, ValueError) as exc:
            raise LedgerError(f"Invalid confidence value for {key!r}.") from exc
    return normalized


def normalize_inferred_fields(value: Any) -> list[str]:
    if value in (None, ""):
        return []
    if not isinstance(value, list):
        raise LedgerError("inferred_fields must be a list.")
    return [str(item).strip() for item in value if str(item).strip()]


def normalize_timestamp(
    value: Any,
    timezone_name: str = DEFAULT_TIMEZONE,
    default_now: datetime | None = None,
) -> str:
    zone = ZoneInfo(timezone_name)
    if value in (None, ""):
        current = default_now or now_local(timezone_name)
        return current.isoformat(timespec="seconds")
    if isinstance(value, datetime):
        dt_value = value
    else:
        raw = str(value).strip()
        if len(raw) == 10:
            try:
                dt_value = datetime.combine(date.fromisoformat(raw), dt_time(12, 0, 0))
            except ValueError as exc:
                raise LedgerError(f"Invalid date: {raw}") from exc
        else:
            try:
                dt_value = datetime.fromisoformat(raw)
            except ValueError as exc:
                raise LedgerError(f"Invalid timestamp: {raw}") from exc
    if dt_value.tzinfo is None:
        dt_value = dt_value.replace(tzinfo=zone)
    else:
        dt_value = dt_value.astimezone(zone)
    return dt_value.isoformat(timespec="seconds")


def parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value)


def local_date(occurred_at: str, timezone_name: str | None = None) -> date:
    dt_value = parse_timestamp(occurred_at)
    if timezone_name:
        dt_value = dt_value.astimezone(ZoneInfo(timezone_name))
    return dt_value.date()


def to_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        text = value.strip().lower()
        if text in {"true", "1", "yes", "y"}:
            return True
        if text in {"false", "0", "no", "n", ""}:
            return False
    if isinstance(value, (int, float)):
        return bool(value)
    raise LedgerError(f"Cannot interpret {value!r} as a boolean.")


def json_dump(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True)


def configure_standard_streams() -> None:
    import sys

    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if stream is not None and hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")


def input_stream_text() -> str:
    import sys

    return sys.stdin.buffer.read().decode("utf-8")


def load_payload(payload_arg: str | None) -> dict[str, Any]:
    if payload_arg and payload_arg != "-":
        with open(payload_arg, "r", encoding="utf-8") as handle:
            return json.load(handle)
    raw = input_stream_text()
    if not raw.strip():
        raise LedgerError("Payload is required via --payload <file> or stdin.")
    return json.loads(raw)


def load_events(data_dir: str | Path | None) -> list[dict[str, Any]]:
    return load_events_from_path(ledger_path(data_dir))


def load_events_from_path(path: str | Path) -> list[dict[str, Any]]:
    resolved = Path(path)
    if not resolved.exists():
        return []
    events: list[dict[str, Any]] = []
    with open(resolved, "r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                events.append(json.loads(stripped))
            except json.JSONDecodeError as exc:
                raise LedgerError(f"Invalid JSON on line {line_number} of {resolved}.") from exc
    return events


def normalize_profile(raw_profile: Any) -> dict[str, dict[str, Any]]:
    if raw_profile in (None, ""):
        raw_profile = {}
    if not isinstance(raw_profile, dict):
        raise LedgerError("profile.json must contain a JSON object.")

    defaults_raw = raw_profile.get("defaults", {})
    aliases_raw = raw_profile.get("aliases", {})
    if defaults_raw in (None, ""):
        defaults_raw = {}
    if aliases_raw in (None, ""):
        aliases_raw = {}
    if not isinstance(defaults_raw, dict):
        raise LedgerError("profile defaults must be an object.")
    if not isinstance(aliases_raw, dict):
        raise LedgerError("profile aliases must be an object.")

    defaults: dict[str, str] = {}
    for field_name, value in defaults_raw.items():
        field = normalize_optional_string(field_name)
        if not field or field not in PROFILE_DEFAULT_FIELDS:
            continue
        normalized = normalize_optional_string(value)
        if normalized:
            defaults[field] = normalized

    aliases: dict[str, dict[str, str]] = {}
    for field_name, mapping in aliases_raw.items():
        field = normalize_optional_string(field_name)
        if not field or field not in PROFILE_ALIAS_FIELDS:
            continue
        if not isinstance(mapping, dict):
            raise LedgerError(f"profile alias map for {field!r} must be an object.")
        normalized_mapping: dict[str, str] = {}
        for alias, canonical in mapping.items():
            alias_key = normalize_optional_string(alias)
            canonical_value = normalize_optional_string(canonical)
            if alias_key and canonical_value:
                normalized_mapping[alias_key] = canonical_value
        if normalized_mapping:
            aliases[field] = normalized_mapping

    return {"defaults": defaults, "aliases": aliases}


def load_profile(data_dir: str | Path | None) -> dict[str, dict[str, Any]]:
    path = profile_path(data_dir)
    if not path.exists():
        return {"defaults": {}, "aliases": {}}
    with open(path, "r", encoding="utf-8") as handle:
        return normalize_profile(json.load(handle))


def write_json_atomically(path: str | Path, payload: Any) -> None:
    resolved = Path(path)
    temp_path = resolved.with_name(resolved.name + ".tmp")
    with open(temp_path, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temp_path, resolved)


def save_profile(
    data_dir: str | Path | None,
    profile: dict[str, Any],
    *,
    lock_already_held: bool = False,
) -> dict[str, dict[str, Any]]:
    normalized = normalize_profile(profile)
    path = profile_path(data_dir)
    if lock_already_held:
        write_json_atomically(path, normalized)
    else:
        with file_lock(data_dir):
            write_json_atomically(path, normalized)
    return normalized


def apply_profile_alias(value: str, field_name: str, profile: dict[str, dict[str, Any]]) -> str:
    aliases = profile.get("aliases", {}).get(field_name, {})
    if not aliases:
        return value
    for alias, canonical in aliases.items():
        if value == alias or value.lower() == alias.lower():
            return canonical
    return value


def normalize_profile_value(
    value: Any,
    field_name: str,
    profile: dict[str, dict[str, Any]],
    fallback: str,
    *,
    allow_default: bool = False,
) -> str:
    text = normalize_optional_string(value)
    if not text and allow_default:
        text = normalize_optional_string(profile.get("defaults", {}).get(field_name))
    if not text:
        text = fallback
    if text and text != UNKNOWN_VALUE and field_name in PROFILE_ALIAS_FIELDS:
        text = apply_profile_alias(text, field_name, profile)
    return text


def _write_lock_metadata(fd: int) -> None:
    payload = json.dumps(
        {
            "pid": os.getpid(),
            "created_at": time.time(),
        },
        ensure_ascii=False,
    )
    os.write(fd, payload.encode("utf-8"))
    os.fsync(fd)


def _lock_age_seconds(path: Path) -> float:
    try:
        return time.time() - path.stat().st_mtime
    except FileNotFoundError:
        return 0.0


@contextmanager
def file_lock(
    data_dir: str | Path | None,
    timeout_seconds: float = 10.0,
    stale_after_seconds: float = LOCK_STALE_SECONDS,
):
    directory = ensure_data_dir(data_dir)
    path = directory / LOCK_FILENAME
    start = time.monotonic()
    fd: int | None = None
    while fd is None:
        try:
            fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_RDWR)
            _write_lock_metadata(fd)
        except FileExistsError:
            if stale_after_seconds > 0 and _lock_age_seconds(path) > stale_after_seconds:
                try:
                    os.unlink(path)
                    continue
                except (FileNotFoundError, PermissionError):
                    pass
            if time.monotonic() - start > timeout_seconds:
                raise LedgerError(f"Could not acquire lock for {path}.")
            time.sleep(0.1)
    try:
        yield
    finally:
        if fd is not None:
            os.close(fd)
        try:
            os.unlink(path)
        except FileNotFoundError:
            pass


def append_event_to_path(path: str | Path, event: dict[str, Any]) -> None:
    resolved = Path(path)
    line = json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n"
    with open(resolved, "a", encoding="utf-8", newline="\n") as handle:
        handle.write(line)
        handle.flush()
        os.fsync(handle.fileno())


def append_event(
    data_dir: str | Path | None,
    event: dict[str, Any],
    *,
    lock_already_held: bool = False,
) -> None:
    path = ledger_path(data_dir)
    if lock_already_held:
        append_event_to_path(path, event)
        return
    with file_lock(data_dir):
        append_event_to_path(path, event)


def atomic_ledger_operation(
    data_dir: str | Path | None,
    handler: Callable[[list[dict[str, Any]], dict[str, dict[str, Any]]], dict[str, Any]],
) -> dict[str, Any]:
    with file_lock(data_dir):
        path = ledger_path(data_dir)
        events = load_events_from_path(path)
        profile = load_profile(data_dir)
        result = handler(events, profile)
        if not isinstance(result, dict):
            raise LedgerError("Atomic handler must return a result object.")
        event = result.get("event")
        should_append = bool(result.get("append", event is not None))
        if event is not None and should_append:
            append_event_to_path(path, event)
            result["events_after"] = events + [event]
        else:
            result["events_after"] = events
        return result


def derive_status(explicit_status: Any, entry: dict[str, Any]) -> str:
    status = normalize_string(explicit_status, "confirmed") if explicit_status else "confirmed"
    if status == "reverted":
        return status
    if to_bool(entry.get("needs_review", False)):
        return "incomplete"
    for field_name in TRACKED_COMPLETION_FIELDS:
        if normalize_string(entry.get(field_name), UNKNOWN_VALUE) == UNKNOWN_VALUE:
            return "incomplete"
    return status


def fingerprint_for_entry(entry: dict[str, Any]) -> str:
    occurred_day = local_date(entry["occurred_at"], entry.get("timezone")).isoformat()
    merchant = normalize_string(entry.get("merchant"), UNKNOWN_VALUE).lower()
    category = normalize_string(entry.get("category"), UNKNOWN_VALUE).lower()
    parts = [
        entry.get("entry_type", "expense"),
        entry.get("amount", "0.00"),
        occurred_day,
        merchant,
        category,
    ]
    return "fp_" + uuid.uuid5(uuid.NAMESPACE_URL, "|".join(parts)).hex[:16]


def materialize_entries(events: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    entries: dict[str, dict[str, Any]] = {}
    for event_index, event in enumerate(events):
        event_type = event.get("event_type")
        entry_id = event.get("entry_id")
        if event_type not in EVENT_TYPES or not entry_id:
            continue
        if event_type == "create":
            entries[entry_id] = {
                "entry_id": entry_id,
                "entry_type": event.get("entry_type", "expense"),
                "amount": event.get("amount", "0.00"),
                "currency": event.get("currency", DEFAULT_CURRENCY),
                "occurred_at": event.get("occurred_at", event.get("recorded_at")),
                "recorded_at": event.get("recorded_at"),
                "created_at": event.get("recorded_at"),
                "updated_at": event.get("recorded_at"),
                "last_event_at": event.get("recorded_at"),
                "timezone": event.get("timezone", DEFAULT_TIMEZONE),
                "category": event.get("category", UNKNOWN_VALUE),
                "payment_method": event.get("payment_method", UNKNOWN_VALUE),
                "account": event.get("account", UNKNOWN_VALUE),
                "merchant": event.get("merchant", UNKNOWN_VALUE),
                "note": event.get("note", ""),
                "status": event.get("status", "incomplete"),
                "needs_review": bool(event.get("needs_review", False)),
                "inferred_fields": list(event.get("inferred_fields", [])),
                "confidence": dict(event.get("confidence", {})),
                "source_text": event.get("source_text", ""),
                "latest_source_text": event.get("source_text", ""),
                "fingerprint": event.get("fingerprint", ""),
                "idempotency_key": event.get("idempotency_key", ""),
                "reverted": False,
                "history_event_ids": [event.get("event_id")],
                "last_event_index": event_index,
            }
            entries[entry_id]["status"] = derive_status(entries[entry_id]["status"], entries[entry_id])
        elif event_type == "update" and entry_id in entries:
            entry = entries[entry_id]
            entry.update(dict(event.get("changes", {})))
            entry["updated_at"] = event.get("recorded_at")
            entry["last_event_at"] = event.get("recorded_at")
            entry["last_event_index"] = event_index
            entry["latest_source_text"] = event.get("source_text", entry["latest_source_text"])
            entry["last_reason"] = event.get("reason", "")
            entry["history_event_ids"].append(event.get("event_id"))
            entry["fingerprint"] = fingerprint_for_entry(entry)
            entry["status"] = derive_status(entry.get("status"), entry)
        elif event_type == "revert" and entry_id in entries:
            entry = entries[entry_id]
            entry["reverted"] = True
            entry["status"] = "reverted"
            entry["updated_at"] = event.get("recorded_at")
            entry["last_event_at"] = event.get("recorded_at")
            entry["last_event_index"] = event_index
            entry["latest_source_text"] = event.get("source_text", entry["latest_source_text"])
            entry["last_reason"] = event.get("reason", "")
            entry["history_event_ids"].append(event.get("event_id"))
    return entries


def active_entries(entries: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    return [entry for entry in entries.values() if not entry.get("reverted")]


def sorted_entries(entries: list[dict[str, Any]], order: str = "recent") -> list[dict[str, Any]]:
    if order == "occurred":
        key = lambda entry: (
            entry.get("occurred_at", ""),
            entry.get("last_event_index", -1),
        )
    else:
        key = lambda entry: (
            entry.get("last_event_index", -1),
            entry.get("last_event_at", entry.get("updated_at", entry.get("recorded_at", ""))),
        )
    return sorted(entries, key=key, reverse=True)


def pending_reasons(entry: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if entry.get("status") == "incomplete":
        reasons.append("status=incomplete")
    if entry.get("needs_review"):
        reasons.append("needs_review")
    for field_name in TRACKED_COMPLETION_FIELDS:
        if normalize_string(entry.get(field_name), UNKNOWN_VALUE) == UNKNOWN_VALUE:
            reasons.append(f"missing:{field_name}")
    return reasons


def is_pending(entry: dict[str, Any]) -> bool:
    return bool(pending_reasons(entry))


def summarize_entries(entries: list[dict[str, Any]]) -> Summary:
    expense = Decimal("0")
    income = Decimal("0")
    refund = Decimal("0")
    transfer = Decimal("0")
    for entry in entries:
        amount = Decimal(entry.get("amount", "0"))
        if entry.get("entry_type") == "expense":
            expense += amount
        elif entry.get("entry_type") == "income":
            income += amount
        elif entry.get("entry_type") == "refund":
            refund += amount
        elif entry.get("entry_type") == "transfer":
            transfer += amount
    return Summary(
        entry_count=len(entries),
        expense_total=expense,
        income_total=income,
        refund_total=refund,
        transfer_total=transfer,
        net_outflow=expense - refund,
    )


def filter_entries_by_period(
    entries: list[dict[str, Any]],
    period: str,
    timezone_name: str = DEFAULT_TIMEZONE,
    exact_date: str | None = None,
) -> list[dict[str, Any]]:
    if period == "all":
        return list(entries)
    today = now_local(timezone_name).date()
    if period == "date":
        if not exact_date:
            raise LedgerError("--date is required when period=date.")
        target_date = date.fromisoformat(exact_date)
        return [entry for entry in entries if local_date(entry["occurred_at"], timezone_name) == target_date]
    month_start = today.replace(day=1)
    week_start = today - timedelta(days=today.weekday())
    filtered: list[dict[str, Any]] = []
    for entry in entries:
        entry_date = local_date(entry["occurred_at"], timezone_name)
        if period == "today" and entry_date == today:
            filtered.append(entry)
        elif period == "week" and week_start <= entry_date <= today:
            filtered.append(entry)
        elif period == "month" and month_start <= entry_date <= today:
            filtered.append(entry)
    return filtered


def group_amounts(entries: list[dict[str, Any]], field_name: str) -> list[dict[str, Any]]:
    buckets: dict[str, dict[str, Any]] = {}
    for entry in entries:
        key = normalize_string(entry.get(field_name), UNKNOWN_VALUE)
        bucket = buckets.setdefault(key, {"key": key, "amount": Decimal("0"), "count": 0})
        bucket["amount"] += Decimal(entry.get("amount", "0"))
        bucket["count"] += 1
    result = []
    for bucket in buckets.values():
        result.append(
            {
                field_name: bucket["key"],
                "amount": decimal_to_str(bucket["amount"]),
                "count": bucket["count"],
            }
        )
    return sorted(result, key=lambda item: (Decimal(item["amount"]), item["count"]), reverse=True)


def detect_duplicate_candidates(
    existing_entries: list[dict[str, Any]],
    candidate: dict[str, Any],
) -> list[dict[str, Any]]:
    matches: list[dict[str, Any]] = []
    candidate_dt = parse_timestamp(candidate["occurred_at"])
    candidate_amount = Decimal(candidate["amount"])
    candidate_date = local_date(candidate["occurred_at"], candidate.get("timezone"))
    candidate_category = normalize_string(candidate.get("category"), UNKNOWN_VALUE).lower()
    candidate_merchant = normalize_string(candidate.get("merchant"), UNKNOWN_VALUE).lower()
    for entry in existing_entries:
        if entry.get("reverted"):
            continue
        if entry.get("entry_type") != candidate.get("entry_type"):
            continue
        if Decimal(entry.get("amount", "0")) != candidate_amount:
            continue
        if local_date(entry["occurred_at"], entry.get("timezone")) != candidate_date:
            continue
        score = 0
        other_category = normalize_string(entry.get("category"), UNKNOWN_VALUE).lower()
        other_merchant = normalize_string(entry.get("merchant"), UNKNOWN_VALUE).lower()
        if candidate_category != UNKNOWN_VALUE and candidate_category == other_category:
            score += 1
        if candidate_merchant != UNKNOWN_VALUE and candidate_merchant == other_merchant:
            score += 2
        if abs(parse_timestamp(entry["occurred_at"]) - candidate_dt) <= timedelta(hours=4):
            score += 1
        if score > 0:
            matches.append(
                {
                    "entry_id": entry["entry_id"],
                    "occurred_at": entry["occurred_at"],
                    "amount": entry["amount"],
                    "category": entry.get("category", UNKNOWN_VALUE),
                    "merchant": entry.get("merchant", UNKNOWN_VALUE),
                    "score": score,
                }
            )
    return sorted(matches, key=lambda item: (item["score"], item["occurred_at"]), reverse=True)[:3]


def find_entry_id_by_idempotency_key(events: list[dict[str, Any]], idempotency_key: str) -> str:
    if not idempotency_key:
        return ""
    for event in events:
        if event.get("event_type") == "create" and event.get("idempotency_key") == idempotency_key:
            return normalize_optional_string(event.get("entry_id"))
    return ""


def build_create_event(
    payload: dict[str, Any],
    events: list[dict[str, Any]],
    profile: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    profile = normalize_profile(profile or {})
    idempotency_key = normalize_optional_string(payload.get("idempotency_key"))
    if idempotency_key:
        existing_entry_id = find_entry_id_by_idempotency_key(events, idempotency_key)
        if existing_entry_id:
            return {
                "append": False,
                "event": None,
                "entry_id": existing_entry_id,
                "reused_existing": True,
                "duplicate_candidates": [],
            }

    timezone_name = normalize_profile_value(
        payload.get("timezone"),
        "timezone",
        profile,
        DEFAULT_TIMEZONE,
        allow_default=True,
    )
    current = now_local(timezone_name)
    source_text = normalize_optional_string(payload.get("source_text"))
    if not source_text:
        raise LedgerError("source_text is required for create.")

    entry = {
        "entry_id": normalize_optional_string(payload.get("entry_id")) or new_id("txn"),
        "entry_type": normalize_profile_value(payload.get("entry_type"), "entry_type", profile, "expense"),
        "amount": decimal_to_str(payload.get("amount")),
        "currency": normalize_profile_value(
            payload.get("currency"),
            "currency",
            profile,
            DEFAULT_CURRENCY,
            allow_default=True,
        ),
        "occurred_at": normalize_timestamp(payload.get("occurred_at"), timezone_name, current),
        "recorded_at": current.isoformat(timespec="seconds"),
        "timezone": timezone_name,
        "category": normalize_profile_value(payload.get("category"), "category", profile, UNKNOWN_VALUE),
        "payment_method": normalize_profile_value(
            payload.get("payment_method"),
            "payment_method",
            profile,
            UNKNOWN_VALUE,
            allow_default=True,
        ),
        "account": normalize_profile_value(
            payload.get("account"),
            "account",
            profile,
            UNKNOWN_VALUE,
            allow_default=True,
        ),
        "merchant": normalize_profile_value(payload.get("merchant"), "merchant", profile, UNKNOWN_VALUE),
        "note": normalize_optional_string(payload.get("note")),
        "needs_review": to_bool(payload.get("needs_review", False)),
        "inferred_fields": normalize_inferred_fields(payload.get("inferred_fields")),
        "confidence": normalize_confidence(payload.get("confidence")),
        "source_text": source_text,
        "idempotency_key": idempotency_key,
    }
    if entry["entry_type"] not in ENTRY_TYPES:
        raise LedgerError(f"entry_type must be one of {sorted(ENTRY_TYPES)}.")
    entry["status"] = derive_status(payload.get("status"), entry)
    entry["fingerprint"] = fingerprint_for_entry(entry)
    event = {
        "event_id": new_id("evt"),
        "event_type": "create",
        **entry,
    }
    duplicates = detect_duplicate_candidates(active_entries(materialize_entries(events)), event)
    return {
        "append": True,
        "event": event,
        "entry_id": event["entry_id"],
        "reused_existing": False,
        "duplicate_candidates": duplicates,
    }


def build_update_event(
    payload: dict[str, Any],
    events: list[dict[str, Any]],
    profile: dict[str, dict[str, Any]] | None = None,
    entry_id_override: str | None = None,
) -> dict[str, Any]:
    profile = normalize_profile(profile or {})
    entry_id = entry_id_override or normalize_optional_string(payload.get("entry_id"))
    if not entry_id:
        raise LedgerError("entry_id is required for update.")
    source_text = normalize_optional_string(payload.get("source_text"))
    if not source_text:
        raise LedgerError("source_text is required for update.")
    changes = payload.get("changes")
    if not isinstance(changes, dict) or not changes:
        raise LedgerError("changes must be a non-empty object.")

    entries = materialize_entries(events)
    entry = entries.get(entry_id)
    if not entry or entry.get("reverted"):
        raise LedgerError(f"Active entry not found: {entry_id}")

    normalized_changes: dict[str, Any] = {}
    for field_name, raw_value in changes.items():
        if field_name not in MUTABLE_FIELDS:
            raise LedgerError(f"Field is not mutable: {field_name}")
        if field_name == "amount":
            normalized_changes[field_name] = decimal_to_str(raw_value)
        elif field_name == "occurred_at":
            normalized_changes[field_name] = normalize_timestamp(
                raw_value,
                entry.get("timezone", DEFAULT_TIMEZONE),
            )
        elif field_name == "needs_review":
            normalized_changes[field_name] = to_bool(raw_value)
        elif field_name == "inferred_fields":
            normalized_changes[field_name] = normalize_inferred_fields(raw_value)
        elif field_name == "confidence":
            normalized_changes[field_name] = normalize_confidence(raw_value)
        elif field_name in {"category", "payment_method", "account", "merchant", "currency", "entry_type"}:
            normalized_changes[field_name] = normalize_profile_value(
                raw_value,
                field_name,
                profile,
                UNKNOWN_VALUE if field_name in TRACKED_COMPLETION_FIELDS else normalize_optional_string(raw_value),
            )
        elif field_name == "status":
            normalized_changes[field_name] = normalize_string(raw_value)
        else:
            normalized_changes[field_name] = normalize_optional_string(raw_value)

    if "entry_type" in normalized_changes and normalized_changes["entry_type"] not in ENTRY_TYPES:
        raise LedgerError(f"entry_type must be one of {sorted(ENTRY_TYPES)}.")

    preview = dict(entry)
    preview.update(normalized_changes)
    preview["status"] = derive_status(normalized_changes.get("status"), preview)
    normalized_changes["status"] = preview["status"]

    timezone_name = normalize_string(entry.get("timezone"), DEFAULT_TIMEZONE)
    event = {
        "event_id": new_id("evt"),
        "event_type": "update",
        "entry_id": entry_id,
        "recorded_at": now_local(timezone_name).isoformat(timespec="seconds"),
        "timezone": timezone_name,
        "source_text": source_text,
        "reason": normalize_optional_string(payload.get("reason")),
        "changes": normalized_changes,
    }
    return {
        "append": True,
        "event": event,
        "entry_id": entry_id,
    }


def build_revert_event(
    payload: dict[str, Any],
    events: list[dict[str, Any]],
    entry_id_override: str | None = None,
) -> dict[str, Any]:
    entry_id = entry_id_override or normalize_optional_string(payload.get("entry_id"))
    if not entry_id:
        raise LedgerError("entry_id is required for revert.")
    source_text = normalize_optional_string(payload.get("source_text"))
    if not source_text:
        raise LedgerError("source_text is required for revert.")
    entries = materialize_entries(events)
    entry = entries.get(entry_id)
    if not entry or entry.get("reverted"):
        raise LedgerError(f"Active entry not found: {entry_id}")
    timezone_name = normalize_string(entry.get("timezone"), DEFAULT_TIMEZONE)
    event = {
        "event_id": new_id("evt"),
        "event_type": "revert",
        "entry_id": entry_id,
        "recorded_at": now_local(timezone_name).isoformat(timespec="seconds"),
        "timezone": timezone_name,
        "source_text": source_text,
        "reason": normalize_optional_string(payload.get("reason")),
    }
    return {
        "append": True,
        "event": event,
        "entry_id": entry_id,
    }


def entry_response(entry: dict[str, Any]) -> dict[str, Any]:
    result = dict(entry)
    result["pending_reasons"] = pending_reasons(entry)
    return result
