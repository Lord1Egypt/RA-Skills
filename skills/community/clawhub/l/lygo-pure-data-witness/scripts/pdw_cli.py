#!/usr/bin/env python3
"""ClawHub CLI for Pure-Data Witness (in-package)."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from pure_data_safety import check_url  # noqa: E402
from pure_data_witness import (  # noqa: E402
    continuum_claims,
    digest_file,
    fetch_url,
    make_egg,
    rebuild_ledger,
    verify_card,
)


def main() -> int:
    ap = argparse.ArgumentParser(description="lygo-pure-data-witness")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("digest")
    p.add_argument("--file", required=True)
    p.add_argument("--out", default="./pdw_out")

    p = sub.add_parser("fetch")
    p.add_argument("--url", required=True)
    p.add_argument("--out", default="./pdw_out")
    p.add_argument("--i-authorize-fetch", action="store_true")

    p = sub.add_parser("register")
    p.add_argument("--url")
    p.add_argument("--file")
    p.add_argument("--out", default="./pdw_out")
    p.add_argument("--i-authorize-fetch", action="store_true")
    p.add_argument("--i-consent", action="store_true")

    p = sub.add_parser("ledger")
    p.add_argument("--dir", default="./pdw_out")
    p.add_argument("--ledger", default="./pdw_out/ledger.json")

    p = sub.add_parser("verify")
    p.add_argument("--card", required=True)

    p = sub.add_parser("check-url")
    p.add_argument("--url", required=True)

    args = ap.parse_args()
    if args.cmd == "check-url":
        print(json.dumps(check_url(args.url), indent=2))
        return 0 if check_url(args.url).get("ok") else 3

    if args.cmd == "digest":
        print(json.dumps(digest_file(Path(args.file), Path(args.out)), indent=2))
        return 0

    if args.cmd == "fetch":
        if not args.i_authorize_fetch:
            print(json.dumps({"ok": False, "error": "need --i-authorize-fetch for network"}))
            return 2
        print(json.dumps(fetch_url(args.url, Path(args.out)), indent=2))
        return 0

    if args.cmd == "register":
        if not args.i_consent:
            print(json.dumps({"ok": False, "error": "need --i-consent"}))
            return 2
        out = Path(args.out)
        if args.url:
            if not args.i_authorize_fetch:
                print(json.dumps({"ok": False, "error": "need --i-authorize-fetch for URL"}))
                return 2
            card = fetch_url(args.url, out)
        elif args.file:
            card = digest_file(Path(args.file), out)
        else:
            print(json.dumps({"ok": False, "error": "need --url or --file"}))
            return 2
        card_path = out / f"{card['witness_id']}.json"
        egg = make_egg(card_path, out / "eggs")
        continuum_claims(card_path)
        led = rebuild_ledger(out, out / "ledger.json")
        # Star submission JSON for steward/stack gate (no subprocess in skill)
        wid = card["witness_id"]
        hexpart = wid.replace("PDW-", "")
        nid = f"NODE_PDW_{hexpart}"
        sub = {
            "signature": "Δ9Φ963-HAVEN-STAR-SUBMISSION-v1",
            "scan_cue": "LYGO-HSC-ATTEST-v1",
            "node": {
                "id": nid,
                "kind": "node",
                "name": f"Witness {wid}",
                "equation": f"H={card['content_sha256'][:20]}…",
                "glyph": "◆",
                "tone": "741Hz",
                "tags": ["PURE_DATA", "PDW", "WITNESS", "ARCHIVE", "FORK_LOG", "DIGEST", "AGENT_SUBMIT"],
                "connections": ["LATTICE_PURE_DATA_WITNESS", "NODE_PDW_ROOT"],
                "urls": {"source": card.get("source_url") or "", "ledger": "local:ledger.json"},
                "layer": "C",
            },
        }
        sub_path = out / f"{wid}.star_submission.json"
        sub_path.write_text(json.dumps(sub, indent=2), encoding="utf-8")
        print(json.dumps({
            "ok": True,
            "witness_id": wid,
            "egg_id": egg.get("egg_id"),
            "ledger_root": led.get("merkle_style_root"),
            "star_submission": str(sub_path),
            "next": "Steward: python tools/haven_star_chart_submit.py <star_submission> --agent-id … --skill-slug lygo-pure-data-witness --i-consent",
        }, indent=2))
        return 0

    if args.cmd == "ledger":
        led = rebuild_ledger(Path(args.dir), Path(args.ledger))
        print(json.dumps({"ok": True, "count": led["count"], "root": led["merkle_style_root"]}, indent=2))
        return 0

    if args.cmd == "verify":
        res = verify_card(Path(args.card))
        print(json.dumps(res, indent=2))
        return 0 if res.get("ok") else 10

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
