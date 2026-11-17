#!/usr/bin/env python3
"""Shared deterministic helpers for ledger scripts.

Shard keys always come from os.path.basename. Slicing a full path such as
``data/ledger/2026/2026-06.json`` can capture the bogus key ``r/202`` from the
``ledger/2026`` directory prefix.
"""

from __future__ import annotations

import csv
import io
import json
import os
import re
from collections import defaultdict
from datetime import date, datetime, timedelta
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Iterable


SCHEMA_VERSION = "0.3.0"
# Empty and 0.2.0 books stay valid. Other values still warn.
ACCEPTED_SCHEMA_VERSIONS = {"", "0.2.0", "0.3.0"}
# Tag namespaces are free-form: any letter-first prefix works. These four are
# only the recommended starter names used in the docs and examples.
RECOMMENDED_TAG_PREFIXES = ("trip", "event", "person", "nature")
TYPES = {"支出", "收入", "还款", "转账", "退款", "报销", "投资"}
ACCOUNT_KINDS = {"资产", "负债"}
INCLUDE_FLAGS = {"included", "excluded"}
REIMBURSE_STATUSES = {"待报销", "已报销", "不报销"}
CREDIT_MODES = {"debt_only", "with_limit"}
DEFAULT_BASE_CURRENCY = "CNY"
DEFAULT_INVEST_OUT_SUBCATEGORY = "赎回"

# Starter account catalog. Accounts, aliases, inclusion flags, and credit-card
# status are all editable in data/accounts.json; nothing here is a fixed enum.
DEFAULT_ACCOUNTS: dict[str, dict[str, Any]] = {
    "建设银行": {"kind": "资产", "include": "included", "credit": False, "aliases": ["建行", "CCB"]},
    "工商银行": {"kind": "资产", "include": "included", "credit": False, "aliases": ["工行", "ICBC"]},
    "招商银行": {"kind": "资产", "include": "included", "credit": False, "aliases": ["招行", "CMB"]},
    "微信钱包": {"kind": "资产", "include": "included", "credit": False, "aliases": ["微信", "WeChat", "wechat"]},
    "支付宝": {"kind": "资产", "include": "included", "credit": False, "aliases": ["Alipay", "alipay"]},
    "美团": {"kind": "资产", "include": "included", "credit": False, "aliases": ["美团钱包"]},
    "白条": {"kind": "负债", "include": "included", "credit": True, "aliases": ["京东白条"]},
    "花呗": {"kind": "负债", "include": "included", "credit": True, "aliases": ["支付宝花呗"]},
    "美团月付": {"kind": "负债", "include": "included", "credit": True, "aliases": []},
    "抖音月付": {"kind": "负债", "include": "included", "credit": True, "aliases": []},
    "Apple Card": {"kind": "负债", "include": "excluded", "credit": True, "aliases": ["AppleCard"]},
    "公积金": {"kind": "资产", "include": "excluded", "credit": False, "aliases": []},
    "助学贷款": {"kind": "负债", "include": "excluded", "credit": False, "aliases": []},
    "加密货币": {"kind": "资产", "include": "excluded", "credit": False, "aliases": ["数字货币", "crypto"]},
}

CREDIT_CARDS = {name for name, meta in DEFAULT_ACCOUNTS.items() if meta["credit"]}

# Starter category catalog. It is a recommendation, not a gate: agents extend or
# replace it in data/categories.json, and unknown values only warn by default.
DEFAULT_CATEGORY_MAP: dict[str, set[str]] = {
    "食品餐饮": {"早餐", "午餐", "晚餐", "正餐", "外卖", "买菜", "生鲜", "水果", "零食", "饮料", "饮料酒水", "咖啡", "聚餐", "其他"},
    "出行交通": {"打车", "公交地铁", "加油", "停车费", "高速费", "火车", "飞机", "住宿", "维修", "其他"},
    "购物消费": {"服饰运动", "数码", "日用百货", "礼品", "虚拟充值", "其他"},
    "服饰美容": {"服装", "美容", "其他"},
    "居家生活": {"水费", "电费", "燃气费", "宽带", "物业费", "家政", "其他"},
    "生活服务": {"超市", "快递", "理发", "洗衣", "其他"},
    "医疗健康": {"挂号", "门诊", "药品", "体检", "其他"},
    "休闲娱乐": {"电影", "游戏", "旅游度假", "运动", "KTV", "其他"},
    "教育学习": {"书籍", "课程", "考试", "文具", "其他"},
    "人情往来": {"红包", "礼物", "聚会", "其他"},
    "通讯网络": {"话费", "流量", "订阅", "其他"},
    "收入": {"工资", "奖金", "补贴", "利息", "其他"},
    "还款": {"信用卡还款", "贷款还款", "其他"},
    "转账": {"个人转账", "其他"},
    "退款": {"退款", "其他"},
    "报销": {"差旅", "餐饮", "交通", "其他"},
    "投资": {"买入", "赎回", "定投", "其他"},
}

CATEGORY_ALIASES = {"健康医疗": "医疗健康"}
SUBCATEGORY_ALIASES = {
    "停车": "停车费",
    "高速费用": "高速费",
    "酒水饮料": "饮料酒水",
    "白条还款": "信用卡还款",
    "月付还款": "信用卡还款",
    "证券入金": "买入",
}
LEGACY_PAIR_ALIASES = {
    ("购物消费", "饮料酒水"): ("食品餐饮", "饮料酒水"),
}

SPEND_CATEGORIES = set(DEFAULT_CATEGORY_MAP) - {"收入", "还款", "转账", "报销", "投资"}
LEDGER_SUFFIXES = {".json", ".csv"}
DECIMAL_RE = re.compile(r"-?(?:0|[1-9]\d*)(?:\.\d+)?")
CURRENCY_RE = re.compile(r"[A-Z]{3}")
TAG_PREFIX_RE = re.compile(r"[A-Za-z][A-Za-z0-9_-]*")
TAG_SUFFIX_RE = re.compile(r"[\w.-]+")
TARGET_RE = re.compile(r"(?:target_account|目标账户|还款账户)\s*[:=：]?\s*([^\s;；,，]+)")

CC_METHOD_A = "A（最近快照+快照后新增）"
CC_METHOD_B = "B（账本从零重放）"


def default_account_catalog() -> dict[str, dict[str, Any]]:
    return {
        name: {
            "kind": meta["kind"],
            "include": meta["include"],
            "credit": bool(meta["credit"]),
            "invest": bool(meta.get("invest", False)),
            "aliases": list(meta["aliases"]),
            "alias_windows": [],
        }
        for name, meta in DEFAULT_ACCOUNTS.items()
    }


def known_accounts() -> set[str]:
    return set(default_account_catalog())


def alias_key(value: Any) -> str:
    return str(value if value is not None else "").strip().casefold()


def account_alias_map(catalog: dict[str, dict[str, Any]] | None = None) -> dict[str, str]:
    catalog = catalog if catalog is not None else default_account_catalog()
    mapping: dict[str, str] = {}
    for name, meta in catalog.items():
        for alias in meta.get("aliases") or []:
            alias_name = alias.get("名称") if isinstance(alias, dict) else alias
            key = alias_key(alias_name)
            if key and key != alias_key(name):
                mapping[key] = name
    return mapping


def resolve_account(
    name: Any,
    catalog: dict[str, dict[str, Any]] | None = None,
    alias_map: dict[str, str] | None = None,
) -> str:
    """Resolve a raw account name, or one of its aliases, to a catalog account."""
    text = str(name if name is not None else "").strip()
    if not text:
        return ""
    catalog = catalog if catalog is not None else default_account_catalog()
    key = alias_key(text)
    if alias_map is None:
        alias_map = account_alias_map(catalog)
    # An explicitly configured alias wins over a starter account with the same name.
    if key in alias_map:
        return alias_map[key]
    if text in catalog:
        return text
    for candidate in catalog:
        if alias_key(candidate) == key:
            return candidate
    return text


def apply_account_aliases(
    book: dict[str, Any],
    catalog: dict[str, dict[str, Any]] | None = None,
    alias_map: dict[str, str] | None = None,
) -> list[str]:
    """Rewrite account names in place when their alias is configured."""
    catalog = catalog if catalog is not None else default_account_catalog()
    alias_map = alias_map if alias_map is not None else account_alias_map(catalog)
    notes: list[str] = []

    def fix(row: Any, field: str, label: str) -> None:
        if not isinstance(row, dict):
            return
        raw = str(row.get(field, "") or "").strip()
        if not raw:
            return
        resolved = resolve_account(raw, catalog, alias_map)
        if resolved != raw:
            row[field] = resolved
            notes.append(f"{label}: 账户别名 {raw} -> {resolved}")

    def fix_note_target(row: Any, label: str) -> None:
        if not isinstance(row, dict):
            return
        for field in ("note", "备注"):
            text = str(row.get(field, "") or "")
            match = TARGET_RE.search(text)
            if not match:
                continue
            raw = match.group(1)
            resolved = resolve_account(raw, catalog, alias_map)
            if resolved != raw:
                row[field] = text[: match.start(1)] + resolved + text[match.end(1) :]
                notes.append(f"{label}: 目标账户别名 {raw} -> {resolved}")

    for index, row in enumerate(book.get("records") or [], 1):
        fix(row, "账户", f"record[{index}]")
        fix(row, "target_account", f"record[{index}]")
        fix_note_target(row, f"record[{index}]")
    for key in ("asset_snapshots", "credit_accounts", "installment_plans", "repayment_reminders", "account_policy"):
        for index, row in enumerate(book.get(key) or [], 1):
            fix(row, "账户", f"{key}[{index}]")
    return notes


def normalize_include(value: Any) -> str:
    text = str(value or "").strip().lower()
    if text in {"excluded", "exclude", "备查", "true", "yes", "1"}:
        return "excluded"
    if text in {"included", "include", "计入", "false", "no", "0"}:
        return "included"
    return ""


def merge_account_policy(
    rows: Iterable[dict[str, Any]] | None,
    base: dict[str, dict[str, Any]] | None = None,
) -> tuple[dict[str, dict[str, Any]], list[str]]:
    source = base if base is not None else default_account_catalog()
    catalog: dict[str, dict[str, Any]] = {
        name: {
            "kind": meta.get("kind", ""),
            "include": meta.get("include", "included"),
            "credit": bool(meta.get("credit", False)),
            "invest": bool(meta.get("invest", False)),
            "aliases": list(meta.get("aliases") or []),
            "alias_windows": list(meta.get("alias_windows") or []),
        }
        for name, meta in source.items()
    }
    errors: list[str] = []
    for i, row in enumerate(rows or [], 1):
        prefix = f"account_policy[{i}]"
        name = str(row.get("账户", "")).strip()
        if not name:
            errors.append(f"{prefix}: missing 账户")
            continue
        current = catalog.get(
            name,
            {"kind": "", "include": "included", "credit": False, "invest": False, "aliases": [], "alias_windows": []},
        )
        kind = str(row.get("账户类型", "")).strip() or current["kind"]
        if kind and kind not in ACCOUNT_KINDS:
            errors.append(f"{prefix}: 账户类型 must be 资产 or 负债")
        include = normalize_include(row.get("纳入", row.get("include", "")))
        if not include and "备查" in row:
            include = "excluded" if truthy(row.get("备查")) else "included"
        if row.get("纳入") not in (None, "") or row.get("include") not in (None, ""):
            if not include:
                errors.append(f"{prefix}: 纳入 must be included or excluded")
        credit = current.get("credit", False)
        if "信用卡" in row or "credit" in row:
            credit = truthy(row.get("信用卡", row.get("credit")))
        invest = current.get("invest", False)
        if "投资账户" in row or "invest" in row:
            invest = truthy(row.get("投资账户", row.get("invest")))
        catalog[name] = {
            "kind": kind or "资产",
            "include": include or current.get("include") or "included",
            "credit": bool(credit),
            "invest": bool(invest),
            "aliases": list(current.get("aliases") or []),
            "alias_windows": list(current.get("alias_windows") or []),
        }
    return catalog, errors


class CategoryCatalog:
    """Category map plus aliases. The shipped defaults are a recommendation."""

    def __init__(
        self,
        mapping: dict[str, Iterable[str]] | None = None,
        category_aliases: dict[str, str] | None = None,
        subcategory_aliases: dict[str, str] | None = None,
    ) -> None:
        base = mapping if mapping is not None else default_category_catalog()
        self.map: dict[str, set[str]] = {str(name): {str(item) for item in subs} for name, subs in base.items()}
        self.category_aliases = dict(CATEGORY_ALIASES)
        self.category_aliases.update(category_aliases or {})
        self.subcategory_aliases = dict(SUBCATEGORY_ALIASES)
        self.subcategory_aliases.update(subcategory_aliases or {})

    def normalize(self, category: str, subcategory: str) -> tuple[str, str, list[str]]:
        warnings: list[str] = []
        original = (category, subcategory)
        if original in LEGACY_PAIR_ALIASES:
            category, subcategory = LEGACY_PAIR_ALIASES[original]
            warnings.append(f"legacy pair {original[0]}/{original[1]} -> {category}/{subcategory}")
        if category in self.category_aliases:
            warnings.append(f"category alias {category} -> {self.category_aliases[category]}")
            category = self.category_aliases[category]
        if subcategory in self.subcategory_aliases:
            warnings.append(f"subcategory alias {subcategory} -> {self.subcategory_aliases[subcategory]}")
            subcategory = self.subcategory_aliases[subcategory]
        return category, subcategory, warnings

    def accepts(self, category: str, subcategory: str) -> bool:
        return category in self.map and subcategory in self.map[category]


def default_category_catalog() -> dict[str, set[str]]:
    return {name: set(subs) for name, subs in DEFAULT_CATEGORY_MAP.items()}


DEFAULT_CATEGORIES = CategoryCatalog()


ACCOUNTS_FILE = "accounts.json"
CATEGORIES_FILE = "categories.json"
SETTINGS_FILE = "settings.json"


def find_config_path(
    name: str,
    paths: Iterable[str | os.PathLike[str]] = (),
    explicit: str | os.PathLike[str] | None = None,
) -> Path | None:
    """Find a config file next to the ledger, the working directory, or data/."""
    if explicit is not None:
        candidate = Path(explicit)
        return candidate if candidate.is_file() else None
    candidates: list[Path] = [Path.cwd() / name, Path.cwd() / "data" / name]
    for raw in paths:
        path = Path(raw)
        base = path if path.is_dir() else path.parent
        for parent in [base, *list(base.parents)[:6]]:
            candidates.append(parent / name)
            candidates.append(parent / "data" / name)
    seen: set[str] = set()
    for candidate in candidates:
        try:
            key = str(candidate.resolve())
        except OSError:
            key = str(candidate)
        if key in seen:
            continue
        seen.add(key)
        if candidate.is_file():
            return candidate
    return None


def load_accounts_config(
    path: Path | str | None = None,
) -> tuple[dict[str, dict[str, Any]], dict[str, str], list[str]]:
    """Load the starter catalog plus optional data/accounts.json overrides."""
    catalog = default_account_catalog()
    errors: list[str] = []
    if path is None:
        return catalog, account_alias_map(catalog), errors
    config_path = Path(path)
    if not config_path.is_file():
        return catalog, account_alias_map(catalog), [f"accounts config not found: {config_path}"]
    try:
        data = loads_json(config_path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        return catalog, account_alias_map(catalog), [f"accounts: invalid JSON: {exc}"]
    if not isinstance(data, dict):
        return catalog, account_alias_map(catalog), ["accounts: config must be a JSON object"]
    if truthy(data.get("replace_defaults")):
        catalog = {}
    rows = data.get("accounts", [])
    if not isinstance(rows, list):
        errors.append("accounts.accounts must be a list")
        rows = []
    for i, row in enumerate(rows, 1):
        prefix = f"accounts[{i}]"
        if not isinstance(row, dict):
            errors.append(f"{prefix}: must be an object")
            continue
        name = str(row.get("账户", row.get("name", ""))).strip()
        if not name:
            errors.append(f"{prefix}: missing 账户")
            continue
        current = catalog.get(
            name,
            {"kind": "", "include": "included", "credit": False, "invest": False, "aliases": [], "alias_windows": []},
        )
        kind = str(row.get("账户类型", row.get("kind", ""))).strip() or current.get("kind", "")
        if kind and kind not in ACCOUNT_KINDS:
            errors.append(f"{prefix}: 账户类型 must be 资产 or 负债")
        include = normalize_include(row.get("纳入", row.get("include", "")))
        if not include and "备查" in row:
            include = "excluded" if truthy(row.get("备查")) else "included"
        if row.get("纳入") not in (None, "") or row.get("include") not in (None, ""):
            if not include:
                errors.append(f"{prefix}: 纳入 must be included or excluded")
        credit = bool(current.get("credit", False))
        if "信用卡" in row or "credit" in row:
            credit = truthy(row.get("信用卡", row.get("credit")))
        invest = bool(current.get("invest", False))
        if "投资账户" in row or "invest" in row:
            invest = truthy(row.get("投资账户", row.get("invest")))
        aliases = list(current.get("aliases") or [])
        windows = list(current.get("alias_windows") or [])
        raw_aliases = row.get("别名", row.get("aliases"))
        if raw_aliases not in (None, ""):
            aliases = []
            windows = []
            if isinstance(raw_aliases, str):
                parts = [part.strip() for part in re.split(r"[;；,，\s]+", raw_aliases) if part.strip()]
                aliases = parts
                windows = [{"名称": part} for part in parts]
            elif isinstance(raw_aliases, list):
                for part in raw_aliases:
                    if isinstance(part, str) and part.strip():
                        aliases.append(part.strip())
                        windows.append({"名称": part.strip()})
                    elif isinstance(part, dict):
                        alias_name = str(part.get("名称", part.get("name", ""))).strip()
                        if not alias_name:
                            errors.append(f"{prefix}: 别名 entry is missing 名称")
                            continue
                        aliases.append(alias_name)
                        windows.append(
                            {
                                key: str(part.get(key, "") or "").strip()
                                for key in ("名称", "含义", "起", "止")
                            }
                        )
                    else:
                        errors.append(f"{prefix}: 别名 entries must be strings or objects")
            else:
                errors.append(f"{prefix}: 别名 must be a list or a string")
        catalog[name] = {
            "kind": kind or "资产",
            "include": include or current.get("include") or "included",
            "credit": credit,
            "invest": invest,
            "aliases": aliases,
            "alias_windows": windows,
        }
    alias_map = account_alias_map(catalog)
    raw_map = data.get("account_aliases") or {}
    if raw_map and not isinstance(raw_map, dict):
        errors.append("account_aliases must be an object")
    elif isinstance(raw_map, dict):
        for alias, target in raw_map.items():
            target_name = str(target or "").strip()
            if not target_name:
                errors.append(f"account_aliases[{alias}]: missing target account")
            elif target_name not in catalog:
                errors.append(f"account_aliases[{alias}]: unknown account {target_name}")
            else:
                alias_map[alias_key(alias)] = target_name
    return catalog, alias_map, errors


def load_categories_config(path: Path | str | None = None) -> tuple[CategoryCatalog, list[str]]:
    """Load the starter category catalog plus optional data/categories.json overrides."""
    if path is None:
        return CategoryCatalog(), []
    config_path = Path(path)
    if not config_path.is_file():
        return CategoryCatalog(), [f"categories config not found: {config_path}"]
    try:
        data = loads_json(config_path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        return CategoryCatalog(), [f"categories: invalid JSON: {exc}"]
    if not isinstance(data, dict):
        return CategoryCatalog(), ["categories: config must be a JSON object"]
    errors: list[str] = []
    mapping: dict[str, set[str]] = {} if truthy(data.get("replace_defaults")) else default_category_catalog()
    rows = data.get("categories", {})
    if rows and not isinstance(rows, dict):
        errors.append("categories.categories must be an object")
    elif isinstance(rows, dict):
        for name, subs in rows.items():
            if isinstance(subs, str):
                subs = [part for part in re.split(r"[;；,，\s]+", subs) if part.strip()]
            if not isinstance(subs, list) or not subs:
                errors.append(f"categories[{name}]: must list subcategories")
                continue
            cleaned = [str(item).strip() for item in subs if str(item).strip()]
            if not cleaned:
                errors.append(f"categories[{name}]: must list subcategories")
                continue
            mapping[str(name).strip()] = set(cleaned)
    raw_category_aliases = data.get("category_aliases") or {}
    raw_subcategory_aliases = data.get("subcategory_aliases") or {}
    for label, value in (
        ("category_aliases", raw_category_aliases),
        ("subcategory_aliases", raw_subcategory_aliases),
    ):
        if value and not isinstance(value, dict):
            errors.append(f"categories.{label} must be an object")
    category_aliases = {
        str(key).strip(): str(value).strip()
        for key, value in (raw_category_aliases.items() if isinstance(raw_category_aliases, dict) else [])
        if str(key).strip() and str(value).strip()
    }
    subcategory_aliases = {
        str(key).strip(): str(value).strip()
        for key, value in (raw_subcategory_aliases.items() if isinstance(raw_subcategory_aliases, dict) else [])
        if str(key).strip() and str(value).strip()
    }
    return CategoryCatalog(mapping, category_aliases, subcategory_aliases), errors


def load_settings_config(path: Path | str | None = None) -> tuple[dict[str, Any], list[str]]:
    """Load optional workspace settings such as the base currency."""
    settings: dict[str, Any] = {
        "base_currency": DEFAULT_BASE_CURRENCY,
        "invest_out_subcategory": DEFAULT_INVEST_OUT_SUBCATEGORY,
    }
    if path is None:
        return settings, []
    config_path = Path(path)
    if not config_path.is_file():
        return settings, [f"settings config not found: {config_path}"]
    try:
        data = loads_json(config_path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        return settings, [f"settings: invalid JSON: {exc}"]
    if not isinstance(data, dict):
        return settings, ["settings: config must be a JSON object"]
    errors: list[str] = []
    currency = str(data.get("base_currency", "") or "").strip().upper()
    if currency:
        if not CURRENCY_RE.fullmatch(currency):
            errors.append("settings.base_currency must be a 3-letter code")
        else:
            settings["base_currency"] = currency
    invest_out = str(data.get("invest_out_subcategory", "") or "").strip()
    if invest_out:
        settings["invest_out_subcategory"] = invest_out
    return settings, errors


class SkillConfig:
    """Accounts, aliases, categories, and settings for one ledger workspace."""

    def __init__(
        self,
        catalog: dict[str, dict[str, Any]] | None = None,
        alias_map: dict[str, str] | None = None,
        categories: CategoryCatalog | None = None,
        accounts_path: Path | None = None,
        categories_path: Path | None = None,
        settings_path: Path | None = None,
        settings: dict[str, Any] | None = None,
        errors: Iterable[str] | None = None,
    ) -> None:
        self.catalog = catalog if catalog is not None else default_account_catalog()
        self.alias_map = alias_map if alias_map is not None else account_alias_map(self.catalog)
        self.categories = categories if categories is not None else CategoryCatalog()
        self.accounts_path = accounts_path
        self.categories_path = categories_path
        self.settings_path = settings_path
        self.settings = settings or {}
        self.base_currency = str(self.settings.get("base_currency", DEFAULT_BASE_CURRENCY))
        self.invest_out_subcategory = str(
            self.settings.get("invest_out_subcategory", DEFAULT_INVEST_OUT_SUBCATEGORY)
        )
        self.errors = list(errors or [])

    @property
    def credit_cards(self) -> set[str]:
        return {name for name, meta in self.catalog.items() if meta.get("credit")}

    def resolve_account(self, name: Any) -> str:
        return resolve_account(name, self.catalog, self.alias_map)

    def normalize_pair(self, category: str, subcategory: str) -> tuple[str, str, list[str]]:
        return self.categories.normalize(category, subcategory)

    def apply_to_book(self, book: dict[str, Any]) -> list[str]:
        return apply_account_aliases(book, self.catalog, self.alias_map)


def load_skill_config(
    paths: Iterable[str | os.PathLike[str]] = (),
    accounts_path: str | os.PathLike[str] | None = None,
    categories_path: str | os.PathLike[str] | None = None,
    settings_path: str | os.PathLike[str] | None = None,
) -> SkillConfig:
    errors: list[str] = []
    accounts_file = find_config_path(ACCOUNTS_FILE, paths, accounts_path)
    categories_file = find_config_path(CATEGORIES_FILE, paths, categories_path)
    settings_file = find_config_path(SETTINGS_FILE, paths, settings_path)
    if accounts_path is not None and accounts_file is None:
        errors.append(f"accounts config not found: {accounts_path}")
    if categories_path is not None and categories_file is None:
        errors.append(f"categories config not found: {categories_path}")
    if settings_path is not None and settings_file is None:
        errors.append(f"settings config not found: {settings_path}")
    catalog, alias_map, account_errors = load_accounts_config(accounts_file)
    categories, category_errors = load_categories_config(categories_file)
    settings, setting_errors = load_settings_config(settings_file)
    errors.extend(account_errors)
    errors.extend(category_errors)
    errors.extend(setting_errors)
    return SkillConfig(
        catalog=catalog,
        alias_map=alias_map,
        categories=categories,
        accounts_path=accounts_file,
        categories_path=categories_file,
        settings_path=settings_file,
        settings=settings,
        errors=errors,
    )


def truthy(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y", "是"}


def shard_key(path: str | os.PathLike[str], mode: str) -> str:
    """Return a day or month key from the file basename only."""
    if mode not in {"day", "month"}:
        raise ValueError(f"shard must be day or month, got {mode!r}")
    base = os.path.basename(os.fspath(path))
    pattern = r"^(\d{4}-\d{2}-\d{2})" if mode == "day" else r"^(\d{4}-\d{2})"
    matched = re.match(pattern, base)
    return matched.group(1) if matched else ""


def index_shard_files(paths: Iterable[Path], mode: str) -> dict[str, list[Path]]:
    grouped: dict[str, list[Path]] = {}
    for path in paths:
        key = shard_key(path, mode) or "unkeyed"
        grouped.setdefault(key, []).append(path)
    return grouped


def iter_ledger_files(root: Path) -> list[Path]:
    if root.is_file():
        return [root]
    files = [path for path in root.rglob("*") if path.is_file() and path.suffix.lower() in LEDGER_SUFFIXES]
    return sorted(files)


def loads_json(text: str) -> Any:
    return json.loads(text, parse_float=Decimal, parse_int=int)


def empty_book() -> dict[str, Any]:
    return {
        "schema_version": "",
        "records": [],
        "asset_snapshots": [],
        "credit_accounts": [],
        "installment_plans": [],
        "repayment_reminders": [],
        "account_policy": [],
        "credit_policy": {},
        "inferred_snapshot": None,
        "is_ledger": True,
    }


def looks_like_ledger(data: Any) -> bool:
    if isinstance(data, list):
        return True
    if not isinstance(data, dict):
        return False
    keys = {
        "records",
        "transactions",
        "asset_snapshots",
        "credit_accounts",
        "installment_plans",
        "repayment_reminders",
        "account_policy",
        "credit_policy",
        "month",
        "schema_version",
    }
    return bool(keys & set(data))


def load_csv_rows(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8-sig")
    if not text.strip():
        return [], [f"empty CSV: {path}"]
    reader = csv.reader(io.StringIO(text))
    try:
        header = next(reader)
    except StopIteration:
        return [], [f"empty CSV: {path}"]
    names = [cell.strip() for cell in header]
    if any(not name for name in names):
        errors.append("CSV header has an empty column name")
    if len(names) != len(set(names)):
        errors.append("CSV header has duplicate column names")
    rows: list[dict[str, str]] = []
    for line_no, cols in enumerate(reader, 2):
        if not any(str(col).strip() for col in cols):
            continue
        if len(cols) != len(names):
            errors.append(f"CSV line {line_no}: expected {len(names)} columns, got {len(cols)}")
            continue
        rows.append({name: value.strip() for name, value in zip(names, cols) if name})
    return rows, errors


def load_file(path: Path) -> tuple[dict[str, Any], list[str]]:
    book = empty_book()
    errors: list[str] = []
    suffix = path.suffix.lower()
    if suffix == ".csv":
        rows, csv_errors = load_csv_rows(path)
        errors.extend(csv_errors)
        book["records"] = rows
        return book, errors
    if suffix == ".json":
        try:
            data = loads_json(path.read_text(encoding="utf-8-sig"))
        except json.JSONDecodeError as exc:
            return book, [f"invalid JSON: {exc}"]
        if isinstance(data, list):
            book["records"] = data
            return book, errors
        if isinstance(data, dict):
            if not looks_like_ledger(data):
                book["is_ledger"] = False
                return book, [f"not a ledger file: {path}"]
            book["schema_version"] = str(data.get("schema_version", "") or "")
            book["records"] = data.get("records", data.get("transactions", []))
            book["asset_snapshots"] = data.get("asset_snapshots", [])
            book["credit_accounts"] = data.get("credit_accounts", [])
            book["installment_plans"] = data.get("installment_plans", [])
            book["repayment_reminders"] = data.get("repayment_reminders", [])
            book["account_policy"] = data.get("account_policy", [])
            policy = data.get("credit_policy") or {}
            book["credit_policy"] = policy if isinstance(policy, dict) else {}
            book["inferred_snapshot"] = data.get("inferred_snapshot")
            book["month"] = data.get("month", "")
            return book, errors
        return book, [f"unsupported JSON shape: {path}"]
    return book, [f"unsupported file type: {path}"]


def decimal_value(value: Any) -> Decimal | None:
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, Decimal):
        return value
    if isinstance(value, int):
        text = str(value)
    elif isinstance(value, float):
        text = format(value, "f")
    else:
        text = str(value).strip()
    if not DECIMAL_RE.fullmatch(text):
        return None
    try:
        return Decimal(text)
    except InvalidOperation:
        return None


def money(value: Any) -> Decimal:
    parsed = decimal_value(value)
    return parsed if parsed is not None else Decimal("0")


def fmt(value: Decimal) -> str:
    return f"{value.quantize(Decimal('0.01'))}"


def fmt_pct(part: Decimal, whole: Decimal) -> str:
    if whole == 0:
        return "0.00%"
    pct = (part / whole * Decimal("100")).quantize(Decimal("0.01"))
    return f"{pct}%"


def parse_time(value: Any) -> datetime | None:
    text = str(value or "").strip()
    if not text:
        return None
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        return None


def default_max_date(today: date | None = None) -> date:
    today = today or date.today()
    return today + timedelta(days=366)


def normalize_pair(
    category: str,
    subcategory: str,
    categories: CategoryCatalog | None = None,
) -> tuple[str, str, list[str]]:
    catalog = categories if categories is not None else DEFAULT_CATEGORIES
    return catalog.normalize(category, subcategory)


def parse_tags(value: Any) -> list[str]:
    if value is None or value == "":
        return []
    if isinstance(value, list):
        parts = [str(item).strip() for item in value]
    else:
        text = str(value).strip()
        if text.startswith("[") and text.endswith("]"):
            try:
                loaded = json.loads(text)
            except json.JSONDecodeError:
                loaded = None
            if isinstance(loaded, list):
                parts = [str(item).strip() for item in loaded]
            else:
                parts = [text]
        else:
            parts = re.split(r"[;；,，\s]+", text)
    return [part for part in parts if part]


def tag_namespace(tag: str) -> str:
    return tag.split(":", 1)[0] if ":" in tag else ""


def check_tag(tag: str) -> tuple[str, str]:
    """Return ('ok'|'legacy'|'error', message).

    Namespaces are chosen by the user. Any letter-first prefix is accepted, so
    project:move or pet:vaccine work without extra configuration.
    """
    if ":" in tag:
        namespace, suffix = tag.split(":", 1)
        if TAG_PREFIX_RE.fullmatch(namespace) and suffix and TAG_SUFFIX_RE.fullmatch(suffix):
            return "ok", ""
        return "error", f"invalid tag {tag!r}; use prefix:suffix with a letter-first prefix"
    return "legacy", f"legacy tag {tag!r}; prefer a namespace such as trip:, event:, person:, or nature:"


def is_refund(row: dict[str, Any]) -> bool:
    if str(row.get("收支类型", "")).strip() == "退款":
        return True
    return bool(str(row.get("refund_of", "")).strip())


def reimburse_ref(row: dict[str, Any]) -> str:
    return str(row.get("reimburse_of", "")).strip()


def reimburse_status(row: dict[str, Any]) -> str:
    """Missing status means the expense is not waiting on reimbursement."""
    text = str(row.get("报销状态", "") or "").strip()
    return text or "不报销"


def credit_mode(row: dict[str, Any] | None, policy: Any = None) -> str:
    """Resolve debt_only vs with_limit. Default is debt_only."""
    row_mode = str((row or {}).get("mode") or "").strip()
    if row_mode in CREDIT_MODES:
        return row_mode
    if isinstance(policy, dict):
        policy_mode = str(policy.get("mode") or "").strip()
        if policy_mode in CREDIT_MODES:
            return policy_mode
    return "debt_only"


def target_account(row: dict[str, Any]) -> str:
    direct = str(row.get("target_account", "")).strip()
    if direct:
        return direct
    text = f"{row.get('note', '')} {row.get('备注', '')}"
    match = TARGET_RE.search(text)
    return match.group(1) if match else ""


def record_id(row: dict[str, Any]) -> str:
    return str(row.get("id", "")).strip()


def pair_id(row: dict[str, Any]) -> str:
    return str(row.get("pairid", "")).strip()


def currency_of(row: dict[str, Any], default: str = DEFAULT_BASE_CURRENCY) -> str:
    text = str(row.get("currency", "") or "").strip().upper()
    return text or default


def json_money(value: Decimal) -> int | float:
    if value == value.to_integral_value():
        return int(value)
    return float(value)


def shift_month(year: int, month: int, delta: int) -> tuple[int, int]:
    index = year * 12 + (month - 1) + delta
    return index // 12, index % 12 + 1


def clamp_day(year: int, month: int, day: int) -> date:
    import calendar

    last = calendar.monthrange(year, month)[1]
    return date(year, month, min(max(day, 1), last))


def cycle_start(as_of: date, bill_day: int) -> date:
    candidate = clamp_day(as_of.year, as_of.month, bill_day)
    if candidate <= as_of:
        return candidate
    year, month = shift_month(as_of.year, as_of.month, -1)
    return clamp_day(year, month, bill_day)


def previous_cycle_start(start: date, bill_day: int) -> date:
    year, month = shift_month(start.year, start.month, -1)
    return clamp_day(year, month, bill_day)


def due_date_for_cycle(start: date, due_day: int, bill_day: int) -> date:
    if due_day > bill_day:
        return clamp_day(start.year, start.month, due_day)
    year, month = shift_month(start.year, start.month, 1)
    return clamp_day(year, month, due_day)


def load_buckets(path: Path) -> list[tuple[str, set[str] | None]]:
    data = loads_json(path.read_text(encoding="utf-8-sig"))
    mapping = data.get("buckets", data) if isinstance(data, dict) else None
    if not isinstance(mapping, dict):
        raise SystemExit(f"buckets config must be a JSON object: {path}")
    buckets: list[tuple[str, set[str] | None]] = []
    seen: set[str] = set()
    star = 0
    for name, categories in mapping.items():
        if not isinstance(categories, list) or not categories:
            raise SystemExit(f"bucket {name!r} must list categories")
        if categories == ["*"] or set(categories) == {"*"}:
            star += 1
            buckets.append((str(name), None))
            continue
        cleaned = {str(item).strip() for item in categories}
        if "*" in cleaned:
            raise SystemExit(f"bucket {name!r} cannot mix * with named categories")
        overlap = cleaned & seen
        if overlap:
            raise SystemExit(f"bucket categories overlap: {', '.join(sorted(overlap))}")
        seen |= cleaned
        buckets.append((str(name), cleaned))
    if star > 1:
        raise SystemExit("only one bucket may use *")
    return buckets


def apply_buckets(
    net_by_category: dict[str, Decimal],
    buckets: list[tuple[str, set[str] | None]],
) -> list[tuple[str, Decimal]]:
    remaining = dict(net_by_category)
    rows: list[tuple[str, Decimal]] = []
    star_name = ""
    for name, categories in buckets:
        if categories is None:
            star_name = name
            continue
        total = sum((remaining.pop(category, Decimal("0")) for category in categories), Decimal("0"))
        rows.append((name, total))
    if star_name:
        rows.append((star_name, sum(remaining.values(), Decimal("0"))))
    return rows


class FlowTotals:
    def __init__(self) -> None:
        self.count = 0
        self.income = Decimal("0")
        self.expense_gross = Decimal("0")
        self.refunds = Decimal("0")
        self.reimbursed = Decimal("0")
        self.pending_reimburse = Decimal("0")
        self.pending_items: list[dict[str, Any]] = []
        self.invest_in = Decimal("0")
        self.invest_out = Decimal("0")
        self.invest_by_account: dict[str, Decimal] = defaultdict(Decimal)
        self.invest_accounts: set[str] = set()
        self.repayment = Decimal("0")
        self.transfer_legs = Decimal("0")
        self.internal_transfer = Decimal("0")
        self.by_category_gross: dict[str, Decimal] = defaultdict(Decimal)
        self.by_category_refund: dict[str, Decimal] = defaultdict(Decimal)
        self.by_category_reimburse: dict[str, Decimal] = defaultdict(Decimal)
        self.by_subcategory: dict[str, Decimal] = defaultdict(Decimal)
        self.by_subcategory_refund: dict[str, Decimal] = defaultdict(Decimal)
        self.by_subcategory_reimburse: dict[str, Decimal] = defaultdict(Decimal)
        self.repayment_by_account: dict[str, Decimal] = defaultdict(Decimal)
        self.cash_expense_net = Decimal("0")

    @property
    def expense_net(self) -> Decimal:
        """实际花销. Pending reimbursement stays in this number until cash arrives."""
        return self.expense_gross - self.refunds - self.reimbursed

    @property
    def investment_net(self) -> Decimal:
        """投入 − 赎回. Not spending and not income."""
        return self.invest_in - self.invest_out


def _category_of(
    row: dict[str, Any],
    categories: CategoryCatalog | None = None,
) -> tuple[str, str]:
    category = str(row.get("类别", "")).strip() or "未分类"
    subcategory = str(row.get("子类", "")).strip() or "未分类"
    category, subcategory, _ = normalize_pair(category, subcategory, categories)
    return category, subcategory


def _note_investment_leg(
    totals: FlowTotals,
    row: dict[str, Any],
    *,
    count_flow: bool,
    categories: CategoryCatalog | None = None,
    catalog: dict[str, dict[str, Any]] | None = None,
) -> None:
    """Record one investment leg.

    Direction comes from the account role: money entering an account marked
    as an investment account is 投入, money leaving it is 赎回. On a cash
    account the sign is authoritative instead: negative is 投入, positive is 赎回.
    """
    amount = money(row.get("金额"))
    account = str(row.get("账户", "")).strip()
    meta = (catalog or {}).get(account, {})
    if account:
        totals.invest_by_account[account] += amount
    if count_flow and amount != 0:
        magnitude = abs(amount)
        is_out = amount < 0 if meta.get("invest") else amount > 0
        if is_out:
            totals.invest_out += magnitude
        else:
            totals.invest_in += magnitude
    target = target_account(row)
    if target and not pair_id(row):
        totals.invest_by_account[target] -= amount
        totals.invest_accounts.add(target)
        return
    if meta.get("invest") and account:
        totals.invest_accounts.add(account)


def _collect_pending(totals: FlowTotals, rows: list[dict[str, Any]]) -> None:
    received: dict[str, Decimal] = defaultdict(Decimal)
    for row in rows:
        if str(row.get("收支类型", "")).strip() != "报销":
            continue
        ref = reimburse_ref(row)
        if ref:
            received[ref] += abs(money(row.get("金额")))
    for row in rows:
        if str(row.get("收支类型", "")).strip() != "支出":
            continue
        if reimburse_status(row) != "待报销":
            continue
        if abs(money(row.get("金额"))) == 0:
            # A zero-amount row has nothing left to reimburse. Validation warns about it.
            continue
        raw_expected = row.get("预计报销", "")
        if raw_expected is None or str(raw_expected).strip() == "":
            expected = abs(money(row.get("金额")))
        else:
            expected = abs(money(raw_expected))
        pending = expected - received.get(record_id(row), Decimal("0"))
        if pending <= 0:
            continue
        totals.pending_reimburse += pending
        stamp = parse_time(row.get("时间"))
        totals.pending_items.append(
            {
                "时间": stamp.date().isoformat() if stamp else "",
                "金额": pending,
                "备注": str(row.get("备注", "")).strip(),
                "账户": str(row.get("账户", "")).strip(),
                "id": record_id(row),
            }
        )


def accumulate(
    rows: list[dict[str, Any]],
    catalog: dict[str, dict[str, Any]] | None = None,
    categories: CategoryCatalog | None = None,
    invest_out_subcategory: str = DEFAULT_INVEST_OUT_SUBCATEGORY,
) -> FlowTotals:
    """花销 counts spending net of refunds and received reimbursements.

    待报销 stays inside 实际花销 until a 报销 row arrives. 投资 is neither
    spending nor income. 内部转账 counts each pair once.
    """
    totals = FlowTotals()
    totals.count = len(rows)
    catalog = catalog or default_account_catalog()
    by_id = {record_id(row): row for row in rows if record_id(row)}
    pair_legs: dict[str, list[dict[str, Any]]] = defaultdict(list)
    invest_legs: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for row in rows:
        tx_type = str(row.get("收支类型", "")).strip()
        amount = money(row.get("金额"))
        magnitude = abs(amount)
        account = str(row.get("账户", "")).strip()
        category, subcategory = _category_of(row, categories)
        kind = catalog.get(account, {}).get("kind", "")
        if is_refund(row):
            target = by_id.get(str(row.get("refund_of", "")).strip())
            if target is not None:
                category, subcategory = _category_of(target, categories)
            totals.refunds += magnitude
            totals.by_category_refund[category] += magnitude
            totals.by_subcategory_refund[f"{category}/{subcategory}"] += magnitude
            if kind != "负债":
                totals.cash_expense_net -= magnitude
            continue
        if tx_type == "收入":
            totals.income += magnitude
        elif tx_type == "支出":
            totals.expense_gross += magnitude
            totals.by_category_gross[category] += magnitude
            totals.by_subcategory[f"{category}/{subcategory}"] += magnitude
            if kind != "负债":
                totals.cash_expense_net += magnitude
        elif tx_type == "报销":
            target = by_id.get(reimburse_ref(row))
            if target is not None:
                category, subcategory = _category_of(target, categories)
                totals.by_category_reimburse[category] += magnitude
                totals.by_subcategory_reimburse[f"{category}/{subcategory}"] += magnitude
            totals.reimbursed += magnitude
            if kind != "负债":
                totals.cash_expense_net -= magnitude
        elif tx_type == "还款":
            totals.repayment += magnitude
            totals.repayment_by_account[account or "未填账户"] += magnitude
        elif tx_type == "转账":
            totals.transfer_legs += magnitude
            pid = pair_id(row)
            if pid:
                pair_legs[pid].append(row)
            else:
                totals.internal_transfer += magnitude
        elif tx_type == "投资":
            pid = pair_id(row)
            if pid:
                invest_legs[pid].append(row)
            else:
                _note_investment_leg(
                    totals,
                    row,
                    count_flow=True,
                    categories=categories,
                    catalog=catalog,
                )

    for legs in pair_legs.values():
        outgoing = [abs(money(leg.get("金额"))) for leg in legs if money(leg.get("金额")) < 0]
        if outgoing:
            totals.internal_transfer += outgoing[0]
        elif legs:
            totals.internal_transfer += max(abs(money(leg.get("金额"))) for leg in legs)
    for legs in invest_legs.values():
        if not legs:
            continue
        flagged = [
            leg
            for leg in legs
            if catalog.get(str(leg.get("账户", "")).strip(), {}).get("invest")
        ]
        counted_leg: dict[str, Any] | None = None
        if flagged:
            counted_leg = flagged[0]
            _note_investment_leg(
                totals,
                counted_leg,
                count_flow=True,
                categories=categories,
                catalog=catalog,
            )
        elif any(_category_of(leg, categories)[1] == invest_out_subcategory for leg in legs):
            totals.invest_out += abs(money(legs[0].get("金额")))
            counted_leg = legs[0]
        else:
            totals.invest_in += abs(money(legs[0].get("金额")))
            counted_leg = legs[0]
        for leg in legs:
            if leg is counted_leg:
                continue
            _note_investment_leg(
                totals,
                leg,
                count_flow=False,
                categories=categories,
                catalog=catalog,
            )
    _collect_pending(totals, rows)
    return totals


def find_optional_data_file(
    name: str,
    paths: Iterable[str | os.PathLike[str]] = (),
) -> Path | None:
    """Find an optional side file next to the ledger, its data/ dir, or the CWD."""
    return find_config_path(name, paths, None)


def currency_totals(
    rows: list[dict[str, Any]],
    base_currency: str = DEFAULT_BASE_CURRENCY,
) -> dict[str, dict[str, Decimal]]:
    """Per-currency totals in the original currency, excluding the base currency.

    Rows without a currency are treated as base currency and skipped here; their
    amount is already in the main totals.
    """
    totals: dict[str, dict[str, Decimal]] = {}
    for row in rows:
        currency = currency_of(row, base_currency)
        if currency == base_currency:
            continue
        original = decimal_value(row.get("original_amount"))
        amount = abs(original if original is not None else money(row.get("金额")))
        bucket = totals.setdefault(
            currency,
            {
                "income": Decimal("0"),
                "expense_gross": Decimal("0"),
                "refunds": Decimal("0"),
                "reimbursed": Decimal("0"),
                "repayment": Decimal("0"),
                "investment": Decimal("0"),
                "count": Decimal("0"),
            },
        )
        bucket["count"] += 1
        tx_type = str(row.get("收支类型", "")).strip()
        if is_refund(row):
            bucket["refunds"] += amount
        elif tx_type == "收入":
            bucket["income"] += amount
        elif tx_type == "支出":
            bucket["expense_gross"] += amount
        elif tx_type == "报销":
            bucket["reimbursed"] += amount
        elif tx_type == "还款":
            bucket["repayment"] += amount
        elif tx_type == "投资":
            bucket["investment"] += amount
    return totals


def category_net(totals: FlowTotals) -> dict[str, Decimal]:
    names = set(totals.by_category_gross) | set(totals.by_category_refund) | set(totals.by_category_reimburse)
    return {
        name: totals.by_category_gross[name] - totals.by_category_refund[name] - totals.by_category_reimburse[name]
        for name in names
    }
