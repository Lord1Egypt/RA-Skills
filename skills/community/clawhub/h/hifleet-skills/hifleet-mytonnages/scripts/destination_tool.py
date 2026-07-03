#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HiFleet pre-arrival (destination) search; contacts on demand via /unlock."""

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
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

DEFAULT_CHARTER_BASE = "https://api.hifleet.com/openclaw/vessel/charter"
DEFAULT_LINER_BASE = "https://api.hifleet.com/openclaw/vessel/charter/liner"
TYPE_CODE_PRE_ARRIVAL = "product_will_arrive_charter"


def default_skill_dir() -> Path:
    env = os.environ.get("HIFLEET_MYTONNAGES_DIR", "").strip()
    if env:
        return Path(env).expanduser()
    return Path(__file__).resolve().parents[1]


def load_config() -> dict[str, Any]:
    api_key = os.environ.get("HIFLEET_API_KEY", "").strip()
    api_base = os.environ.get("HIFLEET_CHARTER_API_BASE", "").strip().rstrip("/")
    liner_base = os.environ.get("HIFLEET_LINER_API_BASE", "").strip().rstrip("/")
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
        except (json.JSONDecodeError, OSError):
            pass
    if not api_base:
        root = (os.environ.get("HIFLEET_API_BASE") or "https://api.hifleet.com").rstrip("/")
        api_base = root + "/openclaw/vessel/charter"
    if not liner_base:
        liner_base = DEFAULT_LINER_BASE
    return {
        "api_key": api_key,
        "api_base": api_base.rstrip("/"),
        "liner_base": liner_base.rstrip("/"),
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


def _http_post_empty(url: str, timeout: int = 90) -> dict[str, Any]:
    req = urllib.request.Request(url, data=b"", method="POST")
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
        {
            "keyword": kw,
            "from": 0,
            "size": max(1, size),
            "api_key": api_key,
        }
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


def paginated_destination_search(
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
    url = f"{base}/destination/search?{urllib.parse.urlencode({'api_key': api_key})}"
    fl = filter_labels if filter_labels is not None else {}
    merged_params = {"isPublic": True, **params}

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

    return {
        "ok": True,
        "endpoint": "destination/search",
        "total": total_expected if total_expected is not None else len(all_rows),
        "count": len(all_rows),
        "stat": last_payload.get("stat"),
        "data": all_rows,
        "pages_fetched": pages,
    }


def fetch_contacts(data_id: str) -> dict[str, Any]:
    """POST {liner}/unlock — typeCode product_will_arrive_charter."""
    cfg = load_config()
    api_key = cfg["api_key"]
    if not api_key:
        return {"ok": False, "error": "missing hifleet_api_key"}
    rid = str(data_id or "").strip()
    if not rid:
        return {"ok": False, "error": "record id required"}
    qs = urllib.parse.urlencode(
        {
            "dataId": rid,
            "typeCode": TYPE_CODE_PRE_ARRIVAL,
            "api_key": api_key,
        }
    )
    url = f"{cfg['liner_base']}/unlock?{qs}"
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
    return {
        "ok": True,
        "dataId": rid,
        "typeCode": TYPE_CODE_PRE_ARRIVAL,
        "contacts": resp,
    }


def fetch_contacts_batch(ids: list[str]) -> dict[str, Any]:
    results: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    for rid in ids:
        r = fetch_contacts(rid)
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


def _ids_from_json_file(path: Path) -> list[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    ids: list[str] = []
    if isinstance(data, list):
        rows = data
    elif isinstance(data, dict):
        rows = data.get("data") or []
    else:
        return ids
    for row in rows:
        if isinstance(row, dict) and row.get("id") is not None:
            ids.append(str(row["id"]))
    return ids


def cmd_search(args: argparse.Namespace) -> int:
    params: dict[str, Any] = {}
    if args.portid:
        params["portid"] = str(args.portid).strip()
    if args.sortcolumn:
        params["sortcolumn"] = args.sortcolumn
    if args.sorttype:
        params["sorttype"] = args.sorttype
    if not params.get("portid"):
        print(json.dumps({"ok": False, "error": "portid required"}, ensure_ascii=False))
        return 1
    fl: dict[str, Any] = {}
    if args.filter_labels_file:
        fl = json.loads(Path(args.filter_labels_file).read_text(encoding="utf-8"))
    result = paginated_destination_search(
        params=params,
        filter_labels=fl,
        page_limit=args.limit,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    return 0 if result.get("ok") else 1


def cmd_ports_suggest(args: argparse.Namespace) -> int:
    result = port_suggest(args.keyword, size=args.size)
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    return 0 if result.get("ok") else 1


def cmd_fetch_contacts(args: argparse.Namespace) -> int:
    if args.all_from_file:
        ids = _ids_from_json_file(Path(args.all_from_file))
        result = fetch_contacts_batch(ids)
    else:
        if not args.id:
            print(json.dumps({"ok": False, "error": "record id required"}, ensure_ascii=False))
            return 1
        result = fetch_contacts(args.id)
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    return 0 if result.get("ok") else 1


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="hifleet-mytonnages pre-arrival search + contacts")
    sub = p.add_subparsers(dest="cmd", required=True)

    pp = sub.add_parser("ports-suggest", help="GET {liner}/ports/suggest → portId")
    pp.add_argument("--keyword", required=True, help="English port name e.g. Tianjin")
    pp.add_argument("--size", type=int, default=1)
    pp.set_defaults(func=cmd_ports_suggest)

    ps = sub.add_parser("search", help="POST /destination/search (full pagination)")
    ps.add_argument("--portid", required=True, help="Port id from ports-suggest (e.g. 15843)")
    ps.add_argument("--sortcolumn", default="dist")
    ps.add_argument("--sorttype", default="asc", choices=("asc", "desc"))
    ps.add_argument("--limit", type=int, default=200, help="page size")
    ps.add_argument("--filter-labels-file", default="", help="JSON object for filterLabels")
    ps.set_defaults(func=cmd_search)

    pf = sub.add_parser("fetch-contacts", help="POST /unlock (product_will_arrive_charter)")
    pf.add_argument("--id", default="", help="Record id from list response")
    pf.add_argument(
        "--all-from-file",
        default="",
        help="JSON from search (list or {data:[]}) — fetch all ids",
    )
    pf.set_defaults(func=cmd_fetch_contacts)

    args = p.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
