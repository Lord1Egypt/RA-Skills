from __future__ import annotations

import csv
import hashlib
import json
import os
from copy import deepcopy
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from nutrition_math import (
    CSV_NUTRIENT_FIELDS,
    NUTRIENT_FIELDS,
    NutritionError,
    missing_values_count,
    normalize_item,
    source_breakdown,
    sum_nutrition,
)


CSV_FIELDS = [
    "date",
    "time",
    "timezone",
    "meal",
    "food",
    "amount_raw",
    "amount_g",
    "kcal",
    "protein_g",
    "carbs_g",
    "fat_g",
    "fiber_g",
    "sugar_g",
    "sodium_mg",
    "source",
    "confidence",
    "note",
    "raw_message",
    "entry_id",
]


class StoreError(ValueError):
    """Raised when a log operation cannot be completed safely."""


def get_log_dir(log_dir=None):
    if log_dir:
        return Path(log_dir)
    env_dir = os.environ.get("NUTRITION_LOG_DIR")
    if env_dir:
        return Path(env_dir)
    workspace_dir = os.environ.get("OPENCLAW_WORKSPACE")
    if workspace_dir:
        return Path(workspace_dir) / "nutrition-log"
    return Path.cwd() / "nutrition-log"


def jsonl_path(log_dir):
    return Path(log_dir) / "food_log.jsonl"


def csv_path(log_dir):
    return Path(log_dir) / "food_log.csv"


def ensure_log_dir(log_dir):
    Path(log_dir).mkdir(parents=True, exist_ok=True)


def now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def stable_entry_id(payload):
    raw = json.dumps(
        {
            "date": payload.get("date"),
            "time": payload.get("time"),
            "timezone": payload.get("timezone"),
            "meal": payload.get("meal"),
            "raw_message": payload.get("raw_message"),
            "items": payload.get("items", []),
        },
        ensure_ascii=False,
        sort_keys=True,
    )
    digest = hashlib.sha1(raw.encode("utf-8")).hexdigest()[:12]
    safe_date = payload.get("date") or "unknown"
    return f"nl_{safe_date}_{digest}"


def correction_id(entry_id, patch):
    raw = json.dumps({"entry_id": entry_id, "patch": patch}, ensure_ascii=False, sort_keys=True)
    return f"corr_{hashlib.sha1(raw.encode('utf-8')).hexdigest()[:12]}"


def deletion_id(entry_id):
    return f"del_{hashlib.sha1(entry_id.encode('utf-8')).hexdigest()[:12]}"


def read_jsonl_events(log_dir):
    path = jsonl_path(log_dir)
    if not path.exists():
        return []
    events = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                events.append(json.loads(stripped))
            except json.JSONDecodeError as exc:
                raise StoreError(f"food_log.jsonl 第 {line_number} 行不是有效 JSON。") from exc
    return events


def append_jsonl(log_dir, event):
    ensure_log_dir(log_dir)
    with jsonl_path(log_dir).open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")


def active_entries_from_events(events):
    entries = {}
    order = []
    for event in events:
        event_type = event.get("event_type", "entry")
        if event_type == "entry":
            entry = deepcopy(event)
            entry["event_type"] = "entry"
            entries[entry["entry_id"]] = entry
            if entry["entry_id"] not in order:
                order.append(entry["entry_id"])
        elif event_type == "correction":
            entry = deepcopy(event.get("entry") or {})
            if entry.get("entry_id"):
                entries[entry["entry_id"]] = entry
                if entry["entry_id"] not in order:
                    order.append(entry["entry_id"])
        elif event_type == "deletion":
            target = event.get("entry_id")
            if target in entries:
                del entries[target]
    return [entries[entry_id] for entry_id in order if entry_id in entries]


def read_active_entries(log_dir):
    return active_entries_from_events(read_jsonl_events(log_dir))


def normalize_entry(payload):
    required = ["date", "time", "timezone", "meal", "raw_message", "items"]
    missing = [field for field in required if field not in payload]
    if missing:
        raise StoreError(f"缺少必填字段：{', '.join(missing)}")
    if not isinstance(payload["items"], list) or not payload["items"]:
        raise StoreError("items 必须是非空数组。")

    items = [normalize_item(item) for item in payload["items"]]
    entry = {
        "event_type": "entry",
        "entry_id": payload.get("entry_id") or stable_entry_id(payload),
        "created_at": payload.get("created_at") or now_iso(),
        "date": payload["date"],
        "time": payload["time"],
        "timezone": payload["timezone"],
        "meal": payload["meal"],
        "raw_message": payload["raw_message"],
        "items": items,
        "totals": sum_nutrition(items),
    }
    if payload.get("note"):
        entry["note"] = payload["note"]
    return entry


def append_entry(log_dir, payload):
    entry = normalize_entry(payload)
    existing_ids = {entry["entry_id"] for entry in read_active_entries(log_dir)}
    if entry["entry_id"] in existing_ids:
        suffix = hashlib.sha1(now_iso().encode("utf-8")).hexdigest()[:6]
        entry["entry_id"] = f"{entry['entry_id']}_{suffix}"
    append_jsonl(log_dir, entry)
    rebuild_csv_from_jsonl(log_dir)
    return entry


def append_csv(log_dir, entries):
    ensure_log_dir(log_dir)
    with csv_path(log_dir).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for entry in entries:
            for item in entry.get("items", []):
                nutrition = item.get("nutrition") or {}
                row = {
                    "date": entry.get("date"),
                    "time": entry.get("time"),
                    "timezone": entry.get("timezone"),
                    "meal": entry.get("meal"),
                    "food": item.get("food"),
                    "amount_raw": item.get("amount_raw"),
                    "amount_g": item.get("amount_g"),
                    "source": item.get("source"),
                    "confidence": item.get("confidence"),
                    "note": item.get("note"),
                    "raw_message": entry.get("raw_message"),
                    "entry_id": entry.get("entry_id"),
                }
                for field in CSV_NUTRIENT_FIELDS:
                    row[field] = nutrition.get(field)
                writer.writerow(row)


def rebuild_csv_from_jsonl(log_dir):
    entries = read_active_entries(log_dir)
    append_csv(log_dir, entries)
    return entries


def read_day(log_dir, target_date):
    return [entry for entry in read_active_entries(log_dir) if entry.get("date") == target_date]


def read_week(log_dir, week_start):
    start = date.fromisoformat(week_start)
    end = start + timedelta(days=6)
    entries = []
    for entry in read_active_entries(log_dir):
        entry_date = date.fromisoformat(entry["date"])
        if start <= entry_date <= end:
            entries.append(entry)
    return entries


def summarize_entries(entries):
    items = []
    for entry in entries:
        items.extend(entry.get("items", []))
    return {
        "totals": sum_nutrition(items),
        "entry_count": len(entries),
        "source_breakdown": source_breakdown(entries),
        "missing_values_count": missing_values_count(items),
    }


def summary_day(log_dir, target_date, tz_name):
    entries = read_day(log_dir, target_date)
    result = summarize_entries(entries)
    result.update({"ok": True, "date": target_date, "timezone": tz_name})
    return result


def summary_week(log_dir, week_start, tz_name):
    start = date.fromisoformat(week_start)
    dates = [(start + timedelta(days=offset)).isoformat() for offset in range(7)]
    entries = read_week(log_dir, week_start)
    by_day = {day: [] for day in dates}
    for entry in entries:
        by_day[entry["date"]].append(entry)

    daily_totals = {
        day: summarize_entries(day_entries)["totals"]
        for day, day_entries in by_day.items()
    }
    missing_days = [day for day, day_entries in by_day.items() if not day_entries]
    average_kcal = round(sum(day["kcal"] for day in daily_totals.values()) / 7, 1)
    average_protein = round(sum(day["protein_g"] for day in daily_totals.values()) / 7, 1)
    if float(average_kcal).is_integer():
        average_kcal = int(average_kcal)
    if float(average_protein).is_integer():
        average_protein = int(average_protein)

    return {
        "ok": True,
        "week_start": week_start,
        "timezone": tz_name,
        "daily_totals": daily_totals,
        "average_kcal": average_kcal,
        "average_protein": average_protein,
        "missing_days": missing_days,
        "source_breakdown": source_breakdown(entries),
    }


def undo_last(log_dir):
    entries = read_active_entries(log_dir)
    if not entries:
        raise StoreError("没有可撤销的记录。")
    entry = entries[-1]
    event = {
        "event_type": "deletion",
        "deletion_id": deletion_id(entry["entry_id"]),
        "entry_id": entry["entry_id"],
        "created_at": now_iso(),
        "reason": "用户要求撤销上一条。",
    }
    append_jsonl(log_dir, event)
    rebuild_csv_from_jsonl(log_dir)
    return entry


def find_candidates(entries, match):
    if not match:
        return []
    wanted_entry_id = match.get("entry_id")
    wanted_food = match.get("food")
    wanted_meal = match.get("meal")

    candidates = []
    for entry in reversed(entries):
        if wanted_entry_id and entry.get("entry_id") != wanted_entry_id:
            continue
        if wanted_meal and entry.get("meal") != wanted_meal:
            continue
        for index, item in enumerate(entry.get("items", [])):
            if wanted_food and wanted_food not in item.get("food", ""):
                continue
            candidates.append({"entry": entry, "item_index": index, "item": item})
    return candidates


def public_candidate(candidate):
    entry = candidate["entry"]
    item = candidate["item"]
    return {
        "entry_id": entry.get("entry_id"),
        "date": entry.get("date"),
        "time": entry.get("time"),
        "meal": entry.get("meal"),
        "food": item.get("food"),
        "amount_raw": item.get("amount_raw"),
        "kcal": (item.get("nutrition") or {}).get("kcal"),
    }


def update_entry(log_dir, payload):
    entries = read_active_entries(log_dir)
    match = payload.get("match") or {}
    patch = payload.get("patch") or {}
    if payload.get("entry_id"):
        match["entry_id"] = payload["entry_id"]

    candidates = find_candidates(entries, match)
    if not candidates:
        raise StoreError("没有找到可修正的记录。")
    if len(candidates) > 1:
        error = StoreError("无法唯一确定要修正的记录，请从候选项中选择。")
        error.candidates = [public_candidate(candidate) for candidate in candidates[:3]]
        raise error

    candidate = candidates[0]
    entry = deepcopy(candidate["entry"])
    item_index = candidate["item_index"]
    item = deepcopy(entry["items"][item_index])

    if patch.get("food"):
        item["food"] = patch["food"]
    if patch.get("amount_raw") is not None:
        item["amount_raw"] = patch["amount_raw"]
    if patch.get("amount_g") is not None:
        item["amount_g"] = patch["amount_g"]
    if patch.get("nutrition"):
        existing = item.get("nutrition") or {}
        existing.update(patch["nutrition"])
        item["nutrition"] = existing
    if patch.get("source"):
        item["source"] = patch["source"]
    if patch.get("confidence"):
        item["confidence"] = patch["confidence"]
    correction_note = patch.get("note") or "根据用户更正更新。"
    previous_note = item.get("note") or ""
    item["note"] = f"{previous_note} 修正：{correction_note}".strip()
    item = normalize_item(item)

    entry["items"][item_index] = item
    entry["totals"] = sum_nutrition(entry["items"])
    entry["corrected_at"] = now_iso()
    entry["correction_note"] = correction_note

    event = {
        "event_type": "correction",
        "correction_id": correction_id(entry["entry_id"], patch),
        "entry_id": entry["entry_id"],
        "created_at": now_iso(),
        "patch": patch,
        "entry": entry,
    }
    append_jsonl(log_dir, event)
    rebuild_csv_from_jsonl(log_dir)
    return entry
