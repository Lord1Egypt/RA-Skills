#!/usr/bin/env python3
"""LYGO Pure-Data Witness v1.3 — digest / fetch / egg / continuum / ledger / hf-pack / verify.

Network fetch requires --i-authorize-fetch. The `all` chain requires --i-confirm-chain
(and --i-authorize-fetch when --url is set). Matches SKILL.md safety contract.

Combined free-tier purity stack:
  A digest+snapshot  B kernel-egg fragment  C HF export pack  D public ledger
Stdlib only. No secrets. HTTPS fetch size-capped.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

SIG = "Delta9Phi963-PURE-DATA-WITNESS-v1.1"
EGG_SIG = "Delta9Phi963-PDW-KERNEL-FRAGMENT-v1"
MAX_FETCH = 256 * 1024
MAX_EGG_JSON = 6 * 1024  # keep egg card tiny
UA = "LYGO-PureDataWitness/1.1 (+https://deepseekoracle.github.io/lygo-protocol-stack/)"

SECRET_RE = re.compile(
    r"(?i)(api[_-]?key|secret|password|token|bearer|moltbook_sk_|moltx_sk_|nvapi-|ghp_|github_pat_)[=:\s]+\S+"
)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def redact_text(s: str) -> str:
    return SECRET_RE.sub("[REDACTED]", s)


def witness_id(content_sha: str, captured: str) -> str:
    return "PDW-" + hashlib.sha256(f"{content_sha}:{captured}".encode()).hexdigest()[:12].upper()


def write_json(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _save_card(out_dir: Path, card: dict, data: bytes) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    wid = card["witness_id"]
    if len(data) <= MAX_FETCH:
        (out_dir / f"{wid}.bin").write_bytes(data)
        card["snapshot_saved"] = True
        card["snapshot_file"] = f"{wid}.bin"
        try:
            text = data.decode("utf-8")
            (out_dir / f"{wid}.txt").write_text(redact_text(text), encoding="utf-8")
            card["snapshot_txt"] = f"{wid}.txt"
            if "charset" not in (card.get("content_type") or ""):
                card["content_type"] = "text/plain; charset=utf-8"
        except UnicodeDecodeError:
            pass
    else:
        card["snapshot_saved"] = False
        card["truncated"] = True
    write_json(out_dir / f"{wid}.json", card)
    return card


def digest_file(path: Path, out_dir: Path, source_url: str | None = None) -> dict:
    data = path.read_bytes()
    captured = utc_now()
    digest = sha256_bytes(data)
    wid = witness_id(digest, captured)
    card = {
        "signature": SIG,
        "witness_id": wid,
        "captured_utc": captured,
        "source_url": source_url,
        "source_path_hint": path.name,
        "content_sha256": digest,
        "bytes": len(data),
        "content_type": "application/octet-stream",
        "method": "local_file",
        "fetch_status": None,
        "truncated": len(data) > MAX_FETCH,
        "max_fetch_bytes": MAX_FETCH,
        "egg_id": None,
        "continuum_claims_file": None,
        "mirrors": [],
        "notes": "Pure-Data Witness — digest is authority.",
    }
    return _save_card(out_dir, card, data[:MAX_FETCH] if len(data) > MAX_FETCH else data)


def fetch_url(url: str, out_dir: Path, *, skip_content_gate: bool = False) -> dict:
    # Safety: scheme/host/SSRF before any request
    try:
        from pure_data_safety import check_url, check_content  # type: ignore
    except ImportError:
        from pure_data_safety import check_url, check_content  # type: ignore

    ugate = check_url(url)
    if not ugate.get("ok"):
        raise SystemExit(json.dumps({"error": "url_safety_reject", "gate": ugate}, indent=2))

    req = urllib.request.Request(url, headers={"User-Agent": UA})
    captured = utc_now()
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            status = resp.status
            ctype = resp.headers.get("Content-Type", "application/octet-stream")
            data = resp.read(MAX_FETCH + 1)
    except urllib.error.HTTPError as e:
        status = e.code
        ctype = "text/plain"
        data = (e.read(MAX_FETCH) if hasattr(e, "read") else str(e).encode())[:MAX_FETCH]
    except Exception as e:
        raise SystemExit(f"fetch failed: {e}") from e

    truncated = len(data) > MAX_FETCH
    if truncated:
        data = data[:MAX_FETCH]

    cgate = check_content(data, ctype)
    if not skip_content_gate and not cgate.get("ok"):
        raise SystemExit(json.dumps({"error": "content_safety_reject", "gate": cgate, "url_gate": ugate}, indent=2))

    digest = sha256_bytes(data)
    wid = witness_id(digest, captured)
    card = {
        "signature": SIG,
        "witness_id": wid,
        "captured_utc": captured,
        "source_url": url,
        "content_sha256": digest,
        "bytes": len(data),
        "content_type": ctype,
        "method": "https_get",
        "fetch_status": status,
        "truncated": truncated,
        "max_fetch_bytes": MAX_FETCH,
        "egg_id": None,
        "continuum_claims_file": None,
        "mirrors": [],
        "safety": {"url_gate": ugate, "content_gate": cgate},
        "notes": "URL witness — digest authority; safety-gated; snapshot may be truncated.",
    }
    return _save_card(out_dir, card, data)


def make_egg(card_path: Path, eggs_dir: Path) -> dict:
    """Phase B: tiny kernel-egg fragment from a witness card (digest only + mini meta)."""
    card = json.loads(card_path.read_text(encoding="utf-8"))
    eggs_dir.mkdir(parents=True, exist_ok=True)
    egg_id = f"pdw-frag-{card['witness_id'].lower()}"
    # Compact payload — digest purity, no bulk snapshot inside egg
    payload = {
        "kind": "pure_data_witness_fragment",
        "witness_id": card.get("witness_id"),
        "content_sha256": card.get("content_sha256"),
        "bytes": card.get("bytes"),
        "source_url": card.get("source_url"),
        "captured_utc": card.get("captured_utc"),
        "method": card.get("method"),
        "fetch_status": card.get("fetch_status"),
        "truncated": card.get("truncated"),
    }
    body = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    merkle_root = sha256_bytes(body)
    egg = {
        "signature": EGG_SIG,
        "egg_id": egg_id,
        "built_utc": utc_now(),
        "publisher": "deepseekoracle",
        "merkle_root": merkle_root,
        "parent_witness": card.get("witness_id"),
        "payload": payload,
        "verify": {
            "rule": "sha256(canonical_payload_json) == merkle_root",
            "canonical": "json.dumps(payload, sort_keys=True, separators=(',', ':'))",
        },
        "notes": "Tiny free-tier fragment. Reassemble purity via digest; full snapshot optional beside card.",
    }
    raw = json.dumps(egg, indent=2, ensure_ascii=False).encode("utf-8")
    if len(raw) > MAX_EGG_JSON:
        # strip notes if oversized
        egg.pop("notes", None)
        raw = json.dumps(egg, indent=2, ensure_ascii=False).encode("utf-8")
    out_json = eggs_dir / f"{egg_id}.json"
    out_bin = eggs_dir / f"{egg_id}.bin"
    out_json.write_bytes(raw)
    out_bin.write_bytes(body)
    # link back into card
    card["egg_id"] = egg_id
    card["egg_merkle_root"] = merkle_root
    card["egg_file"] = str(out_json.name)
    write_json(card_path, card)
    return egg


def verify_egg(egg_path: Path) -> dict:
    egg = json.loads(egg_path.read_text(encoding="utf-8"))
    payload = egg.get("payload") or {}
    body = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    got = sha256_bytes(body)
    ok = got == egg.get("merkle_root")
    return {
        "egg_id": egg.get("egg_id"),
        "ok": ok,
        "expected": egg.get("merkle_root"),
        "observed": got,
        "witness_id": payload.get("witness_id"),
    }


def continuum_claims(card_path: Path, out_path: Path | None = None) -> list:
    """Emit Continuum claims.json so seal/verify can bind the witness on disk."""
    card = json.loads(card_path.read_text(encoding="utf-8"))
    wid = card["witness_id"]
    rel_json = card_path.name
    claims = [
        {"id": f"{wid}-card", "kind": "file_exists", "path": rel_json},
        {
            "id": f"{wid}-sha",
            "kind": "json_path_eq",
            "path": rel_json,
            "jpath": "content_sha256",
            "expect": card["content_sha256"],
        },
        {
            "id": f"{wid}-id",
            "kind": "json_path_eq",
            "path": rel_json,
            "jpath": "witness_id",
            "expect": wid,
        },
    ]
    if card.get("snapshot_file"):
        claims.append({"id": f"{wid}-snap", "kind": "file_exists", "path": card["snapshot_file"]})
        claims.append(
            {
                "id": f"{wid}-snap-sha",
                "kind": "file_sha256",
                "path": card["snapshot_file"],
                "expect": card["content_sha256"],
            }
        )
    if card.get("egg_file"):
        claims.append({"id": f"{wid}-egg", "kind": "file_exists", "path": f"eggs/{card['egg_file']}"})
    out = out_path or (card_path.parent / f"{wid}.continuum-claims.json")
    # Continuum paths are relative to --base; write claims next to card with paths relative to out_dir
    # Rewrite paths relative to card parent as base
    write_json(out, claims)
    card["continuum_claims_file"] = out.name
    write_json(card_path, card)
    return claims


def rebuild_ledger(witness_dir: Path, ledger_path: Path) -> dict:
    rows = []
    for p in sorted(witness_dir.glob("PDW-*.json")):
        if p.name.endswith(".continuum-claims.json"):
            continue
        try:
            rows.append(json.loads(p.read_text(encoding="utf-8")))
        except Exception:
            continue
    joined = "\n".join(sorted(r.get("content_sha256", "") for r in rows)).encode()
    root = sha256_bytes(joined) if rows else sha256_bytes(b"")
    egg_roots = sorted({r.get("egg_merkle_root") for r in rows if r.get("egg_merkle_root")})
    egg_joined = "\n".join(egg_roots).encode()
    egg_root = sha256_bytes(egg_joined) if egg_roots else None
    ledger = {
        "signature": SIG + "-LEDGER",
        "updated_utc": utc_now(),
        "count": len(rows),
        "merkle_style_root": root,
        "egg_fragment_root": egg_root,
        "egg_fragment_count": len(egg_roots),
        "note": "Public digest ledger. Digests refuse rewrites; snapshots/eggs optional.",
        "witnesses": [
            {
                "witness_id": r.get("witness_id"),
                "captured_utc": r.get("captured_utc"),
                "source_url": r.get("source_url"),
                "content_sha256": r.get("content_sha256"),
                "bytes": r.get("bytes"),
                "fetch_status": r.get("fetch_status"),
                "truncated": r.get("truncated"),
                "egg_id": r.get("egg_id"),
                "egg_merkle_root": r.get("egg_merkle_root"),
            }
            for r in rows
        ],
    }
    write_json(ledger_path, ledger)
    return ledger


def verify_card(card_path: Path) -> dict:
    card = json.loads(card_path.read_text(encoding="utf-8"))
    snap = card_path.parent / (card.get("snapshot_file") or "")
    out: dict = {"witness_id": card.get("witness_id"), "ok": False}
    if not snap.is_file():
        out["error"] = "snapshot missing"
        return out
    data = snap.read_bytes()
    got = sha256_bytes(data)
    out["expected"] = card.get("content_sha256")
    out["observed"] = got
    out["ok"] = got == card.get("content_sha256")
    out["bytes"] = len(data)
    if card.get("egg_id"):
        egg_path = card_path.parent / "eggs" / f"{card['egg_id']}.json"
        if egg_path.is_file():
            out["egg"] = verify_egg(egg_path)
            out["ok"] = out["ok"] and out["egg"].get("ok", False)
    return out


def hf_pack(witness_dir: Path, pack_dir: Path, ledger_path: Path) -> dict:
    """Phase C: folder ready to drop on Hugging Face datasets (digests + txt, no secrets)."""
    pack_dir.mkdir(parents=True, exist_ok=True)
    (pack_dir / "witnesses").mkdir(exist_ok=True)
    (pack_dir / "eggs").mkdir(exist_ok=True)
    n = 0
    for p in witness_dir.glob("PDW-*.json"):
        if ".continuum" in p.name:
            continue
        shutil.copy2(p, pack_dir / "witnesses" / p.name)
        txt = p.with_suffix(".txt")
        if txt.is_file():
            shutil.copy2(txt, pack_dir / "witnesses" / txt.name)
        n += 1
    eggs_src = witness_dir / "eggs"
    ne = 0
    if eggs_src.is_dir():
        for p in eggs_src.glob("pdw-frag-*.json"):
            shutil.copy2(p, pack_dir / "eggs" / p.name)
            ne += 1
    if ledger_path.is_file():
        shutil.copy2(ledger_path, pack_dir / "ledger.json")
    readme = f"""# LYGO Pure-Data Witness export

Signature: {SIG}
Witness cards: {n}
Egg fragments: {ne}

Digests are authority. Text snapshots are redacted size-capped extracts.
See https://deepseekoracle.github.io/lygo-protocol-stack/LYGO_PURE_DATA_WITNESS.md
"""
    (pack_dir / "README.md").write_text(readme, encoding="utf-8")
    meta = {"signature": SIG + "-HF-PACK", "witness_cards": n, "egg_fragments": ne, "built_utc": utc_now()}
    write_json(pack_dir / "pack_meta.json", meta)
    return meta


def _consent_denied(need: list[str], *, warning: str, error: str = "consent_required") -> int:
    print(
        json.dumps(
            {
                "ok": False,
                "error": error,
                "need": need,
                "warning": warning,
            },
            indent=2,
        )
    )
    return 2


def main() -> int:
    ap = argparse.ArgumentParser(description="LYGO Pure-Data Witness v1.3 (consent-gated)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p1 = sub.add_parser("digest")
    p1.add_argument("--file", required=True)
    p1.add_argument("--url")
    p1.add_argument("--out", default="data/pure_data")

    p2 = sub.add_parser(
        "fetch",
        help="HTTPS fetch + digest (REQUIRES --i-authorize-fetch)",
    )
    p2.add_argument("--url", required=True)
    p2.add_argument("--out", default="data/pure_data")
    p2.add_argument(
        "--i-authorize-fetch",
        action="store_true",
        help="Required: explicit operator consent for outbound HTTPS GET",
    )

    p3 = sub.add_parser("egg", help="Pack witness card into tiny kernel fragment")
    p3.add_argument("--card", required=True)
    p3.add_argument("--eggs-dir", default=None, help="default: <card_dir>/eggs")

    p4 = sub.add_parser("continuum-claims", help="Write Continuum claims.json for a card")
    p4.add_argument("--card", required=True)

    p5 = sub.add_parser("ledger")
    p5.add_argument("--dir", default="data/pure_data")
    p5.add_argument("--ledger", default="docs/pure-data/ledger.json")

    p6 = sub.add_parser("verify")
    p6.add_argument("--card", required=True)

    p7 = sub.add_parser("verify-egg")
    p7.add_argument("--egg", required=True)

    p8 = sub.add_parser("hf-pack", help="Build HF-ready export folder (consent required)")
    p8.add_argument("--dir", default="data/pure_data")
    p8.add_argument("--ledger", default="docs/pure-data/ledger.json")
    p8.add_argument("--pack", default="data/pure_data/hf_pack")
    p8.add_argument(
        "--i-consent",
        action="store_true",
        help="Required: acknowledge redaction is incomplete; review before any HF upload",
    )
    p8.add_argument(
        "--i-authorize-hf-export",
        action="store_true",
        help="Required: authorize copying local witness .txt/.json into an export pack folder",
    )

    p9 = sub.add_parser(
        "all",
        help=(
            "WARNING: chains digest/fetch + egg + continuum-claims + ledger writes. "
            "URL mode REQUIRES --i-authorize-fetch. Prefer stepwise commands."
        ),
    )
    p9.add_argument("--url")
    p9.add_argument("--file")
    p9.add_argument("--out", default="data/pure_data")
    p9.add_argument("--ledger", default="docs/pure-data/ledger.json")
    p9.add_argument(
        "--i-authorize-fetch",
        action="store_true",
        help="Required when --url is set (outbound HTTPS GET)",
    )
    p9.add_argument(
        "--i-confirm-chain",
        action="store_true",
        help="Required: confirm multi-step persistence (egg + claims + ledger)",
    )

    args = ap.parse_args()

    if args.cmd == "digest":
        print(json.dumps(digest_file(Path(args.file), Path(args.out), args.url), indent=2))
        return 0
    if args.cmd == "fetch":
        if not args.i_authorize_fetch:
            return _consent_denied(
                ["--i-authorize-fetch"],
                error="fetch_consent_required",
                warning=(
                    "Network is OFF by default. Pass --i-authorize-fetch to allow a single "
                    "HTTPS GET of --url (SSRF/malware gates still apply). Prefer --file digests."
                ),
            )
        print(json.dumps(fetch_url(args.url, Path(args.out)), indent=2))
        return 0
    if args.cmd == "egg":
        card_path = Path(args.card)
        eggs_dir = Path(args.eggs_dir) if args.eggs_dir else card_path.parent / "eggs"
        print(json.dumps(make_egg(card_path, eggs_dir), indent=2))
        return 0
    if args.cmd == "continuum-claims":
        claims = continuum_claims(Path(args.card))
        print(json.dumps({"ok": True, "claims": len(claims)}, indent=2))
        return 0
    if args.cmd == "ledger":
        led = rebuild_ledger(Path(args.dir), Path(args.ledger))
        print(json.dumps({"ok": True, "count": led["count"], "root": led["merkle_style_root"], "egg_root": led.get("egg_fragment_root")}, indent=2))
        return 0
    if args.cmd == "verify":
        res = verify_card(Path(args.card))
        print(json.dumps(res, indent=2))
        return 0 if res.get("ok") else 10
    if args.cmd == "verify-egg":
        res = verify_egg(Path(args.egg))
        print(json.dumps(res, indent=2))
        return 0 if res.get("ok") else 10
    if args.cmd == "hf-pack":
        if not args.i_consent or not args.i_authorize_hf_export:
            return _consent_denied(
                ["--i-consent", "--i-authorize-hf-export"],
                error="hf_export_consent_required",
                warning=(
                    "HF export copies local witness cards + redacted .txt snapshots into a pack folder. "
                    "Regex redaction is incomplete by nature — review every file before uploading to "
                    "Hugging Face or any third party. This command does NOT upload; it only builds a local folder."
                ),
            )
        meta = hf_pack(Path(args.dir), Path(args.pack), Path(args.ledger))
        meta["ok"] = True
        meta["warning"] = (
            "Local pack only — no upload performed. Human must review redaction before any HF publish."
        )
        print(json.dumps(meta, indent=2))
        return 0
    if args.cmd == "all":
        if not args.i_confirm_chain:
            return _consent_denied(
                ["--i-confirm-chain"]
                + (["--i-authorize-fetch"] if args.url else []),
                error="chain_consent_required",
                warning=(
                    "'all' is a multi-step state-changing chain: fetch|digest → egg → continuum-claims → ledger. "
                    "Pass --i-confirm-chain to acknowledge. If using --url, also pass --i-authorize-fetch. "
                    "Prefer running digest/fetch, egg, continuum-claims, ledger separately."
                ),
            )
        out = Path(args.out)
        if args.url:
            if not args.i_authorize_fetch:
                return _consent_denied(
                    ["--i-authorize-fetch", "--i-confirm-chain"],
                    error="fetch_consent_required",
                    warning=(
                        "URL mode performs outbound HTTPS GET. Pass --i-authorize-fetch together with "
                        "--i-confirm-chain, or use --file for local-only digest."
                    ),
                )
            card = fetch_url(args.url, out)
        elif args.file:
            card = digest_file(Path(args.file), out, args.url)
        else:
            raise SystemExit("--url or --file required")
        card_path = out / f"{card['witness_id']}.json"
        egg = make_egg(card_path, out / "eggs")
        continuum_claims(card_path)
        led = rebuild_ledger(out, Path(args.ledger))
        print(
            json.dumps(
                {
                    "card": card["witness_id"],
                    "egg": egg["egg_id"],
                    "ledger_root": led["merkle_style_root"],
                    "egg_root": led.get("egg_fragment_root"),
                    "chain_confirmed": True,
                    "network": bool(args.url),
                },
                indent=2,
            )
        )
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

