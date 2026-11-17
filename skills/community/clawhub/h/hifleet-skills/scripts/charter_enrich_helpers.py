#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Map list/API vessel rows → enrich-row request (parse_schema + top-level imo/mmsi)."""

from __future__ import annotations

import os
import re
import sys
from typing import Any, Optional, Tuple

# 与 charter_ai resolve_vessel_type_category / call_deepseek_shiptype 对齐
VESSEL_TYPE_CATEGORIES: tuple[str, ...] = (
    "散货船",
    "集装箱船",
    "石油化学品船",
    "杂货船",
    "油船",
    "滚装船",
)


def _yn_int(val: Any) -> Optional[int]:
    if val is None or val == "":
        return None
    if isinstance(val, bool):
        return 1 if val else 0
    if isinstance(val, (int, float)) and not isinstance(val, bool):
        return int(val)
    s = str(val).strip().lower()
    if s in ("1", "是", "yes", "y", "true"):
        return 1
    if s in ("0", "否", "no", "n", "false"):
        return 0
    return None


def normalize_is_geared(val: Any) -> Optional[int]:
    """是否有船吊 → 1=Geared / 0=Gearless；兼容 geared/gearless 等邮件写法。"""
    yn = _yn_int(val)
    if yn is not None:
        return yn
    if val is None or val == "":
        return None
    s = str(val).strip().lower().replace("'", "'")
    if not s:
        return None
    gearless_tokens = (
        "gearless",
        "gless",
        "g'less",
        "g-less",
        "g less",
        "no gear",
        "without gear",
        "无吊",
        "无船吊",
        "不带吊",
    )
    geared_tokens = (
        "geared",
        "with gear",
        "with crane",
        "with cranes",
        "有吊",
        "有船吊",
        "带吊",
    )
    if any(tok in s for tok in gearless_tokens):
        return 0
    if any(tok in s for tok in geared_tokens):
        return 1
    return None


def normalize_geared_for_storage(val: Any) -> Optional[int]:
    """SQLite 整型列入库：geared/gearless 字符串 → 1/0。"""
    return normalize_is_geared(val)


def _strip_gear_tokens_from_type_text(raw: str) -> str:
    """从船型文本中剥离 geared/gearless 等吊机描述（不应写入船型）。"""
    s = str(raw or "").strip()
    if not s:
        return ""
    for tok in (
        r"\bgeared\b",
        r"\bgearless\b",
        r"\bg'?less\b",
        r"\bg-?less\b",
        r"\bwith\s+gear\b",
        r"\bno\s+gear\b",
        r"有船吊",
        r"无船吊",
        r"带吊",
        r"无吊",
    ):
        s = re.sub(tok, " ", s, flags=re.IGNORECASE)
    s = re.sub(r"[/|,;+\s]+", " ", s).strip()
    return s


def rule_based_vessel_type_category(raw: Any) -> Optional[str]:
    """规则映射 → 六类船型之一；无法判断时返回 None。"""
    if raw is None or raw == "":
        return None
    text = _strip_gear_tokens_from_type_text(str(raw))
    if not text:
        return None
    if text in VESSEL_TYPE_CATEGORIES:
        return text
    u = text.upper()
    # 杂货 / 多用途（须在 CONTAINER 之前，避免 GC/CONT 误判）
    gc_kw = (
        "GC/CONT",
        "GC / CONT",
        "GENERAL CARGO",
        " MULTIPURPOSE",
        " MPP",
        "MPP ",
        "GC/",
        " GC",
        "GC ",
        "SEMI-BOX",
        "SEMI BOX",
        "BOXSHAPED",
        "DECK CARGO",
        "杂货",
        "多用途",
    )
    if any(k in u for k in gc_kw):
        return "杂货船"
    # 集装箱
    if any(k in u for k in ("CONTAINER", " CONT ", "BOX SHIP", "FEEDER", "TEU")) or u.startswith("CONT"):
        return "集装箱船"
    # 滚装
    if any(k in u for k in ("RO-RO", "RORO", "CAR CARRIER", "PCC", "PCTC", "ROLL-ON")):
        return "滚装船"
    # 油船 / 化学品
    if any(k in u for k in ("CHEMICAL", "CHEM ", " PRODUCT TANK", "OIL/CHEM", "CHEM/OIL")):
        return "石油化学品船"
    if any(k in u for k in ("TANKER", "VLCC", "ULCC", "AFRAMAX", "SUEZMAX", " CRUDE", "OIL TANK")):
        return "油船"
    # 散货
    bulk_kw = (
        "BULK",
        "CAPE",
        "CAPESIZE",
        "PANAMAX",
        "PMX",
        "KMAX",
        "HANDY",
        "HMX",
        "SUPRA",
        "ULTRA",
        "SMX",
        "UMX",
        "VLOC",
        "VLBC",
        "COAL",
        "ORE",
        "散货",
    )
    if any(k in u for k in bulk_kw):
        return "散货船"
    return None


def _call_deepseek_shiptype_if_available(hint: str) -> Optional[str]:
    if not hint or not str(hint).strip():
        return None
    root = os.environ.get("HIFLEET_CHARTER_AI_ROOT", "").strip()
    if not root:
        here = os.path.abspath(__file__)
        candidate = os.path.normpath(os.path.join(here, "..", "..", "charter_ai"))
        if os.path.isdir(candidate):
            root = candidate
    if not root or root not in sys.path:
        if root:
            sys.path.insert(0, root)
    try:
        from charter_utils import call_deepseek_shiptype  # type: ignore
    except ImportError:
        return None
    try:
        result = call_deepseek_shiptype(str(hint).strip())
        if isinstance(result, dict):
            cat = str(result.get("shiptype") or "").strip()
            if cat in VESSEL_TYPE_CATEGORIES:
                return cat
    except Exception:
        return None
    return None


def resolve_vessel_type_category(
    shiptype_llm: Any = None,
    *,
    minotype_archive: Any = None,
    shiptype_archive: Any = None,
    use_llm: bool = True,
) -> Optional[str]:
    """
    船型 → 六类之一。顺序：minotype → LLM 船型 → 规则 →（可选）DeepSeek。
    与 charter_ai.resolve_vessel_type_category 语义对齐。
    """
    for hint in (minotype_archive, shiptype_llm, shiptype_archive):
        if hint is None or str(hint).strip() == "":
            continue
        cleaned = _strip_gear_tokens_from_type_text(str(hint))
        cat = rule_based_vessel_type_category(cleaned)
        if cat:
            return cat
        if use_llm:
            llm_cat = _call_deepseek_shiptype_if_available(cleaned or str(hint))
            if llm_cat:
                return llm_cat
    return None


def geared_from_archive_dict(item: dict[str, Any]) -> Optional[int]:
    """从 ship-archive JSON 条目推断 Geared/Gearless（skills 侧兜底，无需 charter_ai）。"""
    if not isinstance(item, dict):
        return None
    for key in ("Gearless", "gearless", "isGearless", "is_gearless"):
        raw = item.get(key)
        if raw is None or raw == "":
            continue
        s = str(raw).strip().upper()
        if s in ("Y", "YES", "1", "TRUE"):
            return 0
        if s in ("N", "NO", "0", "FALSE"):
            return 1
    for key in ("craneCount", "crane_count", "CraneCount", "吊机数量"):
        raw = item.get(key)
        if raw in (None, ""):
            continue
        try:
            return 1 if int(float(str(raw).strip())) > 0 else 0
        except (TypeError, ValueError):
            pass
    gt = str(
        item.get("GearTypeLargest")
        or item.get("gearTypeLargest")
        or item.get("gearType")
        or ""
    ).strip()
    if gt and gt.upper() not in ("NONE", "N/A", "UNKNOWN", "-", "NULL", "NA"):
        g = normalize_is_geared(gt)
        return g if g is not None else 1
    return normalize_is_geared(
        " ".join(
            str(item.get(k) or "")
            for k in ("GearDescriptiveNarrative", "gearDescriptiveNarrative", "type", "minotype")
        )
    )


def _norm_imo(value: Any) -> Optional[str]:
    if value is None or value == "":
        return None
    digits = re.sub(r"\D", "", str(value).strip())
    if len(digits) == 7 and digits != "0000000":
        return digits
    return None


def clean_vessel_name(shipname: str) -> str:
    """Strip MV/MT/M.V. prefix before IMO lookup or enrich (matches charter_enrich_mappers)."""
    if not shipname:
        return ""
    return re.sub(
        r"^(M\s*[\./\\]?\s*(V|T)\s*[\./\\]?\s*)",
        "",
        str(shipname).strip(),
        flags=re.IGNORECASE,
    ).strip()


def normalize_vessel_row_for_enrich(row: dict[str, Any]) -> Tuple[dict[str, Any], Optional[str], Optional[str]]:
    """
    Accept parse_schema (船名/IMO) or public API row (ShipName/imo/dwt).
    Returns (row for body.row, imo for body.imo, mmsi for body.mmsi).
    """
    r = row or {}
    imo = _norm_imo(r.get("IMO") or r.get("imo") or r.get("Imo"))
    mmsi_raw = r.get("mmsi") or r.get("MMSI")
    mmsi = str(mmsi_raw).strip() if mmsi_raw not in (None, "") else None

    out = dict(r)
    if not str(out.get("船名") or "").strip():
        out["船名"] = (
            str(
                r.get("ShipName")
                or r.get("shipName")
                or r.get("vesselName")
                or r.get("name")
                or ""
            ).strip()
        )
    if out.get("载重吨") in (None, "") and r.get("dwt") not in (None, ""):
        out["载重吨"] = r.get("dwt")
    if not out.get("IMO") and imo:
        out["IMO"] = imo
    if not str(out.get("OPEN位置") or "").strip():
        out["OPEN位置"] = (
            str(r.get("OPEN位置") or r.get("openPort") or r.get("destination") or "").strip()
        )
    if not str(out.get("船型") or "").strip():
        out["船型"] = str(r.get("船型") or r.get("type") or r.get("shiptype") or "").strip()
    geared = normalize_is_geared(out.get("是否有船吊"))
    if geared is None and out.get("吊机数量") not in (None, ""):
        try:
            geared = 1 if int(float(str(out.get("吊机数量")).strip())) > 0 else 0
        except (TypeError, ValueError):
            pass
    if geared is not None:
        out["是否有船吊"] = geared
    cat = resolve_vessel_type_category(
        out.get("船型"),
        minotype_archive=out.get("档案_细分船型"),
        shiptype_archive=out.get("档案_船型"),
        use_llm=False,
    )
    if cat:
        out["船型"] = cat
    name = str(out.get("船名") or "").strip()
    if name:
        out["船名"] = clean_vessel_name(name)
    return out, imo, mmsi


def normalize_cargo_row_for_enrich(row: dict[str, Any]) -> dict[str, Any]:
    r = row or {}
    out = dict(r)
    if not str(out.get("货物种类") or "").strip():
        out["货物种类"] = str(
            r.get("货物种类") or r.get("cargoType") or r.get("type") or r.get("cargo") or ""
        ).strip()
    if not str(out.get("装货港") or "").strip():
        out["装货港"] = str(r.get("装货港") or r.get("loadPort") or r.get("openPort") or "").strip()
    if not str(out.get("卸货港") or "").strip():
        out["卸货港"] = str(
            r.get("卸货港") or r.get("dischargePort") or r.get("dischargingPort") or ""
        ).strip()
    if out.get("货物数量") in (None, "") and r.get("quantity") not in (None, ""):
        out["货物数量"] = r.get("quantity")
    return out


def enrich_response_usable(resp: dict[str, Any]) -> bool:
    if not isinstance(resp, dict):
        return False
    if resp.get("ok") is True:
        return True
    if resp.get("imo") or resp.get("data") or resp.get("archive"):
        return True
    code = resp.get("code")
    if code not in (None, 0, 200, "200", "0"):
        return False
    return bool(resp.get("status") in (1, "1", True, "ok", "OK"))
