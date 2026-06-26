#!/usr/bin/env python3
"""Verify pledge eligibility from pasted bond codes against local CSV rules."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path


RATING_ORDER = {
    "AAA": 90,
    "AAA-": 85,
    "AA+": 80,
    "AA": 70,
    "AA-": 60,
    "A+": 50,
    "A": 40,
    "A-": 30,
}

CUSTODIAN_ALIASES = {
    "中央国债登记结算有限责任公司": "中债",
    "中央结算": "中债",
    "中债登": "中债",
    "中债": "中债",
    "银行间市场清算所股份有限公司": "上清",
    "上海清算所": "上清",
    "上清所": "上清",
    "上清": "上清",
}

BOND_TYPE_ALIASES = {
    "国债": "利率债",
    "政金债": "利率债",
    "政策性金融债": "利率债",
    "央票": "利率债",
    "地方政府债": "地方债",
    "地方债": "地方债",
    "同业存单": "CD",
    "银行存单": "CD",
    "CD": "CD",
    "中期票据": "信用债",
    "短期融资券": "信用债",
    "超短期融资券": "信用债",
    "企业债": "信用债",
    "公司债": "信用债",
    "商业银行债": "信用债",
    "二级资本债": "信用债",
    "永续债": "信用债",
    "信用债": "信用债",
}


def truthy(value: str | None) -> bool:
    return (value or "").strip().upper() in {"TRUE", "Y", "YES", "1", "是"}


def split_set(value: str | None) -> set[str]:
    text = (value or "").strip()
    if not text:
        return set()
    if text.upper() == "ANY":
        return {"ANY"}
    return {part.strip() for part in re.split(r"[|,，;；]", text) if part.strip()}


def normalize_custodian(value: str | None) -> str:
    text = (value or "").strip()
    return CUSTODIAN_ALIASES.get(text, text)


def normalize_bond_type(value: str | None) -> str:
    text = (value or "").strip()
    return BOND_TYPE_ALIASES.get(text, text)


def normalize_allowed(values: set[str], normalizer) -> set[str]:
    if "ANY" in values:
        return values
    return {normalizer(value) for value in values}


def load_csv(path: Path, key: str) -> dict[str, dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    data: dict[str, dict[str, str]] = {}
    for row in rows:
        value = (row.get(key) or "").strip()
        if value:
            data[value] = {k: (v or "").strip() for k, v in row.items()}
    return data


def extract_codes(text: str) -> list[str]:
    codes: list[str] = []
    seen_header = False
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        cells = re.split(r"\t|,|，|\s+", line)
        first = cells[0].strip()
        if first.lower() in {"bond_code", "债券代码", "代码"} and not seen_header:
            seen_header = True
            continue
        if re.fullmatch(r"\d+", first) and len(cells) > 1:
            first = cells[1].strip()
        codes.append(first)
    return codes


def selected_rating(bond: dict[str, str]) -> tuple[str, str]:
    for field, label in (
        ("internal_rating", "内部评级"),
        ("issuer_rating", "主体评级"),
        ("bond_rating", "债项评级"),
    ):
        rating = bond.get(field, "").strip()
        if rating:
            return rating, label
    legacy_rating = bond.get("rating", "").strip()
    if legacy_rating:
        return legacy_rating, "评级"
    return "", ""


def rating_ok(bond: dict[str, str], account: dict[str, str]) -> tuple[bool, str, str]:
    bond_type = normalize_bond_type(bond.get("bond_type", ""))
    rating, rating_source = selected_rating(bond)
    min_rating = account.get("min_rating", "")
    if bond_type in {"利率债", "地方债"}:
        return True, "利率债/地方债不看评级", ""
    if rating not in RATING_ORDER or min_rating not in RATING_ORDER:
        return False, "评级缺失或评级序列未定义", rating
    if RATING_ORDER[rating] >= RATING_ORDER[min_rating]:
        return True, f"{rating_source}{rating}满足{min_rating}", rating
    return False, f"{rating_source}{rating}低于账户要求{min_rating}", rating


def verify(code: str, bond: dict[str, str] | None, account: dict[str, str]) -> dict[str, str]:
    if bond is None:
        return {
            "mark": "×",
            "bond_code": code,
            "bond_name": "",
            "used_rating": "",
            "custodian": "",
            "reason": "券库无记录",
        }

    if truthy(bond.get("is_blacklisted")):
        reason = "券库黑名单"
        ok = False
    else:
        ok = True
        reason = "可押"

    blacklist_codes = split_set(account.get("blacklist_codes"))
    blacklist_issuers = split_set(account.get("blacklist_issuers"))
    if ok and code in blacklist_codes:
        ok, reason = False, "账户债券代码黑名单"
    if ok and bond.get("issuer", "") in blacklist_issuers:
        ok, reason = False, "账户主体黑名单"

    allowed_types = split_set(account.get("allowed_bond_types"))
    allowed_types = normalize_allowed(allowed_types, normalize_bond_type)
    bond_type = normalize_bond_type(bond.get("bond_type", ""))
    if ok and "ANY" not in allowed_types and bond_type not in allowed_types:
        ok, reason = False, f"券种{bond.get('bond_type', '')}不在账户范围"

    allowed_custodians = split_set(account.get("allowed_custodians"))
    allowed_custodians = normalize_allowed(allowed_custodians, normalize_custodian)
    custodian = normalize_custodian(bond.get("custodian", ""))
    if ok and "ANY" not in allowed_custodians and custodian not in allowed_custodians:
        ok, reason = False, f"托管地{bond.get('custodian', '')}不在账户范围"

    if ok and truthy(account.get("require_non_related")):
        bond_tags = split_set(bond.get("related_party_tags"))
        account_tags = split_set(account.get("account_related_tags"))
        if bond_tags and account_tags and bond_tags.intersection(account_tags):
            ok, reason = False, "不满足非关联要求"
        elif not account_tags and bond_tags:
            ok, reason = False, "账户关联标签缺失，无法确认非关联"

    used_rating = ""
    if ok:
        ok, reason, used_rating = rating_ok(bond, account)
    else:
        used_rating, _ = selected_rating(bond)

    return {
        "mark": "√" if ok else "×",
        "bond_code": code,
        "bond_name": bond.get("bond_name", ""),
        "used_rating": used_rating,
        "custodian": bond.get("custodian", ""),
        "reason": reason if not ok else "",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify pledge eligibility for pasted bond codes.")
    parser.add_argument("--account", help="Account name in account-pledge-scope.csv. Defaults to the first account as template/test account.")
    parser.add_argument("--bonds", required=True, type=Path, help="Bond rating directory CSV")
    parser.add_argument("--rules", required=True, type=Path, help="Account pledge scope CSV")
    parser.add_argument("--input", type=Path, help="Pasted Excel text/TSV file. Defaults to stdin.")
    args = parser.parse_args()

    bonds = load_csv(args.bonds, "bond_code")
    accounts = load_csv(args.rules, "account_name")
    account_name = args.account
    if not account_name:
        account_name = next(iter(accounts), "")
        if account_name:
            print(f"未指定账户，正在使用测试/模板账户口径：{account_name}", file=sys.stderr)

    account = accounts.get(account_name)
    if account is None:
        print(f"账户未匹配：{account_name}", file=sys.stderr)
        return 2

    text = args.input.read_text(encoding="utf-8-sig") if args.input else sys.stdin.read()
    codes = extract_codes(text)
    writer = csv.DictWriter(
        sys.stdout,
        fieldnames=["mark", "bond_code", "bond_name", "used_rating", "custodian", "reason"],
        delimiter="\t",
        lineterminator="\n",
    )
    writer.writeheader()
    for code in codes:
        writer.writerow(verify(code, bonds.get(code), account))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
