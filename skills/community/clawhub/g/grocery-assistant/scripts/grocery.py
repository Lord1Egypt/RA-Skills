#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
import socket
from urllib import error, parse, request

# Telegram's API servers are reachable via IPv4. Force IPv4 to avoid
# the multi-second delay that happens when IPv6 is attempted first but
# unreachable (same workaround OpenClaw's Node networking applies).
_orig_getaddrinfo = socket.getaddrinfo
def _ipv4_getaddrinfo(host, port, family=0, *args, **kwargs):
    results = _orig_getaddrinfo(host, port, family, *args, **kwargs)
    ipv4 = [r for r in results if r[0] == socket.AF_INET]
    return ipv4 if ipv4 else results
socket.getaddrinfo = _ipv4_getaddrinfo


STATUS_NEEDED = "needed"
STATUS_HAVE = "have"
DEFAULT_ACCOUNT = "default"
CALLBACK_PREFIX = "gchk"
CALLBACK_TOGGLE = "tgl"
CALLBACK_COMMIT = "commit"
CALLBACK_VIEW = "view"
VIEW_NEEDED = "needed"
VIEW_ALL = "all"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def state_path() -> Path:
    raw = os.environ.get("GROCERY_STATE_FILE")
    if raw:
        return Path(raw).expanduser()
    return Path.home() / ".openclaw" / "data" / "grocery-checklist" / "state.json"


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def salvage_json_object(raw: str) -> tuple[dict[str, Any], bool]:
    decoder = json.JSONDecoder()
    parsed, end = decoder.raw_decode(raw)
    if not isinstance(parsed, dict):
        raise SystemExit("State file is invalid.")
    trailing = raw[end:].strip()
    return parsed, bool(trailing)


def prune_corrupted_items(state: dict[str, Any]) -> bool:
    items = state.get("items")
    if not isinstance(items, dict):
        state["items"] = {}
        return True

    changed = False
    remove_ids: list[str] = []
    for item_id, item in items.items():
        if not isinstance(item, dict):
            remove_ids.append(item_id)
            changed = True
            continue
        name = str(item.get("name", "")).strip()
        normalized = normalize_name(name) if name else ""
        if (
            re.fullmatch(r"[0-9a-f]{10}", normalized)
            and normalized in items
            and normalized != item_id
        ):
            remove_ids.append(item_id)
            changed = True
            continue
        if name and item.get("normalized") != normalized:
            item["normalized"] = normalized
            changed = True

    for item_id in remove_ids:
        items.pop(item_id, None)

    return changed


def migrate_v1_to_v2(state: dict[str, Any]) -> bool:
    """Re-index item IDs after plural normalization was added in v2."""
    items = state.get("items")
    if not isinstance(items, dict):
        state["version"] = 2
        return False
    new_items: dict[str, Any] = {}
    changed = False
    for old_id, item in items.items():
        if not isinstance(item, dict):
            changed = True
            continue
        name = item.get("name", "")
        new_normalized = normalize_name(name)
        new_id = item_id_for(new_normalized)
        item["id"] = new_id
        item["normalized"] = new_normalized
        if new_id != old_id:
            changed = True
        if new_id in new_items:
            existing = new_items[new_id]
            if item.get("status") == STATUS_NEEDED or existing.get("status") == STATUS_NEEDED:
                existing["status"] = STATUS_NEEDED
            if item.get("updated_at", "") > existing.get("updated_at", ""):
                existing["updated_at"] = item["updated_at"]
        else:
            new_items[new_id] = item
    state["items"] = new_items
    state["version"] = 2
    return changed


def load_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {
            "version": 2,
            "updated_at": utc_now(),
            "items": {},
            "views": {},
        }
    repaired = False
    raw = path.read_text(encoding="utf-8")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        data, repaired = salvage_json_object(raw)
    if not isinstance(data, dict):
        raise SystemExit("State file is invalid.")
    data.setdefault("version", 1)
    data.setdefault("updated_at", utc_now())
    data.setdefault("items", {})
    data.setdefault("views", {})
    if data.get("version", 1) < 2:
        repaired = migrate_v1_to_v2(data) or repaired
    repaired = prune_corrupted_items(data) or repaired
    if repaired:
        save_state(path, data)
    return data


def save_state(path: Path, state: dict[str, Any]) -> None:
    ensure_parent(path)
    state["updated_at"] = utc_now()
    tmp = path.with_name(f"{path.stem}.{os.getpid()}.tmp")
    with tmp.open("w", encoding="utf-8") as fh:
        json.dump(state, fh, indent=2, sort_keys=True)
        fh.write("\n")
    tmp.replace(path)


def _depluralize_word(word: str) -> str:
    if len(word) <= 3:
        return word
    if word.endswith("ies") and len(word) > 4:
        return word[:-3] + "y"
    if word.endswith("s") and not word.endswith("ss"):
        return word[:-1]
    return word


def normalize_name(value: str) -> str:
    lowered = value.strip().lower()
    lowered = re.sub(r"[&+]", " and ", lowered)
    lowered = re.sub(r"[^a-z0-9]+", " ", lowered)
    lowered = re.sub(r"\s+", " ", lowered).strip()
    return " ".join(_depluralize_word(w) for w in lowered.split())


def display_name(value: str) -> str:
    value = re.sub(r"\s+", " ", value.strip())
    return value


def item_id_for(normalized: str) -> str:
    return hashlib.sha1(normalized.encode("utf-8")).hexdigest()[:10]


_CATEGORY_KEYWORDS: list[tuple[str, list[str]]] = [
    ("Fruits & Vegetables", ["apple", "banana", "orange", "lemon", "lime", "tomato", "onion", "garlic", "ginger", "carrot", "potato", "lettuce", "cucumber", "capsicum", "pepper", "chili", "coriander", "spring onion", "celery", "mushroom", "avocado", "mango", "grape", "berry", "honeydew", "watermelon", "melon", "basil", "parsley", "mint", "spinach", "broccoli", "cauliflower", "zucchini", "eggplant", "corn", "sweet corn", "pea", "bean", "herb"]),
    ("Meat & Fish", ["chicken", "beef", "pork", "lamb", "fish", "prawn", "shrimp", "salmon", "tuna", "mackerel", "turkey", "duck", "sausage", "bacon", "mince", "steak"]),
    ("Dairy & Eggs", ["milk", "cheese", "egg", "yogurt", "yoghurt", "butter", "cream", "condensed milk"]),
    ("Bakery", ["bread", "wrap", "tortilla", "pita", "bun", "roll", "bagel"]),
    ("Staples", ["rice", "pasta", "noodle", "flour", "sugar", "salt", "oil", "vinegar", "sauce", "soy", "stock", "broth", "paste", "mayonnaise", "ketchup", "mustard", "coconut"]),
    ("Spices", ["seasoning", "spice", "cumin", "turmeric", "paprika", "curry", "laksa", "fajita", "chili flake", "chilli flake"]),
    ("Beverages", ["tea", "coffee", "juice", "water", "drink", "soda", "cola"]),
    ("Snacks & Sweets", ["chocolate", "biscuit", "cookie", "crisp", "chip", "marshmallow", "candy", "sweet", "snack"]),
]
_CATEGORY_ORDER = [cat for cat, _ in _CATEGORY_KEYWORDS] + ["Other"]

_HTML_TAG_RE = re.compile(r"<[^>]+>")


def categorize_item(name: str) -> str:
    normalized = normalize_name(name)
    for category, keywords in _CATEGORY_KEYWORDS:
        for keyword in keywords:
            if re.search(r"\b" + re.escape(keyword) + r"\b", normalized):
                return category
    return "Other"


def strip_html(text: str) -> str:
    text = _HTML_TAG_RE.sub("", text)
    return text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")


def split_item_tokens(values: list[str]) -> list[str]:
    items: list[str] = []
    for raw in values:
        for part in re.split(r",|\n|(?:\band\b)", raw):
            cleaned = display_name(part)
            if cleaned:
                items.append(cleaned)
    seen: set[str] = set()
    unique: list[str] = []
    for item in items:
        key = normalize_name(item)
        if not key or key in seen:
            continue
        seen.add(key)
        unique.append(item)
    return unique


def get_or_create_item(state: dict[str, Any], raw_name: str) -> dict[str, Any]:
    name = display_name(raw_name)
    normalized = normalize_name(name)
    if not normalized:
        raise ValueError("Empty grocery item.")
    item_id = item_id_for(normalized)
    items = state["items"]
    existing = items.get(item_id)
    if existing:
        existing["normalized"] = normalized
        existing.setdefault("created_at", utc_now())
        return existing
    item = {
        "id": item_id,
        "name": name,
        "normalized": normalized,
        "status": STATUS_NEEDED,
        "created_at": utc_now(),
        "updated_at": utc_now(),
    }
    items[item_id] = item
    return item


def update_status(state: dict[str, Any], raw_items: list[str], status: str) -> list[dict[str, Any]]:
    changed: list[dict[str, Any]] = []
    for raw_name in split_item_tokens(raw_items):
        item = get_or_create_item(state, raw_name)
        if not item.get("name"):
            item["name"] = display_name(raw_name)
        item["status"] = status
        item["updated_at"] = utc_now()
        changed.append(item)
    return changed


def remove_items(state: dict[str, Any], raw_items: list[str]) -> list[str]:
    removed: list[str] = []
    for raw_name in split_item_tokens(raw_items):
        normalized = normalize_name(raw_name)
        item_id = item_id_for(normalized)
        item = state["items"].pop(item_id, None)
        if item:
            removed.append(item["name"])
    return removed


def merge_items(state: dict[str, Any], destination_name: str, source_names: list[str]) -> dict[str, Any]:
    destination_normalized = normalize_name(destination_name)
    destination_id = item_id_for(destination_normalized)
    destination_existing = state.get("items", {}).get(destination_id)
    destination = get_or_create_item(state, destination_name)
    merged_names: list[str] = []
    statuses: set[str] = set()
    if destination_existing:
        statuses.add(destination.get("status", STATUS_HAVE))

    source_ids = []
    for raw_name in split_item_tokens(source_names):
        normalized = normalize_name(raw_name)
        item_id = item_id_for(normalized)
        if item_id == destination["id"]:
            continue
        source_ids.append(item_id)

    for item_id in source_ids:
        item = state["items"].get(item_id)
        if not item:
            continue
        merged_names.append(item.get("name", item_id))
        statuses.add(item.get("status", STATUS_HAVE))
        state["items"].pop(item_id, None)

    source_statuses = statuses.copy()
    if destination_existing:
        source_statuses.discard(destination.get("status", STATUS_HAVE))
    effective_statuses = source_statuses or statuses
    destination["status"] = STATUS_NEEDED if STATUS_NEEDED in effective_statuses else STATUS_HAVE
    destination["updated_at"] = utc_now()
    return {
        "item": destination,
        "merged": merged_names,
    }


def rename_item(state: dict[str, Any], source_name: str, destination_name: str) -> dict[str, Any]:
    normalized_source = normalize_name(source_name)
    source_id = item_id_for(normalized_source)
    source = state["items"].get(source_id)
    if not source:
        raise RuntimeError(f"Grocery item not found: {source_name}")

    result = merge_items(state, destination_name, [source_name])
    destination = result["item"]
    destination["status"] = source.get("status", destination.get("status", STATUS_HAVE))
    destination["updated_at"] = utc_now()
    return result


def sorted_items(state: dict[str, Any], status: str | None = None) -> list[dict[str, Any]]:
    items = list(state["items"].values())
    if status in {STATUS_NEEDED, STATUS_HAVE}:
        items = [item for item in items if item.get("status") == status]
    return sorted(items, key=lambda item: (item.get("status") != STATUS_NEEDED, item.get("name", "").lower()))


def sender_key(account: str, target: str, thread_id: str | None) -> str:
    return f"{account}:{target}:{thread_id or '-'}"


def html_escape(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def checkbox_line(name: str, checked: bool) -> str:
    safe = html_escape(name)
    if checked:
        return f"☑ <s>{safe}</s>"
    return f"☐ {safe}"


def resolve_view(state: dict[str, Any], account: str, target: str, thread_id: str | None) -> dict[str, Any]:
    key = sender_key(account, target, thread_id)
    views = state["views"]
    raw = views.get(key)
    if isinstance(raw, dict):
        raw.setdefault("mode", VIEW_NEEDED)
        raw.setdefault("account", account)
        raw.setdefault("target", target)
        raw.setdefault("thread_id", thread_id)
        return raw
    view = {
        "account": account,
        "target": target,
        "thread_id": thread_id,
        "mode": VIEW_NEEDED,
        "updated_at": utc_now(),
    }
    views[key] = view
    return view


def render_message(state: dict[str, Any], mode: str = VIEW_NEEDED, session_ids: set[str] | None = None) -> dict[str, Any]:
    needed = sorted_items(state, STATUS_NEEDED)
    have = sorted_items(state, STATUS_HAVE)
    body: list[str] = []
    buttons: list[list[dict[str, str]]] = []

    if mode == VIEW_ALL:
        body.append("<b>Pantry</b>")
        body.append("")
        all_items = needed + have
        if all_items:
            by_cat: dict[str, list] = defaultdict(list)
            for item in all_items:
                by_cat[categorize_item(item["name"])].append(item)
            for cat in _CATEGORY_ORDER:
                cat_items = by_cat.get(cat, [])
                if not cat_items:
                    continue
                in_stock = [html_escape(i["name"]) for i in cat_items if i["status"] == STATUS_HAVE]
                to_buy = [html_escape(i["name"]) for i in cat_items if i["status"] == STATUS_NEEDED]
                body.append(f"<b>{html_escape(cat)}</b>")
                if in_stock:
                    body.append(f"in stock: {', '.join(in_stock)}")
                if to_buy:
                    body.append(f"need to buy: {', '.join(to_buy)}")
                body.append("")
        else:
            body.append("Nothing here yet.")
            body.append("")
        buttons.append([{"text": "Shopping View", "callback_data": f"{CALLBACK_PREFIX}:{CALLBACK_VIEW}:{VIEW_NEEDED}"}])
    else:
        body.append("Groceries to buy")
        body.append("")
        session_have = [item for item in have if session_ids and item["id"] in session_ids]
        all_items = needed + session_have
        if all_items:
            by_cat: dict[str, list] = defaultdict(list)
            for item in all_items:
                by_cat[categorize_item(item["name"])].append(item)
            for cat in _CATEGORY_ORDER:
                cat_items = by_cat.get(cat, [])
                if not cat_items:
                    continue
                body.append(f"<b>{html_escape(cat)}</b>")
                for item in cat_items:
                    if item["status"] == STATUS_NEEDED:
                        body.append(f"☐ {html_escape(item['name'])}")
                    else:
                        body.append(f"<s>☑ {html_escape(item['name'])}</s>")
                body.append("")
        else:
            body.append("Nothing pending.")
            body.append("")
        body.append("Tap to check off. Tap again to undo.")

        row: list[dict[str, str]] = []
        for item in all_items:
            label = f"☐ {item['name']}" if item["status"] == STATUS_NEEDED else f"✅ {item['name']}"
            row.append({
                "text": label,
                "callback_data": f"{CALLBACK_PREFIX}:{CALLBACK_TOGGLE}:{item['id']}",
            })
            if len(row) == 2:
                buttons.append(row)
                row = []
        if row:
            buttons.append(row)
        buttons.append([{"text": "Pantry View", "callback_data": f"{CALLBACK_PREFIX}:{CALLBACK_VIEW}:{VIEW_ALL}"}])
    return {
        "message": "\n".join(body).strip(),
        "buttons": buttons,
    }


def run_openclaw(args: list[str], dry_run: bool = False) -> dict[str, Any]:
    cmd = ["openclaw", *args]
    if dry_run:
        return {"ok": True, "dry_run": True, "command": cmd}
    completed = subprocess.run(cmd, capture_output=True, text=True)
    if completed.returncode != 0:
        raise RuntimeError((completed.stderr or completed.stdout or "openclaw command failed").strip())
    stdout = completed.stdout.strip()
    if not stdout:
        return {"ok": True}
    try:
        return json.loads(stdout)
    except json.JSONDecodeError:
        return {"ok": True, "raw": stdout}


def openclaw_config_path() -> Path:
    return Path.home() / ".openclaw" / "openclaw.json"


def resolve_telegram_token(account: str) -> str:
    config = json.loads(openclaw_config_path().read_text(encoding="utf-8"))
    token = (((config.get("channels") or {}).get("telegram") or {}).get("accounts") or {}).get(account, {}).get("botToken")
    if not token:
        raise RuntimeError(f"Missing Telegram bot token for account {account}.")
    return token


def telegram_api(method: str, payload: dict[str, Any], account: str, dry_run: bool = False) -> dict[str, Any]:
    token = resolve_telegram_token(account)
    if dry_run:
        return {"ok": True, "dry_run": True, "method": method, "payload": payload}
    data = parse.urlencode({k: json.dumps(v) if isinstance(v, (dict, list)) else str(v) for k, v in payload.items()}).encode("utf-8")
    req = request.Request(f"https://api.telegram.org/bot{token}/{method}", data=data, method="POST")
    try:
        with request.urlopen(req, timeout=15) as resp:
            raw = resp.read().decode("utf-8")
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(detail or str(exc)) from exc
    decoded = json.loads(raw)
    if not decoded.get("ok"):
        raise RuntimeError(decoded.get("description", "Telegram API call failed."))
    return decoded


def telegram_send_message(target: str, account: str, text: str, buttons: list[list[dict[str, str]]], thread_id: str | None, dry_run: bool) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "chat_id": target,
        "text": text,
        "parse_mode": "HTML",
        "reply_markup": {"inline_keyboard": buttons},
    }
    if thread_id:
        payload["message_thread_id"] = thread_id
    return telegram_api("sendMessage", payload, account, dry_run=dry_run)


def telegram_edit_message(view: dict[str, Any], account: str, text: str, buttons: list[list[dict[str, str]]], dry_run: bool) -> dict[str, Any]:
    if not view.get("message_id") or not view.get("chat_id"):
        raise RuntimeError("No Telegram checklist message to edit.")
    payload = {
        "chat_id": view["chat_id"],
        "message_id": view["message_id"],
        "text": text,
        "parse_mode": "HTML",
        "reply_markup": {"inline_keyboard": buttons},
    }
    try:
        return telegram_api("editMessageText", payload, account, dry_run=dry_run)
    except RuntimeError as exc:
        if "message is not modified" in str(exc).lower():
            return {"ok": True, "not_modified": True}
        raise


def telegram_delete_message(view: dict[str, Any], account: str, dry_run: bool) -> None:
    if not view.get("message_id") or not view.get("chat_id"):
        return
    try:
        telegram_api("deleteMessage", {
            "chat_id": view["chat_id"],
            "message_id": view["message_id"],
        }, account, dry_run=dry_run)
    except RuntimeError:
        return


def maybe_delete_previous_view(state: dict[str, Any], key: str, account: str, dry_run: bool) -> None:
    view = state["views"].get(key)
    if isinstance(view, dict):
        telegram_delete_message(view, account, dry_run=dry_run)


def send_telegram_view(state: dict[str, Any], target: str, account: str, mode: str, thread_id: str | None, dry_run: bool) -> dict[str, Any]:
    view = resolve_view(state, account, target, thread_id)
    view["mode"] = mode
    if mode == VIEW_NEEDED:
        view["session_ids"] = [item["id"] for item in sorted_items(state, STATUS_NEEDED)]
    session_ids = set(view.get("session_ids") or [])
    payload = render_message(state, mode=mode, session_ids=session_ids)
    key = sender_key(account, target, thread_id)
    if not dry_run:
        maybe_delete_previous_view(state, key, account, dry_run=False)
    result = telegram_send_message(target, account, payload["message"], payload["buttons"], thread_id, dry_run=dry_run)
    message_obj = result.get("result", {})
    view.update({
        "message_id": message_obj.get("message_id"),
        "chat_id": (message_obj.get("chat") or {}).get("id", target),
        "updated_at": utc_now(),
    })
    return {
        "ok": True,
        "view": view,
        "message": payload["message"],
        "buttons": payload["buttons"],
        "result": result,
    }


def parse_callback(raw: str) -> tuple[str, str] | None:
    match = re.search(r"(?:callback_data:\s*)?(gchk:[^\s]+)", raw)
    token = match.group(1).strip() if match else raw.strip()
    parts = token.split(":")
    if len(parts) != 3 or parts[0] != CALLBACK_PREFIX:
        return None
    return parts[1], parts[2]


def edit_existing_view(state: dict[str, Any], target: str, account: str, thread_id: str | None, mode: str, dry_run: bool) -> dict[str, Any]:
    view = resolve_view(state, account, target, thread_id)
    session_ids = set(view.get("session_ids") or [])
    payload = render_message(state, mode=mode, session_ids=session_ids)
    result = telegram_edit_message(view, account, payload["message"], payload["buttons"], dry_run=dry_run)
    view["mode"] = mode
    view["updated_at"] = utc_now()
    return {
        "ok": True,
        "view": view,
        "message": payload["message"],
        "buttons": payload["buttons"],
        "result": result,
    }


def update_all_views(state: dict[str, Any], account: str, dry_run: bool) -> None:
    """Re-render every active view for this account. Used after an item status change."""
    views = state.get("views", {})
    stale_keys: list[str] = []
    for key, view in list(views.items()):
        if not isinstance(view, dict):
            continue
        if view.get("account") != account:
            continue
        if not view.get("message_id"):
            continue
        mode = view.get("mode", VIEW_NEEDED)
        target = view.get("target", "")
        thread_id = view.get("thread_id")
        try:
            edit_existing_view(state, target=target, account=account, thread_id=thread_id, mode=mode, dry_run=dry_run)
        except RuntimeError as exc:
            msg = str(exc).lower()
            if "message to edit not found" in msg or "message_id_invalid" in msg or "chat not found" in msg:
                stale_keys.append(key)
    for key in stale_keys:
        views.pop(key, None)


def handle_callback(state: dict[str, Any], callback: str, target: str, account: str, thread_id: str | None, dry_run: bool) -> dict[str, Any]:
    parsed = parse_callback(callback)
    if not parsed:
        raise RuntimeError("Unsupported callback payload.")
    action, value = parsed
    view = resolve_view(state, account, target, thread_id)
    if action == CALLBACK_TOGGLE:
        return toggle_pending(state, item_id=value, target=target, account=account, thread_id=thread_id, dry_run=dry_run)
    if action == CALLBACK_COMMIT:
        return commit_pending(state, target=target, account=account, thread_id=thread_id, dry_run=dry_run)
    if action == CALLBACK_VIEW:
        mode = VIEW_ALL if value == VIEW_ALL else VIEW_NEEDED
        if mode == VIEW_NEEDED:
            view["session_ids"] = [item["id"] for item in sorted_items(state, STATUS_NEEDED)]
        if view.get("message_id"):
            return edit_existing_view(state, target=target, account=account, thread_id=thread_id, mode=mode, dry_run=dry_run)
        return send_telegram_view(state, target=target, account=account, mode=mode, thread_id=thread_id, dry_run=dry_run)
    raise RuntimeError("Unsupported callback action.")


def toggle_pending(state: dict[str, Any], item_id: str, target: str, account: str, thread_id: str | None, dry_run: bool) -> dict[str, Any]:
    """Immediately toggle item between needed and have, then update all active views."""
    item = state["items"].get(item_id)
    if not item:
        raise RuntimeError("Grocery item not found.")
    if item["status"] == STATUS_NEEDED:
        item["status"] = STATUS_HAVE
    else:
        item["status"] = STATUS_NEEDED
    item["updated_at"] = utc_now()
    update_all_views(state, account, dry_run)
    return {"ok": True, "item": {"id": item["id"], "name": item["name"], "status": item["status"]}}


def commit_pending(state: dict[str, Any], target: str, account: str, thread_id: str | None, dry_run: bool) -> dict[str, Any]:
    """Mark all pending items as bought and refresh the view. Kept for CLI use."""
    view = resolve_view(state, account, target, thread_id)
    pending_ids = set(view.get("pending_ids", []))
    for item_id in list(pending_ids):
        item = state["items"].get(item_id)
        if item:
            item["status"] = STATUS_HAVE
            item["updated_at"] = utc_now()
    view["pending_ids"] = []
    return edit_existing_view(state, target=target, account=account, thread_id=thread_id, mode=VIEW_NEEDED, dry_run=dry_run)


def print_json(data: dict[str, Any]) -> None:
    json.dump(data, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Pantry-backed grocery checklist for OpenClaw and Telegram.")
    parser.add_argument("--state-file", default=None)
    sub = parser.add_subparsers(dest="command", required=True)

    for name, status in [("need", STATUS_NEEDED), ("out", STATUS_NEEDED), ("have", STATUS_HAVE), ("buy", STATUS_HAVE)]:
        cmd = sub.add_parser(name)
        cmd.add_argument("items", nargs="+")
        cmd.set_defaults(status=status)

    remove = sub.add_parser("remove")
    remove.add_argument("items", nargs="+")

    merge = sub.add_parser("merge")
    merge.add_argument("destination")
    merge.add_argument("sources", nargs="+")

    rename = sub.add_parser("rename")
    rename.add_argument("source")
    rename.add_argument("destination")

    show = sub.add_parser("show")
    show.add_argument("--mode", choices=[VIEW_NEEDED, VIEW_ALL], default=VIEW_NEEDED)
    show.add_argument("--json", action="store_true")

    ls = sub.add_parser("list")
    ls.add_argument("--status", choices=[STATUS_NEEDED, STATUS_HAVE, "all"], default="all")
    ls.add_argument("--json", action="store_true")

    stale_cmd = sub.add_parser("stale")
    stale_cmd.add_argument("--days", type=int, default=14)
    stale_cmd.add_argument("--json", action="store_true")

    render = sub.add_parser("render-telegram")
    render.add_argument("--target")
    render.add_argument("--account", default=DEFAULT_ACCOUNT)
    render.add_argument("--mode", choices=[VIEW_NEEDED, VIEW_ALL], default=VIEW_NEEDED)
    render.add_argument("--thread-id")
    render.add_argument("--dry-run", action="store_true")

    callback = sub.add_parser("handle-callback")
    callback.add_argument("callback")
    callback.add_argument("--target", required=True)
    callback.add_argument("--account", default=DEFAULT_ACCOUNT)
    callback.add_argument("--thread-id")
    callback.add_argument("--dry-run", action="store_true")

    toggle = sub.add_parser("toggle")
    toggle.add_argument("item_id")
    toggle.add_argument("--target", required=True)
    toggle.add_argument("--account", default=DEFAULT_ACCOUNT)
    toggle.add_argument("--thread-id")
    toggle.add_argument("--dry-run", action="store_true")

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    path = Path(args.state_file).expanduser() if args.state_file else state_path()
    state = load_state(path)
    changed = False

    if args.command in {"need", "out", "have", "buy"}:
        items = update_status(state, args.items, args.status)
        changed = True
        save_state(path, state)
        print_json({
            "ok": True,
            "updated": [{"id": item["id"], "name": item["name"], "status": item["status"]} for item in items],
            "state_file": str(path),
        })
        return

    if args.command == "remove":
        removed = remove_items(state, args.items)
        changed = True
        save_state(path, state)
        print_json({"ok": True, "removed": removed, "state_file": str(path)})
        return

    if args.command == "merge":
        result = merge_items(state, args.destination, args.sources)
        changed = True
        save_state(path, state)
        print_json({
            "ok": True,
            "state_file": str(path),
            "item": {
                "id": result["item"]["id"],
                "name": result["item"]["name"],
                "status": result["item"]["status"],
            },
            "merged": result["merged"],
        })
        return

    if args.command == "rename":
        result = rename_item(state, args.source, args.destination)
        changed = True
        save_state(path, state)
        print_json({
            "ok": True,
            "state_file": str(path),
            "item": {
                "id": result["item"]["id"],
                "name": result["item"]["name"],
                "status": result["item"]["status"],
            },
            "renamed": args.source,
        })
        return

    if args.command == "show":
        payload = render_message(state, mode=args.mode)
        data = {"ok": True, "message": payload["message"], "buttons": payload["buttons"]}
        if args.json:
            print_json(data)
        else:
            print(strip_html(payload["message"]))
        return

    if args.command == "list":
        status = None if args.status == "all" else args.status
        items = sorted_items(state, status=status)
        data = {"ok": True, "items": items}
        if args.json:
            print_json(data)
        else:
            for item in items:
                print(f"{item['status']}: {item['name']}")
        return

    if args.command == "stale":
        threshold = datetime.now(timezone.utc) - timedelta(days=args.days)
        stale_items = [
            item for item in state["items"].values()
            if item.get("status") == STATUS_NEEDED
            and "updated_at" in item
            and datetime.fromisoformat(item["updated_at"].replace("Z", "+00:00")) < threshold
        ]
        stale_items.sort(key=lambda x: x.get("updated_at", ""))
        if args.json:
            print_json({"ok": True, "stale": stale_items, "days": args.days})
        else:
            if not stale_items:
                print(f"No items needed for more than {args.days} days.")
            else:
                print(f"Items needed for more than {args.days} days:")
                for item in stale_items:
                    print(f"  {item['name']} (since {item['updated_at'][:10]})")
        return

    if args.command == "render-telegram":
        if args.target:
            targets = [args.target]
        else:
            # No target specified: send to all users with an active view for this account,
            # falling back to the account's allowFrom list in openclaw.json.
            views = state.get("views", {})
            targets = [
                v["target"] for v in views.values()
                if isinstance(v, dict) and v.get("account") == args.account and v.get("target")
            ]
            if not targets:
                config = json.loads(openclaw_config_path().read_text(encoding="utf-8"))
                allow = (((config.get("channels") or {}).get("telegram") or {}).get("accounts") or {}).get(args.account, {}).get("allowFrom") or []
                targets = [str(t) for t in allow]
        results = []
        for target in targets:
            result = send_telegram_view(
                state,
                target=target,
                account=args.account,
                mode=args.mode,
                thread_id=args.thread_id,
                dry_run=args.dry_run,
            )
            results.append(result)
        if not args.dry_run:
            save_state(path, state)
        print_json(results[0] if len(results) == 1 else {"ok": True, "results": results})
        return

    if args.command == "handle-callback":
        result = handle_callback(
            state,
            callback=args.callback,
            target=args.target,
            account=args.account,
            thread_id=args.thread_id,
            dry_run=args.dry_run,
        )
        if not args.dry_run:
            save_state(path, state)
        print_json(result)
        return

    if args.command == "toggle":
        result = toggle_pending(
            state,
            item_id=args.item_id,
            target=args.target,
            account=args.account,
            thread_id=args.thread_id,
            dry_run=args.dry_run,
        )
        if not args.dry_run:
            save_state(path, state)
        print_json(result)
        return

    if changed:
        save_state(path, state)


if __name__ == "__main__":
    main()
