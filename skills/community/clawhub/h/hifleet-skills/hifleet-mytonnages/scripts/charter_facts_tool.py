#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""hifleet-mytonnages：解析结果写入 / 检索 charter_facts.sqlite3（货盘表 + 船盘表 + unknown 表）。"""

from __future__ import annotations

import argparse
import json
import os
import re
import sqlite3
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Optional

# 与 SKILL.md §2.4 JSON 键一致
CARGO_FIELD_KEYS: tuple[str, ...] = (
    "客户名称",
    "货物数量",
    "货物种类",
    "装货港",
    "卸货港",
    "装港消约期开始日期",
    "装港消约期结束日期",
    "是否为散装",
    "装货率",
    "装货条款",
    "允许船型",
    "最早船舶建造年份限制",
    "船级限制",
    "是否要求船吊",
    "是否为危险品",
    "冷藏需求",
    "舱型要求",
    "是否接收甲板货",
    "包装要求",
    "货物特殊说明",
    "货主要求",
    "dwt要求",
    "联系电话",
    "即时通讯",
)

OPENVESSEL_FIELD_KEYS: tuple[str, ...] = (
    "船名",
    "IMO",
    "船型",
    "载重吨",
    "建造年份",
    "OPEN位置",
    "OPEN开始日期",
    "OPEN结束日期",
    "航线意向",
    "吊机数量",
    "是否有船吊",
    "吊机类型",
    "舱口尺寸",
    "舱容（立方米）",
    "舱数",
    "舱盖类型",
    "甲板载重能力",
    "是否可装危险品",
    "冷藏插座数量",
    "是否有喷淋系统",
    "燃料类型",
    "所属公司",
    "IMO设备等级",
    "船速（节）",
    "载货设备描述",
    "租船类型",
    "是否可跑CIS航线",
    "是否可跑BH航线",
    "是否可跑AUS航线",
    "是否是BOX HOLD",
    "是否是NO IRAN/ISRAEL/YEMEN",
    "联系电话",
    "即时通讯",
    "卸货港",
    "是否有rightship",
    "O/A其他附加信息",
)

CARGO_INT_KEYS = {
    "货物数量",
    "是否为散装",
    "是否要求船吊",
    "是否为危险品",
    "冷藏需求",
    "是否接收甲板货",
}

OPENVESSEL_INT_KEYS = {
    "载重吨",
    "吊机数量",
    "是否有船吊",
    "舱容（立方米）",
    "舱数",
    "是否可装危险品",
    "冷藏插座数量",
    "是否有喷淋系统",
    "是否可跑CIS航线",
    "是否可跑BH航线",
    "是否可跑AUS航线",
    "是否是BOX HOLD",
    "是否是NO IRAN/ISRAEL/YEMEN",
    "是否有rightship",
}

OPENVESSEL_REAL_KEYS = {"船速（节）"}

# 2.4.2 富化列（与 CHARTER_ENRICH_API.md 一致）
CARGO_ENRICH_KEYS: tuple[str, ...] = ("portid", "discharging_portid", "tags")

SHIP_ARCHIVE_KEYS: tuple[str, ...] = (
    "档案_船名",
    "档案_呼号",
    "档案_建造年",
    "档案_dwt",
    "档案_船旗",
    "档案_船长",
    "档案_船宽",
    "档案_吃水",
    "档案_总吨",
    "档案_造船厂",
    "档案_船型",
    "档案_船东",
    "档案_经营人",
    "档案_管理公司",
    "档案_细分船型",
    "ship_archive_json",
)

OPENVESSEL_ENRICH_KEYS: tuple[str, ...] = ("mmsi", "tags", "portid", "discharging_portid") + SHIP_ARCHIVE_KEYS

DEFAULT_CHARTER_API_BASE = "https://api.hifleet.com/openclaw/vessel/charter"


def _q(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def _norm_intent(intent: Any) -> list[str]:
    if intent is None:
        return []
    if isinstance(intent, str):
        return [intent] if intent else []
    if isinstance(intent, list):
        return [str(x) for x in intent if x is not None]
    return [str(intent)]


def coerce_field(key: str, val: Any, int_keys: set[str], real_keys: set[str]) -> Any:
    if val is None:
        return None
    if key in int_keys:
        if isinstance(val, bool):
            return 1 if val else 0
        if isinstance(val, (int, float)) and not isinstance(val, bool):
            return int(val)
        s = str(val).strip()
        if not s or s.lower() in ("null", "none"):
            return None
        m = re.search(r"-?\d+", s)
        return int(m.group(0)) if m else None
    if key in real_keys:
        if isinstance(val, (int, float)) and not isinstance(val, bool):
            return float(val)
        s = str(val).strip()
        if not s or s.lower() in ("null", "none"):
            return None
        try:
            return float(s.replace(",", ""))
        except ValueError:
            m = re.search(r"-?\d+\.?\d*", s)
            return float(m.group(0)) if m else None
    if isinstance(val, (dict, list)):
        return json.dumps(val, ensure_ascii=False)
    return val if isinstance(val, str) else str(val)


def _search_parts(
    subject: str,
    from_addr: str,
    row: dict[str, Any],
    keys: Iterable[str],
) -> str:
    parts = [subject or "", from_addr or ""]
    for k in keys:
        v = row.get(k)
        if v is not None and v != "":
            parts.append(str(v))
    return " ".join(parts)


class CharterFactsDB:
    def __init__(self, path: Path) -> None:
        self.path = path

    def connect(self) -> sqlite3.Connection:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(self.path))
        conn.row_factory = sqlite3.Row
        return conn

    def init(self, conn: sqlite3.Connection) -> None:
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = {r[0] for r in cur.fetchall()}

        if "charter_fact" in tables:
            cur.execute("DROP TABLE IF EXISTS charter_fact")

        if "cargo_plate" in tables:
            cur.execute("PRAGMA table_info(cargo_plate)")
            cols = {r[1] for r in cur.fetchall()}
            if "客户名称" not in cols:
                cur.execute("DROP TABLE IF EXISTS cargo_plate")
                cur.execute("DROP TABLE IF EXISTS openvessel_plate")
                cur.execute("DROP TABLE IF EXISTS mail_unknown")

        cargo_cols = ", ".join(f'{_q(k)} TEXT' for k in CARGO_FIELD_KEYS)
        cur.execute(
            f"""
            CREATE TABLE IF NOT EXISTS cargo_plate (
              message_id TEXT NOT NULL,
              email_date_utc TEXT,
              from_addr TEXT,
              subject TEXT,
              row_index INTEGER NOT NULL,
              {cargo_cols},
              payload_json TEXT NOT NULL,
              search_text TEXT NOT NULL,
              parsed_at TEXT NOT NULL
            )
            """
        )

        opv_cols = ", ".join(f'{_q(k)} TEXT' for k in OPENVESSEL_FIELD_KEYS)
        cur.execute(
            f"""
            CREATE TABLE IF NOT EXISTS openvessel_plate (
              message_id TEXT NOT NULL,
              email_date_utc TEXT,
              from_addr TEXT,
              subject TEXT,
              row_index INTEGER NOT NULL,
              {opv_cols},
              payload_json TEXT NOT NULL,
              search_text TEXT NOT NULL,
              parsed_at TEXT NOT NULL
            )
            """
        )

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS mail_unknown (
              message_id TEXT NOT NULL,
              email_date_utc TEXT,
              from_addr TEXT,
              subject TEXT,
              intent_json TEXT NOT NULL,
              search_text TEXT NOT NULL,
              parsed_at TEXT NOT NULL
            )
            """
        )

        self._ensure_columns(conn, "cargo_plate", CARGO_ENRICH_KEYS)
        self._ensure_columns(conn, "openvessel_plate", OPENVESSEL_ENRICH_KEYS)
        conn.commit()

    def _ensure_columns(self, conn: sqlite3.Connection, table: str, keys: tuple[str, ...]) -> None:
        cur = conn.cursor()
        cur.execute(f"PRAGMA table_info({table})")
        existing = {r[1] for r in cur.fetchall()}
        for k in keys:
            if k not in existing:
                cur.execute(f'ALTER TABLE {table} ADD COLUMN {_q(k)} TEXT')

    def save_parsed(
        self,
        conn: sqlite3.Connection,
        *,
        message_id: str,
        email_date_utc: str,
        from_addr: str,
        subject: str,
        parsed: dict[str, Any],
    ) -> None:
        self.init(conn)
        cur = conn.cursor()
        intent = _norm_intent(parsed.get("intent"))
        data = parsed.get("data") or {}
        cargo_list = data.get("cargo") if isinstance(data.get("cargo"), list) else []
        opv_list = data.get("openvessels") if isinstance(data.get("openvessels"), list) else []

        cur.execute("DELETE FROM cargo_plate WHERE message_id = ?", (message_id,))
        cur.execute("DELETE FROM openvessel_plate WHERE message_id = ?", (message_id,))
        cur.execute("DELETE FROM mail_unknown WHERE message_id = ?", (message_id,))

        parsed_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        cargo_cols_list = [_q(k) for k in CARGO_FIELD_KEYS]
        cargo_placeholders = ", ".join(["?"] * (5 + len(CARGO_FIELD_KEYS) + 3))
        cargo_insert = (
            f'INSERT INTO cargo_plate (message_id, email_date_utc, from_addr, subject, row_index, '
            f'{", ".join(cargo_cols_list)}, payload_json, search_text, parsed_at) VALUES ({cargo_placeholders})'
        )

        for idx, raw in enumerate(cargo_list):
            if not isinstance(raw, dict):
                continue
            row_vals: dict[str, Any] = {}
            for k in CARGO_FIELD_KEYS:
                row_vals[k] = coerce_field(k, raw.get(k), CARGO_INT_KEYS, set())
            payload = json.dumps(raw, ensure_ascii=False)
            st = _search_parts(subject, from_addr, row_vals, CARGO_FIELD_KEYS)
            vals: list[Any] = [
                message_id,
                email_date_utc,
                from_addr,
                subject,
                idx,
            ]
            vals.extend(row_vals[k] for k in CARGO_FIELD_KEYS)
            vals.extend([payload, st, parsed_at])
            cur.execute(cargo_insert, vals)

        opv_cols_list = [_q(k) for k in OPENVESSEL_FIELD_KEYS]
        opv_placeholders = ", ".join(["?"] * (5 + len(OPENVESSEL_FIELD_KEYS) + 3))
        opv_insert = (
            f'INSERT INTO openvessel_plate (message_id, email_date_utc, from_addr, subject, row_index, '
            f'{", ".join(opv_cols_list)}, payload_json, search_text, parsed_at) VALUES ({opv_placeholders})'
        )

        for idx, raw in enumerate(opv_list):
            if not isinstance(raw, dict):
                continue
            row_vals = {}
            for k in OPENVESSEL_FIELD_KEYS:
                row_vals[k] = coerce_field(k, raw.get(k), OPENVESSEL_INT_KEYS, OPENVESSEL_REAL_KEYS)
            payload = json.dumps(raw, ensure_ascii=False)
            st = _search_parts(subject, from_addr, row_vals, OPENVESSEL_FIELD_KEYS)
            vals = [message_id, email_date_utc, from_addr, subject, idx]
            vals.extend(row_vals[k] for k in OPENVESSEL_FIELD_KEYS)
            vals.extend([payload, st, parsed_at])
            cur.execute(opv_insert, vals)

        has_unknown = any(x.lower() == "unknown" for x in intent)
        if has_unknown and not cargo_list and not opv_list:
            st = " ".join(
                x for x in (subject, from_addr, json.dumps(intent, ensure_ascii=False)) if x
            )
            cur.execute(
                "INSERT INTO mail_unknown (message_id, email_date_utc, from_addr, subject, intent_json, search_text, parsed_at) VALUES (?,?,?,?,?,?,?)",
                (
                    message_id,
                    email_date_utc,
                    from_addr,
                    subject,
                    json.dumps(intent, ensure_ascii=False),
                    st,
                    parsed_at,
                ),
            )

        conn.commit()

    def search(self, conn: sqlite3.Connection, q: str, limit: int = 50) -> list[dict[str, Any]]:
        self.init(conn)
        cur = conn.cursor()
        like = f"%{q}%"
        out: list[dict[str, Any]] = []

        for table, ftype in (
            ("cargo_plate", "cargo"),
            ("openvessel_plate", "openvessel"),
        ):
            cur.execute(
                f"SELECT * FROM {table} WHERE search_text LIKE ? ORDER BY email_date_utc DESC LIMIT ?",
                (like, limit),
            )
            for row in cur.fetchall():
                d = dict(row)
                d["_source_table"] = table
                d["_fact_type"] = ftype
                pj = d.get("payload_json")
                if pj:
                    try:
                        d["payload"] = json.loads(pj)
                    except json.JSONDecodeError:
                        d["payload"] = None
                out.append(d)

        cur.execute(
            "SELECT * FROM mail_unknown WHERE search_text LIKE ? ORDER BY email_date_utc DESC LIMIT ?",
            (like, limit),
        )
        for row in cur.fetchall():
            d = dict(row)
            d["_source_table"] = "mail_unknown"
            d["_fact_type"] = "unknown"
            ij = d.get("intent_json")
            if ij:
                try:
                    d["intent"] = json.loads(ij)
                except json.JSONDecodeError:
                    d["intent"] = None
            out.append(d)

        return out[:limit]


def _row_index_key(message_id: str, row_index: Any, fact_type: str) -> str:
    return f"{message_id}:{row_index}:{fact_type}"


def _clean_vessel_name(shipname: str) -> str:
    if not shipname:
        return ""
    return re.sub(
        r"^(M\s*[\./\\]?\s*(V|T)\s*[\./\\]?\s*)",
        "",
        str(shipname).strip(),
        flags=re.IGNORECASE,
    ).strip()


def _valid_imo_digits(imo: Any) -> str:
    if imo is None:
        return ""
    digits = re.sub(r"\D", "", str(imo).strip())
    if len(digits) == 7 and digits != "0000000":
        return digits
    return ""


def resolve_enrich_row_url() -> str:
    """单行补充信息 API 完整 URL（公网 enrich-row）。"""
    explicit = (
        os.environ.get("HIFLEET_CHARTER_ENRICH_URL", "").strip()
        or os.environ.get("HIFLEET_CHARTER_ENRICH_INTERNAL_BASE", "").strip()
    )
    if explicit:
        u = explicit.rstrip("/")
        if u.endswith("enrich-row") or u.endswith("enrich_row"):
            return u
        if u.endswith("/charterAI"):
            return u + "/enrich_row"
        return u + "/enrich-row" if "enrich" not in u.split("/")[-1] else u
    cfg_path = default_skill_dir() / "config.json"
    if cfg_path.is_file():
        try:
            cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
            for key in ("charter_enrich_url", "charter_enrich_internal_base"):
                v = str(cfg.get(key) or "").strip()
                if not v:
                    continue
                u = v.rstrip("/")
                if u.endswith("enrich-row") or u.endswith("enrich_row"):
                    return u
                if u.endswith("/charterAI"):
                    return u + "/enrich_row"
                if "api.hifleet.com" in u:
                    return u + "/enrich-row" if not u.endswith("enrich-row") else u
                return u
        except (json.JSONDecodeError, OSError):
            pass
    return "https://api.hifleet.com/openclaw/vessel/charter/enrich-row"


def resolve_enrich_internal_base() -> str:
    """兼容旧调用方：返回 enrich-row 完整 URL。"""
    return resolve_enrich_row_url()


def _enrich_auth_query(api_key: str, url: str) -> str:
    if "api.hifleet.com" in url:
        return urllib.parse.urlencode({"api_key": api_key})
    return urllib.parse.urlencode({"sk": api_key})


def _http_post_json_url(url: str, body: dict[str, Any], timeout: int = 60) -> dict[str, Any]:
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _fetch_enrich_row(
    enrich_url: str,
    api_key: str,
    kind: str,
    row: dict[str, Any],
    *,
    source: str = "parse_schema",
    imo: Any = None,
    mmsi: Any = None,
    charter_api_base: str | None = None,
) -> dict[str, Any]:
    """单次调用 enrich-row：船盘返回 imo/mmsi/data/archive；货盘返回 data。"""
    q = _enrich_auth_query(api_key, enrich_url)
    sep = "&" if "?" in enrich_url else "?"
    url = f"{enrich_url}{sep}{q}"
    body: dict[str, Any] = {"kind": kind, "row": row, "source": source}
    if imo is not None:
        body["imo"] = imo
    if mmsi is not None:
        body["mmsi"] = mmsi
    if charter_api_base:
        body["charter_api_base"] = charter_api_base
    try:
        resp = _http_post_json_url(url, body)
    except (urllib.error.URLError, json.JSONDecodeError, TimeoutError) as e:
        return {"_fetch_error": str(e)}
    if resp.get("ok"):
        return resp
    if resp.get("imo") or resp.get("data") or resp.get("archive"):
        resp["partial"] = True
        return resp
    return {}


def _apply_vessel_enrich_updates(
    updates: dict[str, Any],
    resp: dict[str, Any],
    r: dict[str, Any],
) -> None:
    imo_new = _valid_imo_digits(resp.get("imo"))
    if imo_new:
        updates["IMO"] = imo_new
    mmsi_new = resp.get("mmsi")
    if mmsi_new not in (None, ""):
        updates["mmsi"] = str(mmsi_new)
    data = resp.get("data") if isinstance(resp.get("data"), dict) else {}
    if data.get("tags"):
        updates["tags"] = data["tags"]
    if data.get("YearOfBuild") and not r.get("建造年份"):
        updates["建造年份"] = str(data["YearOfBuild"])
    if data.get("dwt") and not r.get("载重吨"):
        updates["载重吨"] = str(data["dwt"])
    archive = resp.get("archive")
    if isinstance(archive, dict) and archive:
        updates.update(archive)
        if archive.get("档案_dwt"):
            updates["载重吨"] = archive["档案_dwt"]
        if archive.get("档案_建造年"):
            updates["建造年份"] = archive["档案_建造年"]
        if archive.get("档案_船型"):
            updates["船型"] = archive["档案_船型"]
        if archive.get("档案_船名"):
            updates["船名"] = archive["档案_船名"]


def _apply_cargo_enrich_updates(updates: dict[str, Any], resp: dict[str, Any]) -> None:
    data = resp.get("data") if isinstance(resp.get("data"), dict) else {}
    if data.get("tags"):
        updates["tags"] = data["tags"]


def _commit_plate_update(
    conn: sqlite3.Connection,
    cur: sqlite3.Cursor,
    table: str,
    updates: dict[str, Any],
    message_id: str,
    row_index: Any,
) -> None:
    if not updates:
        return
    sets = ", ".join(f"{_q(k)} = ?" for k in updates)
    vals = list(updates.values()) + [message_id, row_index]
    cur.execute(
        f"UPDATE {table} SET {sets} WHERE message_id = ? AND row_index = ?",
        vals,
    )
    conn.commit()


def _row_enrich_key(row: dict[str, Any]) -> str:
    return f"{row.get('message_id')}:{row.get('row_index')}"


def _parse_schema_row_from_db_row(d: dict[str, Any], ftype: str) -> dict[str, Any]:
    pj = d.get("payload_json")
    if pj:
        try:
            parsed = json.loads(pj)
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            pass
    out: dict[str, Any] = {}
    keys = OPENVESSEL_FIELD_KEYS if ftype == "openvessel" else CARGO_FIELD_KEYS
    for k in keys:
        if k in d and d[k] not in (None, ""):
            out[k] = d[k]
    return out


def _resolve_single_portid(api_base: str, api_key: str, portname: str | None) -> str:
    """单港名 → portid（首段）。"""
    pn = _normalize_portname(portname)
    if not pn:
        return ""
    m = _fetch_portid_batch(api_base, api_key, [pn])
    raw = m.get(pn, "")
    return str(raw).split(",")[0].strip() if raw else ""


def _portid_field_map(ftype: str) -> tuple[tuple[str, str], ...]:
    """(列名, 更新键)"""
    if ftype == "openvessel":
        return (("OPEN位置", "portid"), ("卸货港", "discharging_portid"))
    return (("装货港", "portid"), ("卸货港", "discharging_portid"))


def _portid_updates_for_row(
    r: dict[str, Any],
    ftype: str,
    port_map: dict[str, str],
    api_base: str,
    api_key: str,
) -> dict[str, Any]:
    updates: dict[str, Any] = {}
    for col, key in _portid_field_map(ftype):
        pn = _normalize_portname(r.get(col))
        if not pn:
            continue
        raw = port_map.get(pn) or _resolve_single_portid(api_base, api_key, pn)
        if raw:
            updates[key] = str(raw).split(",")[0].strip()
    return updates


def _apply_portids_for_table(
    conn: sqlite3.Connection,
    cur: sqlite3.Cursor,
    table: str,
    ftype: str,
    rows: list[dict[str, Any]],
    port_map: dict[str, str],
    api_base: str,
    api_key: str,
    stats: dict[str, Any],
) -> None:
    for r in rows:
        mid, ridx = r["message_id"], r["row_index"]
        row_key = _row_enrich_key(r)
        try:
            updates = _portid_updates_for_row(r, ftype, port_map, api_base, api_key)
            if updates:
                _commit_plate_update(conn, cur, table, updates, mid, ridx)
                if ftype == "openvessel":
                    stats["openvessel_updated"] += 1
                else:
                    stats["cargo_updated"] += 1
                if "portid" in updates:
                    r["portid"] = updates["portid"]
        except Exception as e:
            stats["errors"].append(
                {"row": row_key, "kind": ftype, "step": "portid", "detail": str(e)}
            )


def _ensure_row_portid(
    conn: sqlite3.Connection,
    cur: sqlite3.Cursor,
    table: str,
    ftype: str,
    r: dict[str, Any],
    api_base: str,
    api_key: str,
) -> str:
    """查询前补全单行 portid；成功则写回库。"""
    existing = r.get("portid")
    if existing not in (None, ""):
        return str(existing)
    primary_col = "OPEN位置" if ftype == "openvessel" else "装货港"
    resolved = _resolve_single_portid(api_base, api_key, r.get(primary_col))
    if resolved:
        _commit_plate_update(
            conn, cur, table, {"portid": resolved}, r["message_id"], r["row_index"]
        )
        r["portid"] = resolved
    return resolved


def default_db_path() -> Path:
    env_path = os.environ.get("HIFLEET_CHARTER_DB_PATH", "").strip()
    if env_path:
        return Path(env_path).expanduser()
    return default_skill_dir() / "charter_facts.sqlite3"


def default_skill_dir() -> Path:
    env_path = os.environ.get("HIFLEET_MYTONNAGES_DIR", "").strip()
    if env_path:
        return Path(env_path).expanduser()
    return Path(__file__).resolve().parents[1]


def resolve_charter_api_base(cfg_value: str | None = None) -> str:
    """租船 OpenClaw 根地址：config > HIFLEET_CHARTER_API_BASE > HIFLEET_API_BASE + 路径 > 默认公网。"""
    if cfg_value and str(cfg_value).strip():
        return str(cfg_value).strip().rstrip("/")
    explicit = os.environ.get("HIFLEET_CHARTER_API_BASE", "").strip()
    if explicit:
        return explicit.rstrip("/")
    root = (os.environ.get("HIFLEET_API_BASE") or "https://api.hifleet.com").rstrip("/")
    return root + "/openclaw/vessel/charter"


def load_api_config() -> tuple[str, str]:
    api_key = os.environ.get("HIFLEET_API_KEY", "").strip()
    api_base = resolve_charter_api_base()
    cfg_path = default_skill_dir() / "config.json"
    if cfg_path.is_file():
        try:
            cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
            api_key = api_key or str(cfg.get("hifleet_api_key") or "").strip()
            api_base = resolve_charter_api_base(cfg.get("hifleet_charter_api_base"))
        except (json.JSONDecodeError, OSError):
            pass
    return api_key, api_base.rstrip("/")


def _http_post_json(url: str, body: dict[str, Any], timeout: int = 60) -> dict[str, Any]:
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _api_ok(payload: dict[str, Any]) -> bool:
    st = payload.get("status")
    return st == "1" or st == 1


def _normalize_portname(name: str | None) -> str | None:
    if not name:
        return None
    s = str(name).strip()
    if not s or s.lower() in ("null", "none", "未提及"):
        return None
    return s.replace("/", "+").replace(",", "+")


def _fetch_portid_batch(api_base: str, api_key: str, portnames: list[str]) -> dict[str, str]:
    """portname -> portid 串。"""
    unique = []
    seen: set[str] = set()
    for p in portnames:
        if p and p not in seen:
            seen.add(p)
            unique.append(p)
    if not unique:
        return {}
    joined = "+".join(unique)
    url = f"{api_base}/port/portid?{urllib.parse.urlencode({'api_key': api_key})}"
    try:
        resp = _http_post_json(url, {"portname": joined})
    except (urllib.error.URLError, json.JSONDecodeError, TimeoutError):
        return {}
    if not _api_ok(resp):
        return {}
    data = resp.get("data") or {}
    pid = data.get("portid")
    if not pid:
        return {}
    if len(unique) == 1:
        return {unique[0]: str(pid)}
    parts = [x.strip() for x in str(pid).split(",")]
    out: dict[str, str] = {}
    for i, name in enumerate(unique):
        if i < len(parts):
            out[name] = parts[i]
        else:
            out[name] = str(pid)
    return out


def _fetch_distances(
    api_base: str,
    api_key: str,
    query_portid: str,
    index_data: list[dict[str, str]],
) -> dict[str, dict[str, Any]]:
    if not query_portid or not index_data:
        return {}
    url = f"{api_base}/port-distances/batch?{urllib.parse.urlencode({'api_key': api_key})}"
    try:
        resp = _http_post_json(
            url,
            {"queryPortid": query_portid, "indexData": index_data},
        )
    except (urllib.error.URLError, json.JSONDecodeError, TimeoutError):
        return {}
    if not _api_ok(resp):
        return {}
    data = resp.get("data") or {}
    lst = data.get("list") if isinstance(data.get("list"), list) else []
    out: dict[str, dict[str, Any]] = {}
    for item in lst:
        if not isinstance(item, dict):
            continue
        idx = str(item.get("index") or "")
        if idx:
            out[idx] = item
    return out


def enrich_database(db_path: Path) -> dict[str, Any]:
    api_key, api_base = load_api_config()
    if not api_key:
        return {"ok": False, "error": "missing hifleet_api_key"}

    internal_base = resolve_enrich_row_url()
    db = CharterFactsDB(db_path)
    conn = db.connect()
    stats = {
        "openvessel_updated": 0,
        "cargo_updated": 0,
        "imos_fetched": 0,
        "imos_resolved": 0,
        "tags_vessel": 0,
        "tags_cargo": 0,
        "ports_fetched": 0,
        "errors": [],
    }
    try:
        db.init(conn)
        cur = conn.cursor()

        cur.execute('SELECT * FROM openvessel_plate')
        opv_rows = [dict(r) for r in cur.fetchall()]

        for r in opv_rows:
            mid, ridx = r["message_id"], r["row_index"]
            row_key = _row_enrich_key(r)
            try:
                updates: dict[str, Any] = {}
                parse_row = _parse_schema_row_from_db_row(r, "openvessel")
                enrich_resp = _fetch_enrich_row(
                    internal_base,
                    api_key,
                    "vessel",
                    parse_row,
                    source="parse_schema",
                    imo=r.get("IMO"),
                    mmsi=r.get("mmsi"),
                    charter_api_base=api_base,
                )
                if enrich_resp.get("_fetch_error"):
                    stats["errors"].append(
                        {
                            "row": row_key,
                            "kind": "vessel",
                            "step": "enrich_row",
                            "detail": enrich_resp["_fetch_error"],
                        }
                    )
                    enrich_resp = {}
                if enrich_resp:
                    had_imo = bool(_valid_imo_digits(r.get("IMO")))
                    _apply_vessel_enrich_updates(updates, enrich_resp, r)
                    if not had_imo and updates.get("IMO"):
                        stats["imos_resolved"] += 1
                    if updates.get("tags"):
                        stats["tags_vessel"] += 1
                    if enrich_resp.get("archive"):
                        stats["imos_fetched"] += 1
                    for w in enrich_resp.get("warnings") or []:
                        if isinstance(w, dict):
                            stats["errors"].append(
                                {**w, "row": row_key, "kind": "vessel"}
                            )

                if updates:
                    _commit_plate_update(conn, cur, "openvessel_plate", updates, mid, ridx)
                    stats["openvessel_updated"] += 1
                    if "IMO" in updates:
                        r["IMO"] = updates["IMO"]
            except Exception as e:
                stats["errors"].append(
                    {"row": row_key, "kind": "vessel", "step": "enrich", "detail": str(e)}
                )

        cur.execute('SELECT * FROM openvessel_plate')
        opv_rows = [dict(r) for r in cur.fetchall()]
        port_names: list[str] = []
        for r in opv_rows:
            for col in ("OPEN位置", "卸货港"):
                pn = _normalize_portname(r.get(col))
                if pn:
                    port_names.append(pn)

        cur.execute('SELECT * FROM cargo_plate')
        cargo_rows = [dict(r) for r in cur.fetchall()]
        for r in cargo_rows:
            for col in ("装货港", "卸货港"):
                pn = _normalize_portname(r.get(col))
                if pn:
                    port_names.append(pn)

        port_map: dict[str, str] = {}
        try:
            port_map = _fetch_portid_batch(api_base, api_key, port_names)
            stats["ports_fetched"] = len(port_map)
        except Exception as e:
            stats["errors"].append({"step": "portid_batch", "detail": str(e)})

        _apply_portids_for_table(
            conn, cur, "openvessel_plate", "openvessel",
            opv_rows, port_map, api_base, api_key, stats,
        )

        for r in cargo_rows:
            mid, ridx = r["message_id"], r["row_index"]
            row_key = _row_enrich_key(r)
            try:
                updates: dict[str, Any] = {}
                parse_row = _parse_schema_row_from_db_row(r, "cargo")
                enrich_resp = _fetch_enrich_row(
                    internal_base,
                    api_key,
                    "cargo",
                    parse_row,
                    source="parse_schema",
                )
                if enrich_resp.get("_fetch_error"):
                    stats["errors"].append(
                        {
                            "row": row_key,
                            "kind": "cargo",
                            "step": "enrich_row",
                            "detail": enrich_resp["_fetch_error"],
                        }
                    )
                    enrich_resp = {}
                if enrich_resp:
                    _apply_cargo_enrich_updates(updates, enrich_resp)
                    if updates.get("tags"):
                        stats["tags_cargo"] += 1
                    for w in enrich_resp.get("warnings") or []:
                        if isinstance(w, dict):
                            stats["errors"].append(
                                {**w, "row": row_key, "kind": "cargo"}
                            )
                if updates:
                    _commit_plate_update(conn, cur, "cargo_plate", updates, mid, ridx)
                    stats["cargo_updated"] += 1
            except Exception as e:
                stats["errors"].append(
                    {"row": row_key, "kind": "cargo", "step": "enrich_row", "detail": str(e)}
                )

        _apply_portids_for_table(
            conn, cur, "cargo_plate", "cargo",
            cargo_rows, port_map, api_base, api_key, stats,
        )
    finally:
        conn.close()
    return {"ok": True, "partial": bool(stats["errors"]), **stats}


def query_by_port(db_path: Path, port: str, limit: int = 50) -> list[dict[str, Any]]:
    api_key, api_base = load_api_config()
    if not api_key:
        return [{"_error": "missing hifleet_api_key"}]

    db = CharterFactsDB(db_path)
    conn = db.connect()
    results: list[dict[str, Any]] = []
    try:
        db.init(conn)
        cur = conn.cursor()
        q_pn = _normalize_portname(port)
        if not q_pn:
            return [{"_error": "empty port name"}]

        port_map = _fetch_portid_batch(api_base, api_key, [q_pn])
        query_portid = port_map.get(q_pn) or ""
        if not query_portid:
            query_portid = str(port_map.values())[0] if port_map else ""
        if not query_portid:
            return [{"_error": f"portid not resolved for {port}"}]
        query_portid = query_portid.split(",")[0].strip()

        candidates: list[dict[str, Any]] = []
        for table, ftype in (("openvessel_plate", "openvessel"), ("cargo_plate", "cargo")):
            cur.execute(f"SELECT * FROM {table}")
            for row in cur.fetchall():
                d = dict(row)
                d["_fact_type"] = ftype
                d["_source_table"] = table
                pid = _ensure_row_portid(conn, cur, table, ftype, d, api_base, api_key)
                if not pid:
                    continue
                candidates.append(d)

        index_data = []
        for d in candidates:
            ftype = d.get("_fact_type", "")
            idx_key = _row_index_key(
                str(d.get("message_id") or ""),
                d.get("row_index"),
                str(ftype),
            )
            pid = d.get("portid")
            if not pid:
                continue
            d["_index_key"] = idx_key
            index_data.append({"index": idx_key, "portid": str(pid)})

        dist_map = _fetch_distances(api_base, api_key, query_portid, index_data)

        for d in candidates:
            idx_key = d.get("_index_key", "")
            dist_info = dist_map.get(idx_key) or {}
            d["query_port"] = port
            d["query_portid"] = query_portid
            d["dist"] = dist_info.get("dist")
            d["nearestPortId"] = dist_info.get("nearestPortId")
            pj = d.get("payload_json")
            if pj:
                try:
                    d["payload"] = json.loads(pj)
                except json.JSONDecodeError:
                    d["payload"] = None
            results.append(d)

        results.sort(
            key=lambda x: (
                x.get("dist") is None,
                float(x.get("dist") if x.get("dist") is not None else 1e18),
            )
        )
        return results[:limit]
    finally:
        conn.close()


def cmd_save(args: argparse.Namespace) -> int:
    if args.file:
        raw = Path(args.file).read_text(encoding="utf-8")
    else:
        raw = sys.stdin.read()
    doc = json.loads(raw)
    parsed = doc.get("parsed") or doc
    db = CharterFactsDB(Path(args.db) if args.db else default_db_path())
    conn = db.connect()
    try:
        db.save_parsed(
            conn,
            message_id=doc.get("message_id") or "",
            email_date_utc=doc.get("email_date_utc") or "",
            from_addr=doc.get("from_addr") or "",
            subject=doc.get("subject") or "",
            parsed=parsed if isinstance(parsed, dict) else {},
        )
    finally:
        conn.close()
    return 0


def cmd_search(args: argparse.Namespace) -> int:
    db = CharterFactsDB(Path(args.db) if args.db else default_db_path())
    conn = db.connect()
    try:
        rows = db.search(conn, args.query, limit=args.limit)
    finally:
        conn.close()
    print(json.dumps(rows, ensure_ascii=False, indent=2, default=str))
    return 0


def cmd_enrich(args: argparse.Namespace) -> int:
    stats = enrich_database(Path(args.db) if args.db else default_db_path())
    print(json.dumps(stats, ensure_ascii=False, indent=2))
    return 0 if stats.get("ok") else 1


def cmd_query_by_port(args: argparse.Namespace) -> int:
    rows = query_by_port(
        Path(args.db) if args.db else default_db_path(),
        args.port,
        limit=args.limit,
    )
    print(json.dumps(rows, ensure_ascii=False, indent=2, default=str))
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="hifleet-mytonnages charter_facts SQLite 工具")
    sub = p.add_subparsers(dest="cmd", required=True)

    ps = sub.add_parser("save", help="从 JSON 写入（默认读标准输入，或用 -f 指定文件）")
    ps.add_argument("--db", help="sqlite3 路径（默认 hifleet-mytonnages/charter_facts.sqlite3，可用 HIFLEET_CHARTER_DB_PATH 覆盖）")
    ps.add_argument("--file", "-f", help="JSON 文件路径（未指定则从 stdin 读取）")
    ps.set_defaults(func=cmd_save)

    pr = sub.add_parser("search", help="关键词检索 search_text")
    pr.add_argument("--db", help="sqlite3 路径（默认 hifleet-mytonnages/charter_facts.sqlite3，可用 HIFLEET_CHARTER_DB_PATH 覆盖）")
    pr.add_argument("query")
    pr.add_argument("--limit", type=int, default=50)
    pr.set_defaults(func=cmd_search)

    pe = sub.add_parser(
        "enrich",
        help="enrich-row（IMO+tags+档案）+ portid 补充信息并写回本地库（须 hifleet_api_key 与公网 enrich-row）",
    )
    pe.add_argument("--db", help="sqlite3 路径")
    pe.set_defaults(func=cmd_enrich)

    pq = sub.add_parser("query-by-port", help="按查询港口距离升序返回船盘/货盘")
    pq.add_argument("--db", help="sqlite3 路径")
    pq.add_argument("--port", required=True, help="查询港口名（英文或邮件中的写法）")
    pq.add_argument("--limit", type=int, default=50)
    pq.set_defaults(func=cmd_query_by_port)

    args = p.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
