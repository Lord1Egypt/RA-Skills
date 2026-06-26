#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from contract import (
    WEEKLY_DEAL_BRIEF_SCHEMA_VERSION,
    WEEKLY_DEAL_DISCOUNT_BASES,
    WEEKLY_DEAL_DISPLAY_CATEGORIES,
    WEEKLY_DEAL_ENTRY_ROLES,
    WEEKLY_DEAL_SOURCE_TYPES,
    WEEKLY_DEAL_STORE_STATUSES,
)
from paths import KitchenCompassPaths, write_atomic

NON_WORD_RE = re.compile(r"[^a-z0-9]+")
URL_RE = re.compile(r"^https?://", re.IGNORECASE)
ROLE_SORT_ORDER = {
    "major-protein": 0,
    "supporting-ingredient": 1,
    "side": 2,
    "other": 3,
}
DISPLAY_CATEGORY_SORT_ORDER = {name: index for index, name in enumerate(WEEKLY_DEAL_DISPLAY_CATEGORIES)}
DISPLAY_CATEGORY_HEADERS = {
    "meat": "MEAT",
    "starch": "STARCH",
    "dairy": "DAIRY",
    "fruit-veg": "FRUIT / VEGGIE",
    "beverages": "BEVERAGES",
    "misc": "MISC",
}
MEAT_KEYWORDS = (
    "beef",
    "chicken",
    "pork",
    "salmon",
    "shrimp",
    "steak",
    "sausage",
    "turkey",
    "ham",
    "rib",
    "tenderloin",
    "roast",
    "lamb",
    "fish",
)
STARCH_KEYWORDS = (
    "rice",
    "pasta",
    "potato",
    "potatoes",
    "bread",
    "bun",
    "buns",
    "tortilla",
    "tortillas",
    "roll",
    "rolls",
    "dough",
    "noodle",
    "noodles",
)
DAIRY_KEYWORDS = (
    "cheese",
    "milk",
    "yogurt",
    "butter",
    "cream",
    "cottage",
    "mozzarella",
    "parmesan",
    "feta",
)
FRUIT_VEG_KEYWORDS = (
    "apple",
    "apples",
    "pear",
    "pears",
    "salad",
    "lettuce",
    "broccoli",
    "squash",
    "asparagus",
    "avocado",
    "avocados",
    "cucumber",
    "cucumbers",
    "mango",
    "orange",
    "oranges",
    "tomato",
    "tomatoes",
    "brussels",
    "green beans",
    "mushroom",
    "mushrooms",
    "berry",
    "berries",
    "fruit",
)
BEVERAGE_KEYWORDS = (
    "coffee",
    "tea",
    "soda",
    "juice",
    "drink",
    "water",
    "sparkling",
    "kombucha",
    "beer",
    "wine",
)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")



def slugify(text: str) -> str:
    return NON_WORD_RE.sub("-", (text or "").lower()).strip("-")



def unique_strings(values: list[Any]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        text = str(value or "").strip()
        if not text or text in seen:
            continue
        seen.add(text)
        output.append(text)
    return output



def normalize_source(raw: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = dict(raw or {})
    source_type = slugify(str(payload.get("type") or "manual-note")) or "manual-note"
    if source_type not in WEEKLY_DEAL_SOURCE_TYPES:
        source_type = "manual-note"
    return {
        "type": source_type,
        "url": str(payload.get("url") or "").strip(),
        "label": str(payload.get("label") or "").strip(),
        "notes": str(payload.get("notes") or "").strip(),
        "last_verified_at": payload.get("last_verified_at"),
        "captured_at": payload.get("captured_at"),
    }



def normalize_retrieval_recipe(raw: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = dict(raw or {})
    return {
        "starting_url": str(payload.get("starting_url") or "").strip(),
        "fallback_url": str(payload.get("fallback_url") or "").strip(),
        "store_selector_hint": str(payload.get("store_selector_hint") or "").strip(),
        "steps": unique_strings(list(payload.get("steps", []))),
        "known_friction": unique_strings(list(payload.get("known_friction", []))),
        "last_successful_url": str(payload.get("last_successful_url") or "").strip(),
        "last_successful_at": payload.get("last_successful_at"),
        "notes": str(payload.get("notes") or "").strip(),
    }


VALID_SCAN_DAYS = {
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
}
TIME_OF_DAY_RE = re.compile(r"^(?:[01]\d|2[0-3]):[0-5]\d$")



def normalize_weekly_deal_scan_schedule(raw: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = dict(raw or {})
    return {
        "day_of_week": slugify(str(payload.get("day_of_week") or "")),
        "time_local": str(payload.get("time_local") or "").strip(),
        "timezone": str(payload.get("timezone") or "").strip(),
    }



def normalize_deal_store(raw: dict[str, Any]) -> dict[str, Any]:
    label = str(raw.get("label") or "").strip()
    store_id = slugify(str(raw.get("id") or label))
    retailer = slugify(str(raw.get("retailer") or ""))
    status = slugify(str(raw.get("status") or "active")) or "active"
    if status not in WEEKLY_DEAL_STORE_STATUSES:
        status = "active"
    return {
        "id": store_id,
        "label": label,
        "retailer": retailer,
        "store_code": str(raw.get("store_code") or "").strip(),
        "location_notes": str(raw.get("location_notes") or "").strip(),
        "status": status,
        "manual_setup_required": bool(raw.get("manual_setup_required", True)),
        "source": normalize_source(raw.get("source")),
        "retrieval_recipe": normalize_retrieval_recipe(raw.get("retrieval_recipe")),
        "notes": str(raw.get("notes") or "").strip(),
    }



def ensure_stores_config_shape(state: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = dict(state or {})
    weekly = dict(payload.get("weekly_deal_brief") or {})
    stores = [normalize_deal_store(item) for item in weekly.get("stores", [])]
    store_ids = {item["id"] for item in stores if item.get("id")}
    preferred_stores = [slugify(value) for value in payload.get("preferred_stores", []) if slugify(str(value))]
    default_store_ids = [slugify(value) for value in weekly.get("default_store_ids", []) if slugify(str(value)) in store_ids]
    normalized_weekly = {
        "enabled": bool(weekly.get("enabled", False)),
        "default_store_ids": list(dict.fromkeys(default_store_ids)),
        "scan_schedule": normalize_weekly_deal_scan_schedule(weekly.get("scan_schedule")),
        "stores": sorted(stores, key=lambda item: (item.get("retailer", ""), item.get("label", "").lower())),
    }
    for key, value in weekly.items():
        if key not in normalized_weekly:
            normalized_weekly[key] = value
    normalized = {
        "preferred_stores": list(dict.fromkeys(preferred_stores)),
        "notes": unique_strings(list(payload.get("notes", []))),
        "item_preferences": payload.get("item_preferences") or {},
        "weekly_deal_brief": normalized_weekly,
    }
    for key, value in payload.items():
        if key not in normalized:
            normalized[key] = value
    return normalized



def load_stores_config(paths: KitchenCompassPaths) -> dict[str, Any]:
    path = paths.household_dir / "stores.json"
    if not path.exists():
        return ensure_stores_config_shape()
    return ensure_stores_config_shape(json.loads(path.read_text()))


def load_raw_stores_config(paths: KitchenCompassPaths) -> dict[str, Any]:
    path = paths.household_dir / "stores.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text())



def save_stores_config(paths: KitchenCompassPaths, state: dict[str, Any]) -> None:
    write_atomic(
        paths.household_dir / "stores.json",
        json.dumps(ensure_stores_config_shape(state), indent=2) + "\n",
    )



def load_weekly_deal_input(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text())



def save_weekly_deal_input(path: Path, payload: dict[str, Any]) -> None:
    write_atomic(path, json.dumps(payload, indent=2) + "\n")



def store_index(config: dict[str, Any]) -> dict[str, dict[str, Any]]:
    weekly = ensure_stores_config_shape(config).get("weekly_deal_brief", {})
    return {item["id"]: item for item in weekly.get("stores", [])}



def deal_store_by_id(config: dict[str, Any], store_id: str) -> dict[str, Any] | None:
    return store_index(config).get(slugify(store_id))



def replace_deal_store(config: dict[str, Any], store: dict[str, Any]) -> dict[str, Any]:
    normalized_store = normalize_deal_store(store)
    updated = deepcopy(config or {})
    weekly = deepcopy(updated.get("weekly_deal_brief") or {})
    stores = [
        normalize_deal_store(existing)
        for existing in weekly.get("stores", [])
        if normalize_deal_store(existing).get("id") != normalized_store["id"]
    ]
    stores.append(normalized_store)
    weekly["stores"] = stores
    updated["weekly_deal_brief"] = weekly
    normalized = ensure_stores_config_shape(updated)
    if normalized_store["id"] in normalized.get("weekly_deal_brief", {}).get("default_store_ids", []):
        normalized["preferred_stores"] = list(dict.fromkeys(normalized.get("preferred_stores", []) + [normalized_store["id"]]))
    return ensure_stores_config_shape(normalized)



def validate_stores_config(config: dict[str, Any]) -> list[str]:
    normalized = ensure_stores_config_shape(config)
    errors: list[str] = []
    seen_ids: set[str] = set()
    weekly = normalized.get("weekly_deal_brief", {})
    raw_weekly = dict((config or {}).get("weekly_deal_brief") or {})
    raw_default_store_ids = [
        slugify(str(value))
        for value in raw_weekly.get("default_store_ids", [])
        if slugify(str(value))
    ]

    for store in weekly.get("stores", []):
        store_id = store.get("id") or "<missing>"
        if store_id in seen_ids:
            errors.append(f"duplicate weekly_deal_brief store id: {store_id}")
        seen_ids.add(store_id)
        if not store.get("label"):
            errors.append(f"store {store_id}: label is required")
        if not store.get("retailer"):
            errors.append(f"store {store_id}: retailer is required")
        if store.get("status") not in WEEKLY_DEAL_STORE_STATUSES:
            errors.append(f"store {store_id}: invalid status {store.get('status')}")
        source = normalize_source(store.get("source"))
        if source.get("type") not in WEEKLY_DEAL_SOURCE_TYPES:
            errors.append(f"store {store_id}: invalid source type {source.get('type')}")
        if source.get("url") and not URL_RE.match(source["url"]):
            errors.append(f"store {store_id}: source.url must start with http:// or https://")
        if source.get("type") == "manual-note":
            if not source.get("notes"):
                errors.append(f"store {store_id}: manual-note source requires source.notes")
        elif not source.get("url"):
            errors.append(f"store {store_id}: source.url is required for source type {source.get('type')}")

        retrieval_recipe = normalize_retrieval_recipe(store.get("retrieval_recipe"))
        for field_name in ("starting_url", "fallback_url", "last_successful_url"):
            value = retrieval_recipe.get(field_name)
            if value and not URL_RE.match(value):
                errors.append(f"store {store_id}: retrieval_recipe.{field_name} must start with http:// or https://")

    schedule = normalize_weekly_deal_scan_schedule(weekly.get("scan_schedule"))
    if any(schedule.values()):
        if schedule["day_of_week"] not in VALID_SCAN_DAYS:
            errors.append("weekly_deal_brief.scan_schedule.day_of_week must be a weekday name like friday")
        if not TIME_OF_DAY_RE.match(schedule["time_local"]):
            errors.append("weekly_deal_brief.scan_schedule.time_local must use HH:MM 24-hour format")
        if not schedule["timezone"]:
            errors.append("weekly_deal_brief.scan_schedule.timezone is required when scan_schedule is set")

    for store_id in raw_default_store_ids:
        if store_id not in seen_ids:
            errors.append(f"weekly_deal_brief default store id not found: {store_id}")

    return errors



def render_store(store: dict[str, Any]) -> str:
    source = store.get("source", {})
    retrieval_recipe = normalize_retrieval_recipe(store.get("retrieval_recipe"))
    lines = [
        f"- {store['label']} [{store['id']}]",
        f"  retailer={store['retailer']} | status={store['status']} | manual_setup_required={str(store.get('manual_setup_required', True)).lower()}",
        f"  source={source.get('type', 'manual-note')} | url={source.get('url') or '-'} | store_code={store.get('store_code') or '-'}",
    ]
    if store.get("location_notes"):
        lines.append(f"  location_notes={store['location_notes']}")
    if source.get("notes"):
        lines.append(f"  source_notes={source['notes']}")
    if any(retrieval_recipe.get(key) for key in ("starting_url", "fallback_url", "store_selector_hint", "last_successful_url", "notes")) or retrieval_recipe.get("steps") or retrieval_recipe.get("known_friction"):
        lines.append(
            f"  retrieval_start={retrieval_recipe.get('starting_url') or '-'} | fallback={retrieval_recipe.get('fallback_url') or '-'} | last_success_url={retrieval_recipe.get('last_successful_url') or '-'}"
        )
        if retrieval_recipe.get("store_selector_hint"):
            lines.append(f"  store_selector_hint={retrieval_recipe['store_selector_hint']}")
        if retrieval_recipe.get("steps"):
            lines.append(f"  retrieval_steps={' -> '.join(retrieval_recipe['steps'])}")
        if retrieval_recipe.get("known_friction"):
            lines.append(f"  known_friction={', '.join(retrieval_recipe['known_friction'])}")
        if retrieval_recipe.get("notes"):
            lines.append(f"  retrieval_notes={retrieval_recipe['notes']}")
    if store.get("notes"):
        lines.append(f"  notes={store['notes']}")
    return "\n".join(lines)



def alpha_label(index: int) -> str:
    value = index + 1
    output = ""
    while value > 0:
        value, remainder = divmod(value - 1, 26)
        output = chr(ord("A") + remainder) + output
    return output



def normalize_price(raw: dict[str, Any] | None = None) -> dict[str, Any] | None:
    if raw is None:
        return None
    payload = dict(raw)
    amount = payload.get("amount")
    if amount in (None, ""):
        return None
    return {
        "amount": round(float(amount), 2),
        "currency": str(payload.get("currency") or "USD").strip() or "USD",
        "unit_text": str(payload.get("unit_text") or "").strip(),
    }



def format_money(amount: float) -> str:
    return f"${float(amount):.2f}"



def price_text_from_price(price: dict[str, Any] | None) -> str:
    if not price:
        return ""
    unit_text = str(price.get("unit_text") or "").strip()
    return f"{format_money(float(price['amount']))}/{unit_text}" if unit_text else format_money(float(price["amount"]))



def computed_discount_percent(sale_price: dict[str, Any] | None, regular_price: dict[str, Any] | None) -> int | None:
    if not sale_price or not regular_price:
        return None
    if sale_price.get("currency") != regular_price.get("currency"):
        return None
    sale_unit = str(sale_price.get("unit_text") or "").strip().lower()
    regular_unit = str(regular_price.get("unit_text") or "").strip().lower()
    if sale_unit and regular_unit and sale_unit != regular_unit:
        return None
    sale_amount = float(sale_price.get("amount") or 0)
    regular_amount = float(regular_price.get("amount") or 0)
    if sale_amount <= 0 or regular_amount <= 0 or regular_amount <= sale_amount:
        return None
    return int(round(((regular_amount - sale_amount) / regular_amount) * 100))



def normalize_brief_source(raw: dict[str, Any] | None, store: dict[str, Any] | None) -> dict[str, Any]:
    if raw:
        source = normalize_source(raw)
        if source.get("url") or source.get("notes") or raw.get("captured_at"):
            return source
    if store:
        return normalize_source((store or {}).get("source"))
    return normalize_source()



def infer_display_category(title: str, role: str) -> str:
    lowered = title.lower()
    if role == "major-protein" or any(keyword in lowered for keyword in MEAT_KEYWORDS):
        return "meat"
    if any(keyword in lowered for keyword in STARCH_KEYWORDS):
        return "starch"
    if any(keyword in lowered for keyword in DAIRY_KEYWORDS):
        return "dairy"
    if any(keyword in lowered for keyword in FRUIT_VEG_KEYWORDS):
        return "fruit-veg"
    if any(keyword in lowered for keyword in BEVERAGE_KEYWORDS):
        return "beverages"
    return "misc"



def default_weekly_deal_store_ids(stores_config: dict[str, Any]) -> list[str]:
    config = ensure_stores_config_shape(stores_config)
    weekly = config.get("weekly_deal_brief", {})
    default_store_ids = list(dict.fromkeys(weekly.get("default_store_ids", [])))
    if default_store_ids:
        return default_store_ids
    return [store["id"] for store in weekly.get("stores", []) if store.get("status") == "active"]



def display_category_header(category: str) -> str:
    return DISPLAY_CATEGORY_HEADERS.get(category, category.upper())



def store_display_name(store: dict[str, Any]) -> str:
    retailer = str(store.get("retailer") or "").strip()
    if not retailer:
        label = str(store.get("label") or "").strip()
        return label or "Store"
    tokens = [token.upper() if token in {"acme", "giant"} else token.capitalize() for token in retailer.split("-") if token]
    return " ".join(tokens) or retailer



def normalize_weekly_deal_entry(raw: dict[str, Any], position: int) -> dict[str, Any]:
    title = str(raw.get("title") or "").strip()
    role = slugify(str(raw.get("brief_role") or "other")) or "other"
    if role not in WEEKLY_DEAL_ENTRY_ROLES:
        role = "other"
    sale_price = normalize_price(raw.get("sale_price"))
    regular_price = normalize_price(raw.get("regular_price"))
    price_text = str(raw.get("price_text") or "").strip() or price_text_from_price(sale_price)
    regular_price_text = str(raw.get("regular_price_text") or "").strip() or price_text_from_price(regular_price)
    if not title:
        raise ValueError("each weekly deal item requires title")
    if not price_text:
        raise ValueError(f"weekly deal item '{title}' requires price_text or sale_price.amount")

    why_it_matters = str(raw.get("why_it_matters") or "").strip()
    if not why_it_matters:
        raise ValueError(f"weekly deal item '{title}' requires why_it_matters")

    meal_lanes = unique_strings(list(raw.get("meal_lanes", [])))
    if not meal_lanes:
        raise ValueError(f"weekly deal item '{title}' requires at least one meal_lanes entry")

    explicit_discount = raw.get("discount_percent")
    computed_discount = computed_discount_percent(sale_price, regular_price)
    discount_percent = int(round(float(explicit_discount))) if explicit_discount not in (None, "") else computed_discount
    if discount_percent is not None and discount_percent < 0:
        raise ValueError(f"weekly deal item '{title}' has invalid discount_percent")

    discount_basis = str(raw.get("discount_basis") or "").strip()
    if discount_percent is None:
        discount_basis = None
    elif discount_basis:
        if discount_basis not in WEEKLY_DEAL_DISCOUNT_BASES:
            raise ValueError(f"weekly deal item '{title}' has invalid discount_basis")
    else:
        discount_basis = "source-exposed" if explicit_discount not in (None, "") else "computed"

    raw_display_category = slugify(str(raw.get("display_category") or ""))
    display_category = raw_display_category or infer_display_category(title, role)
    if display_category not in WEEKLY_DEAL_DISPLAY_CATEGORIES:
        raise ValueError(f"weekly deal item '{title}' has invalid display_category")

    return {
        "title": title,
        "brief_role": role,
        "price_text": price_text,
        "sale_price": sale_price,
        "regular_price": regular_price,
        "regular_price_text": regular_price_text,
        "discount_percent": discount_percent,
        "discount_basis": discount_basis,
        "display_category": display_category,
        "why_it_matters": why_it_matters,
        "meal_lanes": meal_lanes,
        "recipe_slugs": [slugify(value) for value in raw.get("recipe_slugs", []) if slugify(str(value))],
        "source_text": str(raw.get("source_text") or "").strip(),
        "input_position": position,
    }



def normalize_weekly_deal_input(raw: dict[str, Any], stores_config: dict[str, Any]) -> dict[str, Any]:
    payload = dict(raw or {})
    weekly = ensure_stores_config_shape(stores_config).get("weekly_deal_brief", {})
    store_id = slugify(str(payload.get("store_id") or ""))
    if not store_id:
        default_store_ids = list(weekly.get("default_store_ids", []))
        if len(default_store_ids) == 1:
            store_id = default_store_ids[0]
        elif len(weekly.get("stores", [])) == 1:
            store_id = weekly["stores"][0]["id"]
    if not store_id:
        raise ValueError("weekly deal brief input requires store_id unless exactly one configured deal store exists")

    store = deal_store_by_id(stores_config, store_id)
    if not store:
        raise ValueError(f"weekly deal brief input references unknown store_id: {store_id}")

    items = payload.get("items") or []
    normalized_items = [normalize_weekly_deal_entry(item, index) for index, item in enumerate(items)]

    sorted_items = sorted(
        normalized_items,
        key=lambda item: (
            ROLE_SORT_ORDER[item["brief_role"]],
            DISPLAY_CATEGORY_SORT_ORDER.get(item["display_category"], len(DISPLAY_CATEGORY_SORT_ORDER)),
            item["input_position"],
        ),
    )
    entries: list[dict[str, Any]] = []
    for index, item in enumerate(sorted_items):
        entry = deepcopy(item)
        entry["brief_label"] = alpha_label(index)
        entry["discount_text"] = (
            f"{entry['discount_percent']}% off ({entry['discount_basis']})"
            if entry.get("discount_percent") is not None and entry.get("discount_basis")
            else None
        )
        entries.append(entry)

    source = normalize_brief_source(payload.get("source"), store)
    if source.get("type") != "manual-note" and not source.get("url"):
        raise ValueError("weekly deal brief source requires a URL unless source.type is manual-note")
    if source.get("type") == "manual-note" and not source.get("notes"):
        raise ValueError("weekly deal brief manual-note source requires notes")

    return {
        "version": WEEKLY_DEAL_BRIEF_SCHEMA_VERSION,
        "generated_at": utc_now_iso(),
        "week_of": str(payload.get("week_of") or "").strip(),
        "curated_by": str(payload.get("curated_by") or "manual").strip() or "manual",
        "notes": str(payload.get("notes") or "").strip(),
        "manual_setup_required": True,
        "store": {
            "id": store["id"],
            "label": store["label"],
            "retailer": store["retailer"],
            "store_code": store.get("store_code") or "",
        },
        "source": source,
        "summary": {
            "total_items": len(entries),
            "major_protein_count": sum(1 for entry in entries if entry["brief_role"] == "major-protein"),
            "supporting_item_count": sum(1 for entry in entries if entry["brief_role"] in {"supporting-ingredient", "side"}),
            "other_item_count": sum(1 for entry in entries if entry["brief_role"] == "other"),
        },
        "entries": entries,
    }



def render_weekly_deal_brief_markdown(brief: dict[str, Any]) -> str:
    lines = [
        f"# Weekly Deal Brief — {brief['store']['label']}",
        "",
        f"- Week of: {brief.get('week_of') or 'not set'}",
        f"- Retailer: {brief['store']['retailer']}",
        f"- Store id: {brief['store']['id']}",
        f"- Source type: {brief['source']['type']}",
        f"- Source URL: {brief['source'].get('url') or '-'}",
        f"- Manual setup required: true",
        f"- Curated by: {brief.get('curated_by') or 'manual'}",
        "",
        "This brief is decision support only. Kitchen Compass does not treat these deals as planner scoring input.",
        "",
        "## Relevant deals",
        "",
    ]
    if not brief.get("entries"):
        lines.append("No relevant deals were surfaced for this store in the current brief.")
    for entry in brief.get("entries", []):
        role_label = entry["brief_role"].replace("-", " ")
        discount_fragment = f" — {entry['discount_percent']}% off" if entry.get("discount_percent") is not None else ""
        lines.append(f"- **{entry['brief_label']}. {entry['title']}** ({role_label}) — **{entry['price_text']}**{discount_fragment}")
        lines.append(f"  - Why it matters: {entry['why_it_matters']}")
        lines.append(f"  - Meal lanes: {'; '.join(entry['meal_lanes'])}")
        lines.append(f"  - Display category: {entry['display_category']}")
        if entry.get("recipe_slugs"):
            lines.append(f"  - Recipe slugs: {', '.join(entry['recipe_slugs'])}")
        if entry.get("source_text"):
            lines.append(f"  - Source note: {entry['source_text']}")
    if brief.get("notes"):
        lines.extend(["", "## Notes", "", brief["notes"]])
    return "\n".join(lines).rstrip() + "\n"



def combine_weekly_deal_briefs(briefs: list[dict[str, Any]]) -> dict[str, Any]:
    if not briefs:
        raise ValueError("combined weekly deal sheet requires at least one store brief")

    week_values = {brief.get('week_of') or '' for brief in briefs}
    if len(week_values) > 1:
        raise ValueError(f"combined weekly deal sheet requires matching week_of values; found: {sorted(week_values)}")

    combined_entries: list[dict[str, Any]] = []
    for brief in briefs:
        for entry in brief.get('entries', []):
            combined_entries.append(
                {
                    'store_id': brief['store']['id'],
                    'store_label': brief['store']['label'],
                    'store_display_name': store_display_name(brief['store']),
                    'retailer': brief['store']['retailer'],
                    'display_category': entry['display_category'],
                    'title': entry['title'],
                    'sale_price_text': entry['price_text'],
                    'normal_price_text': entry.get('regular_price_text') or '',
                    'brief_role': entry['brief_role'],
                    'why_it_matters': entry['why_it_matters'],
                    'meal_lanes': entry['meal_lanes'],
                    'source_text': entry.get('source_text') or '',
                }
            )

    categories = []
    for category in WEEKLY_DEAL_DISPLAY_CATEGORIES:
        entries = [entry for entry in combined_entries if entry['display_category'] == category]
        entries.sort(key=lambda item: (item['store_label'].lower(), item['title'].lower()))
        categories.append(
            {
                'key': category,
                'label': display_category_header(category),
                'entries': entries,
            }
        )

    return {
        'version': WEEKLY_DEAL_BRIEF_SCHEMA_VERSION,
        'generated_at': utc_now_iso(),
        'week_of': briefs[0].get('week_of') or '',
        'store_ids': [brief['store']['id'] for brief in briefs],
        'store_labels': [store_display_name(brief['store']) for brief in briefs],
        'category_count': len(categories),
        'entry_count': len(combined_entries),
        'categories': categories,
    }



def render_combined_weekly_deal_sheet_markdown(payload: dict[str, Any]) -> str:
    lines = [
        '# Combined Weekly Deal Sheet',
        '',
        f"- Week of: {payload.get('week_of') or 'not set'}",
        f"- Stores included: {', '.join(payload.get('store_labels', [])) or '-'}",
        '',
    ]
    for category in payload.get('categories', []):
        lines.extend([f"## {category['label']}", ""])
        if not category.get('entries'):
            lines.append('None surfaced from the current saved outputs')
            lines.append('')
            continue
        for entry in category['entries']:
            fragments = [entry['store_display_name'], entry['title'], entry['sale_price_text']]
            if entry.get('normal_price_text'):
                fragments.append(entry['normal_price_text'])
            lines.append(f"- {' — '.join(fragments)}")
        lines.append('')
    return '\n'.join(lines).rstrip() + '\n'
