from __future__ import annotations

import csv
import hashlib
import json
import re
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

BEIJING_TZ = timezone(timedelta(hours=8))
CNY_TO_USD = Decimal("0.14")

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
ARTIFACTS_DIR = SKILL_DIR / "artifacts"
DATA_DIR = SKILL_DIR / "data"
CONFIG_DIR = SKILL_DIR / "config"
VENDORS_CSV = CONFIG_DIR / "vendors.csv"
TARGET_API_MODELS_CSV = CONFIG_DIR / "target_api_models.csv"
TARGET_SUBSCRIPTION_PLANS_CSV = CONFIG_DIR / "target_subscription_plans.csv"
LATEST_RUN_JSON = ARTIFACTS_DIR / "latest_run.json"
SHEET_STATE_FILE = SKILL_DIR / "sheet_state.json"
FIXED_SPREADSHEET_TITLE = "模型价格追踪"

VENDOR_FIELDS = [
    "source_key",
    "vendor_key",
    "vendor_name",
    "vendor_type",
    "track_type",
    "region",
    "source_url",
    "official_site",
    "status",
    "last_checked_at",
]

SOURCE_PAGE_FIELDS = [
    "source_page_id",
    "source_url",
    "source_title",
    "vendor_keys",
    "track_types",
    "regions",
    "markdown_path",
    "captured_views",
    "status",
    "fetched_at",
    "error_message",
]

COLLECT_ISSUE_FIELDS = [
    "issue_id",
    "stage",
    "vendor_keys",
    "track_types",
    "source_url",
    "severity",
    "message",
    "created_at",
]

TARGET_API_MODEL_FIELDS = [
    "vendor_key",
    "region",
    "product_name",
    "model_name",
    "required",
    "is_active",
]

TARGET_SUBSCRIPTION_PLAN_FIELDS = [
    "vendor_key",
    "region",
    "product_name",
    "plan_name",
    "required",
    "is_active",
]

BUILD_ISSUE_FIELDS = [
    "issue_id",
    "table_name",
    "row_number",
    "vendor_key",
    "source_url",
    "severity",
    "message",
    "created_at",
]

CURRENT_API_FIELDS = [
    "item_key",
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
    "first_seen_at",
    "last_verified_at",
    "last_changed_at",
    "is_active",
]

CURRENT_SUBSCRIPTION_FIELDS = [
    "item_key",
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
    "first_seen_at",
    "last_verified_at",
    "last_changed_at",
    "is_active",
]

HISTORY_API_FIELDS = [
    "history_id",
    "item_key",
    "version_no",
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
    "change_type",
    "changed_fields",
    "change_detected_at",
    "source_url",
]

HISTORY_SUBSCRIPTION_FIELDS = [
    "history_id",
    "item_key",
    "version_no",
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
    "original_price_text",
    "seat_rule",
    "plan_summary",
    "change_type",
    "changed_fields",
    "change_detected_at",
    "source_url",
]

CHANGE_FIELDS = [
    "change_id",
    "table_name",
    "item_key",
    "vendor_key",
    "display_name",
    "change_type",
    "changed_fields",
    "previous_value_summary",
    "new_value_summary",
    "change_detected_at",
    "source_url",
]

SYNC_RUN_FIELDS = [
    "run_id",
    "artifact_run_dir",
    "started_at",
    "finished_at",
    "status",
    "vendors_scope",
    "source_pages_seen",
    "api_rows_seen",
    "subscription_rows_seen",
    "current_upserts",
    "history_appended",
    "changes_appended",
    "build_issues_count",
    "error_summary",
    "spreadsheet_token",
    "spreadsheet_url",
    "identity",
]

DATA_TABLES: dict[str, dict[str, Any]] = {
    "vendors": {"csv_file": "vendors.csv", "sheet_title": "Vendors", "fields": VENDOR_FIELDS},
    "current_api": {"csv_file": "current_api.csv", "sheet_title": "API_Current", "fields": CURRENT_API_FIELDS},
    "current_subscription": {"csv_file": "current_subscription.csv", "sheet_title": "Subscription_Current", "fields": CURRENT_SUBSCRIPTION_FIELDS},
    "history_api": {"csv_file": "history_api.csv", "sheet_title": "API_History", "fields": HISTORY_API_FIELDS},
    "history_subscription": {"csv_file": "history_subscription.csv", "sheet_title": "Subscription_History", "fields": HISTORY_SUBSCRIPTION_FIELDS},
    "changes": {"csv_file": "changes.csv", "sheet_title": "Changes", "fields": CHANGE_FIELDS},
    "sync_runs": {"csv_file": "sync_runs.csv", "sheet_title": "Sync_Runs", "fields": SYNC_RUN_FIELDS},
}

PRICE_FIELDS = {"source_price_amount", "normalized_price_usd"}


def utc_now() -> str:
    return datetime.now(BEIJING_TZ).strftime("%Y-%m-%d %H:%M:%S")


def slugify(value: str) -> str:
    value = value.strip().lower().replace("+", " plus ")
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-")
    return value or "unknown"


def short_hash(text: str, length: int = 10) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:length]


def safe_filename(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9._-]+", "-", value).strip("-") or "page"


def format_price(value: Any) -> str:
    if value in [None, ""]:
        return ""
    try:
        text = f"{float(value):.12f}".rstrip("0").rstrip(".")
        return "0" if text == "-0" else text
    except (TypeError, ValueError):
        return str(value)


def write_csv_rows(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            normalized: dict[str, Any] = {}
            for field in fields:
                value = row.get(field, "")
                if field in PRICE_FIELDS:
                    normalized[field] = format_price(value)
                elif isinstance(value, bool):
                    normalized[field] = "True" if value else "False"
                else:
                    normalized[field] = "" if value is None else value
            writer.writerow(normalized)


def read_csv_rows(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_csv_matrix(path: Path) -> list[list[str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.reader(handle))


def read_json_data(path: Path) -> Any:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"无法解析 JSON 文件 {path}: {exc}") from exc


def write_json_data(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def csv_path(data_dir: Path, key: str) -> Path:
    return data_dir / DATA_TABLES[key]["csv_file"]


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def normalize_float(value: Any) -> float | None:
    if value in [None, "", "null"]:
        return None
    try:
        return float(str(value).replace(",", ""))
    except (TypeError, ValueError):
        return infer_amount_from_text(str(value))


def parse_amount(value: Any) -> Decimal | None:
    if value in [None, ""]:
        return None
    try:
        return Decimal(str(value).replace(",", ""))
    except (InvalidOperation, ValueError):
        return None


def infer_amount_from_text(text: str) -> float | None:
    if not text:
        return None
    match = re.search(r"(?:\$|¥|￥|RMB|USD|CNY)?\s*([\d,]+(?:\.\d+)?)", text, flags=re.IGNORECASE)
    if not match:
        return None
    return normalize_float(match.group(1))


def normalize_price(amount: Any, currency: str, unit_basis: str) -> tuple[float | None, str]:
    value = parse_amount(amount)
    if value is None:
        return None, ""

    normalized_currency = (currency or "").strip().upper()
    if normalized_currency == "CNY":
        value *= CNY_TO_USD
    elif normalized_currency and normalized_currency != "USD":
        return None, ""

    unit = (unit_basis or "").strip().lower()
    if unit in {"per_1k_tokens", "per_1k_token", "per_1k"}:
        return float(value * Decimal("1000")), "per_1m_tokens"
    if unit in {"per_1m_tokens", "per_1m_token", "per_million_tokens", "per_million"}:
        return float(value), "per_1m_tokens"
    if unit in {"per_year", "annual", "yearly"}:
        return float(value / Decimal("12")), "per_month"
    if unit in {"per_user_year", "per_user_annual"}:
        return float(value / Decimal("12")), "per_user_month"
    if unit in {"per_month", "monthly"}:
        return float(value), "per_month"
    if unit in {"per_user_month", "seat_month"}:
        return float(value), "per_user_month"
    return float(value), unit or ""


def stable_key(parts: list[Any]) -> str:
    return ":".join(slugify(str(part)) for part in parts if str(part).strip())


def load_vendor_configs(csv_path: Path | None = None) -> list[dict[str, str]]:
    path = csv_path or VENDORS_CSV
    return read_csv_rows(path)


def load_target_api_models(csv_path: Path | None = None) -> list[dict[str, str]]:
    return read_csv_rows(csv_path or TARGET_API_MODELS_CSV)


def load_target_subscription_plans(csv_path: Path | None = None) -> list[dict[str, str]]:
    return read_csv_rows(csv_path or TARGET_SUBSCRIPTION_PLANS_CSV)


def unique_vendor_keys(configs: list[dict[str, str]]) -> list[str]:
    keys: list[str] = []
    seen: set[str] = set()
    for config in configs:
        if not parse_bool(config.get("enabled", "true")):
            continue
        vendor_key = config.get("vendor_key", "").strip()
        if not vendor_key or vendor_key in seen:
            continue
        seen.add(vendor_key)
        keys.append(vendor_key)
    return keys


def filter_vendor_configs(configs: list[dict[str, str]], allowed_vendor_keys: set[str] | None = None) -> list[dict[str, str]]:
    results: list[dict[str, str]] = []
    for config in configs:
        if not parse_bool(config.get("enabled", "true")):
            continue
        vendor_key = config.get("vendor_key", "").strip()
        if allowed_vendor_keys is not None and vendor_key not in allowed_vendor_keys:
            continue
        results.append(config)
    return results


def vendor_rows_from_configs(configs: list[dict[str, str]], now_text: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for config in configs:
        rows.append(
            {
                "source_key": f"{config.get('vendor_key', '').strip()}:{config.get('track_type', '').strip()}:{config.get('region', '').strip()}",
                "vendor_key": config.get("vendor_key", "").strip(),
                "vendor_name": config.get("vendor_name", "").strip(),
                "vendor_type": config.get("vendor_type", "").strip(),
                "track_type": config.get("track_type", "").strip(),
                "region": config.get("region", "").strip(),
                "source_url": config.get("source_url", "").strip(),
                "official_site": config.get("official_site", "").strip(),
                "status": "active" if parse_bool(config.get("enabled", "true")) else "disabled",
                "last_checked_at": now_text,
            }
        )
    return rows


def generate_run_dir() -> str:
    return datetime.now(BEIJING_TZ).strftime("%Y%m%d")


def run_dir_path(run_dir: str) -> Path:
    return ARTIFACTS_DIR / run_dir


def save_latest_run(run_dir: str) -> None:
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    LATEST_RUN_JSON.write_text(json.dumps({"run_dir": run_dir, "updated_at": utc_now()}, ensure_ascii=False, indent=2), encoding="utf-8")


def load_latest_run() -> str:
    if not LATEST_RUN_JSON.exists():
        raise RuntimeError("缺少 artifacts/latest_run.json，请先运行 --mode collect 或显式传 --run-dir。")
    try:
        payload = json.loads(LATEST_RUN_JSON.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"无法解析 {LATEST_RUN_JSON}: {exc}") from exc
    run_dir = str(payload.get("run_dir", "")).strip()
    if not run_dir:
        raise RuntimeError(f"{LATEST_RUN_JSON} 中没有 run_dir，请先重新运行 --mode collect。")
    return run_dir


def resolve_run_dir(run_dir: str = "") -> str:
    return run_dir.strip() if run_dir.strip() else load_latest_run()


def resolve_run_path(run_dir: str = "") -> tuple[str, Path]:
    resolved = resolve_run_dir(run_dir)
    path = run_dir_path(resolved)
    if not path.exists():
        raise RuntimeError(f"找不到 artifacts/{resolved}，请先运行 --mode collect。")
    return resolved, path
