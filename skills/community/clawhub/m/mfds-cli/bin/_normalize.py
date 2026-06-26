#!/usr/bin/env python3
"""Normalize MFDS API responses (XML or JSON) into stable JSONL records.

Reads response body from stdin. Emits one JSON object per line on stdout.

Field-mapping tables are intentionally conservative: known fields get nice
ASCII keys, everything else is dumped under `_raw` for callers that need it.
"""
from __future__ import annotations

import argparse
import json
import sys
import xml.etree.ElementTree as ET
from typing import Any

# --- Field maps ---------------------------------------------------------------

DRUG_FIELDS = {
    "ITEM_SEQ": "item_seq",
    "ITEM_NAME": "item_name_ko",
    "ITEM_ENG_NAME": "item_name_en",
    "ENTP_NAME": "maker",
    "ENTP_ENG_NAME": "maker_en",
    "ITEM_PERMIT_DATE": "permit_date",
    "ENTP_NO": "maker_no",
    "BIZRNO": "bizrno",
    "CHART": "chart",
    "MATERIAL_NAME": "main_ingredient",
    "ETC_OTC_CODE": "prescription",
    "EE_DOC_DATA": "efficacy_doc",
    "UD_DOC_DATA": "method_doc",
    "NB_DOC_DATA": "warning_doc",
    "PN_DOC_DATA": "leaflet_doc",
    "STORAGE_METHOD": "storage",
    "VALID_TERM": "valid_term",
    "PERMIT_KIND_CODE": "permit_kind_code",
    "CANCEL_DATE": "cancel_date",
    "CANCEL_NAME": "cancel_name",
    "ATC_CODE": "atc_code",
    "MAIN_ITEM_INGR": "ingredient_compound",
    "INGR_NAME": "ingredient_name",
    "NARCOTIC_KIND_CODE": "narcotic_kind_code",
    "NEWDRUG_CLASS_NAME": "newdrug_class",
}

DRUG_EASY_FIELDS = {
    "itemSeq": "item_seq",
    "itemName": "item_name_ko",
    "entpName": "maker",
    "itemImage": "image_url",
    "efcyQesitm": "efficacy",
    "useMethodQesitm": "usage",
    "atpnWarnQesitm": "strong_warning",
    "atpnQesitm": "warning",
    "intrcQesitm": "interaction",
    "seQesitm": "side_effect",
    "depositMethodQesitm": "storage",
    "openDe": "open_date",
    "updateDe": "update_date",
}

DUR_FIELDS = {
    "TYPE_NAME": "dur_type_name",
    "MIX_TYPE": "mix_type",
    "INGR_KOR_NAME": "ingredient_name",
    "INGR_ENG_NAME": "ingredient_name_en",
    "INGR_CODE": "ingredient_code",
    "MIXTURE_INGR_KOR_NAME": "mixture_ingredient_name",
    "MIXTURE_INGR_ENG_NAME": "mixture_ingredient_name_en",
    "MIXTURE_INGR_CODE": "mixture_ingredient_code",
    "ITEM_NAME": "item_name_ko",
    "ITEM_SEQ": "item_seq",
    "ENTP_NAME": "maker",
    "PROHBT_CONTENT": "prohibit_reason",
    "REMARK": "remark",
    "MIXTURE_ITEM_NAME": "mixture_item_name",
    "MIXTURE_ITEM_SEQ": "mixture_item_seq",
    "MIXTURE_ENTP_NAME": "mixture_maker",
    "NOTIFICATION_DATE": "notify_date",
    "EFFECTIVE_DATE": "effective_date",
    "PROHBT_DURATION": "prohibit_duration",
    "FORM_NAME": "form_name",
    "AGE_BASE": "age_base",
}

RECALL_FIELDS = {
    "DSPSL_PRDLST_NM": "item_name_ko",
    "ENTRPS_NM": "maker",
    "ITEM_SEQ": "item_seq",
    "RECALL_PUBLIC_DT": "publish_date",
    "BIZRNO": "bizrno",
    "RECALL_REASON": "reason",
    "RECALL_PRODUCT_NAME": "product_name",
    "RECALL_PRODUCT_TYPE": "product_type",
    "RECALL_TARGET": "target",
    "PRDUCTN_DT": "production_date",
    "DSPSL_DT": "action_date",
    "DSPSL_TYPE_NM": "action_name",
    "DSPSL_RSN": "action_reason",
    "DSPSL_NM": "action_label",
    "EXEC_TYPE_NAME": "exec_type",
    "ITEM_NAME": "item_name_ko",
    "ENTP_NAME": "maker",
}


def _xml_record_to_dict(elem: ET.Element) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for child in elem:
        out[child.tag] = (child.text or "").strip()
    return out


def _iter_xml_records(body: str):
    """Yield <item> elements from an MFDS XML response."""
    try:
        root = ET.fromstring(body)
    except ET.ParseError as e:
        raise SystemExit(f"mfds-cli: malformed XML response: {e}\n--- body ---\n{body[:500]}")
    # MFDS XML shape: <response><body><items><item>...</item></items></body></response>
    items = root.findall(".//item")
    for it in items:
        yield _xml_record_to_dict(it)
    # Some endpoints surface error text under <header><resultMsg>
    if not items:
        msg = root.findtext(".//resultMsg") or root.findtext(".//returnAuthMsg")
        if msg and msg.strip().upper() not in ("NORMAL SERVICE.", "OK", "SUCCESS"):
            print(f"mfds-cli: API returned no items (msg={msg!r})", file=sys.stderr)


def _iter_json_records(body: str):
    """Yield item dicts from an MFDS JSON response."""
    try:
        data = json.loads(body)
    except json.JSONDecodeError as e:
        raise SystemExit(f"mfds-cli: malformed JSON response: {e}\n--- body ---\n{body[:500]}")
    items = (
        data.get("response", {})
        .get("body", {})
        .get("items", [])
    )
    if isinstance(items, dict):
        # MFDS sometimes returns {"item": {...}} or {"item": [...]}
        items = items.get("item", [])
    if isinstance(items, dict):
        items = [items]
    if items is None:
        items = []
    for it in items:
        if isinstance(it, dict):
            yield it


def _detect_and_iter(body: str):
    body = body.lstrip()
    if body.startswith("<"):
        yield from _iter_xml_records(body)
    else:
        yield from _iter_json_records(body)


def _normalize(record: dict[str, Any], field_map: dict[str, str], record_type: str) -> dict[str, Any]:
    out: dict[str, Any] = {"type": record_type}
    raw: dict[str, Any] = {}
    for k, v in record.items():
        nice = field_map.get(k)
        if nice:
            out[nice] = v
        else:
            raw[k] = v
    if raw:
        out["_raw"] = raw
    return out


FIELD_MAPS = {
    "drug": DRUG_FIELDS,
    "drug-easy": DRUG_EASY_FIELDS,
    "dur": DUR_FIELDS,
    "recall": RECALL_FIELDS,
}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--type", required=True, choices=sorted(FIELD_MAPS))
    ap.add_argument("--output", default="jsonl", choices=["jsonl", "json"])
    args = ap.parse_args()

    body = sys.stdin.read()
    field_map = FIELD_MAPS[args.type]

    records = [_normalize(r, field_map, args.type) for r in _detect_and_iter(body)]

    if args.output == "json":
        json.dump(records, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        for r in records:
            sys.stdout.write(json.dumps(r, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
