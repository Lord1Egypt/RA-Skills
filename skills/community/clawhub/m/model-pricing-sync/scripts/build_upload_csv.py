from __future__ import annotations

import uuid
from pathlib import Path
from typing import Any

from _shared import (
    BUILD_ISSUE_FIELDS,
    CHANGE_FIELDS,
    CURRENT_API_FIELDS,
    CURRENT_SUBSCRIPTION_FIELDS,
    DATA_DIR,
    HISTORY_API_FIELDS,
    HISTORY_SUBSCRIPTION_FIELDS,
    SYNC_RUN_FIELDS,
    VENDOR_FIELDS,
    filter_vendor_configs,
    format_price,
    infer_amount_from_text,
    load_target_api_models,
    load_target_subscription_plans,
    load_vendor_configs,
    normalize_float,
    normalize_price,
    parse_bool,
    read_csv_rows,
    read_json_data,
    resolve_run_path,
    stable_key,
    utc_now,
    vendor_rows_from_configs,
    write_csv_rows,
)

API_SNAPSHOT_FIELDS = [
    "vendor_key",
    "vendor_name",
    "region",
    "product_name",
    "model_name",
    "price_dimension",
    "source_price_amount",
    "currency",
    "unit_basis",
    "normalized_price_usd",
    "normalized_unit",
    "original_price_text",
    "notes",
    "source_url",
    "is_active",
]

SUBSCRIPTION_SNAPSHOT_FIELDS = [
    "vendor_key",
    "vendor_name",
    "region",
    "product_name",
    "plan_name",
    "billing_cycle",
    "source_price_amount",
    "currency",
    "unit_basis",
    "normalized_price_usd",
    "normalized_unit",
    "seat_rule",
    "plan_summary",
    "original_price_text",
    "notes",
    "source_url",
    "is_active",
]

NUMERIC_SNAPSHOT_FIELDS = {"source_price_amount", "normalized_price_usd"}
BOOLEAN_SNAPSHOT_FIELDS = {"is_active"}
API_CHANGE_COMPARE_FIELDS = [field for field in API_SNAPSHOT_FIELDS if field != "notes"]
SUBSCRIPTION_CHANGE_COMPARE_FIELDS = [field for field in SUBSCRIPTION_SNAPSHOT_FIELDS if field != "notes"]


def build_issue(table_name: str, row_number: int, row: dict[str, Any], severity: str, message: str, created_at: str) -> dict[str, Any]:
    return {
        "issue_id": f"{table_name}:{row_number}:{uuid.uuid4().hex[:8]}",
        "table_name": table_name,
        "row_number": row_number,
        "vendor_key": row.get("vendor_key", ""),
        "source_url": row.get("source_url", ""),
        "severity": severity,
        "message": message,
        "created_at": created_at,
    }


def friendly_table_name(table_name: str) -> str:
    return {
        "api_pricing": "api_pricing.json",
        "subscription_plans": "subscription_plans.json",
    }.get(table_name, table_name)


def api_item_key(row: dict[str, Any]) -> str:
    return stable_key(
        [
            row.get("vendor_key", ""),
            row.get("region", ""),
            row.get("product_name", ""),
            row.get("model_name", ""),
            row.get("price_dimension", ""),
            row.get("unit_basis", ""),
        ]
    )


def subscription_item_key(row: dict[str, Any]) -> str:
    return stable_key(
        [
            row.get("vendor_key", ""),
            row.get("region", ""),
            row.get("product_name", ""),
            row.get("plan_name", ""),
            row.get("billing_cycle", ""),
            row.get("unit_basis", ""),
        ]
    )


def api_parent_key(row: dict[str, Any]) -> tuple[str, str, str, str]:
    return object_key(row, "model_name")


def subscription_parent_key(row: dict[str, Any]) -> tuple[str, str, str, str]:
    return object_key(row, "plan_name")


def scoped_target_keys(
    target_rows: list[dict[str, str]],
    name_field: str,
    run_vendor_keys: set[str],
    *,
    active: bool | None = None,
) -> set[tuple[str, str, str, str]]:
    keys: set[tuple[str, str, str, str]] = set()
    for target in target_rows:
        if target.get("vendor_key", "").strip() not in run_vendor_keys:
            continue
        if active is not None and parse_bool(target.get("is_active", "true")) != active:
            continue
        key = object_key(target, name_field)
        if all(key):
            keys.add(key)
    return keys


def api_child_label(row: dict[str, Any]) -> str:
    parts = [str(row.get("price_dimension", "")).strip(), str(row.get("unit_basis", "")).strip()]
    label = " / ".join(part for part in parts if part)
    return label or str(row.get("item_key", "")).strip()


def subscription_child_label(row: dict[str, Any]) -> str:
    parts = [str(row.get("billing_cycle", "")).strip(), str(row.get("unit_basis", "")).strip()]
    label = " / ".join(part for part in parts if part)
    return label or str(row.get("item_key", "")).strip()


def compact_summary(row: dict[str, Any] | None, display_name: str) -> str:
    if not row:
        return ""
    parts = [
        display_name,
        f"source={row.get('source_price_amount')} {row.get('currency')}".strip(),
        f"normalized={row.get('normalized_price_usd')} {row.get('normalized_unit')}".strip(),
        f"raw={row.get('original_price_text')}" if row.get("original_price_text") else "",
        "inactive" if row.get("is_active") is False or str(row.get("is_active", "")).lower() == "false" else "",
    ]
    return " | ".join(part for part in parts if part and part != "source= " and part != "normalized= ")


def canonical_snapshot_value(field: str, value: Any) -> str:
    if value in [None, ""]:
        return ""
    if field in NUMERIC_SNAPSHOT_FIELDS:
        number = normalize_float(value)
        return format_price(number) if number is not None else str(value).strip()
    if field in BOOLEAN_SNAPSHOT_FIELDS:
        return "true" if parse_bool(value) else "false"
    return str(value).strip()


def diff_snapshots(previous: dict[str, Any] | None, current: dict[str, Any]) -> tuple[str, list[str]]:
    if previous is None:
        return "new", sorted(current.keys())
    changed = sorted(
        [
            key
            for key, value in current.items()
            if canonical_snapshot_value(key, previous.get(key)) != canonical_snapshot_value(key, value)
        ]
    )
    if not changed:
        return "unchanged", []
    if {"source_price_amount", "currency", "normalized_price_usd"} & set(changed):
        return "price_changed", changed
    if parse_bool(previous.get("is_active")) and not parse_bool(current.get("is_active", True)):
        return "deactivated", changed
    return "metadata_changed", changed


def snapshot(row: dict[str, Any] | None, fields: list[str]) -> dict[str, Any] | None:
    if row is None:
        return None
    return {field: row.get(field, "") for field in fields}


def api_display_name(row: dict[str, Any]) -> str:
    parts = [row.get("product_name", ""), row.get("model_name", ""), row.get("price_dimension", "")]
    return " / ".join(part for part in parts if part)


def subscription_display_name(row: dict[str, Any]) -> str:
    parts = [row.get("product_name", ""), row.get("plan_name", ""), row.get("billing_cycle", "")]
    return " / ".join(part for part in parts if part)


def history_api_row(row: dict[str, Any], version_no: int, change_type: str, changed_fields: list[str], now_text: str) -> dict[str, Any]:
    return {
        "history_id": f"{row.get('item_key')}:{version_no}",
        "item_key": row.get("item_key", ""),
        "version_no": version_no,
        "vendor_key": row.get("vendor_key", ""),
        "vendor_name": row.get("vendor_name", ""),
        "region": row.get("region", ""),
        "product_name": row.get("product_name", ""),
        "model_name": row.get("model_name", ""),
        "price_dimension": row.get("price_dimension", ""),
        "source_price_amount": row.get("source_price_amount", ""),
        "currency": row.get("currency", ""),
        "unit_basis": row.get("unit_basis", ""),
        "normalized_price_usd": row.get("normalized_price_usd", ""),
        "normalized_unit": row.get("normalized_unit", ""),
        "original_price_text": row.get("original_price_text", ""),
        "change_type": change_type,
        "changed_fields": ", ".join(changed_fields),
        "change_detected_at": now_text,
        "source_url": row.get("source_url", ""),
    }


def history_subscription_row(row: dict[str, Any], version_no: int, change_type: str, changed_fields: list[str], now_text: str) -> dict[str, Any]:
    return {
        "history_id": f"{row.get('item_key')}:{version_no}",
        "item_key": row.get("item_key", ""),
        "version_no": version_no,
        "vendor_key": row.get("vendor_key", ""),
        "vendor_name": row.get("vendor_name", ""),
        "region": row.get("region", ""),
        "product_name": row.get("product_name", ""),
        "plan_name": row.get("plan_name", ""),
        "billing_cycle": row.get("billing_cycle", ""),
        "source_price_amount": row.get("source_price_amount", ""),
        "currency": row.get("currency", ""),
        "unit_basis": row.get("unit_basis", ""),
        "normalized_price_usd": row.get("normalized_price_usd", ""),
        "normalized_unit": row.get("normalized_unit", ""),
        "original_price_text": row.get("original_price_text", ""),
        "seat_rule": row.get("seat_rule", ""),
        "plan_summary": row.get("plan_summary", ""),
        "change_type": change_type,
        "changed_fields": ", ".join(changed_fields),
        "change_detected_at": now_text,
        "source_url": row.get("source_url", ""),
    }


def change_row(
    *,
    table_name: str,
    row: dict[str, Any],
    version_no: int,
    previous: dict[str, Any] | None,
    current: dict[str, Any],
    display_name: str,
    change_type: str,
    changed_fields: list[str],
    now_text: str,
) -> dict[str, Any]:
    return {
        "change_id": f"{row.get('item_key')}:{version_no}",
        "table_name": table_name,
        "item_key": row.get("item_key", ""),
        "vendor_key": row.get("vendor_key", ""),
        "display_name": display_name,
        "change_type": change_type,
        "changed_fields": ", ".join(changed_fields),
        "previous_value_summary": compact_summary(previous, display_name),
        "new_value_summary": compact_summary(current, display_name),
        "change_detected_at": now_text,
        "source_url": row.get("source_url", ""),
    }


def date_prefix(text: Any) -> str:
    value = str(text or "").strip()
    return value[:10] if len(value) >= 10 else value


def has_prior_successful_build_before_day(existing_runs: list[dict[str, Any]], now_text: str) -> bool:
    build_date = date_prefix(now_text)
    return any(
        str(row.get("status", "")).strip().lower() == "success"
        and date_prefix(row.get("finished_at", "")) < build_date
        for row in existing_runs
    )


def diff_snapshots_for_fields(previous: dict[str, Any] | None, current: dict[str, Any], fields: list[str]) -> tuple[str, list[str]]:
    if previous is None:
        return "new", sorted(fields)
    changed = sorted(
        [
            field
            for field in fields
            if canonical_snapshot_value(field, previous.get(field)) != canonical_snapshot_value(field, current.get(field))
        ]
    )
    if not changed:
        return "unchanged", []
    if {"source_price_amount", "currency", "normalized_price_usd"} & set(changed):
        return "price_changed", changed
    if parse_bool(previous.get("is_active")) and not parse_bool(current.get("is_active", True)):
        return "deactivated", changed
    return "metadata_changed", changed


def latest_history_before_day(
    history_by_item: dict[str, list[dict[str, Any]]],
    item_key: str,
    build_date: str,
) -> dict[str, Any] | None:
    rows = history_by_item.get(item_key, [])
    candidates = [row for row in rows if date_prefix(row.get("change_detected_at", "")) < build_date]
    if not candidates:
        return None
    return max(
        candidates,
        key=lambda row: (
            str(row.get("change_detected_at", "")),
            int(float(row.get("version_no", 0) or 0)),
        ),
    )


def api_snapshot_from_history(row: dict[str, Any] | None) -> dict[str, Any] | None:
    if row is None:
        return None
    return {
        "vendor_key": row.get("vendor_key", ""),
        "vendor_name": row.get("vendor_name", ""),
        "region": row.get("region", ""),
        "product_name": row.get("product_name", ""),
        "model_name": row.get("model_name", ""),
        "price_dimension": row.get("price_dimension", ""),
        "source_price_amount": row.get("source_price_amount", ""),
        "currency": row.get("currency", ""),
        "unit_basis": row.get("unit_basis", ""),
        "normalized_price_usd": row.get("normalized_price_usd", ""),
        "normalized_unit": row.get("normalized_unit", ""),
        "original_price_text": row.get("original_price_text", ""),
        "source_url": row.get("source_url", ""),
        "is_active": True,
    }


def subscription_snapshot_from_history(row: dict[str, Any] | None) -> dict[str, Any] | None:
    if row is None:
        return None
    return {
        "vendor_key": row.get("vendor_key", ""),
        "vendor_name": row.get("vendor_name", ""),
        "region": row.get("region", ""),
        "product_name": row.get("product_name", ""),
        "plan_name": row.get("plan_name", ""),
        "billing_cycle": row.get("billing_cycle", ""),
        "source_price_amount": row.get("source_price_amount", ""),
        "currency": row.get("currency", ""),
        "unit_basis": row.get("unit_basis", ""),
        "normalized_price_usd": row.get("normalized_price_usd", ""),
        "normalized_unit": row.get("normalized_unit", ""),
        "seat_rule": row.get("seat_rule", ""),
        "plan_summary": row.get("plan_summary", ""),
        "original_price_text": row.get("original_price_text", ""),
        "source_url": row.get("source_url", ""),
        "is_active": True,
    }


def version_index_from_history(history_rows: list[dict[str, Any]]) -> dict[str, int]:
    version_index: dict[str, int] = {}
    for row in history_rows:
        item_key = row.get("item_key", "")
        if item_key:
            version_index[item_key] = max(version_index.get(item_key, 0), int(float(row.get("version_no", 0) or 0)))
    return version_index


def build_daily_final_changes(
    *,
    current_rows: list[dict[str, Any]],
    history_rows: list[dict[str, Any]],
    build_date: str,
    now_text: str,
    table_name: str,
    snapshot_fields: list[str],
    compare_fields: list[str],
    display_name_fn,
    history_snapshot_fn,
) -> list[dict[str, Any]]:
    history_by_item: dict[str, list[dict[str, Any]]] = {}
    for row in history_rows:
        item_key = str(row.get("item_key", "")).strip()
        if item_key:
            history_by_item.setdefault(item_key, []).append(row)
    version_index = version_index_from_history(history_rows)
    changes: list[dict[str, Any]] = []
    for row in current_rows:
        if date_prefix(row.get("last_changed_at", "")) != build_date:
            continue
        item_key = str(row.get("item_key", "")).strip()
        previous_history = latest_history_before_day(history_by_item, item_key, build_date)
        previous_snapshot = history_snapshot_fn(previous_history)
        current_snapshot = snapshot(row, snapshot_fields) or {}
        change_type, changed_fields = diff_snapshots_for_fields(previous_snapshot, current_snapshot, compare_fields)
        if change_type == "unchanged":
            continue
        changes.append(
            change_row(
                table_name=table_name,
                row=row,
                version_no=version_index.get(item_key, 0),
                previous=previous_snapshot,
                current=current_snapshot,
                display_name=display_name_fn(row),
                change_type=change_type,
                changed_fields=changed_fields,
                now_text=now_text,
            )
        )
    return changes


def collect_run_vendor_keys(source_pages: list[dict[str, Any]]) -> set[str]:
    keys: set[str] = set()
    for row in source_pages:
        for vendor_key in str(row.get("vendor_keys", "")).split(";"):
            vendor_key = vendor_key.strip()
            if vendor_key:
                keys.add(vendor_key)
    return keys


def read_extracted_json_array(path: Path) -> list[dict[str, Any]]:
    payload = read_json_data(path)
    if payload is None:
        raise RuntimeError(f"缺少 {path}，请先运行 --mode collect 生成 JSON 骨架，再按采集 Markdown 补全 prices。")
    if not isinstance(payload, list):
        raise RuntimeError(f"{path} 必须是 JSON 数组。")
    rows: list[dict[str, Any]] = []
    for index, item in enumerate(payload, start=1):
        if not isinstance(item, dict):
            raise RuntimeError(f"{path} 第 {index} 项必须是对象。")
        rows.append(item)
    return rows


def ok_source_urls(source_pages: list[dict[str, Any]]) -> set[str]:
    return {
        str(row.get("source_url", "")).strip()
        for row in source_pages
        if str(row.get("status", "")).strip().lower() == "ok" and str(row.get("source_url", "")).strip()
    }


def source_url_for_target(target: dict[str, Any], track_type: str, configs: list[dict[str, str]]) -> str:
    vendor_key = str(target.get("vendor_key", "")).strip()
    region = str(target.get("region", "")).strip()
    candidates = [
        config
        for config in configs
        if config.get("vendor_key", "").strip() == vendor_key
        and config.get("track_type", "").strip() == track_type
        and config.get("source_url", "").strip()
    ]
    exact = [config for config in candidates if config.get("region", "").strip() == region]
    if exact:
        return exact[0].get("source_url", "").strip()
    if len(candidates) == 1:
        return candidates[0].get("source_url", "").strip()
    return ""


def vendor_config_for_row(row: dict[str, Any], track_type: str, configs: list[dict[str, str]]) -> dict[str, str]:
    vendor_key = str(row.get("vendor_key", "")).strip()
    region = str(row.get("region", "")).strip()
    candidates = [
        config
        for config in configs
        if config.get("vendor_key", "").strip() == vendor_key
        and config.get("track_type", "").strip() == track_type
    ]
    exact = [config for config in candidates if config.get("region", "").strip() == region]
    if exact:
        return exact[0]
    if len(candidates) == 1:
        return candidates[0]
    vendor_matches = [config for config in configs if config.get("vendor_key", "").strip() == vendor_key]
    return vendor_matches[0] if vendor_matches else {}


def object_matches_target(item: dict[str, Any], target: dict[str, Any], name_field: str) -> bool:
    for field in ["vendor_key", "region", "product_name", name_field]:
        if str(item.get(field, "")).strip() != str(target.get(field, "")).strip():
            return False
    return True


def object_key(item: dict[str, Any], name_field: str) -> tuple[str, str, str, str]:
    return (
        str(item.get("vendor_key", "")).strip(),
        str(item.get("region", "")).strip(),
        str(item.get("product_name", "")).strip(),
        str(item.get(name_field, "")).strip(),
    )


def target_keys(target_rows: list[dict[str, str]], name_field: str, *, active_only: bool = False) -> set[tuple[str, str, str, str]]:
    keys: set[tuple[str, str, str, str]] = set()
    for target in target_rows:
        if active_only and not parse_bool(target.get("is_active", "true")):
            continue
        key = object_key(target, name_field)
        if all(key):
            keys.add(key)
    return keys


def prices_len(item: dict[str, Any]) -> int:
    prices = item.get("prices", [])
    return len(prices) if isinstance(prices, list) else 0


def suspect_missing_issue(
    *,
    table_name: str,
    parent_key: tuple[str, str, str, str],
    rows: list[dict[str, Any]],
    child_label_fn,
    row_number: int,
    now_text: str,
) -> dict[str, Any]:
    labels = sorted(dict.fromkeys(child_label_fn(row) for row in rows if child_label_fn(row)))
    labels_text = "、".join(labels[:6])
    if len(labels) > 6:
        labels_text += f" 等 {len(labels)} 项"
    vendor_key, _, product_name, object_name = parent_key
    return build_issue(
        table_name,
        row_number,
        rows[0],
        "warning",
        f"{table_name} 疑似遗漏子项：{vendor_key} / {product_name} / {object_name} 缺少 {labels_text}。已保留 current 旧值，未写入 changes/history，请复查页面或 JSON。",
        now_text,
    )


def validate_price_shapes(rows: list[dict[str, Any]], *, table_name: str, name_field: str, now_text: str) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    for item_index, item in enumerate(rows, start=1):
        prices = item.get("prices", [])
        if prices in [None, ""]:
            prices = []
        if not isinstance(prices, list):
            issues.append(
                build_issue(
                    table_name,
                    item_index,
                    item,
                    "error",
                    f"{table_name} 的 prices 必须是数组：{item.get('vendor_key')} / {item.get('product_name')} / {item.get(name_field)}",
                    now_text,
                )
            )
            continue
        for price_index, price in enumerate(prices, start=1):
            if not isinstance(price, dict):
                issues.append(
                    build_issue(
                        table_name,
                        item_index * 1000 + price_index,
                        item,
                        "error",
                        f"{table_name} 的第 {price_index} 个 price 必须是对象：{item.get('vendor_key')} / {item.get('product_name')} / {item.get(name_field)}",
                        now_text,
                    )
                )
    return issues


def filter_targeted_rows(
    *,
    rows: list[dict[str, Any]],
    target_rows: list[dict[str, str]],
    table_name: str,
    name_field: str,
    now_text: str,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    all_keys = target_keys(target_rows, name_field)
    active_keys = target_keys(target_rows, name_field, active_only=True)
    filtered: list[dict[str, Any]] = []
    issues: list[dict[str, Any]] = []
    for index, item in enumerate(rows, start=1):
        key = object_key(item, name_field)
        if key in active_keys:
            filtered.append(item)
            continue
        if key not in all_keys and prices_len(item) > 0:
            issues.append(
                build_issue(
                    table_name,
                    index,
                    item,
                    "error",
                    f"{table_name} 出现目标表未维护但已填 prices 的对象：{item.get('vendor_key')} / {item.get('product_name')} / {item.get(name_field)}。请加入目标表，或清空该对象 prices。",
                    now_text,
                )
            )
    return filtered, issues


def active_targets(target_rows: list[dict[str, str]], run_vendor_keys: set[str]) -> list[dict[str, str]]:
    return [
        row
        for row in target_rows
        if parse_bool(row.get("is_active", "true")) and row.get("vendor_key", "").strip() in run_vendor_keys
    ]


def validate_target_objects(
    *,
    table_name: str,
    target_rows: list[dict[str, str]],
    extracted_rows: list[dict[str, Any]],
    run_vendor_keys: set[str],
    source_configs: list[dict[str, str]],
    source_urls_ok: set[str],
    track_type: str,
    name_field: str,
    now_text: str,
) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    for index, target in enumerate(active_targets(target_rows, run_vendor_keys), start=2):
        if not parse_bool(target.get("required", "true")):
            continue
        source_url = source_url_for_target(target, track_type, source_configs)
        issue_target = {**target, "source_url": source_url}
        name = target.get(name_field, "").strip()
        if not source_url:
            issues.append(
                build_issue(
                    table_name,
                    index,
                    issue_target,
                    "error",
                    f"{table_name} 目标 {target.get('vendor_key')} / {target.get('product_name')} / {name} 在 vendors.csv 中找不到 {track_type} 来源 URL。",
                    now_text,
                )
            )
        elif source_url not in source_urls_ok:
            issues.append(
                build_issue(
                    table_name,
                    index,
                    issue_target,
                    "error",
                    f"{table_name} 目标 {target.get('vendor_key')} / {target.get('product_name')} / {name} 的来源页未成功采集：{source_url}",
                    now_text,
                )
            )
        matches = [item for item in extracted_rows if object_matches_target(item, target, name_field)]
        if not matches:
            issues.append(
                build_issue(
                    table_name,
                    index,
                    issue_target,
                    "error",
                    f"{table_name} 缺少 required 目标对象：{target.get('vendor_key')} / {target.get('product_name')} / {name}",
                    now_text,
                )
            )
            continue
        if not any(isinstance(item.get("prices"), list) and item.get("prices") for item in matches):
            issues.append(
                build_issue(
                    table_name,
                    index,
                    issue_target,
                    "error",
                    f"{table_name} required 目标对象没有 prices：{target.get('vendor_key')} / {target.get('product_name')} / {name}",
                    now_text,
                )
            )
    return issues


def missing_price_fields(price: dict[str, Any], required_fields: list[str]) -> list[str]:
    missing: list[str] = []
    for field in required_fields:
        value = price.get(field)
        if value in [None, "", "null"]:
            missing.append(field)
    if "source_price_amount" in required_fields and normalize_float(price.get("source_price_amount")) is None:
        if "source_price_amount" not in missing:
            missing.append("source_price_amount")
    return missing


def validate_price_items(
    rows: list[dict[str, Any]],
    *,
    table_name: str,
    name_field: str,
    required_fields: list[str],
    now_text: str,
) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    for item_index, item in enumerate(rows, start=1):
        prices = item.get("prices", []) or []
        if not isinstance(prices, list):
            continue
        for price_index, price in enumerate(prices, start=1):
            if not isinstance(price, dict):
                continue
            missing = missing_price_fields(price, required_fields)
            if missing:
                issues.append(
                    build_issue(
                        table_name,
                        item_index * 1000 + price_index,
                        item,
                        "error",
                        f"{table_name} 价格项缺少字段 {', '.join(missing)}：{item.get('vendor_key')} / {item.get('product_name')} / {item.get(name_field)}",
                        now_text,
                    )
                )
    return issues


def with_valid_prices(rows: list[dict[str, Any]], required_fields: list[str]) -> list[dict[str, Any]]:
    valid_rows: list[dict[str, Any]] = []
    for item in rows:
        prices = item.get("prices", []) or []
        if not isinstance(prices, list):
            continue
        valid_prices = [
            price
            for price in prices
            if isinstance(price, dict) and not missing_price_fields(price, required_fields)
        ]
        if not valid_prices:
            continue
        copied = dict(item)
        copied["prices"] = valid_prices
        valid_rows.append(copied)
    return valid_rows


def combine_notes(*values: Any) -> str:
    parts = [str(value).strip() for value in values if str(value or "").strip()]
    return "; ".join(dict.fromkeys(parts))


def feature_summary(item: dict[str, Any]) -> str:
    explicit = str(item.get("plan_summary", "")).strip()
    if explicit:
        return explicit
    features = item.get("features", [])
    if isinstance(features, list):
        return "; ".join(str(feature).strip() for feature in features if str(feature).strip())
    if isinstance(features, str):
        return features.strip()
    return ""


def expand_api_json(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    expanded: list[dict[str, Any]] = []
    for item in rows:
        prices = item.get("prices", [])
        if not isinstance(prices, list):
            continue
        for price in prices:
            if not isinstance(price, dict):
                continue
            expanded.append(
                {
                    "vendor_key": item.get("vendor_key", ""),
                    "region": item.get("region", ""),
                    "product_name": item.get("product_name", ""),
                    "model_name": item.get("model_name", ""),
                    "price_dimension": price.get("price_dimension", ""),
                    "source_price_amount": price.get("source_price_amount", ""),
                    "currency": price.get("currency", ""),
                    "unit_basis": price.get("unit_basis", ""),
                    "original_price_text": price.get("original_price_text", ""),
                    "notes": combine_notes(item.get("notes", ""), price.get("notes", "")),
                    "source_url": price.get("source_url", "") or item.get("source_url", ""),
                }
            )
    return expanded


def expand_subscription_json(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    expanded: list[dict[str, Any]] = []
    for item in rows:
        prices = item.get("prices", [])
        if not isinstance(prices, list):
            continue
        summary = feature_summary(item)
        for price in prices:
            if not isinstance(price, dict):
                continue
            expanded.append(
                {
                    "vendor_key": item.get("vendor_key", ""),
                    "region": item.get("region", ""),
                    "product_name": item.get("product_name", ""),
                    "plan_name": item.get("plan_name", ""),
                    "billing_cycle": price.get("billing_cycle", ""),
                    "source_price_amount": price.get("source_price_amount", ""),
                    "currency": price.get("currency", ""),
                    "unit_basis": price.get("unit_basis", ""),
                    "seat_rule": price.get("seat_rule", ""),
                    "plan_summary": summary,
                    "original_price_text": price.get("original_price_text", ""),
                    "notes": combine_notes(item.get("notes", ""), price.get("notes", "")),
                    "source_url": price.get("source_url", "") or item.get("source_url", ""),
                }
            )
    return expanded


def format_issue_report(errors: list[dict[str, Any]], warnings: list[dict[str, Any]]) -> str:
    lines = [f"build/push 校验失败：发现 {len(errors)} 个错误。"]
    for issue in errors[:40]:
        lines.append(f"- [{issue.get('table_name')}] {issue.get('message')}")
    if len(errors) > 40:
        lines.append(f"- 另有 {len(errors) - 40} 个错误未展开。")
    if warnings:
        lines.append(f"同时发现 {len(warnings)} 个 warning：")
        for issue in warnings[:12]:
            lines.append(f"- [{issue.get('table_name')}] {issue.get('message')}")
        if len(warnings) > 12:
            lines.append(f"- 另有 {len(warnings) - 12} 个 warning 未展开。")
    return "\n".join(lines)


def normalize_api_rows(rows: list[dict[str, Any]], vendor_configs: list[dict[str, str]], now_text: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    normalized_rows: list[dict[str, Any]] = []
    issues: list[dict[str, Any]] = []
    for index, row in enumerate(rows, start=2):
        if not any((value or "").strip() for value in row.values()):
            continue
        vendor_key = row.get("vendor_key", "").strip()
        vendor_info = vendor_config_for_row(row, "api", vendor_configs)
        source_price_amount = normalize_float(row.get("source_price_amount"))
        if source_price_amount is None:
            source_price_amount = infer_amount_from_text(str(row.get("original_price_text", "")))
        normalized_price_usd, normalized_unit = normalize_price(source_price_amount, row.get("currency", ""), row.get("unit_basis", ""))
        item = {
            "item_key": "",
            "vendor_key": vendor_key,
            "vendor_name": vendor_info.get("vendor_name", "").strip(),
            "region": row.get("region", "").strip() or vendor_info.get("region", "").strip() or "global",
            "product_name": row.get("product_name", "").strip(),
            "model_name": row.get("model_name", "").strip(),
            "price_dimension": row.get("price_dimension", "").strip(),
            "source_price_amount": source_price_amount,
            "currency": row.get("currency", "").strip().upper(),
            "unit_basis": row.get("unit_basis", "").strip(),
            "normalized_price_usd": normalized_price_usd,
            "normalized_unit": normalized_unit,
            "original_price_text": row.get("original_price_text", "").strip(),
            "notes": row.get("notes", "").strip(),
            "source_url": row.get("source_url", "").strip() or vendor_info.get("source_url", "").strip(),
        }
        critical_missing = [
            field
            for field in ["vendor_key", "product_name", "model_name", "price_dimension", "currency", "unit_basis", "source_url"]
            if not item.get(field)
        ]
        if item["source_price_amount"] is None and not item["original_price_text"]:
            critical_missing.append("source_price_amount")
        if critical_missing:
            issues.append(
                build_issue(
                    "api_pricing",
                    index,
                    item,
                    "error",
                    f"{friendly_table_name('api_pricing')} 缺少关键字段: {', '.join(sorted(set(critical_missing)))}。请先确认产品/模型/价格维度、币种、单位和来源 URL 是否已填。",
                    now_text,
                )
            )
            continue
        if item["normalized_price_usd"] is None:
            issues.append(
                build_issue(
                    "api_pricing",
                    index,
                    item,
                    "warning",
                    "无法完成价格归一化。请检查 source_price_amount 是否为纯数字，并确认 currency 与 unit_basis 是否使用推荐词表中的值。",
                    now_text,
                )
            )
        item["item_key"] = api_item_key(item)
        normalized_rows.append(item)
    return normalized_rows, issues


def normalize_subscription_rows(rows: list[dict[str, Any]], vendor_configs: list[dict[str, str]], now_text: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    normalized_rows: list[dict[str, Any]] = []
    issues: list[dict[str, Any]] = []
    for index, row in enumerate(rows, start=2):
        if not any((value or "").strip() for value in row.values()):
            continue
        vendor_key = row.get("vendor_key", "").strip()
        vendor_info = vendor_config_for_row(row, "subscription", vendor_configs)
        source_price_amount = normalize_float(row.get("source_price_amount"))
        if source_price_amount is None:
            source_price_amount = infer_amount_from_text(str(row.get("original_price_text", "")))
        normalized_price_usd, normalized_unit = normalize_price(source_price_amount, row.get("currency", ""), row.get("unit_basis", ""))
        item = {
            "item_key": "",
            "vendor_key": vendor_key,
            "vendor_name": vendor_info.get("vendor_name", "").strip(),
            "region": row.get("region", "").strip() or vendor_info.get("region", "").strip() or "global",
            "product_name": row.get("product_name", "").strip(),
            "plan_name": row.get("plan_name", "").strip(),
            "billing_cycle": row.get("billing_cycle", "").strip(),
            "source_price_amount": source_price_amount,
            "currency": row.get("currency", "").strip().upper(),
            "unit_basis": row.get("unit_basis", "").strip(),
            "normalized_price_usd": normalized_price_usd,
            "normalized_unit": normalized_unit,
            "seat_rule": row.get("seat_rule", "").strip(),
            "plan_summary": row.get("plan_summary", "").strip(),
            "original_price_text": row.get("original_price_text", "").strip(),
            "notes": row.get("notes", "").strip(),
            "source_url": row.get("source_url", "").strip() or vendor_info.get("source_url", "").strip(),
        }
        critical_missing = [
            field
            for field in ["vendor_key", "product_name", "plan_name", "currency", "unit_basis", "source_url"]
            if not item.get(field)
        ]
        if item["source_price_amount"] is None and not item["original_price_text"]:
            critical_missing.append("source_price_amount")
        if critical_missing:
            issues.append(
                build_issue(
                    "subscription_plans",
                    index,
                    item,
                    "error",
                    f"{friendly_table_name('subscription_plans')} 缺少关键字段: {', '.join(sorted(set(critical_missing)))}。请先确认产品/套餐、币种、单位、来源 URL 和价格文本是否已填。",
                    now_text,
                )
            )
            continue
        if item["normalized_price_usd"] is None:
            issues.append(
                build_issue(
                    "subscription_plans",
                    index,
                    item,
                    "warning",
                    "无法完成价格归一化。请检查 source_price_amount 是否为纯数字，并确认 currency、unit_basis、billing_cycle 是否符合字段说明。",
                    now_text,
                )
            )
        item["item_key"] = subscription_item_key(item)
        normalized_rows.append(item)
    return normalized_rows, issues


def reconcile_api_table(
    new_rows: list[dict[str, Any]],
    run_vendor_keys: set[str],
    now_text: str,
    *,
    data_dir: Path,
    initial_bootstrap: bool,
    active_parent_keys: set[tuple[str, str, str, str]],
    inactive_parent_keys: set[tuple[str, str, str, str]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], int]:
    current_existing = {row.get("item_key", ""): row for row in read_csv_rows(data_dir / "current_api.csv") if row.get("item_key")}
    history_existing = read_csv_rows(data_dir / "history_api.csv")
    version_index: dict[str, int] = {}
    for row in history_existing:
        item_key = row.get("item_key", "")
        if item_key:
            version_index[item_key] = max(version_index.get(item_key, 0), int(float(row.get("version_no", 0) or 0)))

    history_new: list[dict[str, Any]] = []
    changes_new: list[dict[str, Any]] = []
    warnings_new: list[dict[str, Any]] = []
    seen_keys: set[str] = set()
    seen_parent_keys: set[tuple[str, str, str, str]] = set()
    existing_parent_keys = {api_parent_key(row) for row in current_existing.values() if all(api_parent_key(row))}
    upserts = 0

    for row in new_rows:
        item_key = row["item_key"]
        seen_keys.add(item_key)
        parent_key = api_parent_key(row)
        if all(parent_key):
            seen_parent_keys.add(parent_key)
        existing = current_existing.get(item_key)
        current_row = {
            **{field: row.get(field, "") for field in CURRENT_API_FIELDS if field not in {"first_seen_at", "last_verified_at", "last_changed_at", "is_active"}},
            "first_seen_at": existing.get("first_seen_at") if existing else now_text,
            "last_verified_at": now_text,
            "last_changed_at": existing.get("last_changed_at") if existing else now_text,
            "is_active": True,
        }
        previous_snapshot = snapshot(existing, API_SNAPSHOT_FIELDS)
        next_snapshot = snapshot(current_row, API_SNAPSHOT_FIELDS) or {}
        change_type, changed_fields = diff_snapshots(previous_snapshot, next_snapshot)
        should_record = False
        if change_type == "price_changed":
            should_record = True
        elif change_type == "new" and parent_key not in existing_parent_keys:
            should_record = True
        if should_record:
            current_row["last_changed_at"] = now_text
            version_index[item_key] = version_index.get(item_key, 0) + 1
            history_new.append(history_api_row(current_row, version_index[item_key], change_type, changed_fields, now_text))
            if not (initial_bootstrap and change_type == "new"):
                changes_new.append(
                    change_row(
                        table_name="api",
                        row=current_row,
                        version_no=version_index[item_key],
                        previous=previous_snapshot,
                        current=next_snapshot,
                        display_name=api_display_name(current_row),
                        change_type=change_type,
                        changed_fields=changed_fields,
                        now_text=now_text,
                    )
                )
        current_existing[item_key] = current_row
        upserts += 1

    suspect_missing_by_parent: dict[tuple[str, str, str, str], list[dict[str, Any]]] = {}
    for item_key, existing in list(current_existing.items()):
        if item_key in seen_keys or existing.get("vendor_key", "") not in run_vendor_keys or not parse_bool(existing.get("is_active", True)):
            continue
        parent_key = api_parent_key(existing)
        if parent_key in inactive_parent_keys:
            updated = dict(existing)
            updated["is_active"] = False
            updated["last_verified_at"] = now_text
            updated["last_changed_at"] = now_text
            version_index[item_key] = version_index.get(item_key, 0) + 1
            history_new.append(history_api_row(updated, version_index[item_key], "deactivated", ["is_active"], now_text))
            changes_new.append(
                change_row(
                    table_name="api",
                    row=updated,
                    version_no=version_index[item_key],
                    previous=snapshot(existing, API_SNAPSHOT_FIELDS),
                    current=snapshot(updated, API_SNAPSHOT_FIELDS) or {},
                    display_name=api_display_name(updated),
                    change_type="deactivated",
                    changed_fields=["is_active"],
                    now_text=now_text,
                )
            )
            current_existing[item_key] = updated
            continue
        if parent_key in active_parent_keys and parent_key in seen_parent_keys:
            suspect_missing_by_parent.setdefault(parent_key, []).append(existing)

    write_csv_rows(data_dir / "current_api.csv", list(current_existing.values()), CURRENT_API_FIELDS)
    write_csv_rows(data_dir / "history_api.csv", history_existing + history_new, HISTORY_API_FIELDS)
    for index, (parent_key, rows) in enumerate(sorted(suspect_missing_by_parent.items()), start=1):
        warnings_new.append(
            suspect_missing_issue(
                table_name="api_pricing",
                parent_key=parent_key,
                rows=rows,
                child_label_fn=api_child_label,
                row_number=900000 + index,
                now_text=now_text,
            )
        )
    return list(current_existing.values()), history_new, changes_new, warnings_new, upserts


def reconcile_subscription_table(
    new_rows: list[dict[str, Any]],
    run_vendor_keys: set[str],
    now_text: str,
    *,
    data_dir: Path,
    initial_bootstrap: bool,
    active_parent_keys: set[tuple[str, str, str, str]],
    inactive_parent_keys: set[tuple[str, str, str, str]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], int]:
    current_existing = {row.get("item_key", ""): row for row in read_csv_rows(data_dir / "current_subscription.csv") if row.get("item_key")}
    history_existing = read_csv_rows(data_dir / "history_subscription.csv")
    version_index: dict[str, int] = {}
    for row in history_existing:
        item_key = row.get("item_key", "")
        if item_key:
            version_index[item_key] = max(version_index.get(item_key, 0), int(float(row.get("version_no", 0) or 0)))

    history_new: list[dict[str, Any]] = []
    changes_new: list[dict[str, Any]] = []
    warnings_new: list[dict[str, Any]] = []
    seen_keys: set[str] = set()
    seen_parent_keys: set[tuple[str, str, str, str]] = set()
    existing_parent_keys = {subscription_parent_key(row) for row in current_existing.values() if all(subscription_parent_key(row))}
    upserts = 0

    for row in new_rows:
        item_key = row["item_key"]
        seen_keys.add(item_key)
        parent_key = subscription_parent_key(row)
        if all(parent_key):
            seen_parent_keys.add(parent_key)
        existing = current_existing.get(item_key)
        current_row = {
            **{field: row.get(field, "") for field in CURRENT_SUBSCRIPTION_FIELDS if field not in {"first_seen_at", "last_verified_at", "last_changed_at", "is_active"}},
            "first_seen_at": existing.get("first_seen_at") if existing else now_text,
            "last_verified_at": now_text,
            "last_changed_at": existing.get("last_changed_at") if existing else now_text,
            "is_active": True,
        }
        previous_snapshot = snapshot(existing, SUBSCRIPTION_SNAPSHOT_FIELDS)
        next_snapshot = snapshot(current_row, SUBSCRIPTION_SNAPSHOT_FIELDS) or {}
        change_type, changed_fields = diff_snapshots(previous_snapshot, next_snapshot)
        should_record = False
        if change_type == "price_changed":
            should_record = True
        elif change_type == "new" and parent_key not in existing_parent_keys:
            should_record = True
        if should_record:
            current_row["last_changed_at"] = now_text
            version_index[item_key] = version_index.get(item_key, 0) + 1
            history_new.append(history_subscription_row(current_row, version_index[item_key], change_type, changed_fields, now_text))
            if not (initial_bootstrap and change_type == "new"):
                changes_new.append(
                    change_row(
                        table_name="subscription",
                        row=current_row,
                        version_no=version_index[item_key],
                        previous=previous_snapshot,
                        current=next_snapshot,
                        display_name=subscription_display_name(current_row),
                        change_type=change_type,
                        changed_fields=changed_fields,
                        now_text=now_text,
                    )
                )
        current_existing[item_key] = current_row
        upserts += 1

    suspect_missing_by_parent: dict[tuple[str, str, str, str], list[dict[str, Any]]] = {}
    for item_key, existing in list(current_existing.items()):
        if item_key in seen_keys or existing.get("vendor_key", "") not in run_vendor_keys or not parse_bool(existing.get("is_active", True)):
            continue
        parent_key = subscription_parent_key(existing)
        if parent_key in inactive_parent_keys:
            updated = dict(existing)
            updated["is_active"] = False
            updated["last_verified_at"] = now_text
            updated["last_changed_at"] = now_text
            version_index[item_key] = version_index.get(item_key, 0) + 1
            history_new.append(history_subscription_row(updated, version_index[item_key], "deactivated", ["is_active"], now_text))
            changes_new.append(
                change_row(
                    table_name="subscription",
                    row=updated,
                    version_no=version_index[item_key],
                    previous=snapshot(existing, SUBSCRIPTION_SNAPSHOT_FIELDS),
                    current=snapshot(updated, SUBSCRIPTION_SNAPSHOT_FIELDS) or {},
                    display_name=subscription_display_name(updated),
                    change_type="deactivated",
                    changed_fields=["is_active"],
                    now_text=now_text,
                )
            )
            current_existing[item_key] = updated
            continue
        if parent_key in active_parent_keys and parent_key in seen_parent_keys:
            suspect_missing_by_parent.setdefault(parent_key, []).append(existing)

    write_csv_rows(data_dir / "current_subscription.csv", list(current_existing.values()), CURRENT_SUBSCRIPTION_FIELDS)
    write_csv_rows(data_dir / "history_subscription.csv", history_existing + history_new, HISTORY_SUBSCRIPTION_FIELDS)
    for index, (parent_key, rows) in enumerate(sorted(suspect_missing_by_parent.items()), start=1):
        warnings_new.append(
            suspect_missing_issue(
                table_name="subscription_plans",
                parent_key=parent_key,
                rows=rows,
                child_label_fn=subscription_child_label,
                row_number=910000 + index,
                now_text=now_text,
            )
        )
    return list(current_existing.values()), history_new, changes_new, warnings_new, upserts


def run_build(run_dir: str = "", *, data_dir: Path | None = None, identity: str = "") -> dict[str, Any]:
    now_text = utc_now()
    data_root = data_dir or DATA_DIR
    data_root.mkdir(parents=True, exist_ok=True)

    resolved_run_dir, run_path = resolve_run_path(run_dir)
    collected_dir = run_path / "collected"
    extracted_dir = run_path / "extracted"

    source_pages = read_csv_rows(collected_dir / "source_pages.csv")
    api_json_rows = read_extracted_json_array(extracted_dir / "api_pricing.json")
    subscription_json_rows = read_extracted_json_array(extracted_dir / "subscription_plans.json")
    if not source_pages:
        raise RuntimeError(f"{collected_dir / 'source_pages.csv'} 为空或不存在，请先运行 --mode collect。")

    run_vendor_keys = collect_run_vendor_keys(source_pages)
    vendor_configs = load_vendor_configs()
    vendor_rows = vendor_rows_from_configs(filter_vendor_configs(vendor_configs), now_text)
    source_configs = filter_vendor_configs(vendor_configs)
    target_api_rows = load_target_api_models()
    target_subscription_rows = load_target_subscription_plans()
    source_urls_ok = ok_source_urls(source_pages)

    shape_issues = [
        *validate_price_shapes(
            api_json_rows,
            table_name="api_pricing",
            name_field="model_name",
            now_text=now_text,
        ),
        *validate_price_shapes(
            subscription_json_rows,
            table_name="subscription_plans",
            name_field="plan_name",
            now_text=now_text,
        ),
    ]
    if shape_issues:
        write_csv_rows(run_path / "build_issues.csv", shape_issues, BUILD_ISSUE_FIELDS)
        raise RuntimeError(format_issue_report(shape_issues, []))

    active_api_json_rows, api_target_issues = filter_targeted_rows(
        rows=api_json_rows,
        target_rows=target_api_rows,
        table_name="api_pricing",
        name_field="model_name",
        now_text=now_text,
    )
    active_subscription_json_rows, subscription_target_issues = filter_targeted_rows(
        rows=subscription_json_rows,
        target_rows=target_subscription_rows,
        table_name="subscription_plans",
        name_field="plan_name",
        now_text=now_text,
    )

    validation_issues = [
        *validate_target_objects(
            table_name="api_pricing",
            target_rows=target_api_rows,
            extracted_rows=active_api_json_rows,
            run_vendor_keys=run_vendor_keys,
            source_configs=source_configs,
            source_urls_ok=source_urls_ok,
            track_type="api",
            name_field="model_name",
            now_text=now_text,
        ),
        *validate_target_objects(
            table_name="subscription_plans",
            target_rows=target_subscription_rows,
            extracted_rows=active_subscription_json_rows,
            run_vendor_keys=run_vendor_keys,
            source_configs=source_configs,
            source_urls_ok=source_urls_ok,
            track_type="subscription",
            name_field="plan_name",
            now_text=now_text,
        ),
        *validate_price_items(
            active_api_json_rows,
            table_name="api_pricing",
            name_field="model_name",
            required_fields=["price_dimension", "source_price_amount", "currency", "unit_basis", "original_price_text"],
            now_text=now_text,
        ),
        *validate_price_items(
            active_subscription_json_rows,
            table_name="subscription_plans",
            name_field="plan_name",
            required_fields=["source_price_amount", "currency", "unit_basis", "original_price_text"],
            now_text=now_text,
        ),
    ]
    api_rows = expand_api_json(
        with_valid_prices(
            active_api_json_rows,
            ["price_dimension", "source_price_amount", "currency", "unit_basis", "original_price_text"],
        )
    )
    subscription_rows = expand_subscription_json(
        with_valid_prices(
            active_subscription_json_rows,
            ["source_price_amount", "currency", "unit_basis", "original_price_text"],
        )
    )
    normalized_api_rows, api_issues = normalize_api_rows(api_rows, source_configs, now_text)
    normalized_subscription_rows, subscription_issues = normalize_subscription_rows(subscription_rows, source_configs, now_text)
    build_issues = [*api_target_issues, *subscription_target_issues, *validation_issues, *api_issues, *subscription_issues]

    if not normalized_api_rows and not normalized_subscription_rows:
        write_csv_rows(run_path / "build_issues.csv", build_issues, BUILD_ISSUE_FIELDS)
        raise RuntimeError("规范化后没有可用数据，请检查 extracted/api_pricing.json 和 extracted/subscription_plans.json 是否已补 prices。")

    existing_runs = read_csv_rows(data_root / "sync_runs.csv")
    build_date = date_prefix(now_text)
    existing_changes = [
        row for row in read_csv_rows(data_root / "changes.csv") if date_prefix(row.get("change_detected_at", "")) != build_date
    ]
    initial_bootstrap = not any(
        [
            read_csv_rows(data_root / "current_api.csv"),
            read_csv_rows(data_root / "current_subscription.csv"),
            read_csv_rows(data_root / "history_api.csv"),
            read_csv_rows(data_root / "history_subscription.csv"),
            existing_changes,
            existing_runs,
        ]
    )

    active_api_parent_keys = scoped_target_keys(target_api_rows, "model_name", run_vendor_keys, active=True)
    inactive_api_parent_keys = scoped_target_keys(target_api_rows, "model_name", run_vendor_keys, active=False)
    active_subscription_parent_keys = scoped_target_keys(target_subscription_rows, "plan_name", run_vendor_keys, active=True)
    inactive_subscription_parent_keys = scoped_target_keys(target_subscription_rows, "plan_name", run_vendor_keys, active=False)

    _, api_history_new, api_changes_new, api_warnings_new, api_upserts = reconcile_api_table(
        normalized_api_rows,
        run_vendor_keys,
        now_text,
        data_dir=data_root,
        initial_bootstrap=initial_bootstrap,
        active_parent_keys=active_api_parent_keys,
        inactive_parent_keys=inactive_api_parent_keys,
    )
    _, subscription_history_new, subscription_changes_new, subscription_warnings_new, subscription_upserts = reconcile_subscription_table(
        normalized_subscription_rows,
        run_vendor_keys,
        now_text,
        data_dir=data_root,
        initial_bootstrap=initial_bootstrap,
        active_parent_keys=active_subscription_parent_keys,
        inactive_parent_keys=inactive_subscription_parent_keys,
    )

    build_issues = [*build_issues, *api_warnings_new, *subscription_warnings_new]
    write_csv_rows(run_path / "build_issues.csv", build_issues, BUILD_ISSUE_FIELDS)

    if has_prior_successful_build_before_day(existing_runs, now_text):
        current_api_rows = read_csv_rows(data_root / "current_api.csv")
        current_subscription_rows = read_csv_rows(data_root / "current_subscription.csv")
        history_api_rows = read_csv_rows(data_root / "history_api.csv")
        history_subscription_rows = read_csv_rows(data_root / "history_subscription.csv")
        changes_new = [
            *build_daily_final_changes(
                current_rows=current_api_rows,
                history_rows=history_api_rows,
                build_date=build_date,
                now_text=now_text,
                table_name="api",
                snapshot_fields=API_SNAPSHOT_FIELDS,
                compare_fields=API_CHANGE_COMPARE_FIELDS,
                display_name_fn=api_display_name,
                history_snapshot_fn=api_snapshot_from_history,
            ),
            *build_daily_final_changes(
                current_rows=current_subscription_rows,
                history_rows=history_subscription_rows,
                build_date=build_date,
                now_text=now_text,
                table_name="subscription",
                snapshot_fields=SUBSCRIPTION_SNAPSHOT_FIELDS,
                compare_fields=SUBSCRIPTION_CHANGE_COMPARE_FIELDS,
                display_name_fn=subscription_display_name,
                history_snapshot_fn=subscription_snapshot_from_history,
            ),
        ]
    else:
        changes_new = []
    write_csv_rows(data_root / "changes.csv", existing_changes + changes_new, CHANGE_FIELDS)
    write_csv_rows(data_root / "vendors.csv", vendor_rows, VENDOR_FIELDS)

    run_id = uuid.uuid4().hex
    run_row = {
        "run_id": run_id,
        "artifact_run_dir": resolved_run_dir,
        "started_at": now_text,
        "finished_at": now_text,
        "status": "success",
        "vendors_scope": ",".join(sorted(run_vendor_keys)),
        "source_pages_seen": len(source_pages),
        "api_rows_seen": len(normalized_api_rows),
        "subscription_rows_seen": len(normalized_subscription_rows),
        "current_upserts": api_upserts + subscription_upserts,
        "history_appended": len(api_history_new) + len(subscription_history_new),
        "changes_appended": len(changes_new),
        "build_issues_count": len(build_issues),
        "error_summary": " | ".join(issue.get("message", "") for issue in build_issues[:8]),
        "spreadsheet_token": "",
        "spreadsheet_url": "",
        "identity": identity,
    }
    write_csv_rows(data_root / "sync_runs.csv", existing_runs + [run_row], SYNC_RUN_FIELDS)

    return {
        "run_id": run_id,
        "run_dir": resolved_run_dir,
        "artifact_dir": str(run_path),
        "data_dir": str(data_root),
        "api_rows_seen": len(normalized_api_rows),
        "subscription_rows_seen": len(normalized_subscription_rows),
        "build_issues": len(build_issues),
        "current_upserts": api_upserts + subscription_upserts,
        "history_appended": len(api_history_new) + len(subscription_history_new),
        "changes_appended": len(changes_new),
        "summary": run_row,
    }
