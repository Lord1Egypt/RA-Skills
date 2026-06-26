#!/usr/bin/env python3
"""
data_enrichment.py

Structured extraction helpers for transform_doc_to_data.py.
"""

from __future__ import annotations

import csv
import html
import json
import re
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

from utils import detect_title, ensure_dir, iter_blocks, normalize_whitespace


KEY_PATTERNS: list[tuple[set[str], str, str | None]] = [
    ({"invoice number", "invoice no", "invoice #", "invoice id", "发票号", "发票号码", "票据号码"}, "invoice_number", "invoice_number"),
    ({"invoice code", "发票代码", "票据代码"}, "invoice_code", "code"),
    ({"check code", "校验码", "检验码", "検驗码"}, "check_code", "code"),
    ({"machine number", "machine no", "机器编号"}, "machine_number", "code"),
    ({"purchase order", "po number", "po #", "采购单号"}, "purchase_order_number", "code"),
    ({"invoice date", "bill date", "date", "日期", "开票日期"}, "invoice_date", "date"),
    ({"due date", "截止日期", "到期日"}, "due_date", "date"),
    ({"amount due", "total due", "due amount", "应付金额"}, "amount_due", "amount"),
    ({"total amount", "grand total", "total", "合计", "总金额", "价税合计", "金额合计"}, "total_amount", "amount"),
    ({"subtotal", "小计"}, "subtotal", "amount"),
    ({"tax", "vat", "税额"}, "tax_amount", "amount"),
    ({"email", "e-mail", "电子邮箱", "邮箱"}, "email", "email"),
    ({"phone", "mobile", "tel", "telephone", "联系电话", "电话"}, "phone", "phone"),
    ({"vendor", "supplier", "seller", "from", "卖方", "供应商", "销售方", "收款单位", "收款单位 章"}, "vendor_name", "organization"),
    ({"customer", "bill to", "ship to", "buyer", "客户", "买方", "购买方", "购货方", "交款人", "付款方", "患者"}, "customer_name", "organization"),
    ({"buyer tax id", "buyer taxpayer id", "购买方税号", "购买方统一社会信用代码", "购买方纳税人识别号"}, "buyer_tax_id", "code"),
    ({"seller tax id", "seller taxpayer id", "销售方税号", "销售方统一社会信用代码", "销售方纳税人识别号"}, "seller_tax_id", "code"),
    ({"payer tax id", "payer identifier", "交款人统一社会信用代码"}, "payer_tax_id", "code"),
    ({"insurance number", "医保编号"}, "insurance_number", "code"),
    ({"insurance type", "医保类型"}, "insurance_type", "text"),
    ({"outpatient number", "门诊号"}, "outpatient_number", "code"),
    ({"visit date", "就诊日期"}, "visit_date", "date"),
    ({"medical institution type", "医疗机构类型"}, "medical_institution_type", "text"),
    ({"business serial number", "业务流水号"}, "business_serial_number", "code"),
    ({"center serial number", "中心流水号"}, "center_serial_number", "code"),
    ({"insurance pool payment", "医保统筹基金支付"}, "insurance_pool_payment", "amount"),
    ({"personal account payment", "个人账户支付"}, "personal_account_payment", "amount"),
    ({"mutual aid payment", "共济支付"}, "mutual_aid_payment", "amount"),
    ({"additional fund payment", "附加基金支付"}, "additional_fund_payment", "amount"),
    ({"other payment", "其他支付"}, "other_payment", "amount"),
    ({"cash payment", "个人现金支付"}, "cash_payment", "amount"),
    ({"personal self pay", "个人自付"}, "personal_self_pay", "amount"),
    ({"personal self funded", "个人自费"}, "personal_self_funded", "amount"),
    ({"personal burden", "个人自负", "分类自负"}, "personal_burden", "amount"),
    ({"insurance account balance", "医保当年账户余额"}, "insurance_account_balance", "amount"),
    ({"gender", "性别"}, "gender", "text"),
    ({"notes", "备注", "其他信息"}, "notes", "text"),
]

INVOICE_TOKENS = (
    "发票",
    "票据",
    "收费票据",
    "invoice",
    "receipt",
)

MEDICAL_TOKENS = (
    "医疗",
    "门诊",
    "医保",
    "药费",
    "检查费",
    "医学院附属",
    "收费票据",
)

RESTAURANT_TOKENS = ("餐饮", "饭店", "菜品", "餐费", "就餐", "桌号")
RETAIL_TOKENS = ("商品", "超市", "日用品", "零售", "规格", "品名")
TRANSPORT_TOKENS = ("车票", "出租车", "交通", "机票", "高铁", "铁路")
HOTEL_TOKENS = ("酒店", "住宿", "房费")
UTILITY_TOKENS = ("电费", "水费", "燃气", "物业", "话费")

HTML_BLOCK_PREFIXES = ("<div", "<img", "<table", "<tr", "<td", "<tbody", "<thead")

INLINE_KEY_ALIASES: dict[str, str] = {
    "业务流水号": "business_serial_number",
    "中心流水号": "center_serial_number",
    "医疗机构类型": "medical_institution_type",
    "医保统筹基金支付": "insurance_pool_payment",
    "个人账户支付": "personal_account_payment",
    "共济支付": "mutual_aid_payment",
    "附加基金支付": "additional_fund_payment",
    "其他支付": "other_payment",
    "个人现金支付": "cash_payment",
    "个人自付": "personal_self_pay",
    "个人自费": "personal_self_funded",
    "个人自负": "personal_burden",
    "分类自负": "personal_burden",
    "医保编号": "insurance_number",
    "医保类型": "insurance_type",
    "医保当年账户余额": "insurance_account_balance",
    "门诊号": "outpatient_number",
    "就诊日期": "visit_date",
    "性别": "gender",
    "备注": "notes",
    "收款单位(章)": "vendor_name",
    "收款单位": "vendor_name",
    "交款人": "customer_name",
    "交款人统一社会信用代码": "payer_tax_id",
    "票据代码": "invoice_code",
    "票据号码": "invoice_number",
    "校验码": "check_code",
    "检验码": "check_code",
    "検驗码": "check_code",
    "开票日期": "invoice_date",
    "购买方税号": "buyer_tax_id",
    "销售方税号": "seller_tax_id",
}

AMOUNT_KEYS = {
    "amount_due",
    "total_amount",
    "subtotal",
    "tax_amount",
    "insurance_pool_payment",
    "personal_account_payment",
    "mutual_aid_payment",
    "additional_fund_payment",
    "other_payment",
    "cash_payment",
    "personal_self_pay",
    "personal_self_funded",
    "personal_burden",
    "insurance_account_balance",
}

TEXT_REPLACEMENTS = {
    "項目": "项目",
    "検驗": "检验",
}


@dataclass
class EmbeddedTable:
    table_id: str
    page_id: str
    source_block_ids: list[str]
    source_text: str
    headers: list[str]
    rows: list[list[str]]
    table_kind: str


def normalize_email(value: str) -> str:
    return normalize_whitespace(value).lower()


def normalize_phone(value: str) -> str:
    return re.sub(r"[^\d+]", "", value)


def normalize_amount(value: str) -> str:
    return value.replace(",", "").strip()


def normalize_date(value: str) -> str:
    return normalize_whitespace(value)


def cleanup_ocr_text(value: str) -> str:
    text = normalize_whitespace(value)
    for src, dst in TEXT_REPLACEMENTS.items():
        text = text.replace(src, dst)
    return text


def normalize_amount_info(value: str) -> dict[str, Any]:
    clean = normalize_whitespace(value)
    currency = None
    if "$" in clean:
        currency = "USD"
    elif "\xa5" in clean or "\uffe5" in clean:
        currency = "CNY"
    elif "\u20ac" in clean:
        currency = "EUR"
    elif "\xa3" in clean:
        currency = "GBP"

    match = re.search(r"[-+]?\d[\d,]*(?:\.\d+)?", clean)
    if not match:
        return {"raw": value, "normalized": clean, "currency": currency, "amount_decimal": None}

    numeric = match.group(0).replace(",", "")
    try:
        decimal_value = str(Decimal(numeric).normalize())
    except InvalidOperation:
        decimal_value = numeric

    return {
        "raw": value,
        "normalized": numeric,
        "currency": currency,
        "amount_decimal": decimal_value,
    }


def normalize_date_info(value: str) -> dict[str, Any]:
    clean = normalize_whitespace(value)
    candidates = [
        (clean, ["%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d", "%m/%d/%Y", "%d/%m/%Y", "%Y%m%d"]),
        (clean.replace("年", "-").replace("月", "-").replace("日", ""), ["%Y-%m-%d"]),
    ]
    iso_date = None
    for candidate, patterns in candidates:
        candidate = candidate.strip()
        for pattern in patterns:
            try:
                iso_date = datetime.strptime(candidate, pattern).date().isoformat()
                break
            except ValueError:
                continue
        if iso_date:
            break
    return {"raw": value, "normalized": clean, "iso_date": iso_date}


def normalize_phone_info(value: str) -> dict[str, Any]:
    normalized = normalize_phone(value)
    return {
        "raw": value,
        "normalized": normalized,
        "digit_count": len(re.sub(r"\D", "", normalized)),
    }


def normalize_email_info(value: str) -> dict[str, Any]:
    normalized = normalize_email(value)
    return {"raw": value, "normalized": normalized}


def simplify_key(value: str) -> str:
    text = cleanup_ocr_text(value).strip().lower()
    text = text.replace("：", ":")
    text = re.sub(r"[#:/()（）]+", " ", text)
    text = re.sub(r"[_\-]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def alias_match(simple: str, alias: str) -> bool:
    return simple == alias or simple.startswith(alias + " ") or simple.endswith(" " + alias) or f" {alias} " in f" {simple} "


def canonicalize_key(key: str) -> tuple[str, str | None]:
    simple = simplify_key(key)
    for aliases, canonical, entity_type in KEY_PATTERNS:
        if any(alias_match(simple, alias) for alias in aliases):
            return canonical, entity_type
    return re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "_", simple).strip("_") or "field", None


def build_normalized_value(value_type: str, value: str) -> tuple[str, dict[str, Any]]:
    if value_type == "email":
        info = normalize_email_info(value)
        return info["normalized"], info
    if value_type == "phone":
        info = normalize_phone_info(value)
        return info["normalized"], info
    if value_type == "amount":
        info = normalize_amount_info(value)
        return str(info["normalized"]), info
    if value_type == "date":
        info = normalize_date_info(value)
        return str(info.get("iso_date") or info["normalized"]), info
    return normalize_whitespace(value), {"raw": value, "normalized": normalize_whitespace(value)}


def infer_value_type(key: str | None, value: str, hinted_entity_type: str | None = None) -> str:
    key_hint = simplify_key(key or "")
    clean = normalize_whitespace(value)
    if hinted_entity_type in {"email", "phone", "amount", "date", "invoice_number", "code", "organization", "text"}:
        return hinted_entity_type if hinted_entity_type != "organization" else "text"
    if any(token in key_hint for token in ["code", "number", "serial", "编号", "代码", "票据", "发票", "流水号"]):
        return "code"
    if any(token in key_hint for token in ["amount", "price", "cost", "total", "tax", "due", "金额", "合计", "价税", "支付"]):
        return "amount"
    if any(token in key_hint for token in ["date", "日期", "就诊"]) or re.search(r"\d{4}[-/.]?\d{1,2}[-/.]?\d{1,2}", clean):
        return "date"
    if re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", clean):
        return "email"
    if re.search(r"(?:\+?\d[\d(). -]{6,}\d)", clean) and not re.search(r"[A-Za-z]{2}\d+", clean):
        return "phone"
    return "text"


def strip_tags(text: str) -> str:
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"</(?:td|th)>", "\t", text, flags=re.IGNORECASE)
    text = re.sub(r"</tr>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", "", text)
    return normalize_whitespace(html.unescape(text))


def is_html_like(text: str) -> bool:
    clean = text.strip().lower()
    return clean.startswith(HTML_BLOCK_PREFIXES)


def parse_kv_pair_from_text(text: str) -> tuple[str, str] | None:
    clean = cleanup_ocr_text(text)
    if not clean or is_html_like(clean):
        return None
    patterns = [
        r"^(.{1,80}?)\s*[:：]\s*(.+?)$",
        r"^(.{1,80}?)\s*[-–—]\s+(.+?)$",
    ]
    for pattern in patterns:
        match = re.match(pattern, clean)
        if match:
            return match.group(1).strip(), match.group(2).strip()
    return None


def extract_entities(document: dict[str, Any]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for item in document.get("entities", []):
        entity_type = item.get("type")
        value = item.get("value", "")
        normalized_value = item.get("normalized_value") or normalize_whitespace(value)
        results.append(
            {
                "entity_id": item.get("entity_id"),
                "type": entity_type,
                "value": value,
                "normalized_value": normalized_value,
                "page_id": item.get("page_id"),
                "source_block_ids": item.get("source_block_ids", []),
                "confidence": item.get("confidence"),
                "source": "parser",
            }
        )
    return results


def extract_base_kv_pairs(document: dict[str, Any]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    index = 0
    for row in iter_blocks(document):
        page_id = row["page_id"]
        block = row["block"]
        block_id = block.get("block_id")
        text = block.get("text") or ""
        pair = parse_kv_pair_from_text(text)
        if not pair:
            continue
        key, value = pair
        canonical_key, key_entity_type = canonicalize_key(key)
        value_type = infer_value_type(key, value, key_entity_type)
        normalized_value, normalized = build_normalized_value(value_type, value)
        index += 1
        results.append(
            {
                "kv_id": f"kv_{index}",
                "key": key,
                "canonical_key": canonical_key,
                "value": value,
                "value_type": value_type,
                "normalized_value": normalized_value,
                "normalized": normalized,
                "page_id": page_id,
                "source_block_ids": [block_id] if block_id else [],
                "confidence": block.get("confidence"),
                "source_text": text,
                "source": "text_pattern",
            }
        )
    return results


def find_first_amount(text: str) -> str | None:
    match = re.search(r"[-+]?\d[\d,]*\.\d{2}", text)
    if not match:
        match = re.search(r"[-+]?\d[\d,]*(?:\.\d+)?", text)
    return match.group(0).replace(",", "") if match else None


def parse_quantity_unit(text: str) -> tuple[str | None, str | None]:
    clean = cleanup_ocr_text(text)
    if not clean:
        return None, None
    match = re.match(r"^(\d+(?:\.\d+)?)\s*(\S+)?$", clean)
    if not match:
        return None, clean
    return match.group(1), match.group(2)


def parse_html_table(html_text: str) -> list[list[str]]:
    rows: list[list[str]] = []
    tr_matches = re.findall(r"<tr[^>]*>(.*?)</tr>", html_text, flags=re.IGNORECASE | re.DOTALL)
    for tr in tr_matches:
        cells = re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", tr, flags=re.IGNORECASE | re.DOTALL)
        parsed_cells = [strip_tags(cell) for cell in cells]
        if any(parsed_cells):
            rows.append(parsed_cells)
    return rows


def normalize_compact_label(text: str) -> str:
    return cleanup_ocr_text(text).replace(" ", "")


def dedupe_repeated_text(text: str) -> str:
    clean = cleanup_ocr_text(text)
    if len(clean) >= 4 and len(clean) % 2 == 0:
        half = len(clean) // 2
        if clean[:half] == clean[half:]:
            return clean[:half]
    return clean


def detect_table_kind(rows: list[list[str]], source_text: str) -> str:
    joined = " ".join(" ".join(row) for row in rows) + " " + source_text
    if any(token in joined for token in MEDICAL_TOKENS):
        return "medical_invoice_table"
    if any(token in joined for token in RESTAURANT_TOKENS):
        return "restaurant_invoice_table"
    if any(token in joined for token in RETAIL_TOKENS):
        return "retail_invoice_table"
    return "generic_table"


def extract_embedded_tables(document: dict[str, Any]) -> list[EmbeddedTable]:
    tables: list[EmbeddedTable] = []
    table_index = 0
    for row in iter_blocks(document):
        block = row["block"]
        text = block.get("text") or ""
        if "<table" not in text.lower():
            continue
        parsed_rows = parse_html_table(text)
        if not parsed_rows:
            continue
        table_index += 1
        headers = parsed_rows[0]
        rows = parsed_rows[1:]
        tables.append(
            EmbeddedTable(
                table_id=f"embedded_table_{table_index}",
                page_id=row["page_id"],
                source_block_ids=[block.get("block_id")] if block.get("block_id") else [],
                source_text=text,
                headers=headers,
                rows=rows,
                table_kind=detect_table_kind(parsed_rows, text),
            )
        )
    return tables


def extract_known_inline_pairs(text: str, alias_map: dict[str, str]) -> list[tuple[str, str, str]]:
    clean = normalize_whitespace(text)
    if not clean:
        return []
    aliases = sorted(alias_map, key=len, reverse=True)
    pattern = re.compile(r"(" + "|".join(re.escape(alias) for alias in aliases) + r")[:：]")
    matches = list(pattern.finditer(clean))
    results: list[tuple[str, str, str]] = []
    for idx, match in enumerate(matches):
        raw_key = match.group(1)
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(clean)
        value = clean[start:end].strip(" ;；，,。")
        if value:
            results.append((raw_key, alias_map[raw_key], value))
    return results


def parse_party_cell(cell_text: str) -> dict[str, str]:
    clean = cleanup_ocr_text(cell_text)
    result: dict[str, str] = {}
    name_match = re.search(r"名称[:：]\s*(.+?)(?:统一社会信用代码/纳税人识别号|纳税人识别号|$)", clean)
    tax_match = re.search(r"(?:统一社会信用代码/纳税人识别号|纳税人识别号)[:：]?\s*([0-9A-Z]{10,20})", clean)
    if name_match:
        result["name"] = name_match.group(1).strip(" ：:;；，,")
    if tax_match:
        result["tax_id"] = tax_match.group(1).strip()
    return result


def make_kv_item(
    index: int,
    key: str,
    canonical_key: str,
    value: str,
    page_id: str,
    source_block_ids: list[str],
    confidence: float | None,
    source_text: str,
    source: str,
) -> dict[str, Any]:
    hinted_entity_type = next((entity_type for aliases, canonical, entity_type in KEY_PATTERNS if canonical == canonical_key), None)
    value_type = infer_value_type(key, value, hinted_entity_type)
    normalized_value, normalized = build_normalized_value(value_type, value)
    return {
        "kv_id": f"kv_{index}",
        "key": key,
        "canonical_key": canonical_key,
        "value": value,
        "value_type": value_type,
        "normalized_value": normalized_value,
        "normalized": normalized,
        "page_id": page_id,
        "source_block_ids": source_block_ids,
        "confidence": confidence,
        "source_text": source_text,
        "source": source,
    }


def derive_table_kv_pairs(embedded_tables: list[EmbeddedTable], start_index: int) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    index = start_index
    for table in embedded_tables:
        if table.table_kind == "restaurant_invoice_table":
            first_row = [cleanup_ocr_text(cell) for cell in table.headers]
            if len(first_row) >= 4 and "购买方信息" in normalize_compact_label(first_row[0]) and "销售方信息" in normalize_compact_label(first_row[2]):
                buyer = parse_party_cell(first_row[1])
                seller = parse_party_cell(first_row[3])
                for raw_key, canonical_key, value in [
                    ("购买方名称", "customer_name", buyer.get("name")),
                    ("购买方税号", "buyer_tax_id", buyer.get("tax_id")),
                    ("销售方名称", "vendor_name", seller.get("name")),
                    ("销售方税号", "seller_tax_id", seller.get("tax_id")),
                ]:
                    if not value:
                        continue
                    index += 1
                    results.append(
                        make_kv_item(
                            index=index,
                            key=raw_key,
                            canonical_key=canonical_key,
                            value=value,
                            page_id=table.page_id,
                            source_block_ids=table.source_block_ids,
                            confidence=None,
                            source_text=" | ".join(first_row),
                            source="table_party_inference",
                        )
                    )
        all_rows = [table.headers] + table.rows
        for row in all_rows:
            cleaned_row = [cleanup_ocr_text(cell) for cell in row]
            joined = " ".join(cell for cell in cleaned_row if cell)
            if not joined:
                continue
            for raw_key, canonical_key, value in extract_known_inline_pairs(joined, INLINE_KEY_ALIASES):
                index += 1
                results.append(
                    make_kv_item(
                        index=index,
                        key=raw_key,
                        canonical_key=canonical_key,
                        value=value,
                        page_id=table.page_id,
                        source_block_ids=table.source_block_ids,
                        confidence=None,
                        source_text=joined,
                        source="table_inline_inference",
                    )
                )
            if any(token in joined for token in ["金额合计", "价税合计", "小写"]):
                amount = find_first_amount(joined)
                if amount:
                    index += 1
                    results.append(
                        make_kv_item(
                            index=index,
                            key="金额合计",
                            canonical_key="total_amount",
                            value=amount,
                            page_id=table.page_id,
                            source_block_ids=table.source_block_ids,
                            confidence=None,
                            source_text=joined,
                            source="table_total_inference",
                        )
                    )
            compact_first = normalize_compact_label(cleaned_row[0]) if cleaned_row else ""
            if compact_first == "合计" and len(cleaned_row) >= 3:
                summary_values = [
                    ("合计金额", "subtotal", cleaned_row[1]),
                    ("合计税额", "tax_amount", cleaned_row[2]),
                ]
                for raw_key, canonical_key, raw_value in summary_values:
                    amount = find_first_amount(raw_value or "")
                    if not amount:
                        continue
                    index += 1
                    results.append(
                        make_kv_item(
                            index=index,
                            key=raw_key,
                            canonical_key=canonical_key,
                            value=amount,
                            page_id=table.page_id,
                            source_block_ids=table.source_block_ids,
                            confidence=None,
                            source_text=joined,
                            source="table_summary_inference",
                        )
                    )
    return results


def dedupe_kv_pairs(kv_pairs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    deduped: list[dict[str, Any]] = []
    seen: set[tuple[Any, ...]] = set()
    for item in kv_pairs:
        key = (
            item.get("canonical_key"),
            item.get("normalized_value"),
            item.get("page_id"),
            tuple(item.get("source_block_ids", [])),
        )
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)
    for idx, item in enumerate(deduped, start=1):
        item["kv_id"] = f"kv_{idx}"
    return deduped


def extract_kv_pairs(document: dict[str, Any]) -> tuple[list[dict[str, Any]], list[EmbeddedTable]]:
    base = extract_base_kv_pairs(document)
    embedded_tables = extract_embedded_tables(document)
    derived = derive_table_kv_pairs(embedded_tables, len(base))
    return dedupe_kv_pairs(base + derived), embedded_tables


def infer_entities_from_kv_pairs(kv_pairs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    inferred: list[dict[str, Any]] = []
    for idx, item in enumerate(kv_pairs, start=1):
        canonical_key = item.get("canonical_key")
        value_type = item.get("value_type")
        entity_type = None
        if canonical_key in {"invoice_number", "invoice_code"}:
            entity_type = "invoice_number"
        elif canonical_key in {"invoice_date", "due_date", "visit_date"} or value_type == "date":
            entity_type = "date"
        elif canonical_key in AMOUNT_KEYS or value_type == "amount":
            entity_type = "amount"
        elif canonical_key == "email" or value_type == "email":
            entity_type = "email"
        elif canonical_key == "phone" or value_type == "phone":
            entity_type = "phone"
        elif canonical_key in {"vendor_name", "customer_name"}:
            entity_type = "organization"
        if not entity_type:
            continue
        inferred.append(
            {
                "entity_id": f"inferred_e{idx}",
                "type": entity_type,
                "value": item.get("value"),
                "normalized_value": item.get("normalized_value"),
                "page_id": item.get("page_id"),
                "source_block_ids": item.get("source_block_ids", []),
                "confidence": item.get("confidence"),
                "source": "kv_inference",
            }
        )
    return inferred


def infer_entities_from_text(document: dict[str, Any], existing_entities: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen = {
        (item.get("type"), item.get("normalized_value"), item.get("page_id"), tuple(item.get("source_block_ids", [])))
        for item in existing_entities
    }
    inferred: list[dict[str, Any]] = []
    index = 0
    for row in iter_blocks(document):
        page_id = row["page_id"]
        block = row["block"]
        block_id = block.get("block_id")
        text = block.get("text") or ""
        if is_html_like(text):
            continue
        for match in re.finditer(r"[\w.+-]+@[\w-]+\.[\w.-]+", text):
            value = match.group(0)
            normalized_value, _ = build_normalized_value("email", value)
            key = ("email", normalized_value, page_id, (block_id,) if block_id else ())
            if key in seen:
                continue
            seen.add(key)
            index += 1
            inferred.append(
                {
                    "entity_id": f"regex_e{index}",
                    "type": "email",
                    "value": value,
                    "normalized_value": normalized_value,
                    "page_id": page_id,
                    "source_block_ids": [block_id] if block_id else [],
                    "confidence": block.get("confidence"),
                    "source": "regex_inference",
                }
            )
    return inferred


def combine_entities(document: dict[str, Any], kv_pairs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    entities = extract_entities(document)
    entities.extend(infer_entities_from_kv_pairs(kv_pairs))
    entities.extend(infer_entities_from_text(document, entities))
    deduped: list[dict[str, Any]] = []
    seen: set[tuple[Any, ...]] = set()
    for item in entities:
        key = (
            item.get("type"),
            item.get("normalized_value"),
            item.get("page_id"),
            tuple(item.get("source_block_ids", [])),
        )
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)
    return deduped


def export_tables(
    document: dict[str, Any],
    embedded_tables: list[EmbeddedTable],
    out_dir: Path,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    tables_dir = out_dir / "tables"
    ensure_dir(tables_dir)
    combined_csv_path = out_dir / "tables.csv"
    table_index: list[dict[str, Any]] = []
    trace_rows: list[dict[str, Any]] = []
    with combined_csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["table_id", "page_id", "row_index", "row_json"])
        combined_tables: list[dict[str, Any]] = list(document.get("tables", []))
        combined_tables.extend(
            {
                "table_id": table.table_id,
                "page_id": table.page_id,
                "headers": table.headers,
                "rows": table.rows,
                "caption": table.table_kind,
                "source_block_ids": table.source_block_ids,
            }
            for table in embedded_tables
        )
        for table in combined_tables:
            table_id = table.get("table_id") or f"table_{len(table_index) + 1}"
            page_id = table.get("page_id")
            headers = table.get("headers", [])
            rows = table.get("rows", [])
            source_block_ids = table.get("source_block_ids", [])
            per_table_csv = tables_dir / f"{table_id}.csv"
            with per_table_csv.open("w", newline="", encoding="utf-8") as tf:
                table_writer = csv.writer(tf)
                if headers:
                    table_writer.writerow(headers)
                for row_idx, row in enumerate(rows, start=1):
                    table_writer.writerow(row)
                    writer.writerow([table_id, page_id, row_idx, json.dumps(row, ensure_ascii=False)])
                    trace_rows.append(
                        {
                            "generated_unit_id": f"table.{table_id}.row.{row_idx}",
                            "generated_text": json.dumps(row, ensure_ascii=False),
                            "source_refs": [{"page_id": page_id, "block_id": block_id} for block_id in source_block_ids],
                            "assumption": None,
                        }
                    )
            table_index.append(
                {
                    "table_id": table_id,
                    "page_id": page_id,
                    "caption": table.get("caption"),
                    "headers": headers,
                    "row_count": len(rows),
                    "csv_path": f"tables/{table_id}.csv",
                    "source_block_ids": source_block_ids,
                }
            )
    return table_index, trace_rows


def collect_document_text(document: dict[str, Any]) -> str:
    chunks: list[str] = []
    for row in iter_blocks(document):
        text = row["block"].get("text") or ""
        if "<table" in text.lower():
            chunks.append(strip_tags(text))
        elif not is_html_like(text):
            chunks.append(text)
    return "\n".join(chunk for chunk in chunks if chunk)


def summarize_document(document: dict[str, Any]) -> dict[str, Any]:
    block_counts: dict[str, int] = {}
    for row in iter_blocks(document):
        block_type = row["block"].get("type") or "unknown"
        block_counts[block_type] = block_counts.get(block_type, 0) + 1
    return {
        "document_id": document.get("document_id"),
        "source": document.get("source", {}),
        "parse_info": document.get("parse_info", {}),
        "title": detect_title(document),
        "page_count": len(document.get("pages", [])),
        "block_type_counts": block_counts,
        "table_count": len(document.get("tables", [])),
        "figure_count": len(document.get("figures", [])),
        "entity_count": len(document.get("entities", [])),
    }


def classify_document(
    document: dict[str, Any],
    kv_pairs: list[dict[str, Any]],
    table_index: list[dict[str, Any]],
    embedded_tables: list[EmbeddedTable],
) -> dict[str, Any]:
    title = detect_title(document)
    text = title + "\n" + collect_document_text(document)
    lower = text.lower()
    evidence: list[str] = []
    canonical_keys = {str(item.get("canonical_key")) for item in kv_pairs}
    if any(token in text for token in INVOICE_TOKENS) or {"invoice_number", "invoice_code"} & canonical_keys:
        category = "invoice"
        evidence.append("invoice keywords or invoice identifiers found")
    elif embedded_tables and len(kv_pairs) <= 2:
        category = "data_table"
        evidence.append("tabular content dominates document")
    elif embedded_tables and any(token in lower for token in ("report", "summary", "analysis")):
        category = "report"
        evidence.append("report-like title with tables")
    elif len(kv_pairs) >= 3:
        category = "form"
        evidence.append("multiple structured key-value fields found")
    else:
        category = "generic_document"
        evidence.append("fallback classification")

    subtype = None
    if category == "invoice":
        if any(token in text for token in MEDICAL_TOKENS):
            subtype = "medical_invoice"
            evidence.append("medical invoice keywords found")
        elif any(token in text for token in RESTAURANT_TOKENS):
            subtype = "restaurant_invoice"
            evidence.append("restaurant invoice keywords found")
        elif any(token in text for token in RETAIL_TOKENS):
            subtype = "retail_invoice"
            evidence.append("retail invoice keywords found")
        elif any(token in text for token in HOTEL_TOKENS):
            subtype = "hotel_invoice"
            evidence.append("hotel invoice keywords found")
        elif any(token in text for token in UTILITY_TOKENS):
            subtype = "utility_invoice"
            evidence.append("utility invoice keywords found")
        elif any(token in text for token in TRANSPORT_TOKENS):
            subtype = "transport_invoice"
            evidence.append("transport invoice keywords found")
        else:
            subtype = "general_invoice"
            evidence.append("invoice detected but subtype ambiguous")

    return {
        "document_category": category,
        "document_subtype": subtype,
        "evidence": evidence,
    }


def build_field_map(kv_pairs: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    field_map: dict[str, list[dict[str, Any]]] = {}
    for item in kv_pairs:
        canonical_key = str(item.get("canonical_key") or "field")
        field_map.setdefault(canonical_key, []).append(
            {
                "kv_id": item.get("kv_id"),
                "key": item.get("key"),
                "value": item.get("value"),
                "normalized_value": item.get("normalized_value"),
                "value_type": item.get("value_type"),
                "page_id": item.get("page_id"),
                "source_block_ids": item.get("source_block_ids", []),
                "source": item.get("source"),
            }
        )
    return field_map


def first_field_value(field_map: dict[str, list[dict[str, Any]]], key: str) -> dict[str, Any] | None:
    values = field_map.get(key, [])
    return values[0] if values else None


def clean_optional_amount(item: dict[str, Any] | None) -> dict[str, Any] | None:
    if not item:
        return None
    return item


def split_dual_row(row: list[str]) -> list[list[str]]:
    if len(row) >= 8:
        return [row[:4], row[4:8]]
    return [row]


def extract_amount_and_overflow(text: str) -> tuple[str, str | None]:
    clean = cleanup_ocr_text(text)
    amount = find_first_amount(clean) or ""
    if not amount:
        return clean, None
    match = re.search(r"[-+]?\d[\d,]*\.\d{2}", clean)
    if not match:
        return amount, None
    overflow = clean[match.end():].strip(" ;；，,。")
    overflow = re.sub(r"^(?:[-+]?\d[\d,]*\.\d{2}\s*[;；]?\s*)+", "", overflow).strip(" ;；，,。")
    if overflow and not re.match(r"^[0-9.;\s]+$", overflow):
        return amount, overflow
    return amount, None


def has_right_side_values(half: list[str]) -> bool:
    return any(cell.strip() for cell in half[:3])


def normalize_dual_halves(row: list[str]) -> list[list[str]]:
    halves = split_dual_row([cleanup_ocr_text(cell) for cell in row])
    if len(halves) != 2:
        return halves

    left = halves[0][:]
    right = halves[1][:]

    left_name, left_qty, left_amount, left_note = (left + ["", "", "", ""])[:4]
    right_name, right_qty, right_amount, right_note = (right + ["", "", "", ""])[:4]

    trimmed_left_amount, overflow_name = extract_amount_and_overflow(left_amount)
    if trimmed_left_amount:
        left_amount = trimmed_left_amount

    if overflow_name and not right_name.strip():
        right_name = overflow_name

    if not right_name.strip() and has_right_side_values(right) and left_note.strip():
        right_name = left_note.strip()
        left_note = ""

    left = [left_name, left_qty, left_amount, left_note]
    right = [right_name, right_qty, right_amount, right_note]
    return [left, right]


def row_looks_like_header(row: list[str]) -> bool:
    joined = " ".join(row)
    return any(token in joined for token in ["项目名称", "項目名称", "数量/单位", "金额", "备注"])


def build_line_item(half: list[str], row_index: int, side: str, subtype: str | None) -> dict[str, Any] | None:
    if len(half) < 1:
        return None
    if all(not cell for cell in half):
        return None
    name = cleanup_ocr_text(half[0].strip()) if len(half) > 0 else ""
    quantity_text = cleanup_ocr_text(half[1].strip()) if len(half) > 1 else ""
    amount_text = cleanup_ocr_text(half[2].strip()) if len(half) > 2 else ""
    note_text = cleanup_ocr_text(half[3].strip()) if len(half) > 3 else ""
    if not any([name, quantity_text, amount_text, note_text]):
        return None
    if any(token in name for token in ["金额合计", "其他信息"]):
        return None
    quantity, unit = parse_quantity_unit(quantity_text)
    amount = find_first_amount(amount_text)
    item: dict[str, Any] = {
        "line_id": f"line_{row_index}_{side}",
        "name": name or note_text or "unnamed_item",
        "quantity_text": quantity_text or None,
        "quantity": quantity,
        "unit": unit,
        "amount_text": amount or amount_text or None,
        "amount": amount,
        "raw_amount_text": amount_text or None,
        "note": note_text or None,
        "invoice_subtype": subtype,
        "raw_cells": half,
    }
    if subtype == "medical_invoice":
        is_category_charge = bool(name and not quantity_text and amount)
        item["medical_category"] = name if is_category_charge else None
        item["line_role"] = "category_charge" if is_category_charge else "service_line"
    return item


def restaurant_header_row_index(rows: list[list[str]]) -> int | None:
    for idx, row in enumerate(rows):
        compact = [normalize_compact_label(cell) for cell in row]
        if {"项目名称", "数量", "单价", "金额", "税率/征收率", "税额"}.issubset(set(compact)):
            return idx
    return None


def build_restaurant_invoice_line_items(embedded_tables: list[EmbeddedTable]) -> list[dict[str, Any]]:
    line_items: list[dict[str, Any]] = []
    line_index = 0
    for table in embedded_tables:
        rows = [[cleanup_ocr_text(cell) for cell in row] for row in table.rows]
        header_idx = restaurant_header_row_index(rows)
        if header_idx is None:
            continue
        for row in rows[header_idx + 1 :]:
            first = normalize_compact_label(row[0]) if row else ""
            if not any(cell.strip() for cell in row):
                continue
            if first.startswith("合计") or first.startswith("价税合计") or first.startswith("备注"):
                continue
            if len(row) < 8:
                continue
            name = dedupe_repeated_text(row[0]).strip("* ")
            spec = cleanup_ocr_text(row[1])
            unit = cleanup_ocr_text(row[2])
            quantity = cleanup_ocr_text(row[3])
            unit_price = find_first_amount(row[4] or "")
            amount = find_first_amount(row[5] or "")
            tax_rate = cleanup_ocr_text(row[6])
            tax_amount = find_first_amount(row[7] or "")
            if not name:
                continue
            line_index += 1
            line_items.append(
                {
                    "line_id": f"line_{line_index}",
                    "name": name,
                    "specification": spec or None,
                    "unit": unit or None,
                    "quantity_text": quantity or None,
                    "quantity": quantity or None,
                    "unit_price": unit_price,
                    "amount_text": amount or row[5] or None,
                    "amount": amount,
                    "tax_rate": tax_rate or None,
                    "tax_amount": tax_amount,
                    "invoice_subtype": "restaurant_invoice",
                    "raw_cells": row,
                }
            )
    return line_items


def build_invoice_line_items(embedded_tables: list[EmbeddedTable], subtype: str | None) -> list[dict[str, Any]]:
    if subtype == "restaurant_invoice":
        return build_restaurant_invoice_line_items(embedded_tables)
    line_items: list[dict[str, Any]] = []
    for table in embedded_tables:
        for row_index, row in enumerate(table.rows, start=1):
            if row_looks_like_header(row):
                continue
            if any("金额合计" in cell or "其他信息" in cell for cell in row):
                continue
            for side_index, half in enumerate(normalize_dual_halves(row), start=1):
                item = build_line_item(half, row_index, f"s{side_index}", subtype)
                if item:
                    line_items.append(item)
    return [item for item in line_items if item.get("name") and item.get("name") != "unnamed_item"]


def summarize_medical_invoice(
    field_map: dict[str, list[dict[str, Any]]],
    embedded_tables: list[EmbeddedTable],
    line_items: list[dict[str, Any]],
) -> dict[str, Any]:
    def infer_medical_parent_category(service_name: str, categories: list[str]) -> str | None:
        rules = [
            (("检查", "镜检", "喉镜", "鼻咽镜", "检验"), "检查费"),
            (("药", "喷雾剂", "颗粒", "胶囊", "片", "滴眼", "奥洛他定", "氮卓斯汀", "苯环"), "西药费"),
        ]
        for keywords, category_name in rules:
            if any(keyword in service_name for keyword in keywords) and category_name in categories:
                return category_name
        return categories[-1] if categories else None

    payment_breakdown = {
        key: clean_optional_amount(first_field_value(field_map, key))
        for key in [
            "insurance_pool_payment",
            "personal_account_payment",
            "mutual_aid_payment",
            "additional_fund_payment",
            "other_payment",
            "cash_payment",
            "personal_self_pay",
            "personal_self_funded",
            "personal_burden",
            "insurance_account_balance",
        ]
        if first_field_value(field_map, key)
    }
    encounter = {
        key: first_field_value(field_map, key)
        for key in [
            "outpatient_number",
            "visit_date",
            "insurance_number",
            "insurance_type",
            "business_serial_number",
            "center_serial_number",
            "medical_institution_type",
            "gender",
        ]
        if first_field_value(field_map, key)
    }
    category_charges: list[dict[str, Any]] = []
    service_lines: list[dict[str, Any]] = []
    seen_categories: set[str] = set()
    for item in line_items:
        name = str(item.get("name") or "").strip()
        amount = item.get("amount")
        if not name or not amount or name in seen_categories:
            if item.get("line_role") == "service_line":
                service_lines.append(item)
            continue
        if item.get("line_role") == "category_charge" or not item.get("quantity_text"):
            category_charges.append({"name": name, "amount": amount})
            seen_categories.add(name)
        else:
            service_lines.append(item)

    category_names = [item["name"] for item in category_charges]
    category_groups: list[dict[str, Any]] = []
    for category in category_charges:
        category_groups.append(
            {
                "category_name": category["name"],
                "category_amount": category["amount"],
                "service_lines": [],
            }
        )
    for item in service_lines:
        assigned = infer_medical_parent_category(str(item.get("name") or ""), category_names)
        item["parent_category"] = assigned
        for group in category_groups:
            if group["category_name"] == assigned:
                group["service_lines"].append(item)
                break

    return {
        "patient_name": first_field_value(field_map, "customer_name"),
        "provider_name": first_field_value(field_map, "vendor_name"),
        "encounter": encounter,
        "payment_breakdown": payment_breakdown,
        "category_charges": category_charges,
        "service_lines": service_lines,
        "category_groups": category_groups,
        "table_count": len(embedded_tables),
    }


def summarize_generic_invoice(
    field_map: dict[str, list[dict[str, Any]]],
    line_items: list[dict[str, Any]],
    subtype: str | None,
) -> dict[str, Any]:
    return {
        "invoice_subtype": subtype,
        "invoice_code": first_field_value(field_map, "invoice_code"),
        "invoice_number": first_field_value(field_map, "invoice_number"),
        "check_code": first_field_value(field_map, "check_code"),
        "invoice_date": first_field_value(field_map, "invoice_date"),
        "buyer": first_field_value(field_map, "customer_name"),
        "buyer_tax_id": first_field_value(field_map, "buyer_tax_id"),
        "seller": first_field_value(field_map, "vendor_name"),
        "seller_tax_id": first_field_value(field_map, "seller_tax_id"),
        "subtotal": first_field_value(field_map, "subtotal"),
        "total_amount": first_field_value(field_map, "total_amount"),
        "tax_amount": first_field_value(field_map, "tax_amount"),
        "amount_due": first_field_value(field_map, "amount_due"),
        "line_items": line_items,
    }


def build_structured_record(
    classification: dict[str, Any],
    field_map: dict[str, list[dict[str, Any]]],
    embedded_tables: list[EmbeddedTable],
) -> dict[str, Any]:
    category = classification.get("document_category")
    subtype = classification.get("document_subtype")
    key_fields = {
        key: first_field_value(field_map, key)
        for key in [
            "invoice_code",
            "invoice_number",
            "check_code",
            "machine_number",
            "invoice_date",
            "due_date",
            "customer_name",
            "buyer_tax_id",
            "vendor_name",
            "seller_tax_id",
            "payer_tax_id",
            "subtotal",
            "tax_amount",
            "total_amount",
            "amount_due",
        ]
        if first_field_value(field_map, key)
    }
    line_items = build_invoice_line_items(embedded_tables, subtype) if category == "invoice" else []
    record: dict[str, Any] = {
        "document_category": category,
        "document_subtype": subtype,
        "key_fields": key_fields,
        "line_items": line_items,
    }
    if category == "invoice":
        if subtype == "medical_invoice":
            record["invoice"] = summarize_medical_invoice(field_map, embedded_tables, line_items)
        else:
            record["invoice"] = summarize_generic_invoice(field_map, line_items, subtype)
    return record


def build_record_summary(
    document: dict[str, Any],
    kv_pairs: list[dict[str, Any]],
    entities: list[dict[str, Any]],
    table_index: list[dict[str, Any]],
    embedded_tables: list[EmbeddedTable],
) -> dict[str, Any]:
    classification = classify_document(document, kv_pairs, table_index, embedded_tables)
    field_map = build_field_map(kv_pairs)
    entity_counts: dict[str, int] = {}
    for entity in entities:
        entity_type = str(entity.get("type") or "custom")
        entity_counts[entity_type] = entity_counts.get(entity_type, 0) + 1
    structured_record = build_structured_record(classification, field_map, embedded_tables)
    return {
        "document_type": classification["document_category"],
        "document_category": classification["document_category"],
        "document_subtype": classification.get("document_subtype"),
        "classification": classification,
        "field_map": field_map,
        "entity_counts": entity_counts,
        "table_count": len(table_index),
        "structured_record": structured_record,
    }


def build_entity_traceability(entities: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in entities:
        rows.append(
            {
                "generated_unit_id": f"entity.{item.get('entity_id')}",
                "generated_text": str(item.get("value", "")),
                "source_refs": [{"page_id": item.get("page_id"), "block_id": block_id} for block_id in item.get("source_block_ids", [])],
                "assumption": None,
            }
        )
    return rows


def build_kv_traceability(kv_pairs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in kv_pairs:
        rows.append(
            {
                "generated_unit_id": f"kv.{item.get('kv_id')}",
                "generated_text": f"{item.get('key')}: {item.get('value')}",
                "source_refs": [{"page_id": item.get("page_id"), "block_id": block_id} for block_id in item.get("source_block_ids", [])],
                "assumption": item.get("source"),
            }
        )
    return rows
