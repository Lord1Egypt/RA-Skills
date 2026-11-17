#!/usr/bin/env python3
"""
Read-only status of Excavationpro music lattice surfaces.
No publish. Optional network checks of public HTTPS endpoints.
"""
from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PORTAL = ROOT / "references" / "MUSIC_PORTAL.json"


def http_ok(url: str, timeout: int = 25) -> dict:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "lygo-excavationpro-music-lattice/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return {"url": url, "status": r.status, "ok": 200 <= r.status < 400, "bytes": int(r.headers.get("Content-Length") or 0)}
    except Exception as e:
        return {"url": url, "ok": False, "error": str(e)[:200]}


def main() -> int:
    portal = json.loads(PORTAL.read_text(encoding="utf-8"))
    pub = portal.get("public") or {}
    live = portal.get("live_portals") or {}

    out = {
        "signature": portal.get("signature"),
        "version": portal.get("version"),
        "public_checks": {},
        "live_portals": live,
        "local_stack": None,
    }

    # public surfaces
    for key in ("listen", "catalog", "sovereign_vault", "eternal_haven", "playlist_json", "ads_txt", "sitemap"):
        url = pub.get(key)
        if url:
            out["public_checks"][key] = http_ok(url)

    # sample stream head
    base = pub.get("hf_stream_base")
    if base:
        # probe playlist for one track if stack present; else dataset page
        sample = None
        try:
            from _stack_paths import resolve_stack_root

            stack = resolve_stack_root()
            pl_path = stack / "data" / "music_catalog" / "public_stream_playlist.json"
            if pl_path.exists():
                pl = json.loads(pl_path.read_text(encoding="utf-8"))
                tracks = pl.get("tracks") or []
                out["local_stack"] = {
                    "root": str(stack),
                    "tracks": len(tracks),
                    "playable": sum(1 for t in tracks if t.get("stream_url")),
                    "gb": (pl.get("stats") or {}).get("total_stream_gb"),
                    "merkle": None,
                }
                vault = stack / "data" / "music_catalog" / "music_vault_manifest.json"
                if vault.exists():
                    v = json.loads(vault.read_text(encoding="utf-8"))
                    out["local_stack"]["merkle"] = v.get("merkle_root")
                    out["local_stack"]["vault_objects"] = (v.get("stats") or {}).get("unique_objects")
                for t in tracks:
                    if t.get("stream_url"):
                        sample = t["stream_url"]
                        break
        except SystemExit:
            out["local_stack"] = {"note": "set LYGO_STACK_ROOT for local playlist stats"}
        if sample:
            req = urllib.request.Request(
                sample,
                headers={"User-Agent": "lygo-excavationpro-music-lattice/1.0", "Range": "bytes=0-1023"},
            )
            try:
                with urllib.request.urlopen(req, timeout=30) as r:
                    out["public_checks"]["sample_stream"] = {
                        "url": sample[:120] + "…",
                        "status": r.status,
                        "ok": r.status in (200, 206),
                        "bytes_read": len(r.read()),
                    }
            except Exception as e:
                out["public_checks"]["sample_stream"] = {"ok": False, "error": str(e)[:200]}

    out["human_links"] = {
        "listen": pub.get("listen"),
        "donate": pub.get("donate_paypal"),
        "kick": live.get("kick"),
        "rumble_live": live.get("rumble_live"),
        "twitch": live.get("twitch"),
    }

    print(json.dumps(out, indent=2))
    fails = [k for k, v in (out.get("public_checks") or {}).items() if isinstance(v, dict) and not v.get("ok")]
    return 1 if fails else 0


if __name__ == "__main__":
    # allow import of sibling _stack_paths
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    raise SystemExit(main())
