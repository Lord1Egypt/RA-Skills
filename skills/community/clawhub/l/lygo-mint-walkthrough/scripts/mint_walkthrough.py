#!/usr/bin/env python3
"""
LYGO Mint Walkthrough — interactive mint → verify → anchor tutorial.

Pure stdlib local mint (canonicalize + SHA-256 + ledger + anchor snippet).
Compatible with lygo-mint-verifier concepts; does not require workspace tools/lygo_mint.

No subprocess. Writes only under skill state/ with --i-consent (or explicit step flags).

Signature: Delta9Phi963-MINT-WALKTHROUGH-v1.0.0
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SIG = "Delta9Phi963-MINT-WALKTHROUGH-v1.0.0"
VERSION = "1.0.0"
HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
STATE = SKILL / "state"
LEDGER = STATE / "walkthrough_ledger.jsonl"
CANON = STATE / "walkthrough_canonical.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def canonicalize_text(text: str) -> str:
    """Deterministic canonicalize: CRLF→LF, strip trailing spaces, ensure trailing newline."""
    t = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [ln.rstrip() for ln in t.split("\n")]
    # collapse >2 blank lines
    out: list[str] = []
    blank = 0
    for ln in lines:
        if ln == "":
            blank += 1
            if blank <= 2:
                out.append("")
        else:
            blank = 0
            out.append(ln)
    body = "\n".join(out).strip() + "\n"
    return body


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_canon() -> dict[str, Any]:
    if CANON.is_file():
        return json.loads(CANON.read_text(encoding="utf-8"))
    return {"signature": SIG, "version": VERSION, "by_hash": {}}


def append_ledger(rec: dict[str, Any]) -> None:
    STATE.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def step_intro() -> dict[str, Any]:
    return {
        "ok": True,
        "step": "intro",
        "title": "Mint → Verify → Anchor",
        "plain_english": (
            "Minting makes a pack *checkable*: the same content always yields the same SHA-256. "
            "You can share a short Anchor Snippet as a public receipt without uploading secrets."
        ),
        "rules": [
            "Never put API keys or passwords in a pack",
            "You remain the publisher — this skill never posts for you",
            "Full production path also available via lygo-mint-verifier",
        ],
        "next": "python scripts/mint_walkthrough.py mint --pack path/to/pack.md --i-consent",
    }


def step_mint(pack: str, version: str, title: str, i_consent: bool) -> dict[str, Any]:
    p = Path(pack)
    if not p.is_file():
        return {"ok": False, "error": "pack_not_found", "path": pack}
    raw = p.read_text(encoding="utf-8", errors="replace")
    canon = canonicalize_text(raw)
    digest = sha256_text(canon)
    rec = {
        "kind": "mint",
        "signature": SIG,
        "created_utc": utc_now(),
        "title": title or p.name,
        "version": version,
        "path": str(p.resolve()),
        "bytes_raw": len(raw.encode("utf-8")),
        "bytes_canonical": len(canon.encode("utf-8")),
        "sha256": digest,
    }
    if i_consent:
        append_ledger(rec)
        canon_db = load_canon()
        canon_db.setdefault("by_hash", {})[digest] = {
            "title": rec["title"],
            "version": version,
            "path": rec["path"],
            "created_utc": rec["created_utc"],
        }
        STATE.mkdir(parents=True, exist_ok=True)
        CANON.write_text(json.dumps(canon_db, indent=2) + "\n", encoding="utf-8")
        rec["ledger"] = str(LEDGER)
        rec["canonical_db"] = str(CANON)
        rec["written"] = True
    else:
        rec["written"] = False
        rec["hint"] = "pass --i-consent to write local ledger under skill state/"

    snippet = (
        f"=== LYGO-MINT ANCHOR SNIPPET ===\n"
        f"title: {rec['title']}\n"
        f"version: {version}\n"
        f"sha256: {digest}\n"
        f"tool: {SIG}\n"
        f"created: {rec['created_utc']}\n"
        f"note: public receipt only — pack content not included\n"
        f"=== END ===\n"
    )
    return {
        "ok": True,
        "step": "mint",
        "plain_english": (
            f"Pack **{rec['title']}** minted. Hash `{digest[:16]}…`. "
            + ("Ledger written under skill state/." if rec["written"] else "Dry-run only (no ledger write).")
        ),
        "record": rec,
        "anchor_snippet": snippet,
        "next": f"python scripts/mint_walkthrough.py snippet --hash {digest} --title \"{rec['title']}\"",
    }


def step_snippet(hash_hex: str, title: str) -> dict[str, Any]:
    h = re.sub(r"[^0-9a-fA-F]", "", hash_hex).lower()
    if len(h) != 64:
        return {"ok": False, "error": "need_64_hex_hash"}
    snippet = (
        f"=== LYGO-MINT ANCHOR SNIPPET ===\n"
        f"title: {title or 'untitled'}\n"
        f"sha256: {h}\n"
        f"tool: {SIG}\n"
        f"created: {utc_now()}\n"
        f"=== END ===\n"
    )
    return {
        "ok": True,
        "step": "snippet",
        "plain_english": "Copy the snippet below and paste it wherever you want a public receipt. Human posts only.",
        "anchor_snippet": snippet,
        "next": f"python scripts/mint_walkthrough.py backfill --hash {h} --channel manual --id <url> --i-consent",
    }


def step_backfill(hash_hex: str, channel: str, anchor_id: str, i_consent: bool) -> dict[str, Any]:
    h = re.sub(r"[^0-9a-fA-F]", "", hash_hex).lower()
    if len(h) != 64:
        return {"ok": False, "error": "need_64_hex_hash"}
    if not anchor_id.strip():
        return {"ok": False, "error": "need_anchor_id"}
    rec = {
        "kind": "backfill",
        "signature": SIG,
        "created_utc": utc_now(),
        "sha256": h,
        "channel": channel or "manual",
        "anchor_id": anchor_id.strip(),
    }
    if i_consent:
        append_ledger(rec)
        canon_db = load_canon()
        entry = canon_db.setdefault("by_hash", {}).setdefault(h, {})
        entry.setdefault("anchors", []).append(
            {"channel": rec["channel"], "id": rec["anchor_id"], "utc": rec["created_utc"]}
        )
        STATE.mkdir(parents=True, exist_ok=True)
        CANON.write_text(json.dumps(canon_db, indent=2) + "\n", encoding="utf-8")
        rec["written"] = True
    else:
        rec["written"] = False
        rec["hint"] = "pass --i-consent to record backfill"
    return {
        "ok": True,
        "step": "backfill",
        "plain_english": (
            f"Backfill recorded for `{h[:16]}…` → {channel}:{anchor_id}"
            if rec.get("written")
            else "Dry-run backfill (add --i-consent to write)."
        ),
        "record": rec,
        "done": True,
        "next": "Walkthrough complete. Pair with lygo-mint-verifier for production ledgers.",
    }


def step_verify(hash_hex: str = "", pack: str = "") -> dict[str, Any]:
    if pack:
        p = Path(pack)
        if not p.is_file():
            return {"ok": False, "error": "pack_not_found"}
        canon = canonicalize_text(p.read_text(encoding="utf-8", errors="replace"))
        digest = sha256_text(canon)
        canon_db = load_canon()
        known = digest in (canon_db.get("by_hash") or {})
        return {
            "ok": True,
            "step": "verify",
            "sha256": digest,
            "in_local_ledger": known,
            "plain_english": (
                f"Recomputed hash `{digest[:16]}…`. "
                + ("Found in local walkthrough ledger." if known else "Not in local ledger yet (mint with --i-consent first).")
            ),
        }
    h = re.sub(r"[^0-9a-fA-F]", "", hash_hex).lower()
    if len(h) != 64:
        return {"ok": False, "error": "need_pack_or_hash"}
    canon_db = load_canon()
    entry = (canon_db.get("by_hash") or {}).get(h)
    return {
        "ok": True,
        "step": "verify",
        "sha256": h,
        "found": bool(entry),
        "entry": entry,
        "plain_english": "Hash found in local ledger." if entry else "Hash not in local walkthrough ledger.",
    }


def interactive() -> dict[str, Any]:
    print(
        """
LYGO Mint Walkthrough
1) Intro
2) Mint a pack file
3) Make anchor snippet from hash
4) Verify pack or hash
5) Backfill public anchor id
"""
    )
    c = (input("Choice [1]: ").strip() or "1")
    if c == "2":
        pack = input("Path to pack file: ").strip()
        ver = input("Version label [v1]: ").strip() or "v1"
        consent = input("Write local ledger? y/N: ").strip().lower() in ("y", "yes")
        return step_mint(pack, ver, "", consent)
    if c == "3":
        h = input("64-hex sha256: ").strip()
        t = input("Title: ").strip()
        return step_snippet(h, t)
    if c == "4":
        pack = input("Pack path (or empty): ").strip()
        h = input("Or hash: ").strip()
        return step_verify(hash_hex=h, pack=pack)
    if c == "5":
        h = input("Hash: ").strip()
        ch = input("Channel [manual]: ").strip() or "manual"
        aid = input("Post URL or id: ").strip()
        consent = input("Write backfill? y/N: ").strip().lower() in ("y", "yes")
        return step_backfill(h, ch, aid, consent)
    return step_intro()


def main() -> int:
    ap = argparse.ArgumentParser(description="LYGO Mint Walkthrough")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("intro")
    p = sub.add_parser("mint")
    p.add_argument("--pack", required=True)
    p.add_argument("--version", default="v1")
    p.add_argument("--title", default="")
    p.add_argument("--i-consent", action="store_true")
    p = sub.add_parser("snippet")
    p.add_argument("--hash", required=True)
    p.add_argument("--title", default="")
    p = sub.add_parser("verify")
    p.add_argument("--hash", default="")
    p.add_argument("--pack", default="")
    p = sub.add_parser("backfill")
    p.add_argument("--hash", required=True)
    p.add_argument("--channel", default="manual")
    p.add_argument("--id", required=True, dest="anchor_id")
    p.add_argument("--i-consent", action="store_true")
    sub.add_parser("start")
    args = ap.parse_args()

    cmd = args.cmd or "intro"
    if cmd == "start":
        out = interactive() if sys.stdin.isatty() else step_intro()
    elif cmd == "intro":
        out = step_intro()
    elif cmd == "mint":
        out = step_mint(args.pack, args.version, args.title, args.i_consent)
    elif cmd == "snippet":
        out = step_snippet(args.hash, args.title)
    elif cmd == "verify":
        out = step_verify(hash_hex=args.hash, pack=args.pack)
    elif cmd == "backfill":
        out = step_backfill(args.hash, args.channel, args.anchor_id, args.i_consent)
    else:
        out = step_intro()

    out["signature"] = SIG
    out["version"] = VERSION
    print(json.dumps(out, indent=2))
    if out.get("anchor_snippet"):
        print("\n" + out["anchor_snippet"])
    return 0 if out.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
