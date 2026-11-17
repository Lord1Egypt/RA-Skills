#!/usr/bin/env python3
"""Import CSV/XLSX bills into the standard Chinese ledger JSON format."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import zipfile
from collections import defaultdict
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

from ledgerlib import (
    SCHEMA_VERSION,
    SkillConfig,
    find_config_path,
    load_skill_config,
    resolve_account,
    shard_key,
)
from validate_ledger import validate_records


FIELDS = [
    "时间",
    "收支类型",
    "金额",
    "类别",
    "子类",
    "账户",
    "备注",
    "tags",
    "note",
    "id",
    "refund_of",
    "pairid",
    "target_account",
    "currency",
    "original_amount",
    "fx_rate",
    "cny_amount",
]
DEFAULT_ACCOUNT_BY_SOURCE = {
    "alipay": "支付宝",
    "wechat": "微信钱包",
    "meituan": "美团",
}
COLUMN_ALIASES = {
    "时间": ["时间", "交易时间", "交易创建时间", "付款时间", "日期", "交易日期", "time", "date"],
    "收支类型": ["收支类型", "收/支", "收支", "类型", "交易类型", "direction"],
    "金额": ["金额", "金额(元)", "金额（元）", "交易金额", "amount"],
    "收入金额": ["收入金额", "收入", "入账金额"],
    "支出金额": ["支出金额", "支出", "出账金额"],
    "类别": ["类别", "分类", "一级分类", "category"],
    "子类": ["子类", "二级分类", "subcategory"],
    "账户": ["账户", "支付方式", "付款方式", "收/付款方式", "account"],
    "备注": ["备注", "商品", "商品说明", "交易对方", "商户", "摘要", "说明", "description", "note"],
    "tags": ["tags", "标签"],
    "note": ["note", "导入备注"],
    "id": ["id", "交易单号"],
    "refund_of": ["refund_of", "退款关联"],
    "reimburse_of": ["reimburse_of", "报销关联"],
    "报销状态": ["报销状态"],
    "预计报销": ["预计报销"],
    "item_id": ["item_id", "物品"],
    "pairid": ["pairid", "配对号"],
    "target_account": ["target_account", "目标账户", "对方账户"],
    "currency": ["currency", "币种"],
    "original_amount": ["original_amount", "原币金额"],
    "fx_rate": ["fx_rate", "汇率"],
    "cny_amount": ["cny_amount", "人民币金额"],
}
# Starter keyword table. Override it with data/import_rules.json.
DEFAULT_CATEGORY_KEYWORDS: list[tuple[str, str, list[str]]] = [
    ("收入", "工资", ["工资", "薪资", "salary"]),
    ("收入", "补贴", ["补贴", "津贴", "补助"]),
    ("食品餐饮", "外卖", ["外卖", "饿了么", "美团外卖"]),
    ("食品餐饮", "早餐", ["早餐"]),
    ("食品餐饮", "午餐", ["午餐"]),
    ("食品餐饮", "晚餐", ["晚餐"]),
    ("食品餐饮", "饮料酒水", ["饮料", "奶茶", "咖啡", "酒水"]),
    ("食品餐饮", "水果", ["水果"]),
    ("食品餐饮", "生鲜", ["生鲜", "买菜"]),
    ("食品餐饮", "正餐", ["餐厅", "饭店", "正餐", "吃饭"]),
    ("出行交通", "打车", ["打车", "滴滴", "出租车", "网约车"]),
    ("出行交通", "公交地铁", ["公交", "地铁", "交通卡"]),
    ("出行交通", "火车", ["火车", "高铁", "动车"]),
    ("出行交通", "飞机", ["飞机", "机票", "航班"]),
    ("出行交通", "加油", ["加油"]),
    ("出行交通", "停车费", ["停车"]),
    ("出行交通", "高速费", ["高速", "通行费"]),
    ("医疗健康", "挂号", ["挂号"]),
    ("医疗健康", "药品", ["药", "药房", "买药"]),
    ("医疗健康", "门诊", ["医院", "门诊"]),
    ("购物消费", "数码", ["数码", "电脑", "键盘", "鼠标", "手机"]),
    ("购物消费", "服饰运动", ["服装", "衣服", "鞋", "运动"]),
    ("生活服务", "快递", ["快递", "邮费"]),
    ("生活服务", "超市", ["超市", "便利店"]),
    ("居家生活", "水费", ["水费"]),
    ("居家生活", "电费", ["电费"]),
    ("出行交通", "住宿", ["住宿", "房租", "酒店"]),
    ("出行交通", "维修", ["维修", "保养"]),
    ("休闲娱乐", "游戏", ["游戏"]),
    ("休闲娱乐", "KTV", ["KTV", "卡拉OK", "卡拉 OK"]),
    ("休闲娱乐", "旅游度假", ["旅游", "度假"]),
]


IMPORT_RULES_FILE = "import_rules.json"


class ImportRules:
    """Category keyword table, fallback pair, and source-account map for imports."""

    def __init__(
        self,
        category_keywords: list[tuple[str, str, list[str]]] | None = None,
        fallback: tuple[str, str] | None = None,
        source_accounts: dict[str, str] | None = None,
        errors: list[str] | None = None,
    ) -> None:
        self.category_keywords = list(category_keywords or DEFAULT_CATEGORY_KEYWORDS)
        self.fallback = fallback
        self.source_accounts = dict(source_accounts or DEFAULT_ACCOUNT_BY_SOURCE)
        self.errors = list(errors or [])


def load_import_rules(path: Path | str | None = None) -> ImportRules:
    keywords = list(DEFAULT_CATEGORY_KEYWORDS)
    fallback: tuple[str, str] | None = None
    source_accounts = dict(DEFAULT_ACCOUNT_BY_SOURCE)
    errors: list[str] = []
    if path is None:
        return ImportRules(keywords, fallback, source_accounts)
    config_path = Path(path)
    if not config_path.is_file():
        return ImportRules(keywords, fallback, source_accounts, [f"import rules not found: {config_path}"])
    try:
        data = json.loads(config_path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        return ImportRules(keywords, fallback, source_accounts, [f"import_rules: invalid JSON: {exc}"])
    if not isinstance(data, dict):
        return ImportRules(keywords, fallback, source_accounts, ["import_rules: config must be a JSON object"])
    if data.get("category_keywords") is not None:
        rows = data.get("category_keywords")
        if not isinstance(rows, list):
            errors.append("import_rules.category_keywords must be a list")
        else:
            cleaned: list[tuple[str, str, list[str]]] = []
            for index, row in enumerate(rows, 1):
                if not isinstance(row, dict):
                    errors.append(f"import_rules.category_keywords[{index}]: must be an object")
                    continue
                category = str(row.get("类别", "")).strip()
                subcategory = str(row.get("子类", "")).strip()
                words = row.get("关键词", [])
                if isinstance(words, str):
                    words = [part.strip() for part in re.split(r"[;；,，\s]+", words) if part.strip()]
                if not category or not subcategory or not isinstance(words, list) or not words:
                    errors.append(
                        f"import_rules.category_keywords[{index}]: needs 类别, 子类, and a 关键词 list"
                    )
                    continue
                cleaned.append((category, subcategory, [str(word) for word in words]))
            if cleaned and not data.get("append_defaults"):
                keywords = cleaned
            else:
                keywords = [*keywords, *cleaned]
    raw_fallback = data.get("fallback")
    if isinstance(raw_fallback, dict):
        category = str(raw_fallback.get("类别", "")).strip()
        subcategory = str(raw_fallback.get("子类", "")).strip()
        if category and subcategory:
            fallback = (category, subcategory)
        elif raw_fallback:
            errors.append("import_rules.fallback needs 类别 and 子类")
    elif raw_fallback is not None:
        errors.append("import_rules.fallback must be an object")
    raw_sources = data.get("source_accounts")
    if isinstance(raw_sources, dict):
        for source, account in raw_sources.items():
            source_key = str(source).strip().lower()
            account_name = str(account or "").strip()
            if source_key and account_name:
                source_accounts[source_key] = account_name
    elif raw_sources is not None:
        errors.append("import_rules.source_accounts must be an object")
    if errors:
        return ImportRules(keywords, fallback, source_accounts, errors)
    return ImportRules(keywords, fallback, source_accounts)


def read_csv(path: Path) -> list[dict[str, str]]:
    for encoding in ("utf-8-sig", "gb18030"):
        try:
            with path.open("r", encoding=encoding, newline="") as f:
                return list(csv.DictReader(f))
        except UnicodeDecodeError:
            continue
    raise SystemExit(f"Cannot decode CSV: {path}")


def column_index(cell_ref: str) -> int:
    letters = "".join(ch for ch in cell_ref if ch.isalpha())
    total = 0
    for ch in letters:
        total = total * 26 + ord(ch.upper()) - ord("A") + 1
    return total - 1


def read_shared_strings(zf: zipfile.ZipFile) -> list[str]:
    try:
        root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
    except KeyError:
        return []
    ns = {"x": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    values = []
    for si in root.findall("x:si", ns):
        parts = [node.text or "" for node in si.findall(".//x:t", ns)]
        values.append("".join(parts))
    return values


def read_xlsx(path: Path) -> list[dict[str, str]]:
    with zipfile.ZipFile(path) as zf:
        shared = read_shared_strings(zf)
        sheet_name = "xl/worksheets/sheet1.xml"
        root = ET.fromstring(zf.read(sheet_name))
    ns = {"x": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    table: list[list[str]] = []
    for row in root.findall(".//x:sheetData/x:row", ns):
        values: list[str] = []
        for cell in row.findall("x:c", ns):
            idx = column_index(cell.attrib.get("r", "A1"))
            while len(values) <= idx:
                values.append("")
            cell_type = cell.attrib.get("t")
            value_node = cell.find("x:v", ns)
            inline_node = cell.find("x:is/x:t", ns)
            if cell_type == "s" and value_node is not None:
                value = shared[int(value_node.text or "0")]
            elif inline_node is not None:
                value = inline_node.text or ""
            elif value_node is not None:
                value = value_node.text or ""
            else:
                value = ""
            values[idx] = value
        table.append(values)
    if not table:
        return []
    headers = [str(v).strip() for v in table[0]]
    return [dict(zip(headers, row + [""] * (len(headers) - len(row)))) for row in table[1:] if any(row)]


def load_rows(path: Path) -> list[dict[str, Any]]:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return read_csv(path)
    if suffix == ".xlsx":
        return read_xlsx(path)
    if suffix == ".json":
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            return data.get("records", data.get("transactions", []))
    raise SystemExit(f"Unsupported input file: {path}")


def get_value(row: dict[str, Any], field: str) -> str:
    lowered = {str(k).strip().lower(): v for k, v in row.items()}
    for alias in COLUMN_ALIASES[field]:
        if alias.lower() in lowered:
            value = lowered[alias.lower()]
            if value is not None and str(value).strip() != "":
                return str(value).strip()
    return ""


def parse_amount(value: str) -> Decimal | None:
    cleaned = value.strip().replace(",", "")
    cleaned = cleaned.replace("￥", "").replace("¥", "").replace("元", "")
    cleaned = cleaned.replace("+", "")
    if cleaned.startswith("(") and cleaned.endswith(")"):
        cleaned = "-" + cleaned[1:-1]
    match = re.search(r"-?\d+(?:\.\d+)?", cleaned)
    if not match:
        return None
    try:
        return Decimal(match.group(0))
    except InvalidOperation:
        return None


def normalize_time(value: str) -> str:
    value = value.strip().replace("/", "-")
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            parsed = datetime.strptime(value[:19], fmt)
            return parsed.strftime("%Y-%m-%d %H:%M") if " " in fmt else parsed.strftime("%Y-%m-%d")
        except ValueError:
            pass
    return value


def normalize_type(raw_type: str, amount: Decimal | None, text: str) -> str:
    stripped = raw_type.strip()
    if stripped in {"支出", "收入", "还款", "转账", "退款", "报销", "投资"}:
        return stripped
    raw = raw_type.lower()
    text_lower = text.lower()
    if "退款" in raw or (not raw and "退款" in text_lower):
        return "退款"
    if "还款" in raw:
        return "还款"
    if any(word in raw for word in ["转账", "提现", "不计收支"]):
        return "转账"
    if any(word in raw for word in ["收入", "收款", "入账", "入金"]):
        return "收入"
    if any(word in raw for word in ["支出", "付款", "消费", "扣款"]):
        return "支出"
    if "还款" in text_lower:
        return "还款"
    if any(word in text_lower for word in ["转账", "提现", "不计收支"]):
        return "转账"
    if any(word in text_lower for word in ["收入", "收款", "入账", "入金"]):
        return "收入"
    if any(word in text_lower for word in ["支出", "付款", "消费", "扣款"]):
        return "支出"
    if amount is not None and amount < 0:
        return "支出"
    return "收入"


def fallback_pair(config: SkillConfig, rules: ImportRules) -> tuple[str, str]:
    """The configured fallback, or the first category when the fallback is absent."""
    if rules.fallback and config.categories.accepts(*rules.fallback):
        return rules.fallback
    for category, subs in config.categories.map.items():
        for subcategory in sorted(subs):
            return category, subcategory
    return "未分类", "其他"


def classify(
    row: dict[str, Any],
    tx_type: str,
    text: str,
    account: str,
    config: SkillConfig,
    rules: ImportRules,
) -> tuple[str, str, bool]:
    raw_category = get_value(row, "类别")
    raw_subcategory = get_value(row, "子类")
    category, subcategory, _ = config.normalize_pair(raw_category, raw_subcategory)
    if config.categories.accepts(category, subcategory):
        return category, subcategory, False
    lowered = text.lower()
    if tx_type == "退款":
        for rule_category, rule_subcategory, keywords in rules.category_keywords:
            if rule_category in {"收入"}:
                continue
            if not config.categories.accepts(rule_category, rule_subcategory):
                continue
            if any(keyword.lower() in lowered for keyword in keywords):
                return rule_category, rule_subcategory, False
        if config.categories.accepts("退款", "退款"):
            return "退款", "退款", False
        return (*fallback_pair(config, rules), False)
    if tx_type == "报销":
        if config.categories.accepts("报销", "其他"):
            return "报销", "其他", False
        return (*fallback_pair(config, rules), False)
    if tx_type == "投资":
        if config.categories.accepts("投资", "其他"):
            return "投资", "其他", False
        return (*fallback_pair(config, rules), False)
    if tx_type == "收入":
        for rule_category, rule_subcategory, keywords in rules.category_keywords:
            if rule_category == "收入" and any(k.lower() in lowered for k in keywords):
                return rule_category, rule_subcategory, False
        if config.categories.accepts("收入", "其他"):
            return "收入", "其他", raw_category != "收入"
        return (*fallback_pair(config, rules), raw_category != "收入")
    if tx_type == "还款":
        credit_account = config.catalog.get(account, {}).get("credit", False)
        pair = ("还款", "信用卡还款") if credit_account else ("还款", "其他")
        if config.categories.accepts(*pair):
            return (*pair, False)
        return (*fallback_pair(config, rules), False)
    if tx_type == "转账":
        if config.categories.accepts("转账", "个人转账"):
            return "转账", "个人转账", False
        return (*fallback_pair(config, rules), False)
    for rule_category, rule_subcategory, keywords in rules.category_keywords:
        if rule_category == "收入" or not config.categories.accepts(rule_category, rule_subcategory):
            continue
        if any(k.lower() in lowered for k in keywords):
            return rule_category, rule_subcategory, False
    return (*fallback_pair(config, rules), True)


def configured_source_account(config: SkillConfig, rules: ImportRules, source: str) -> str:
    name = rules.source_accounts.get(source.lower(), "")
    if name:
        resolved = config.resolve_account(name)
        if resolved in config.catalog:
            return resolved
    for account, meta in config.catalog.items():
        if meta.get("kind") == "资产" and meta.get("include", "included") == "included":
            return account
    return ""


def normalize_account(
    raw_account: str,
    source: str,
    fallback: str | None,
    config: SkillConfig,
    rules: ImportRules,
) -> str:
    """Resolve an account through configured aliases, then by substring match."""
    if raw_account:
        resolved = config.resolve_account(raw_account)
        if resolved in config.catalog:
            return resolved
        lowered = raw_account.casefold()
        for account, meta in config.catalog.items():
            if account.casefold() in lowered:
                return account
            for alias in meta.get("aliases") or []:
                alias_name = alias.get("名称") if isinstance(alias, dict) else alias
                if str(alias_name).casefold() in lowered:
                    return account
    if fallback:
        resolved = config.resolve_account(fallback)
        if resolved in config.catalog:
            return resolved
    return configured_source_account(config, rules, source)


def normalize_record(
    row: dict[str, Any],
    source: str,
    fallback_account: str | None,
    config: SkillConfig,
    rules: ImportRules,
) -> dict[str, Any]:
    remark_parts = [get_value(row, "备注"), get_value(row, "note")]
    text = " ".join(part for part in remark_parts if part)
    raw_amount = get_value(row, "金额")
    amount = parse_amount(raw_amount)
    income_amount = parse_amount(get_value(row, "收入金额"))
    expense_amount = parse_amount(get_value(row, "支出金额"))
    if amount is None and income_amount is not None:
        amount = abs(income_amount)
    if amount is None and expense_amount is not None:
        amount = -abs(expense_amount)
    if amount is None:
        amount = Decimal("0")
    tx_type = normalize_type(get_value(row, "收支类型"), amount, text)
    if tx_type == "支出":
        signed_amount = -abs(amount)
    elif tx_type == "投资":
        signed_amount = amount
    else:
        signed_amount = abs(amount)
    base_currency = config.base_currency
    currency = get_value(row, "currency").upper() or base_currency
    original_amount = parse_amount(get_value(row, "original_amount"))
    fx_rate = parse_amount(get_value(row, "fx_rate"))
    cny_amount = parse_amount(get_value(row, "cny_amount"))
    if original_amount is not None:
        original_amount = -abs(original_amount) if tx_type == "支出" else abs(original_amount)
    if currency != base_currency and original_amount is not None and fx_rate is not None:
        signed_amount = (original_amount * fx_rate).quantize(Decimal("0.01"))
    elif cny_amount is not None and currency != base_currency:
        signed_amount = -abs(cny_amount) if tx_type == "支出" else abs(cny_amount)
    account = normalize_account(get_value(row, "账户"), source, fallback_account, config, rules)
    category, subcategory, pending = classify(row, tx_type, text, account, config, rules)
    note_parts = []
    existing_note = get_value(row, "note")
    if existing_note:
        note_parts.append(existing_note)
    if source != "auto":
        note_parts.append(f"source={source}")
    if pending:
        note_parts.append("待确认分类")
    record = {
        "时间": normalize_time(get_value(row, "时间")),
        "收支类型": tx_type,
        "金额": float(signed_amount) if signed_amount % 1 else int(signed_amount),
        "类别": category,
        "子类": subcategory,
        "账户": account,
        "备注": get_value(row, "备注") or text or "导入记录",
        "tags": get_value(row, "tags"),
        "note": "; ".join(note_parts),
    }
    for field in ("id", "refund_of", "reimburse_of", "报销状态", "预计报销", "item_id", "pairid", "target_account"):
        value = get_value(row, field)
        if value:
            record[field] = value
    if currency and currency != base_currency:
        record["currency"] = currency
        if original_amount is not None:
            record["original_amount"] = float(original_amount) if original_amount % 1 else int(original_amount)
        if fx_rate is not None:
            record["fx_rate"] = float(fx_rate) if fx_rate % 1 else int(fx_rate)
        record["cny_amount"] = record["金额"]
    elif get_value(row, "currency"):
        record["currency"] = base_currency
    return record


def month_of(record: dict[str, Any]) -> str:
    return str(record["时间"])[:7]


def write_json(
    path: Path,
    records: list[dict[str, Any]],
    month: str | None = None,
    *,
    overwrite: bool = False,
) -> None:
    """Write one ledger shard. Existing files are refused unless overwrite is set."""
    if path.exists() and not overwrite:
        raise SystemExit(
            f"Refusing to overwrite existing ledger file: {path}. "
            "No further files will be written. Back up the ledger and pass --overwrite to replace it."
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"schema_version": SCHEMA_VERSION, "month": month or "mixed", "records": records}
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def existing_ledger_paths(paths: list[Path]) -> list[Path]:
    return [path for path in paths if path.exists()]


def refuse_existing_targets(paths: list[Path], overwrite: bool) -> None:
    """Abort the whole batch before any write when a target already exists."""
    if overwrite:
        return
    existing = existing_ledger_paths(paths)
    if not existing:
        return
    print(
        "Refusing to overwrite existing ledger files. No files were written.\n"
        "Re-import replaces each target file and drops records that are not in the new bill.\n"
        "Back up the ledger, then re-run with --overwrite only to replace these files:",
        file=sys.stderr,
    )
    for path in existing:
        print(f"- {path}", file=sys.stderr)
    raise SystemExit(1)


def output_path_for(args: argparse.Namespace, records: list[dict[str, Any]]) -> Path:
    if args.output:
        return Path(args.output)
    months = sorted({month_of(record) for record in records})
    if len(months) == 1:
        return Path("data") / f"{months[0]}.json"
    return Path("data") / "imported.json"


def record_shard_key(record: dict[str, Any], mode: str) -> str:
    text = str(record.get("时间", ""))
    if mode == "day":
        return text[:10]
    return text[:7]


def shard_output_path(out_dir: Path, key: str, year_dirs: bool, mode: str) -> Path:
    # The filename itself is the shard key so os.path.basename can recover it.
    filename = f"{key}.json"
    if mode == "day":
        if year_dirs:
            return out_dir / key[:4] / key[:7] / filename
        return out_dir / filename
    if year_dirs:
        return out_dir / key[:4] / filename
    return out_dir / filename


def monthly_output_path(out_dir: Path, month: str, year_dirs: bool) -> Path:
    return shard_output_path(out_dir, month, year_dirs, "month")


def main() -> int:
    parser = argparse.ArgumentParser(description="Import CSV/XLSX bills into standard ledger JSON.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", "-o", help="Output file or directory. Default: data/<month>.json or data/imported.json")
    parser.add_argument("--source", default="auto", choices=["auto", "standard", "alipay", "wechat", "meituan", "bank"])
    parser.add_argument("--account", help="Fallback account when the source file has no account column.")
    parser.add_argument("--accounts", type=Path, help="Account config. Default: data/accounts.json when present.")
    parser.add_argument("--categories", type=Path, help="Category config. Default: data/categories.json when present.")
    parser.add_argument("--settings", type=Path, help="Workspace settings. Default: data/settings.json when present.")
    parser.add_argument("--import-rules", type=Path, help="Import keyword rules. Default: data/import_rules.json when present.")
    parser.add_argument("--month", help="Only import records whose 时间 starts with YYYY-MM.")
    parser.add_argument("--split-by-month", action="store_true", help="Write one JSON file per month.")
    parser.add_argument("--shard", choices=["day", "month"], help="Write one JSON file per day or month. Keys use the file basename.")
    parser.add_argument("--year-dirs", action="store_true", help="Nest shard files under YYYY/ (and YYYY-MM/ for days).")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help=(
            "Replace existing ledger files. Without this flag, any existing target aborts the "
            "whole batch and nothing is written. Back up the ledger first; records missing from "
            "the new bill are dropped."
        ),
    )
    args = parser.parse_args()

    if args.split_by_month and args.shard == "day":
        raise SystemExit("--split-by-month cannot be combined with --shard day")
    if args.split_by_month and args.shard is None:
        args.shard = "month"
    if args.year_dirs and not args.shard:
        raise SystemExit("--year-dirs requires --split-by-month or --shard")
    config = load_skill_config(
        [args.input, args.output if args.output else Path("data")],
        args.accounts,
        args.categories,
        args.settings,
    )
    if config.errors:
        raise SystemExit("\n".join(config.errors))
    rules_path = (
        args.import_rules
        if args.import_rules is not None
        else find_config_path(IMPORT_RULES_FILE, [args.input, args.output if args.output else Path("data")], None)
    )
    rules = load_import_rules(rules_path)
    if rules.errors:
        raise SystemExit("\n".join(rules.errors))
    if args.account:
        resolved_account = config.resolve_account(args.account)
        if resolved_account not in config.catalog:
            raise SystemExit(
                f"Invalid fallback account: {args.account}. Add it to data/accounts.json or pass a known account."
            )
        args.account = resolved_account
    rows = load_rows(args.input)
    records = [normalize_record(row, args.source, args.account, config, rules) for row in rows]
    if args.month:
        records = [record for record in records if str(record["时间"]).startswith(args.month)]
    errors, warnings = validate_records(
        records,
        catalog=config.catalog,
        categories=config.categories,
        base_currency=config.base_currency,
    )
    if errors:
        print("INVALID IMPORT", file=sys.stderr)
        for error in errors[:50]:
            print(f"- {error}", file=sys.stderr)
        return 1
    planned: list[tuple[Path, list[dict[str, Any]], str | None, str | None]] = []
    if args.shard:
        out_dir = Path(args.output or "data")
        grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for record in records:
            grouped[record_shard_key(record, args.shard)].append(record)
        for key, shard_records in sorted(grouped.items()):
            out = shard_output_path(out_dir, key, args.year_dirs, args.shard)
            month = key if args.shard == "month" else key[:7]
            planned.append((out, shard_records, month, key))
    else:
        out = output_path_for(args, records)
        month = args.month or (month_of(records[0]) if records else None)
        planned.append((out, records, month, None))

    refuse_existing_targets([path for path, _records, _month, _key in planned], args.overwrite)
    for out, shard_records, month, key in planned:
        write_json(out, shard_records, month, overwrite=args.overwrite)
        if key is None:
            print(f"wrote {out} records={len(shard_records)} warnings={len(warnings)}")
            continue
        written_key = shard_key(out, args.shard)
        if written_key != key:
            raise SystemExit(f"shard key mismatch for {out}: basename key {written_key!r} != {key!r}")
        print(f"wrote {out} records={len(shard_records)} shard={written_key} warnings={len(warnings)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
