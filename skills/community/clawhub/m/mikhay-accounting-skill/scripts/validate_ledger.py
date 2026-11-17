#!/usr/bin/env python3
"""Validate Chinese personal ledger CSV/JSON files."""

from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import date
from decimal import Decimal
from pathlib import Path
from typing import Any

from ledgerlib import (
    ACCEPTED_SCHEMA_VERSIONS,
    ACCOUNT_KINDS,
    CREDIT_MODES,
    CURRENCY_RE,
    REIMBURSE_STATUSES,
    SCHEMA_VERSION,
    TYPES,
    CategoryCatalog,
    check_tag,
    credit_mode,
    currency_of,
    decimal_value,
    default_max_date,
    is_refund,
    iter_ledger_files,
    load_file,
    load_skill_config,
    merge_account_policy,
    normalize_include,
    normalize_pair,
    pair_id,
    parse_tags,
    parse_time,
    record_id,
    reimburse_ref,
    reimburse_status,
    resolve_account,
    target_account,
)


REQUIRED_RECORD = ["时间", "收支类型", "金额", "类别", "子类", "账户", "备注"]


def is_datetime(value: Any) -> bool:
    return parse_time(value) is not None


def _blank(value: Any) -> bool:
    return str(value if value is not None else "").strip() == ""


def _check_upper(prefix: str, value: Any, max_date: date, errors: list[str], field: str = "时间") -> None:
    parsed = parse_time(value)
    if parsed is None:
        errors.append(f"{prefix}: invalid {field}")
        return
    if parsed.date() > max_date:
        errors.append(f"{prefix}: {field} {parsed.date().isoformat()} is after upper bound {max_date.isoformat()}")


def _check_currency(
    prefix: str,
    row: dict[str, Any],
    amount: Decimal | None,
    errors: list[str],
    base_currency: str = "CNY",
) -> None:
    raw_currency = row.get("currency", "")
    if not _blank(raw_currency) and not CURRENCY_RE.fullmatch(str(raw_currency).strip().upper()):
        errors.append(f"{prefix}: currency must be a 3-letter code")
        return
    currency = currency_of(row, base_currency)
    original = row.get("original_amount", "")
    fx = row.get("fx_rate", "")
    cny = row.get("cny_amount", "")
    original_amount = decimal_value(original) if not _blank(original) else None
    fx_rate = decimal_value(fx) if not _blank(fx) else None
    cny_amount = decimal_value(cny) if not _blank(cny) else None
    if not _blank(original) and original_amount is None:
        errors.append(f"{prefix}: original_amount must be numeric")
    if not _blank(fx) and (fx_rate is None or fx_rate <= 0):
        errors.append(f"{prefix}: fx_rate must be a positive number")
    if not _blank(cny) and cny_amount is None:
        errors.append(f"{prefix}: cny_amount must be numeric")
    if amount is None:
        return
    if currency == base_currency:
        if fx_rate is not None and fx_rate != 1:
            errors.append(f"{prefix}: {base_currency} fx_rate must be 1")
        if original_amount is not None and original_amount != amount:
            errors.append(f"{prefix}: {base_currency} original_amount must equal 金额")
        if cny_amount is not None and cny_amount != amount:
            errors.append(f"{prefix}: base-currency amount must equal 金额")
        return
    if original_amount is None or fx_rate is None:
        errors.append(
            f"{prefix}: non-{base_currency} records require original_amount and fx_rate "
            f"(base currency is {base_currency}, set in data/settings.json)"
        )
        return
    expected = (original_amount * fx_rate).quantize(Decimal("0.01"))
    actual = amount.quantize(Decimal("0.01"))
    if abs(expected - actual) > Decimal("0.01"):
        errors.append(f"{prefix}: 金额 {actual} != original_amount * fx_rate {expected}")
    if cny_amount is not None and abs(cny_amount.quantize(Decimal("0.01")) - actual) > Decimal("0.01"):
        errors.append(f"{prefix}: base-currency amount must equal 金额")


def validate_records(
    rows: list[dict[str, Any]],
    *,
    max_date: date | None = None,
    strict_refs: bool = False,
    catalog: dict[str, dict[str, Any]] | None = None,
    categories: CategoryCatalog | None = None,
    strict: bool = False,
    base_currency: str = "CNY",
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    max_date = max_date or default_max_date()
    catalog = catalog if catalog is not None else merge_account_policy([])[0]
    categories = categories if categories is not None else CategoryCatalog()

    def issue(message: str) -> None:
        """Custom catalogs are a warning by default; --strict turns them into errors."""
        if strict:
            errors.append(message)
        else:
            warnings.append(message)

    seen_ids: dict[str, int] = {}
    seen_rows: dict[tuple[Any, ...], int] = {}
    id_index: dict[str, dict[str, Any]] = {}
    pairs: dict[str, list[tuple[int, dict[str, Any]]]] = defaultdict(list)

    if not isinstance(rows, list):
        return ["records must be a list"], warnings

    for i, row in enumerate(rows, 1):
        prefix = f"record[{i}]"
        if not isinstance(row, dict):
            errors.append(f"{prefix}: record must be an object")
            continue
        for field in REQUIRED_RECORD:
            if _blank(row.get(field)):
                errors.append(f"{prefix}: missing {field}")
        tx_type = str(row.get("收支类型", "")).strip()
        amount = decimal_value(row.get("金额"))
        account = str(row.get("账户", "")).strip()
        category = str(row.get("类别", "")).strip()
        subcategory = str(row.get("子类", "")).strip()
        norm_category, norm_subcategory, pair_warnings = normalize_pair(category, subcategory)
        warnings.extend(f"{prefix}: {w}" for w in pair_warnings)
        _check_upper(prefix, row.get("时间"), max_date, errors)
        if tx_type not in TYPES:
            errors.append(f"{prefix}: invalid 收支类型 {tx_type!r}")
        if amount is None:
            errors.append(f"{prefix}: 金额 must be a decimal number")
        else:
            if amount != amount.quantize(Decimal("0.01")):
                warnings.append(f"{prefix}: 金额 has more than 2 decimal places")
            if tx_type == "支出" and amount > 0:
                warnings.append(f"{prefix}: 支出 usually uses a negative 金额")
            elif tx_type in {"收入", "还款"} and amount < 0:
                warnings.append(f"{prefix}: {tx_type} usually uses a positive 金额")
            elif tx_type == "退款" and amount < 0:
                warnings.append(f"{prefix}: 退款 usually uses a positive 金额")
            elif tx_type == "报销" and amount < 0:
                warnings.append(f"{prefix}: 报销 usually uses a positive 金额")
            elif tx_type == "转账" and amount < 0 and not pair_id(row):
                warnings.append(f"{prefix}: legacy 转账 usually uses a positive 金额; pair legs may be signed")
        resolved_account = resolve_account(account, catalog)
        if resolved_account != account:
            issue(f"{prefix}: 账户别名 {account} -> {resolved_account}")
        if resolved_account not in catalog:
            issue(
                f"{prefix}: 账户 {account!r} 不在账户表。自定义账户写入 data/accounts.json，"
                "或在账本 account_policy 里声明；默认只是推荐清单"
            )
        if not categories.accepts(norm_category, norm_subcategory):
            if norm_category not in categories.map:
                issue(
                    f"{prefix}: 类别 {category!r} 不在类别表。自定义类别写入 data/categories.json；"
                    "默认只是推荐清单，不是硬枚举"
                )
            else:
                issue(
                    f"{prefix}: 子类 {subcategory!r} 不在类别 {norm_category} 下。"
                    "自定义子类写入 data/categories.json；默认只是推荐清单"
                )
        if tx_type == "退款" or (is_refund(row) and tx_type != "支出"):
            if norm_category in {"收入", "还款", "转账", "报销", "投资"}:
                issue(f"{prefix}: 退款 通常不使用 类别 {norm_category}")
        else:
            expected_category = {
                "收入": "收入",
                "还款": "还款",
                "转账": "转账",
                "报销": "报销",
                "投资": "投资",
            }.get(tx_type)
            if expected_category and norm_category != expected_category:
                issue(f"{prefix}: 收支类型 {tx_type} 通常使用 类别 {expected_category}")
            if tx_type == "支出" and norm_category in {"收入", "还款", "转账", "退款", "报销", "投资"}:
                issue(f"{prefix}: 支出 通常不使用 类别 {norm_category}")
        if tx_type == "收入" and norm_subcategory == "报销":
            warnings.append(
                f"{prefix}: 收入/报销 is a legacy shape and still counts as income; "
                "new records should use 收支类型=报销. Rewriting old rows is the user's decision"
            )
        for tag in parse_tags(row.get("tags")):
            status, message = check_tag(tag)
            if status == "error":
                errors.append(f"{prefix}: {message}")
            elif status == "legacy":
                warnings.append(f"{prefix}: {message}")
        _check_currency(prefix, row, amount, errors, base_currency)
        noted_target = target_account(row)
        if noted_target:
            resolved_target = resolve_account(noted_target, catalog)
            if resolved_target != noted_target:
                issue(f"{prefix}: target_account 别名 {noted_target} -> {resolved_target}")
            elif resolved_target not in catalog:
                issue(
                    f"{prefix}: target_account {noted_target!r} 不在账户表。"
                    "自定义账户写入 data/accounts.json，或在 account_policy 里声明"
                )
        if tx_type == "转账" and not pair_id(row) and not noted_target:
            warnings.append(f"{prefix}: 转账 has neither pairid nor target_account")
        if tx_type == "投资" and not pair_id(row) and not noted_target:
            warnings.append(f"{prefix}: 投资 has neither pairid nor target_account")
        status = str(row.get("报销状态", "") or "").strip()
        if status and status not in REIMBURSE_STATUSES:
            errors.append(f"{prefix}: 报销状态 must be 待报销, 已报销, or 不报销")
        elif status and tx_type != "支出":
            warnings.append(f"{prefix}: 报销状态 belongs on 支出 records")
        expected_reimburse = row.get("预计报销", "")
        if not _blank(expected_reimburse):
            expected_amount = decimal_value(expected_reimburse)
            if expected_amount is None or expected_amount < 0:
                errors.append(f"{prefix}: 预计报销 must be a non-negative decimal")
            elif tx_type != "支出":
                warnings.append(f"{prefix}: 预计报销 belongs on 支出 records")
            elif amount is not None and expected_amount > abs(amount):
                warnings.append(f"{prefix}: 预计报销 is larger than 金额")
        if (
            tx_type == "支出"
            and amount is not None
            and amount == 0
            and reimburse_status(row) == "待报销"
        ):
            warnings.append(
                f"{prefix}: 金额为 0 的支出仍标为 待报销；改回原金额，或把 报销状态 改成 已报销"
            )
        rid = record_id(row)
        if rid:
            if rid in seen_ids:
                errors.append(f"{prefix}: duplicate id {rid!r} also at record[{seen_ids[rid]}]")
            else:
                seen_ids[rid] = i
                id_index[rid] = row
        if amount is not None and is_datetime(row.get("时间")):
            dup_key = (str(row.get("时间", "")).strip(), tx_type, amount, account, str(row.get("备注", "")).strip())
            if dup_key in seen_rows:
                warnings.append(
                    f"{prefix}: same time/type/amount/account/note as record[{seen_rows[dup_key]}]; "
                    "check for an accidental double entry"
                )
            else:
                seen_rows[dup_key] = i
        if pair_id(row):
            pairs[pair_id(row)].append((i, row))
        refund_ref = str(row.get("refund_of", "")).strip()
        if refund_ref:
            if tx_type not in {"退款", "支出"}:
                errors.append(f"{prefix}: refund_of is only valid on 退款 records")
        if reimburse_ref(row) and tx_type != "报销":
            errors.append(f"{prefix}: reimburse_of is only valid on 报销 records")

    for pid, legs in pairs.items():
        label = f"pairid {pid}"
        if len(legs) != 2:
            errors.append(f"{label}: expected 2 legs, found {len(legs)}")
            continue
        (left_i, left), (right_i, right) = legs
        left_amount = decimal_value(left.get("金额"))
        right_amount = decimal_value(right.get("金额"))
        left_type = str(left.get("收支类型", "")).strip()
        right_type = str(right.get("收支类型", "")).strip()
        if {left_type, right_type} not in ({"转账"}, {"投资"}):
            errors.append(f"{label}: both legs must be 转账, or both must be 投资")
        if left_amount is None or right_amount is None:
            continue
        if abs(left_amount) != abs(right_amount):
            errors.append(f"{label}: amounts are not equal ({left_amount} vs {right_amount})")
        if left_amount * right_amount > 0:
            errors.append(f"{label}: legs must have opposite directions")
        elif left_amount == 0 or right_amount == 0:
            warnings.append(f"{label}: zero-amount leg; a transfer or investment leg is normally non-zero")
        if str(left.get("账户", "")).strip() == str(right.get("账户", "")).strip():
            errors.append(f"{label}: legs must use different accounts")

    for i, row in enumerate(rows, 1):
        if not isinstance(row, dict):
            continue
        refund_ref = str(row.get("refund_of", "")).strip()
        if not refund_ref:
            continue
        target = id_index.get(refund_ref)
        prefix = f"record[{i}]"
        if target is None:
            message = f"{prefix}: refund_of {refund_ref!r} does not match a record id"
            if strict_refs:
                errors.append(message)
            else:
                warnings.append(message + " in this file")
        elif str(target.get("收支类型", "")).strip() != "支出":
            errors.append(f"{prefix}: refund_of target must be 支出")

    for i, row in enumerate(rows, 1):
        if not isinstance(row, dict):
            continue
        linked = reimburse_ref(row)
        if not linked:
            continue
        target = id_index.get(linked)
        prefix = f"record[{i}]"
        if target is None:
            message = f"{prefix}: reimburse_of {linked!r} does not match a record id"
            if strict_refs:
                errors.append(message)
            else:
                warnings.append(message + " in this file")
        elif str(target.get("收支类型", "")).strip() != "支出":
            errors.append(f"{prefix}: reimburse_of target must be 支出")
    return errors, warnings


def validate_assets(
    rows: list[dict[str, Any]],
    catalog: dict[str, dict[str, Any]],
    max_date: date,
    *,
    strict: bool = False,
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    def issue(message: str) -> None:
        if strict:
            errors.append(message)
        else:
            warnings.append(message)

    for i, row in enumerate(rows, 1):
        prefix = f"asset_snapshot[{i}]"
        if not isinstance(row, dict):
            errors.append(f"{prefix}: snapshot must be an object")
            continue
        for field in ["时间", "账户"]:
            if _blank(row.get(field)):
                errors.append(f"{prefix}: missing {field}")
        if _blank(row.get("余额", row.get("金额", ""))):
            errors.append(f"{prefix}: missing 金额")
        _check_upper(prefix, row.get("时间"), max_date, errors)
        account = str(row.get("账户", "")).strip()
        if resolve_account(account, catalog) not in catalog:
            issue(
                f"{prefix}: 账户 {account!r} 不在账户表。自定义账户写入 data/accounts.json，"
                "或在 account_policy 里声明"
            )
        kind = str(row.get("账户类型", "")).strip()
        if kind and kind not in ACCOUNT_KINDS:
            errors.append(f"{prefix}: 账户类型 must be 资产 or 负债")
        include = str(row.get("纳入", "")).strip()
        if include and not normalize_include(include):
            errors.append(f"{prefix}: 纳入 must be included or excluded")
        amount = decimal_value(row.get("余额", row.get("金额")))
        if amount is None:
            errors.append(f"{prefix}: 金额 must be a decimal number")
        elif kind == "资产" and amount < 0:
            warnings.append(f"{prefix}: asset account usually uses non-negative 金额")
        elif kind == "负债" and amount > 0:
            warnings.append(f"{prefix}: liability snapshot usually uses negative 金额")
        currency = str(row.get("currency", "") or "").strip()
        if currency and not CURRENCY_RE.fullmatch(currency.upper()):
            errors.append(f"{prefix}: currency must be a 3-letter code")
    return errors, warnings


def validate_day(value: Any) -> bool:
    try:
        day = int(value)
    except (TypeError, ValueError):
        return False
    return 1 <= day <= 31


def validate_credit_accounts(
    rows: list[dict[str, Any]],
    catalog: dict[str, dict[str, Any]],
    *,
    default_mode: str = "debt_only",
    strict: bool = False,
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    def issue(message: str) -> None:
        if strict:
            errors.append(message)
        else:
            warnings.append(message)

    for i, row in enumerate(rows, 1):
        prefix = f"credit_account[{i}]"
        if not isinstance(row, dict):
            errors.append(f"{prefix}: credit account must be an object")
            continue
        for field in ["账户", "欠款"]:
            if _blank(row.get(field)):
                errors.append(f"{prefix}: missing {field}")
        account = str(row.get("账户", "")).strip()
        resolved = resolve_account(account, catalog)
        kind = catalog.get(resolved, {}).get("kind")
        if resolved not in catalog:
            issue(
                f"{prefix}: 账户 {account!r} 不在账户表，无法确认是负债账户。"
                "自定义账户写入 data/accounts.json，或在 account_policy 里声明"
            )
        elif kind != "负债":
            issue(f"{prefix}: 账户 {resolved!r} 应为负债账户（当前 {kind or '未知'}）")
        debt = decimal_value(row.get("欠款"))
        if debt is None or debt < 0:
            errors.append(f"{prefix}: 欠款 must be a non-negative decimal")
        for field in ["额度", "可用额度"]:
            value = row.get(field, "")
            if not _blank(value) and decimal_value(value) is None:
                errors.append(f"{prefix}: {field} must be numeric")
        for field in ["账单日", "还款日"]:
            value = row.get(field, "")
            if not _blank(value) and not validate_day(value):
                errors.append(f"{prefix}: {field} must be 1-31")
        row_mode = str(row.get("mode") or "").strip()
        if row_mode and row_mode not in CREDIT_MODES:
            errors.append(f"{prefix}: mode must be debt_only or with_limit")
        mode = credit_mode(row, {"mode": default_mode})
        if mode == "with_limit" and debt is not None:
            if _blank(row.get("额度")):
                warnings.append(f"{prefix}: with_limit mode is missing 额度")
            else:
                limit = decimal_value(row.get("额度"))
                available_raw = row.get("可用额度", "")
                if limit is not None and not _blank(available_raw):
                    available = decimal_value(available_raw)
                    if available is not None and abs((limit - debt) - available) > Decimal("1"):
                        warnings.append(
                            f"{prefix}: 可用额度 differs from 额度-欠款 by more than 1"
                        )
    return errors, warnings


def validate_installments(
    rows: list[dict[str, Any]],
    catalog: dict[str, dict[str, Any]],
    max_date: date,
    *,
    strict: bool = False,
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    def issue(message: str) -> None:
        if strict:
            errors.append(message)
        else:
            warnings.append(message)

    required = ["id", "账户", "本金", "总期数", "已还期数", "每期金额", "下一还款日", "状态"]
    seen_ids: set[str] = set()
    for i, row in enumerate(rows, 1):
        prefix = f"installment_plan[{i}]"
        if not isinstance(row, dict):
            errors.append(f"{prefix}: installment must be an object")
            continue
        for field in required:
            if _blank(row.get(field)):
                errors.append(f"{prefix}: missing {field}")
        plan_id = str(row.get("id", "")).strip()
        if plan_id:
            if plan_id in seen_ids:
                errors.append(f"{prefix}: duplicate installment id {plan_id!r}")
            seen_ids.add(plan_id)
        account = str(row.get("账户", "")).strip()
        resolved = resolve_account(account, catalog)
        if resolved not in catalog:
            issue(f"{prefix}: 账户 {account!r} 不在账户表；自定义账户写入 data/accounts.json")
        elif catalog.get(resolved, {}).get("kind") != "负债":
            issue(f"{prefix}: 账户 {resolved!r} 应为负债账户")
        for field in ["本金", "每期金额"]:
            value = decimal_value(row.get(field))
            if value is None or value <= 0:
                errors.append(f"{prefix}: {field} must be a positive decimal")
        try:
            total = int(row.get("总期数", ""))
            paid = int(row.get("已还期数", ""))
        except (TypeError, ValueError):
            errors.append(f"{prefix}: 总期数 and 已还期数 must be integers")
        else:
            if total <= 0:
                errors.append(f"{prefix}: 总期数 must be positive")
            if paid < 0:
                errors.append(f"{prefix}: 已还期数 cannot be negative")
            if total > 0 and paid > total:
                errors.append(f"{prefix}: 已还期数 cannot exceed 总期数")
        _check_upper(prefix, row.get("下一还款日"), max_date, errors, "下一还款日")
    return errors, warnings


def validate_reminders(
    rows: list[dict[str, Any]],
    catalog: dict[str, dict[str, Any]],
    max_date: date,
    *,
    strict: bool = False,
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    def issue(message: str) -> None:
        if strict:
            errors.append(message)
        else:
            warnings.append(message)

    for i, row in enumerate(rows, 1):
        prefix = f"repayment_reminder[{i}]"
        if not isinstance(row, dict):
            errors.append(f"{prefix}: reminder must be an object")
            continue
        for field in ["时间", "账户", "金额", "状态"]:
            if _blank(row.get(field)):
                errors.append(f"{prefix}: missing {field}")
        _check_upper(prefix, row.get("时间"), max_date, errors)
        account = str(row.get("账户", "")).strip()
        resolved = resolve_account(account, catalog)
        if resolved not in catalog:
            issue(f"{prefix}: 账户 {account!r} 不在账户表；自定义账户写入 data/accounts.json")
        elif catalog.get(resolved, {}).get("kind") != "负债":
            issue(f"{prefix}: 账户 {resolved!r} 应为负债账户")
        amount = decimal_value(row.get("金额"))
        if amount is None or amount <= 0:
            errors.append(f"{prefix}: 金额 must be a positive decimal")
    return errors, warnings


def validate_book(
    book: dict[str, Any],
    *,
    max_date: date | None = None,
    strict_refs: bool = False,
    catalog: dict[str, dict[str, Any]] | None = None,
    categories: CategoryCatalog | None = None,
    strict: bool = False,
    base_currency: str = "CNY",
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    max_date = max_date or default_max_date()
    version = str(book.get("schema_version", "") or "")
    if version not in ACCEPTED_SCHEMA_VERSIONS:
        warnings.append(f"unrecognized schema_version {version!r}; this tool writes {SCHEMA_VERSION}")
    policy = book.get("credit_policy") or {}
    default_mode = "debt_only"
    if policy and not isinstance(policy, dict):
        errors.append("credit_policy must be an object")
    elif isinstance(policy, dict):
        mode = str(policy.get("mode") or "").strip()
        if mode and mode not in CREDIT_MODES:
            errors.append("credit_policy.mode must be debt_only or with_limit")
        elif mode:
            default_mode = mode
    base_catalog = catalog if catalog is not None else None
    merged_catalog, policy_errors = merge_account_policy(book.get("account_policy") or [], base=base_catalog)
    catalog = merged_catalog
    errors.extend(policy_errors)
    record_errors, record_warnings = validate_records(
        book.get("records") or [],
        max_date=max_date,
        strict_refs=strict_refs,
        catalog=catalog,
        categories=categories,
        strict=strict,
        base_currency=base_currency,
    )
    asset_errors, asset_warnings = validate_assets(
        book.get("asset_snapshots") or [], catalog, max_date, strict=strict
    )
    credit_errors, credit_warnings = validate_credit_accounts(
        book.get("credit_accounts") or [],
        catalog,
        default_mode=default_mode,
        strict=strict,
    )
    installment_errors, installment_warnings = validate_installments(
        book.get("installment_plans") or [], catalog, max_date, strict=strict
    )
    reminder_errors, reminder_warnings = validate_reminders(
        book.get("repayment_reminders") or [], catalog, max_date, strict=strict
    )
    errors.extend(record_errors)
    errors.extend(asset_errors)
    errors.extend(credit_errors)
    errors.extend(installment_errors)
    errors.extend(reminder_errors)
    warnings.extend(record_warnings)
    warnings.extend(asset_warnings)
    warnings.extend(credit_warnings)
    warnings.extend(installment_warnings)
    warnings.extend(reminder_warnings)
    return errors, warnings


def collect_paths(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_dir():
            files.extend(iter_ledger_files(path))
        else:
            files.append(path)
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Chinese personal ledger CSV/JSON files.")
    parser.add_argument("paths", nargs="+", type=Path, help="Ledger files or directories. Directories are scanned fully.")
    parser.add_argument("--max-date", help="Upper bound for dates, YYYY-MM-DD. Default: today + 366 days.")
    parser.add_argument(
        "--accounts",
        type=Path,
        help="Account config. Default: data/accounts.json next to the ledger or in the working directory.",
    )
    parser.add_argument(
        "--categories",
        type=Path,
        help="Category config. Default: data/categories.json next to the ledger or in the working directory.",
    )
    parser.add_argument(
        "--settings",
        type=Path,
        help="Workspace settings such as base_currency. Default: data/settings.json when present.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat custom accounts, custom categories, and type/category conflicts as errors. Default: warnings.",
    )
    args = parser.parse_args()
    if args.max_date:
        parsed = parse_time(args.max_date)
        if parsed is None:
            raise SystemExit("--max-date must be YYYY-MM-DD")
        max_date = parsed.date()
    else:
        max_date = default_max_date()

    config = load_skill_config(args.paths, args.accounts, args.categories, args.settings)
    files = collect_paths(args.paths)
    if not files:
        raise SystemExit("no ledger files found")

    errors: list[str] = list(config.errors)
    warnings: list[str] = []
    books: list[tuple[Path, dict[str, Any]]] = []
    for path in files:
        book, load_errors = load_file(path)
        if not book.get("is_ledger", True):
            warnings.append(f"{path}: skipped non-ledger file")
            continue
        if load_errors:
            errors.extend(f"{path}: {item}" for item in load_errors)
        warnings.extend(f"{path}: {item}" for item in config.apply_to_book(book))
        books.append((path, book))

    combined_records = [row for _, book in books for row in book["records"] if isinstance(row, dict)]
    if not books:
        print("INVALID: no ledger files")
        for error in errors:
            print(f"- {error}")
        return 1

    if len(books) == 1:
        book_errors, book_warnings = validate_book(
            books[0][1],
            max_date=max_date,
            strict_refs=False,
            catalog=config.catalog,
            categories=config.categories,
            strict=args.strict,
            base_currency=config.base_currency,
        )
        errors.extend(book_errors)
        warnings.extend(book_warnings)
    else:
        catalog = {name: dict(meta) for name, meta in config.catalog.items()}
        for path, book in books:
            partial = dict(book)
            partial["records"] = []
            book_errors, book_warnings = validate_book(
                partial,
                max_date=max_date,
                strict_refs=False,
                catalog=catalog,
                categories=config.categories,
                strict=args.strict,
                base_currency=config.base_currency,
            )
            errors.extend(f"{path}: {item}" for item in book_errors)
            warnings.extend(f"{path}: {item}" for item in book_warnings)
            merged, _policy_errors = merge_account_policy(book.get("account_policy") or [], base=catalog)
            catalog = merged
        record_errors, record_warnings = validate_records(
            combined_records,
            max_date=max_date,
            strict_refs=True,
            catalog=catalog,
            categories=config.categories,
            strict=args.strict,
            base_currency=config.base_currency,
        )
        errors.extend(record_errors)
        warnings.extend(record_warnings)

    label = files[0] if len(files) == 1 else f"{len(files)} files"
    if config.accounts_path is not None:
        warnings.append(f"accounts config: {config.accounts_path}")
    if config.categories_path is not None:
        warnings.append(f"categories config: {config.categories_path}")
    if errors:
        print(f"INVALID: {label}")
        for error in errors:
            print(f"- {error}")
        if warnings:
            print("WARNINGS:")
            for warning in warnings[:50]:
                print(f"- {warning}")
            if len(warnings) > 50:
                print(f"- ... {len(warnings) - 50} more warnings")
        return 1

    print(f"OK: {label}")
    print(f"records: {len(combined_records)}")
    if len(books) == 1:
        book = books[0][1]
        print(f"asset_snapshots: {len(book['asset_snapshots'])}")
        print(f"credit_accounts: {len(book['credit_accounts'])}")
        print(f"installment_plans: {len(book['installment_plans'])}")
        print(f"repayment_reminders: {len(book['repayment_reminders'])}")
    if warnings:
        print(f"warnings: {len(warnings)}")
        for warning in warnings[:20]:
            print(f"- {warning}")
        if len(warnings) > 20:
            print(f"- ... {len(warnings) - 20} more warnings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
