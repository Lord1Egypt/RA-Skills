#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from contract import (
    INVENTORY_KINDS,
    INVENTORY_LOCATIONS,
    INVENTORY_PRIORITIES,
    INVENTORY_SCHEMA_VERSION,
)
from paths import KitchenCompassPaths, append_jsonl, write_atomic

NON_WORD_RE = re.compile(r"[^a-z0-9]+")
TOKEN_RE = re.compile(r"[a-z0-9]+")

UNIT_ALIASES = {
    "lb": "lb",
    "lbs": "lb",
    "pound": "lb",
    "pounds": "lb",
    "oz": "oz",
    "ounce": "oz",
    "ounces": "oz",
    "each": "each",
    "ea": "each",
    "count": "each",
    "piece": "each",
    "pieces": "each",
    "unit": "each",
    "units": "each",
    "pack": "pack",
    "packs": "pack",
    "package": "pack",
    "packages": "pack",
    "bag": "bag",
    "bags": "bag",
    "container": "container",
    "containers": "container",
    "portion": "portion",
    "portions": "portion",
    "meal": "portion",
    "meals": "portion",
    "serving": "portion",
    "servings": "portion",
}

PROTEIN_ALIASES = {
    "beef": "beef",
    "steak": "beef",
    "ground-beef": "beef",
    "burger": "beef",
    "burgers": "beef",
    "chicken": "chicken",
    "pork": "pork",
    "sausage": "pork",
    "tenderloin": "pork",
    "chops": "pork",
    "shrimp": "shrimp",
    "fish": "fish",
    "salmon": "fish",
    "cod": "fish",
    "turkey": "turkey",
}

INVENTORY_BONUS_PROFILES = {
    False: {
        "bonus_cap": 7,
        "match_type_boosts": {
            "recipe-slug": 0,
            "search-term": 0,
            "core-protein": 0,
        },
    },
    True: {
        "bonus_cap": 11,
        "match_type_boosts": {
            "recipe-slug": 3,
            "search-term": 2,
            "core-protein": 0,
        },
    },
}


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")



def slugify(text: str) -> str:
    return NON_WORD_RE.sub("-", text.lower()).strip("-")



def normalize_text(text: str) -> str:
    return " ".join(TOKEN_RE.findall((text or "").lower()))



def normalize_unit(unit: str) -> str:
    normalized = slugify(unit or "")
    return UNIT_ALIASES.get(normalized, normalized or "each")



def quantity_dict(amount: float, unit: str) -> dict[str, Any]:
    return {"amount": round(float(amount), 3), "unit": normalize_unit(unit)}



def format_amount(amount: float) -> str:
    rounded = round(float(amount), 3)
    return str(int(rounded)) if rounded.is_integer() else (f"{rounded:.3f}".rstrip("0").rstrip("."))



def format_quantity(quantity: dict[str, Any]) -> str:
    amount = float(quantity.get("amount", 0) or 0)
    unit = normalize_unit(str(quantity.get("unit", "each")))
    return f"{format_amount(amount)} {unit}"



def unit_family(unit: str) -> str:
    unit = normalize_unit(unit)
    if unit in {"lb", "oz"}:
        return "weight"
    if unit in {"each", "pack", "bag", "container", "portion"}:
        return "count"
    return "other"



def convert_amount(amount: float, from_unit: str, to_unit: str) -> float:
    from_unit = normalize_unit(from_unit)
    to_unit = normalize_unit(to_unit)
    if from_unit == to_unit:
        return float(amount)
    if unit_family(from_unit) != unit_family(to_unit):
        raise ValueError(f"Cannot convert {from_unit} to {to_unit}")
    if from_unit == "lb" and to_unit == "oz":
        return float(amount) * 16
    if from_unit == "oz" and to_unit == "lb":
        return float(amount) / 16
    raise ValueError(f"Unsupported conversion from {from_unit} to {to_unit}")



def normalize_core_protein(value: str) -> str | None:
    normalized = slugify(value or "")
    if not normalized:
        return None
    if normalized in PROTEIN_ALIASES:
        return PROTEIN_ALIASES[normalized]
    for token in normalized.split("-"):
        if token in PROTEIN_ALIASES:
            return PROTEIN_ALIASES[token]
    return normalized



def derive_core_proteins(label: str) -> list[str]:
    proteins: list[str] = []
    for token in slugify(label).split("-"):
        protein = normalize_core_protein(token)
        if protein and protein in {"beef", "chicken", "pork", "shrimp", "fish", "turkey"} and protein not in proteins:
            proteins.append(protein)
    return proteins



def ensure_inventory_state_shape(state: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = dict(state or {})
    items = payload.get("items") or []
    return {
        "version": payload.get("version", INVENTORY_SCHEMA_VERSION),
        "updated_at": payload.get("updated_at"),
        "items": [normalize_inventory_item(item) for item in items],
    }



def load_inventory_state(paths: KitchenCompassPaths) -> dict[str, Any]:
    path = paths.inventory_items_file
    if not path.exists():
        return ensure_inventory_state_shape()
    payload = json.loads(path.read_text())
    version = payload.get("version")
    if version is not None and version != INVENTORY_SCHEMA_VERSION:
        raise SystemExit(
            f"{path}: inventory schema version {version} is not supported "
            f"(this engine reads version {INVENTORY_SCHEMA_VERSION})."
        )
    return ensure_inventory_state_shape(payload)



def save_inventory_state(paths: KitchenCompassPaths, state: dict[str, Any]) -> None:
    normalized = ensure_inventory_state_shape(state)
    normalized["updated_at"] = utc_now_iso()
    write_atomic(paths.inventory_items_file, json.dumps(normalized, indent=2) + "\n")



def append_inventory_transaction(paths: KitchenCompassPaths, event: dict[str, Any]) -> None:
    append_jsonl(paths.inventory_transactions_file, event)



def recipe_text_blob(recipe: dict[str, Any]) -> str:
    return normalize_text(" ".join([
        recipe.get("title", ""),
        recipe.get("slug", ""),
        recipe.get("search_blob", ""),
        recipe.get("ingredients_blob", ""),
        recipe.get("core_protein", ""),
    ]))



def recipe_token_set(recipe: dict[str, Any]) -> set[str]:
    return set(TOKEN_RE.findall(recipe_text_blob(recipe)))



def significant_tokens(tokens: set[str]) -> set[str]:
    return {token for token in tokens if len(token) >= 4}



def quantity_bonus_multiplier(quantity: dict[str, Any]) -> float:
    amount = float(quantity.get("amount", 0) or 0)
    unit = normalize_unit(str(quantity.get("unit", "each")))
    if amount <= 0:
        return 0.0
    if unit == "oz":
        amount = convert_amount(amount, "oz", "lb")
        unit = "lb"
    if unit == "lb":
        if amount >= 2:
            return 1.0
        if amount >= 1:
            return 0.75
        return 0.45
    if unit == "portion":
        if amount >= 2:
            return 0.9
        return 0.7
    if unit in {"each", "pack", "bag", "container"}:
        if amount >= 2:
            return 0.8
        return 0.6
    return 0.55



def item_is_available(item: dict[str, Any]) -> bool:
    quantity = item.get("quantity") or {}
    return float(quantity.get("amount", 0) or 0) > 0



def derive_default_match_rules(label: str, explicit_core_proteins: list[str] | None = None) -> dict[str, list[str]]:
    terms = [normalize_text(label)] if normalize_text(label) else []
    core_proteins = explicit_core_proteins if explicit_core_proteins is not None else derive_core_proteins(label)
    return {
        "recipe_slugs": [],
        "search_terms": terms,
        "core_proteins": core_proteins,
    }



def normalize_match_rules(label: str, rules: dict[str, Any] | None = None) -> dict[str, list[str]]:
    payload = rules or {}
    derived = derive_default_match_rules(label)
    recipe_slugs = [slugify(value) for value in payload.get("recipe_slugs", []) if slugify(str(value))]
    search_terms_raw = payload.get("search_terms")
    search_terms = [normalize_text(str(value)) for value in (search_terms_raw or []) if normalize_text(str(value))]
    core_values = payload.get("core_proteins")
    core_proteins = [protein for value in (core_values or []) if (protein := normalize_core_protein(str(value)))]
    return {
        "recipe_slugs": list(dict.fromkeys(recipe_slugs or derived["recipe_slugs"])),
        "search_terms": list(dict.fromkeys(search_terms or derived["search_terms"])),
        "core_proteins": list(dict.fromkeys(core_proteins or derived["core_proteins"])),
    }



def normalize_inventory_item(raw: dict[str, Any]) -> dict[str, Any]:
    label = str(raw.get("label") or "").strip()
    location = slugify(str(raw.get("location") or "freezer")) or "freezer"
    if location not in INVENTORY_LOCATIONS:
        location = "other"
    kind = slugify(str(raw.get("kind") or "other")) or "other"
    if kind not in INVENTORY_KINDS:
        kind = "other"
    priority = slugify(str(((raw.get("planning") or {}).get("priority") or "normal"))) or "normal"
    if priority not in INVENTORY_PRIORITIES:
        priority = "normal"

    quantity = raw.get("quantity") or {}
    amount = float(quantity.get("amount", 0) or 0)
    unit = normalize_unit(str(quantity.get("unit", "each")))
    item_id = slugify(str(raw.get("id") or f"{location}-{label}"))

    return {
        "id": item_id,
        "label": label,
        "location": location,
        "kind": kind,
        "quantity": quantity_dict(amount, unit),
        "match_rules": normalize_match_rules(label, raw.get("match_rules")),
        "planning": {"priority": priority},
        "notes": str(raw.get("notes") or "").strip(),
        "updated_at": raw.get("updated_at") or utc_now_iso(),
    }



def inventory_index(state: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {item["id"]: item for item in state.get("items", [])}



def inventory_item_by_id(state: dict[str, Any], item_id: str) -> dict[str, Any] | None:
    normalized = slugify(item_id)
    return inventory_index(state).get(normalized)



def ensure_unique_item_id(state: dict[str, Any], item_id: str) -> None:
    if inventory_item_by_id(state, item_id):
        raise ValueError(f"Inventory item already exists: {item_id}")



def replace_inventory_item(state: dict[str, Any], item: dict[str, Any]) -> dict[str, Any]:
    items = [existing for existing in state.get("items", []) if existing.get("id") != item["id"]]
    items.append(normalize_inventory_item(item))
    items.sort(key=lambda existing: (existing.get("location", ""), existing.get("label", "").lower()))
    return {
        **ensure_inventory_state_shape(state),
        "items": items,
    }



def available_inventory_items(state: dict[str, Any]) -> list[dict[str, Any]]:
    return [item for item in state.get("items", []) if item_is_available(item)]



def priority_bonus(priority: str) -> int:
    if priority == "prefer-soon":
        return 1
    if priority == "low":
        return -1
    return 0



def inventory_bonus_profile(prioritize_inventory: bool) -> dict[str, Any]:
    return INVENTORY_BONUS_PROFILES[bool(prioritize_inventory)]



def top_inventory_match(recipe: dict[str, Any], item: dict[str, Any], prioritize_inventory: bool = False) -> dict[str, Any] | None:
    if not item_is_available(item):
        return None

    recipe_blob = recipe_text_blob(recipe)
    recipe_tokens = recipe_token_set(recipe)
    recipe_significant_tokens = significant_tokens(recipe_tokens)
    base_bonus = 0
    match_type = ""
    match_reason = ""

    recipe_slugs = set(item.get("match_rules", {}).get("recipe_slugs", []))
    if recipe.get("slug") in recipe_slugs:
        base_bonus = 6
        match_type = "recipe-slug"
        match_reason = f"explicitly tagged for {recipe['title']}"

    for term in item.get("match_rules", {}).get("search_terms", []):
        if not term:
            continue
        term_tokens = set(TOKEN_RE.findall(term))
        if not term_tokens:
            continue
        term_significant_tokens = significant_tokens(term_tokens)
        if term in recipe_blob:
            if 5 > base_bonus:
                base_bonus = 5
                match_type = "search-term"
                match_reason = f"matches recipe text for {term}"
        elif term_significant_tokens and len(term_significant_tokens & recipe_significant_tokens) >= (2 if len(term_tokens) > 1 else 1):
            if 4 > base_bonus:
                base_bonus = 4
                match_type = "search-term"
                match_reason = f"shares specific recipe tokens for {term}"

    recipe_core = normalize_core_protein(str(recipe.get("core_protein", "")))
    for core in item.get("match_rules", {}).get("core_proteins", []):
        if not core:
            continue
        if recipe_core == core or core in TOKEN_RE.findall(recipe_blob):
            if 3 > base_bonus:
                base_bonus = 3
                match_type = "core-protein"
                match_reason = f"fits the {core} lane"

    if base_bonus <= 0:
        return None

    quantity_multiplier = quantity_bonus_multiplier(item.get("quantity", {}))
    profile = inventory_bonus_profile(prioritize_inventory)
    match_type_boost = profile["match_type_boosts"].get(match_type, 0)
    bonus = max(1, round(base_bonus * quantity_multiplier) + priority_bonus(item.get("planning", {}).get("priority", "normal")) + match_type_boost)
    quantity_text = format_quantity(item["quantity"])
    explanation = f"you already have {quantity_text} {item['label']} in the {item['location']}"
    return {
        "item_id": item["id"],
        "label": item["label"],
        "location": item["location"],
        "quantity": deepcopy(item["quantity"]),
        "quantity_text": quantity_text,
        "bonus": bonus,
        "match_type": match_type,
        "match_reason": match_reason,
        "priority": item.get("planning", {}).get("priority", "normal"),
        "explanation": explanation,
    }



def recipe_inventory_support(recipe: dict[str, Any], state: dict[str, Any], prioritize_inventory: bool = False) -> dict[str, Any]:
    profile = inventory_bonus_profile(prioritize_inventory)
    matches = [match for item in available_inventory_items(state) if (match := top_inventory_match(recipe, item, prioritize_inventory=prioritize_inventory))]
    matches.sort(key=lambda match: (-match["bonus"], match["label"].lower()))
    total_bonus = min(profile["bonus_cap"], sum(match["bonus"] for match in matches[:2])) if matches else 0
    return {
        "mode": "prioritized" if prioritize_inventory else "light",
        "total_bonus": total_bonus,
        "matches": matches[:3],
    }



def build_transaction(action: str, item: dict[str, Any], before: dict[str, Any] | None = None, notes: str = "", metadata: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = {
        "timestamp": utc_now_iso(),
        "action": action,
        "item_id": item["id"],
        "label": item["label"],
        "location": item["location"],
        "quantity": deepcopy(item["quantity"]),
    }
    if before is not None:
        payload["before_quantity"] = deepcopy(before.get("quantity", {}))
    if notes:
        payload["notes"] = notes
    if metadata:
        payload.update(metadata)
    return payload



def subtract_quantity(current: dict[str, Any], amount: float, unit: str) -> dict[str, Any]:
    current_amount = float(current.get("amount", 0) or 0)
    current_unit = normalize_unit(str(current.get("unit", "each")))
    amount = float(amount)
    unit = normalize_unit(unit)
    subtraction = convert_amount(amount, unit, current_unit) if unit != current_unit else amount
    remaining = round(current_amount - subtraction, 3)
    if remaining < -0.0001:
        raise ValueError(f"Cannot use {format_amount(amount)} {unit}; only {format_quantity(current)} available")
    return quantity_dict(max(0.0, remaining), current_unit)
