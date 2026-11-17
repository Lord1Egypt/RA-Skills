#!/usr/bin/env python3
"""
LYGO-MINT Verifier v1.1.1 — in-process pack mint / verify / snippet / backfill.

Pure stdlib. No subprocess. No network. No auto-publish.
Ledgers default under skill state/ (override with --state-dir).
Compat wrappers never inject --i-consent.

Signature: Delta9Phi963-MINT-VERIFIER-v1.1.1
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

SIG = "Delta9Phi963-MINT-VERIFIER-v1.1.1"
VERSION = "1.1.1"
HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
DEFAULT_STATE = SKILL / "state"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def canonicalize_text(text: str) -> str:
    t = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [ln.rstrip() for ln in t.split("\n")]
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
    return "\n".join(out).strip() + "\n"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def state_paths(state_dir: Path) -> tuple[Path, Path]:
    return state_dir / "lygo_mint_ledger.jsonl", state_dir / "lygo_mint_ledger_canonical.json"


def load_canon(canon_path: Path) -> dict[str, Any]:
    if canon_path.is_file():
        data = json.loads(canon_path.read_text(encoding="utf-8"))
        if isinstance(data, dict) and "by_hash" in data:
            return data
        if isinstance(data, dict):
            # legacy flat hash→record
            return {"signature": SIG, "version": VERSION, "by_hash": data}
        if isinstance(data, list):
            by: dict[str, Any] = {}
            for r in data:
                h = str(r.get("hash") or r.get("sha256") or r.get("LYGO_HASH_SHA256") or "")
                if h:
                    by[h] = r
            return {"signature": SIG, "version": VERSION, "by_hash": by}
    return {"signature": SIG, "version": VERSION, "by_hash": {}}


def append_ledger(ledger: Path, rec: dict[str, Any]) -> None:
    ledger.parent.mkdir(parents=True, exist_ok=True)
    with ledger.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def write_canon(canon_path: Path, data: dict[str, Any]) -> None:
    canon_path.parent.mkdir(parents=True, exist_ok=True)
    canon_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def resolve_pack(pack: str) -> Path:
    p = Path(pack)
    if p.is_file():
        return p.resolve()
    cand = (Path.cwd() / pack).resolve()
    if cand.is_file():
        return cand
    raise SystemExit(f"Pack not found: {pack}")


def mint_pack(
    pack: str,
    version: str,
    *,
    champion: str = "",
    anchor: str = "",
    title: str = "",
    state_dir: Path = DEFAULT_STATE,
    i_consent: bool = False,
) -> dict[str, Any]:
    path = resolve_pack(pack)
    raw = path.read_text(encoding="utf-8", errors="replace")
    canon = canonicalize_text(raw)
    digest = sha256_text(canon)
    rec = {
        "kind": "mint",
        "signature": SIG,
        "tool_version": VERSION,
        "minted_at_utc": utc_now(),
        "title": title or path.stem,
        "pack_path": str(path),
        "pack_version": version,
        "champion": champion,
        "anchor": anchor,
        "bytes_raw": len(raw.encode("utf-8")),
        "bytes_canonical": len(canon.encode("utf-8")),
        "sha256": digest,
        "hash": digest,
        "LYGO_HASH_SHA256": digest,
    }
    ledger, canon_path = state_paths(state_dir)
    if i_consent:
        append_ledger(ledger, rec)
        db = load_canon(canon_path)
        db.setdefault("by_hash", {})[digest] = {
            "title": rec["title"],
            "pack_version": version,
            "pack_path": rec["pack_path"],
            "champion": champion,
            "anchor": anchor,
            "minted_at_utc": rec["minted_at_utc"],
            "sha256": digest,
            "hash": digest,
        }
        db["updated_utc"] = utc_now()
        write_canon(canon_path, db)
        rec["written"] = True
        rec["ledger"] = str(ledger)
        rec["canonical"] = str(canon_path)
    else:
        rec["written"] = False
        rec["hint"] = "pass --i-consent to write ledgers under skill state/"

    rec["anchor_snippet"] = make_snippet(
        digest,
        title=rec["title"],
        version=version,
        champion=champion,
        anchor=anchor,
        minted_at=rec["minted_at_utc"],
    )
    rec["ok"] = True
    return rec


def verify_pack(pack: str, expect_hash: str) -> dict[str, Any]:
    path = resolve_pack(pack)
    raw = path.read_text(encoding="utf-8", errors="replace")
    digest = sha256_text(canonicalize_text(raw))
    expect = re.sub(r"[^0-9a-fA-F]", "", expect_hash).lower()
    match = digest == expect
    return {
        "ok": match,
        "sha256": digest,
        "expect": expect,
        "match": match,
        "pack_path": str(path),
        "signature": SIG,
    }


def make_snippet(
    hash_hex: str,
    *,
    title: str = "",
    version: str = "",
    champion: str = "",
    anchor: str = "",
    minted_at: str = "",
) -> str:
    h = re.sub(r"[^0-9a-fA-F]", "", hash_hex).lower()
    lines = [
        "=== LYGO-MINT ANCHOR SNIPPET ===",
        f"LYGO-MINT v1 | {title or 'PACK'} | {version}".strip(),
        f"HASH_SHA256: {h}",
    ]
    if champion:
        lines.append(f"CHAMPION: {champion}")
    if anchor:
        lines.append(f"ANCHOR: {anchor}")
    lines.append(f"GENERATED_AT_UTC: {minted_at or utc_now()}")
    lines.append(f"TOOL: {SIG}")
    lines.append("note: public receipt only — pack content not included")
    lines.append("ANCHORS: (fill after posting)")
    lines.append("- moltbook: ")
    lines.append("- x: ")
    lines.append("- discord: ")
    lines.append("- 4claw: ")
    lines.append("=== END ===")
    return "\n".join(lines) + "\n"


def snippet_cmd(hash_hex: str, state_dir: Path, title: str = "", version: str = "") -> dict[str, Any]:
    h = re.sub(r"[^0-9a-fA-F]", "", hash_hex).lower()
    if len(h) != 64:
        return {"ok": False, "error": "hash_must_be_64_hex"}
    _, canon_path = state_paths(state_dir)
    db = load_canon(canon_path)
    rec = (db.get("by_hash") or {}).get(h) or {}
    text = make_snippet(
        h,
        title=title or rec.get("title") or "PACK",
        version=version or rec.get("pack_version") or "",
        champion=str(rec.get("champion") or ""),
        anchor=str(rec.get("anchor") or ""),
    )
    return {"ok": True, "anchor_snippet": text, "record": rec, "signature": SIG}


def backfill(
    hash_hex: str,
    channel: str,
    anchor_id: str,
    *,
    state_dir: Path,
    i_consent: bool,
) -> dict[str, Any]:
    h = re.sub(r"[^0-9a-fA-F]", "", hash_hex).lower()
    if len(h) != 64:
        return {"ok": False, "error": "hash_must_be_64_hex"}
    if not i_consent:
        return {"ok": False, "error": "need --i-consent to append ledger"}
    ledger, canon_path = state_paths(state_dir)
    rec = {
        "kind": "anchor_update",
        "signature": SIG,
        "ts": utc_now(),
        "hash": h,
        "channel": channel,
        "anchor_id": anchor_id,
    }
    append_ledger(ledger, rec)
    db = load_canon(canon_path)
    entry = db.setdefault("by_hash", {}).setdefault(h, {"sha256": h, "hash": h})
    anchors = entry.setdefault("anchors", {})
    anchors[channel] = anchor_id
    entry["updated_utc"] = utc_now()
    write_canon(canon_path, db)
    return {"ok": True, "record": rec, "canonical": str(canon_path)}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except Exception:
        pass

    ap = argparse.ArgumentParser(description="LYGO-MINT Verifier v1.1 (in-process)")
    ap.add_argument(
        "--state-dir",
        default=str(DEFAULT_STATE),
        help="Ledger directory (default: skill state/)",
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_m = sub.add_parser("mint", help="Canonicalize + SHA-256 + optional ledger write")
    p_m.add_argument("--pack", required=True)
    p_m.add_argument("--version", required=True)
    p_m.add_argument("--champion", default="")
    p_m.add_argument("--anchor", default="")
    p_m.add_argument("--title", default="")
    p_m.add_argument("--i-consent", action="store_true", help="Write ledgers under --state-dir")
    p_m.add_argument("--json", action="store_true")

    p_v = sub.add_parser("verify", help="Recompute pack hash and compare")
    p_v.add_argument("--pack", required=True)
    p_v.add_argument("--hash", required=True)
    p_v.add_argument("--json", action="store_true")

    p_s = sub.add_parser("snippet", help="Emit portable anchor snippet")
    p_s.add_argument("--hash", required=True)
    p_s.add_argument("--title", default="")
    p_s.add_argument("--version", default="")
    p_s.add_argument("--json", action="store_true")

    p_b = sub.add_parser("backfill", help="Append anchor id/url for a hash")
    p_b.add_argument("--hash", required=True)
    p_b.add_argument("--channel", required=True, help="moltbook|x|discord|4claw|other")
    p_b.add_argument("--id", required=True)
    p_b.add_argument("--i-consent", action="store_true")
    p_b.add_argument("--json", action="store_true")

    args = ap.parse_args()
    state = Path(args.state_dir)

    if args.cmd == "mint":
        out = mint_pack(
            args.pack,
            args.version,
            champion=args.champion,
            anchor=args.anchor,
            title=args.title,
            state_dir=state,
            i_consent=args.i_consent,
        )
        if args.json:
            print(json.dumps(out, indent=2, ensure_ascii=False))
        else:
            print("MINTED")
            print("pack:", out["pack_path"])
            print("version:", out["pack_version"])
            print("hash:", out["sha256"])
            print("written:", out.get("written"))
            print("\nANCHOR_SNIPPET")
            print(out["anchor_snippet"])
        return 0 if out.get("ok") else 1

    if args.cmd == "verify":
        out = verify_pack(args.pack, args.hash)
        print(json.dumps(out, indent=2) if args.json else out)
        if not args.json:
            print("MATCH" if out["match"] else "MISMATCH")
            print("sha256:", out["sha256"])
        return 0 if out.get("ok") else 10

    if args.cmd == "snippet":
        out = snippet_cmd(args.hash, state, title=args.title, version=args.version)
        if not out.get("ok"):
            print(json.dumps(out, indent=2))
            return 1
        if args.json:
            print(json.dumps(out, indent=2, ensure_ascii=False))
        else:
            print(out["anchor_snippet"])
        return 0

    if args.cmd == "backfill":
        out = backfill(args.hash, args.channel, args.id, state_dir=state, i_consent=args.i_consent)
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return 0 if out.get("ok") else 2

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
