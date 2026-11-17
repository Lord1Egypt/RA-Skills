#!/usr/bin/env python3
"""LYGO Public Witness — public=REFERENCE, lattice=CANON.

Subcommands: doctrine, canon, reference, overlay, propose, ollama
HTTPS GET allowlist only. Optional localhost Ollama. No live Star Chart write.
Signature: Delta9Phi963-PUBLIC-WITNESS-v1.0.0
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

SIG = "Delta9Phi963-PUBLIC-WITNESS-v1.0.0"
VERSION = "1.0.0"
UA = "LYGO-PublicWitness/1.0.0 (+https://chatagent.ca/witness/; +https://clawhub.ai/deepseekoracle)"

CANON: list[dict[str, str]] = [
    {
        "id": "immutable_anchors",
        "url": "https://deepseekoracle.github.io/lygo-protocol-stack/network_builder/IMMUTABLE_ANCHORS.json",
        "role": "link_ledger",
    },
    {
        "id": "haven_star_feed",
        "url": "https://deepseekoracle.github.io/lygo-protocol-stack/haven_star_chart/haven_star_chart_feed.json",
        "role": "star_ledger",
    },
    {
        "id": "agora_pulse",
        "url": "https://deepseekoracle.github.io/lygo-protocol-stack/agent-agora/api/pulse.json",
        "role": "agent_square_pulse",
    },
    {
        "id": "git_lattice_overview",
        "url": "https://deepseekoracle.github.io/lygo-protocol-stack/GIT_LATTICE_OVERVIEW.json",
        "role": "lattice_map",
    },
    {
        "id": "kernel_egg_page",
        "url": "https://deepseekoracle.github.io/lygo-protocol-stack/KernelEggRetrieval.html",
        "role": "eggs_surface",
    },
]

REFERENCE: list[dict[str, str]] = [
    {
        "id": "usgs_quakes_2_5_day",
        "url": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson",
        "role": "quakes",
    },
    {
        "id": "nasa_eonet_open",
        "url": "https://eonet.gsfc.nasa.gov/api/v3/events?status=open&limit=40",
        "role": "natural_events",
    },
    {
        "id": "iss_wheretheiss",
        "url": "https://api.wheretheiss.at/v1/satellites/25544",
        "role": "iss",
    },
]

# FULL zip may add these; tentacle refuses unless --i-full-feeds and URL still allowlisted.
FULL_REFERENCE: list[dict[str, str]] = [
    {
        "id": "celestrak_stations",
        "url": "https://celestrak.org/NORAD/elements/gp.php?GROUP=stations&FORMAT=json",
        "role": "tle_stations",
    }
]

DOCTRINE = {
    "signature": SIG,
    "public_is": "REFERENCE",
    "lattice_is": "CANON",
    "rule": "If the data never reaches a public source, do not invent it. Empty layer beats a pretty lie.",
    "not": [
        "private intelligence",
        "Palantir clone",
        "classified satellite video",
        "World Monitor clone",
        "God's Eye View clone",
        "live Star Chart ingest",
    ],
    "site": "https://chatagent.ca/witness/",
    "mirror": "https://eternalhaven.ca/witness/",
    "skillhub_full": "https://chatagent.ca/lygoskillhub.html#full-lygo",
    "star_chart": "https://deepseekoracle.github.io/lygo-protocol-stack/HavenStarChart.html",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def https_only(url: str) -> bool:
    try:
        p = urlparse(url)
        return p.scheme == "https" and bool(p.netloc)
    except Exception:
        return False


def allowlisted(url: str, table: list[dict[str, str]]) -> bool:
    return any(url == row["url"] for row in table)


def fetch(url: str, timeout: float = 20.0) -> dict[str, Any]:
    if not https_only(url):
        return {"ok": False, "status": 0, "error": "https_only", "bytes": 0, "sha256": None, "json": None}
    req = urllib.request.Request(url, headers={"User-Agent": UA}, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read()
            sample = body[: 2_000_000]
            parsed = None
            if url.split("?")[0].endswith((".json", ".geojson")) or "format=json" in url or "api/v3" in url or "satellites" in url:
                try:
                    parsed = json.loads(sample.decode("utf-8", errors="replace"))
                except Exception:
                    parsed = None
            return {
                "ok": 200 <= resp.status < 400,
                "status": resp.status,
                "error": None,
                "bytes": len(body),
                "sha256": hashlib.sha256(sample).hexdigest() if sample else None,
                "json": parsed,
            }
    except urllib.error.HTTPError as e:
        return {"ok": False, "status": e.code, "error": str(e), "bytes": 0, "sha256": None, "json": None}
    except Exception as e:
        return {"ok": False, "status": 0, "error": str(e), "bytes": 0, "sha256": None, "json": None}


def summarize_canon(row: dict[str, str], got: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {
        "id": row["id"],
        "class": "CANON",
        "url": row["url"],
        "ok": got.get("ok"),
        "status": got.get("status"),
        "error": got.get("error"),
        "sha256": got.get("sha256"),
        "bytes": got.get("bytes"),
    }
    js = got.get("json")
    if not isinstance(js, dict):
        return out
    if row["id"] == "immutable_anchors":
        buckets = js.get("immutable_anchors") or {}
        n = sum(len(v) for v in buckets.values() if isinstance(v, list))
        out["anchor_count"] = n
        out["signature"] = js.get("signature")
    elif row["id"] == "haven_star_feed":
        out["chain_valid"] = js.get("chain_valid")
        out["entry_count"] = js.get("entry_count")
        out["sample"] = [
            {
                "node_id": e.get("node_id"),
                "node_name": e.get("node_name"),
                "status": e.get("status"),
                "kind": e.get("kind"),
            }
            for e in (js.get("entries") or [])[:8]
            if isinstance(e, dict)
        ]
    elif row["id"] == "agora_pulse":
        out["signature"] = js.get("signature")
        out["keys"] = sorted(list(js.keys()))[:12]
    elif row["id"] == "git_lattice_overview":
        out["keys"] = sorted(list(js.keys()))[:16]
    return out


def summarize_ref(row: dict[str, str], got: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {
        "id": row["id"],
        "class": "REFERENCE",
        "url": row["url"],
        "ok": got.get("ok"),
        "status": got.get("status"),
        "error": got.get("error"),
        "sha256": got.get("sha256"),
        "bytes": got.get("bytes"),
        "points": [],
    }
    js = got.get("json")
    if not got.get("ok"):
        out["note"] = "source unreachable — layer empty, not invented"
        return out
    if row["id"].startswith("usgs") and isinstance(js, dict):
        for f in (js.get("features") or [])[:40]:
            if not isinstance(f, dict):
                continue
            geom = f.get("geometry") or {}
            coords = geom.get("coordinates") or [None, None]
            props = f.get("properties") or {}
            out["points"].append(
                {
                    "lat": coords[1],
                    "lon": coords[0],
                    "mag": props.get("mag"),
                    "place": props.get("place"),
                    "class": "REFERENCE",
                }
            )
    elif row["id"].startswith("nasa_eonet") and isinstance(js, dict):
        for ev in (js.get("events") or [])[:40]:
            if not isinstance(ev, dict):
                continue
            geos = ev.get("geometry") or []
            geo = geos[-1] if geos else {}
            coords = (geo.get("coordinates") if isinstance(geo, dict) else None) or [None, None]
            out["points"].append(
                {
                    "lat": coords[1] if len(coords) > 1 else None,
                    "lon": coords[0] if coords else None,
                    "title": ev.get("title"),
                    "class": "REFERENCE",
                }
            )
    elif row["id"].startswith("iss") and isinstance(js, dict):
        out["points"].append(
            {
                "lat": js.get("latitude"),
                "lon": js.get("longitude"),
                "name": "ISS",
                "class": "REFERENCE",
            }
        )
    elif row["id"].startswith("celestrak") and isinstance(js, list):
        out["count"] = len(js)
        out["note"] = "TLE JSON is REFERENCE orbital elements, not classified video"
    return out


def pull(table: list[dict[str, str]], summarizer) -> list[dict[str, Any]]:
    rows = []
    for spec in table:
        if not allowlisted(spec["url"], table):
            rows.append({"id": spec["id"], "ok": False, "error": "not_allowlisted"})
            continue
        got = fetch(spec["url"])
        rows.append(summarizer(spec, got))
    return rows


def maybe_write(path: str | None, payload: dict[str, Any]) -> None:
    if not path:
        return
    p = Path(path)
    if ".." in p.parts:
        raise SystemExit("write path rejects ..")
    p.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def cmd_doctrine(_: argparse.Namespace) -> dict[str, Any]:
    return {"ok": True, **DOCTRINE, "utc": utc_now(), "version": VERSION}


def cmd_canon(args: argparse.Namespace) -> dict[str, Any]:
    rows = pull(CANON, summarize_canon)
    payload = {
        "ok": any(r.get("ok") for r in rows),
        "class": "CANON",
        "signature": SIG,
        "utc": utc_now(),
        "sources": rows,
        "live_star_chart_write": False,
    }
    maybe_write(getattr(args, "write_report", None), payload)
    return payload


def cmd_reference(args: argparse.Namespace) -> dict[str, Any]:
    table = list(REFERENCE)
    if getattr(args, "i_full_feeds", False):
        table.extend(FULL_REFERENCE)
    rows = pull(table, summarize_ref)
    payload = {
        "ok": any(r.get("ok") for r in rows),
        "class": "REFERENCE",
        "signature": SIG,
        "utc": utc_now(),
        "sources": rows,
        "note": "REFERENCE does not upgrade to CANON in this skill",
    }
    maybe_write(getattr(args, "write_report", None), payload)
    return payload


def cmd_overlay(args: argparse.Namespace) -> dict[str, Any]:
    payload = {
        "ok": True,
        "signature": SIG,
        "utc": utc_now(),
        "doctrine": DOCTRINE,
        "canon": cmd_canon(args),
        "reference": cmd_reference(args),
        "live_star_chart_write": False,
        "site": DOCTRINE["site"],
    }
    payload["ok"] = bool(payload["canon"].get("ok") or payload["reference"].get("ok"))
    maybe_write(getattr(args, "write_report", None), payload)
    return payload


def cmd_propose(args: argparse.Namespace) -> dict[str, Any]:
    agent = (args.agent_id or "UNSET-AGENT").strip()[:64]
    payload = {
        "ok": True,
        "signature": SIG,
        "utc": utc_now(),
        "live_write": {"requested": False, "performed": False},
        "proposal": {
            "kind": "public_witness_overlay",
            "agent_id": agent,
            "display_name": args.display_name or agent,
            "note": "Public overlay is REFERENCE. Do not ingest USGS/EONET/ISS as Haven Star Chart canon.",
            "site": DOCTRINE["site"],
            "skill": "lygo-public-witness",
        },
        "next": "Human may pair lygo-haven-star-chart with --i-consent. This skill never submits.",
    }
    if getattr(args, "i_consent", False):
        payload["consent_recorded"] = True
        payload["live_write"]["requested"] = True
        payload["live_write"]["performed"] = False
        payload["live_write"]["reason"] = "public_witness_forbids_live_ingest"
    maybe_write(getattr(args, "write", None), payload)
    return payload


def cmd_ollama(args: argparse.Namespace) -> dict[str, Any]:
    overlay = {
        "doctrine": "public=REFERENCE lattice=CANON",
        "hint": "Do not invent sources. Summarize only.",
    }
    body = json.dumps(
        {
            "model": args.model or "llama3.2:1b",
            "stream": False,
            "prompt": "LYGO Public Witness. "
            + json.dumps(overlay)
            + " Six short bullets. Never claim classified data.",
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        "http://127.0.0.1:11434/api/generate",
        data=body,
        headers={"Content-Type": "application/json", "User-Agent": UA},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            raw = resp.read()
            parsed = json.loads(raw.decode("utf-8", errors="replace"))
            return {
                "ok": True,
                "class": "LOCAL_OPTIONAL",
                "host": "127.0.0.1:11434",
                "response": parsed.get("response"),
                "note": "Local draft only. Not canon.",
            }
    except Exception as e:
        return {
            "ok": False,
            "class": "LOCAL_OPTIONAL",
            "error": str(e),
            "note": "Ollama optional. Witness still valid without it.",
        }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="witness_cli")
    p.add_argument("--json", action="store_true")
    p.add_argument("--write-report", default=None)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("doctrine")
    sub.add_parser("canon")
    r = sub.add_parser("reference")
    r.add_argument("--i-full-feeds", action="store_true", help="FULL zip extra allowlist (Celestrak)")
    o = sub.add_parser("overlay")
    o.add_argument("--i-full-feeds", action="store_true")
    pr = sub.add_parser("propose")
    pr.add_argument("--agent-id", default="WITNESS-AGENT")
    pr.add_argument("--display-name", default=None)
    pr.add_argument("--i-consent", action="store_true")
    pr.add_argument("--write", default=None)
    ol = sub.add_parser("ollama")
    ol.add_argument("--model", default="llama3.2:1b")
    args = p.parse_args(argv)
    fn = {
        "doctrine": cmd_doctrine,
        "canon": cmd_canon,
        "reference": cmd_reference,
        "overlay": cmd_overlay,
        "propose": cmd_propose,
        "ollama": cmd_ollama,
    }[args.cmd]
    result = fn(args)
    print(json.dumps(result, indent=2))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
