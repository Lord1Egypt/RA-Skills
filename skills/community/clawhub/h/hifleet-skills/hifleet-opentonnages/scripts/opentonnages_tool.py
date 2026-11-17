#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HiFleet public open vessel / cargo search; contacts on demand."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Optional

_SCRIPT_DIR = Path(__file__).resolve().parent
_SKILLS_SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"
for _p in (_SCRIPT_DIR, _SKILLS_SCRIPTS):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from charter_contact_dedup import dedupe_unlock_payload
from charter_enrich_helpers import (
    enrich_response_usable,
    normalize_cargo_row_for_enrich,
    normalize_vessel_row_for_enrich,
)

DEFAULT_CHARTER_BASE = "https://api.hifleet.com/openclaw/vessel/charter"
DEFAULT_LINER_BASE = "https://api.hifleet.com/openclaw/vessel/charter/liner"
DEFAULT_ENRICH_URL = "https://api.hifleet.com/openclaw/vessel/charter/enrich-row"

TYPE_CODE_VESSEL = "product_vessel_charter"
TYPE_CODE_CARGO = "product_cargo_charter"


def default_skill_dir() -> Path:
    env = os.environ.get("HIFLEET_OPENTONNAGES_DIR", "").strip()
    if env:
        return Path(env).expanduser()
    return Path(__file__).resolve().parents[1]


def load_config() -> dict[str, Any]:
    api_key = os.environ.get("HIFLEET_API_KEY", "").strip()
    api_base = os.environ.get("HIFLEET_CHARTER_API_BASE", "").strip().rstrip("/")
    liner_base = os.environ.get("HIFLEET_LINER_API_BASE", "").strip().rstrip("/")
    enrich_url = os.environ.get("HIFLEET_CHARTER_ENRICH_URL", "").strip()
    cfg_path = default_skill_dir() / "config.json"
    if cfg_path.is_file():
        try:
            cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
            if isinstance(cfg, dict):
                api_key = api_key or str(cfg.get("hifleet_api_key") or "").strip()
                if not api_base:
                    api_base = str(cfg.get("hifleet_charter_api_base") or "").strip().rstrip("/")
                if not liner_base:
                    liner_base = str(cfg.get("hifleet_liner_api_base") or "").strip().rstrip("/")
                if not enrich_url:
                    enrich_url = str(cfg.get("charter_enrich_url") or "").strip()
        except (json.JSONDecodeError, OSError):
            pass
    if not api_base:
        root = (os.environ.get("HIFLEET_API_BASE") or "https://api.hifleet.com").rstrip("/")
        api_base = root + "/openclaw/vessel/charter"
    if not liner_base:
        liner_base = DEFAULT_LINER_BASE
    if not enrich_url:
        enrich_url = DEFAULT_ENRICH_URL
    return {
        "api_key": api_key,
        "api_base": api_base.rstrip("/"),
        "liner_base": liner_base.rstrip("/"),
        "enrich_url": enrich_url,
    }


def _http_post_json(url: str, body: dict[str, Any], timeout: int = 90) -> dict[str, Any]:
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _extract_rows(payload: dict[str, Any]) -> tuple[list[dict[str, Any]], int]:
    total = 0
    if isinstance(payload.get("total"), (int, float)):
        total = int(payload["total"])
    data = payload.get("data")
    if isinstance(data, list):
        rows = [x for x in data if isinstance(x, dict)]
        if not total:
            total = len(rows)
        return rows, total
    if isinstance(data, dict):
        for key in ("list", "rows", "data"):
            inner = data.get(key)
            if isinstance(inner, list):
                rows = [x for x in inner if isinstance(x, dict)]
                if not total and isinstance(data.get("total"), (int, float)):
                    total = int(data["total"])
                if not total:
                    total = len(rows)
                return rows, total
    return [], total


def _api_ok(payload: dict[str, Any]) -> bool:
    st = payload.get("status")
    if st in (1, "1", "ok", "OK", True):
        return True
    if payload.get("code") in (0, 200, "200"):
        return True
    if "data" in payload:
        return True
    return False


def paginated_search(
    endpoint: str,
    *,
    params: dict[str, Any],
    filter_labels: Optional[dict[str, Any]] = None,
    page_limit: int = 200,
    max_pages: int = 500,
) -> dict[str, Any]:
    cfg = load_config()
    api_key = cfg["api_key"]
    if not api_key:
        return {"ok": False, "error": "missing hifleet_api_key"}

    base = cfg["api_base"]
    url = f"{base}/{endpoint.lstrip('/')}?{urllib.parse.urlencode({'api_key': api_key})}"
    merged_params = {"isPublic": True, "isDuplicate": False, **params}
    fl = filter_labels or {}

    all_rows: list[dict[str, Any]] = []
    total_expected: Optional[int] = None
    offset = 1
    pages = 0
    last_payload: dict[str, Any] = {}

    while pages < max_pages:
        body: dict[str, Any] = {
            "offset": offset,
            "limit": page_limit,
            "params": merged_params,
            "filterLabels": fl,
        }
        try:
            last_payload = _http_post_json(url, body)
        except urllib.error.HTTPError as e:
            try:
                detail = e.read().decode("utf-8", errors="replace")
            except Exception:
                detail = str(e)
            return {"ok": False, "error": f"HTTP {e.code}", "detail": detail}
        except Exception as e:
            return {"ok": False, "error": str(e)}

        if not _api_ok(last_payload):
            return {
                "ok": False,
                "error": last_payload.get("message") or last_payload.get("msg") or "api_failed",
                "payload": last_payload,
            }

        chunk, total = _extract_rows(last_payload)
        if total_expected is None and total:
            total_expected = total
        if not chunk:
            break
        all_rows.extend(chunk)
        pages += 1
        if total_expected and len(all_rows) >= total_expected:
            break
        if len(chunk) < page_limit:
            break
        offset += page_limit

    stat = last_payload.get("stat")
    return {
        "ok": True,
        "endpoint": endpoint,
        "total": total_expected if total_expected is not None else len(all_rows),
        "count": len(all_rows),
        "stat": stat,
        "data": all_rows,
        "pages_fetched": pages,
    }


def _http_get_json(url: str, headers: Optional[dict[str, str]] = None, timeout: int = 90) -> dict[str, Any]:
    req = urllib.request.Request(url, method="GET", headers=headers or {})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def port_suggest(keyword: str, *, size: int = 1) -> dict[str, Any]:
    """GET {liner}/ports/suggest — resolve portId for params.portid."""
    cfg = load_config()
    api_key = cfg["api_key"]
    if not api_key:
        return {"ok": False, "error": "missing hifleet_api_key"}
    kw = (keyword or "").strip()
    if not kw:
        return {"ok": False, "error": "keyword required (English port name)"}
    qs = urllib.parse.urlencode(
        {"keyword": kw, "from": 0, "size": max(1, size), "api_key": api_key}
    )
    url = f"{cfg['liner_base']}/ports/suggest?{qs}"
    headers = {"api_key": api_key}
    try:
        resp = _http_get_json(url, headers=headers)
    except urllib.error.HTTPError as e:
        try:
            detail = e.read().decode("utf-8", errors="replace")
        except Exception:
            detail = str(e)
        return {"ok": False, "error": f"HTTP {e.code}", "detail": detail}
    except Exception as e:
        return {"ok": False, "error": str(e)}
    data = resp.get("data")
    ports: list[dict[str, Any]] = []
    if isinstance(data, list):
        ports = [x for x in data if isinstance(x, dict)]
    return {"ok": True, "keyword": kw, "ports": ports, "payload": resp}


def _http_post_empty(url: str, timeout: int = 90) -> dict[str, Any]:
    req = urllib.request.Request(url, data=b"", method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def type_code_for_kind(kind: str) -> str:
    k = (kind or "").strip().lower()
    if k in ("cargo", "g"):
        return TYPE_CODE_CARGO
    return TYPE_CODE_VESSEL


def fetch_contacts(data_id: str, *, kind: str = "vessel") -> dict[str, Any]:
    """POST {liner}/unlock — internal API; user-facing text: 获取联系方式."""
    cfg = load_config()
    api_key = cfg["api_key"]
    if not api_key:
        return {"ok": False, "error": "missing hifleet_api_key"}
    rid = str(data_id or "").strip()
    if not rid:
        return {"ok": False, "error": "record id required"}
    type_code = type_code_for_kind(kind)
    base = cfg["liner_base"]
    qs = urllib.parse.urlencode(
        {"dataId": rid, "typeCode": type_code, "api_key": api_key}
    )
    url = f"{base}/unlock?{qs}"
    try:
        resp = _http_post_empty(url)
    except urllib.error.HTTPError as e:
        try:
            detail = e.read().decode("utf-8", errors="replace")
        except Exception:
            detail = str(e)
        return {"ok": False, "error": f"HTTP {e.code}", "detail": detail}
    except Exception as e:
        return {"ok": False, "error": str(e)}
    deduped = dedupe_unlock_payload(resp)
    return {
        "ok": True,
        "dataId": rid,
        "kind": kind,
        "typeCode": type_code,
        "contacts": resp,
        "contacts_deduped": deduped.get("contacts_deduped", []),
        "deduped_count": deduped.get("deduped_count", 0),
        "original_contact_count": deduped.get("original_contact_count", 0),
    }


def fetch_contacts_batch(ids: list[str], *, kind: str = "vessel") -> dict[str, Any]:
    results: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    for rid in ids:
        r = fetch_contacts(rid, kind=kind)
        if r.get("ok"):
            results.append(r)
        else:
            errors.append({"dataId": rid, **r})
    return {
        "ok": not errors or bool(results),
        "count": len(results),
        "results": results,
        "errors": errors,
    }


def enrich_row(
    kind: str,
    row: dict[str, Any],
    *,
    query_port: str = "",
) -> dict[str, Any]:
    cfg = load_config()
    api_key = cfg["api_key"]
    if not api_key:
        return {"ok": False, "error": "missing hifleet_api_key"}
    url = cfg["enrich_url"]
    if "?" not in url:
        url = f"{url}?{urllib.parse.urlencode({'api_key': api_key})}"

    k = (kind or "").strip().lower()
    imo: Any = None
    mmsi: Any = None
    if k in ("cargo", "g"):
        mapped_row = normalize_cargo_row_for_enrich(row)
    else:
        mapped_row, imo, mmsi = normalize_vessel_row_for_enrich(row)

    body: dict[str, Any] = {
        "kind": "cargo" if k in ("cargo", "g") else "vessel",
        "source": "parse_schema",
        "row": mapped_row,
        "include_archive": True,
        "charter_api_base": cfg["api_base"],
    }
    if imo:
        body["imo"] = imo
    if mmsi:
        body["mmsi"] = mmsi
    if query_port:
        body["query_port"] = query_port
    try:
        resp = _http_post_json(url, body)
    except Exception as e:
        return {"ok": False, "error": str(e)}
    if not enrich_response_usable(resp):
        return {
            "ok": False,
            "error": resp.get("message") or resp.get("error") or resp.get("msg") or "enrich_empty",
            "enrich": resp,
            "request_row": mapped_row,
        }
    return {"ok": True, "enrich": resp, "request_row": mapped_row}


def cmd_search_vessels(args: argparse.Namespace) -> int:
    params: dict[str, Any] = {}
    if args.keyword:
        params["keyword"] = args.keyword
    if args.open_port:
        params["openPort"] = args.open_port
    if args.portid:
        params["portid"] = args.portid
    if args.shiptype:
        params["shiptype"] = args.shiptype
    if args.open_date_start:
        params["openDateStart"] = args.open_date_start
    if args.open_date_end:
        params["openDateEnd"] = args.open_date_end
    result = paginated_search("vessels/search", params=params, page_limit=args.limit)
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    return 0 if result.get("ok") else 1


def cmd_search_cargo(args: argparse.Namespace) -> int:
    params: dict[str, Any] = {}
    if args.keyword:
        params["keyword"] = args.keyword
    if args.load_port:
        params["openPort"] = args.load_port
    if args.portid:
        params["portid"] = args.portid
    if args.discharge_portid:
        params["dischargingPortid"] = args.discharge_portid
    if args.laycan_start:
        params["laycanStart"] = args.laycan_start
    if args.laycan_end:
        params["laycanEnd"] = args.laycan_end
    result = paginated_search("cargo/search", params=params, page_limit=args.limit)
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    return 0 if result.get("ok") else 1


def cmd_ports_suggest(args: argparse.Namespace) -> int:
    result = port_suggest(args.keyword, size=args.size)
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    return 0 if result.get("ok") else 1


def cmd_fetch_contacts(args: argparse.Namespace) -> int:
    if args.all_from_file:
        data = json.loads(Path(args.all_from_file).read_text(encoding="utf-8"))
        ids: list[str] = []
        if isinstance(data, list):
            for row in data:
                if isinstance(row, dict) and row.get("id") is not None:
                    ids.append(str(row["id"]))
        elif isinstance(data, dict):
            for row in data.get("data") or []:
                if isinstance(row, dict) and row.get("id") is not None:
                    ids.append(str(row["id"]))
        result = fetch_contacts_batch(ids, kind=args.kind)
    else:
        if not args.id:
            print(json.dumps({"ok": False, "error": "record id required"}, ensure_ascii=False))
            return 1
        result = fetch_contacts(args.id, kind=args.kind)
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    return 0 if result.get("ok") else 1


def cmd_enrich(args: argparse.Namespace) -> int:
    row = json.loads(Path(args.file).read_text(encoding="utf-8"))
    if not isinstance(row, dict):
        print(json.dumps({"ok": False, "error": "row must be JSON object"}, ensure_ascii=False))
        return 1
    result = enrich_row(args.kind, row, query_port=args.query_port or "")
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    return 0 if result.get("ok") else 1


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="hifleet-opentonnages public vessel/cargo search")
    sub = p.add_subparsers(dest="cmd", required=True)

    pp = sub.add_parser("ports-suggest", help="GET {liner}/ports/suggest → portId")
    pp.add_argument("--keyword", required=True, help="English port name e.g. Tianjin")
    pp.add_argument("--size", type=int, default=1)
    pp.set_defaults(func=cmd_ports_suggest)

    sv = sub.add_parser("search-vessels", help="POST /vessels/search (full pagination)")
    sv.add_argument("--keyword", default="")
    sv.add_argument("--open-port", default="")
    sv.add_argument("--portid", default="")
    sv.add_argument("--shiptype", default="")
    sv.add_argument("--open-date-start", default="")
    sv.add_argument("--open-date-end", default="")
    sv.add_argument("--limit", type=int, default=200, help="page size")
    sv.set_defaults(func=cmd_search_vessels)

    sc = sub.add_parser("search-cargo", help="POST /cargo/search (full pagination)")
    sc.add_argument("--keyword", default="")
    sc.add_argument("--load-port", default="")
    sc.add_argument("--portid", default="")
    sc.add_argument("--discharge-portid", default="")
    sc.add_argument("--laycan-start", default="")
    sc.add_argument("--laycan-end", default="")
    sc.add_argument("--limit", type=int, default=200)
    sc.set_defaults(func=cmd_search_cargo)

    pe = sub.add_parser("enrich", help="POST enrich-row for one mapped row")
    pe.add_argument("--kind", choices=("vessel", "cargo"), required=True)
    pe.add_argument("--file", "-f", required=True, help="JSON row file")
    pe.add_argument("--query-port", default="")
    pe.set_defaults(func=cmd_enrich)

    pf = sub.add_parser("fetch-contacts", help="POST /unlock for contact details (by record id)")
    pf.add_argument("--kind", choices=("vessel", "cargo"), default="vessel")
    pf.add_argument("--id", default="", help="Record id from list response")
    pf.add_argument(
        "--all-from-file",
        default="",
        help="JSON file from search (list or {data:[]}) — fetch all ids",
    )
    pf.set_defaults(func=cmd_fetch_contacts)

    args = p.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
