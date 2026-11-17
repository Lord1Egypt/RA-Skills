#!/usr/bin/env python3
"""LYGO Immutable Anchor — local CA geodesic seals + mycelium fold (no network)."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SIG = "Delta9Phi963-IMMUTABLE-ANCHOR-v1.0.0"
VERSION = "1.0.0"
BLUEPRINT = "biophase7-immutable-anchor-2026-08-24"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def canonical(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_obj(obj: Any) -> str:
    return hashlib.sha256(canonical(obj)).hexdigest()


def merkle_root(leaves: list[str]) -> str:
    if not leaves:
        return sha256_text("")
    layer = [bytes.fromhex(x) if len(x) == 64 and all(c in "0123456789abcdef" for c in x.lower()) else hashlib.sha256(x.encode()).digest() for x in leaves]
    while len(layer) > 1:
        nxt: list[bytes] = []
        for i in range(0, len(layer), 2):
            left = layer[i]
            right = layer[i + 1] if i + 1 < len(layer) else left
            nxt.append(hashlib.sha256(left + right).digest())
        layer = nxt
    return layer[0].hex()


def consent_ok(ns: argparse.Namespace) -> bool:
    return bool(getattr(ns, "i_consent", False))


def refuse_write(path: str | None, consent: bool) -> dict | None:
    if not path:
        return None
    if not consent:
        return {
            "ok": False,
            "error": "CONSENT_REQUIRED",
            "hint": "pass --i-consent with --write",
        }
    return None


def maybe_write(path: str | None, obj: dict, consent: bool) -> dict:
    bad = refuse_write(path, consent)
    if bad:
        return bad
    if path:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        obj = {**obj, "written": str(p.resolve())}
    return obj


def cmd_seal(ns: argparse.Namespace) -> dict:
    truth = (ns.truth or "").strip()
    light = (ns.light or "").strip()
    chaos = (ns.chaos or "").strip() or "creative-chaos"
    node_id = (ns.node_id or "NODE_LOCAL").strip()
    if not truth or not light:
        return {"ok": False, "error": "truth_and_light_required"}
    t_h = sha256_text(truth)
    l_h = sha256_text(light)
    c_h = sha256_text(chaos)
    # Equal-weight geodesic: Truth and Light both present (no collapse)
    collapsing = (not truth) or (not light)
    leaf = sha256_obj(
        {
            "node_id": node_id,
            "truth_sha256": t_h,
            "light_sha256": l_h,
            "chaos_sha256": c_h,
            "blueprint": BLUEPRINT,
        }
    )
    slm_gossip = sha256_text(f"SLM|{node_id}|{leaf}")
    p7_hook = sha256_text(f"P7|{node_id}|{leaf}")
    root = merkle_root([t_h, l_h, leaf, slm_gossip, p7_hook])
    receipt = {
        "ok": True,
        "signature": SIG,
        "version": VERSION,
        "blueprint": BLUEPRINT,
        "service": "LYGO-Local-CA",
        "created_utc": utc_now(),
        "node_id": node_id,
        "truth_sha256": t_h,
        "light_sha256": l_h,
        "chaos_sha256": c_h,
        "geodesic_leaf": leaf,
        "slm_gossip_leaf": slm_gossip,
        "p7_hook_leaf": p7_hook,
        "merkle_root": root,
        "non_collapsing": not collapsing,
        "turbo": False,
        "note": "Local CA only. Arweave Turbo is stack tools/lygo_anchor.py with human consent — not this skill.",
    }
    if collapsing:
        receipt["ok"] = False
        receipt["error"] = "collapse_refused"
        return receipt
    return maybe_write(ns.write, receipt, consent_ok(ns))


def cmd_fold(ns: argparse.Namespace) -> dict:
    note = (ns.note or "").strip()
    if not note:
        return {"ok": False, "error": "note_required"}
    prev = (ns.prev_hash or "").strip() or ("0" * 64)
    fragment = {
        "note_sha256": sha256_text(note),
        "prev_hash": prev,
        "utc": utc_now(),
        "node_id": (ns.node_id or "NODE_LOCAL").strip(),
    }
    entry_hash = sha256_obj(fragment)
    out = {
        "ok": True,
        "signature": SIG,
        "event": "mycelium_fold",
        "entry_hash": entry_hash,
        "prev_hash": prev,
        "fragment": fragment,
        "turbo": False,
        "note": "Local mycelium fold. Permanent Turbo fold is stack MultiAnchor, consent-gated.",
    }
    return maybe_write(ns.write, out, consent_ok(ns))


def cmd_verify(ns: argparse.Namespace) -> dict:
    path = Path(ns.from_file)
    if not path.is_file():
        return {"ok": False, "error": "missing_file"}
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("geodesic_leaf"):
        leaf = sha256_obj(
            {
                "node_id": data.get("node_id"),
                "truth_sha256": data.get("truth_sha256"),
                "light_sha256": data.get("light_sha256"),
                "chaos_sha256": data.get("chaos_sha256"),
                "blueprint": data.get("blueprint") or BLUEPRINT,
            }
        )
        slm = sha256_text(f"SLM|{data.get('node_id')}|{leaf}")
        p7 = sha256_text(f"P7|{data.get('node_id')}|{leaf}")
        root = merkle_root([data.get("truth_sha256") or "", data.get("light_sha256") or "", leaf, slm, p7])
        return {
            "ok": leaf == data.get("geodesic_leaf") and root == data.get("merkle_root") and data.get("non_collapsing") is True,
            "kind": "geodesic_seal",
            "leaf_match": leaf == data.get("geodesic_leaf"),
            "merkle_match": root == data.get("merkle_root"),
            "non_collapsing": bool(data.get("non_collapsing")),
            "computed_merkle_root": root,
        }
    if data.get("entry_hash") and data.get("fragment"):
        eh = sha256_obj(data["fragment"])
        return {"ok": eh == data.get("entry_hash"), "kind": "mycelium_fold", "hash_match": eh == data.get("entry_hash")}
    return {"ok": False, "error": "unrecognized_receipt"}


def cmd_receipt(ns: argparse.Namespace) -> dict:
    path = Path(ns.from_file)
    if not path.is_file():
        return {"ok": False, "error": "missing_file"}
    src = json.loads(path.read_text(encoding="utf-8"))
    v = cmd_verify(argparse.Namespace(from_file=ns.from_file))
    rec = {
        "ok": bool(v.get("ok")),
        "signature": SIG,
        "event": "non_collapsing_receipt",
        "created_utc": utc_now(),
        "source_verify": v,
        "integral": "∫(Truth × Light) df",
        "source_merkle": src.get("merkle_root") or src.get("entry_hash"),
        "non_collapsing": True,
    }
    return maybe_write(ns.write, rec, consent_ok(ns))


def cmd_status(ns: argparse.Namespace) -> dict:
    stack = (ns.stack_root or "").strip()
    return {
        "ok": True,
        "signature": SIG,
        "version": VERSION,
        "blueprint": BLUEPRINT,
        "local_ca": True,
        "turbo_in_skill": False,
        "subprocess": False,
        "network": False,
        "stack_root_set": bool(stack),
        "stack_hint": "python tools/run_anchor_audit.py · python tools/anchor_autonomy_worker.py --loop --interval 300 --slm-each-pulse",
        "docs": "docs/ANCHOR_DEPLOYMENT.md",
    }


def cmd_worker_plan(_ns: argparse.Namespace) -> dict:
    return {
        "ok": True,
        "signature": SIG,
        "executes": False,
        "reason": "This skill never starts the loop. Human runs stack worker.",
        "steps": [
            "export LYGO_STACK_ROOT to trusted lygo-protocol-stack",
            "python tools/run_anchor_audit.py",
            "python tools/install_anchor_network.py  # consent; may write profile",
            "python tools/anchor_autonomy_worker.py --loop --interval 300 --slm-each-pulse",
        ],
        "env": "LYGO_ANCHOR_MODE=local|turbo|multi|airgap",
        "turbo": "Only via stack lygo_anchor.py — not this CLI",
    }


def cmd_demo(_ns: argparse.Namespace) -> dict:
    seal = cmd_seal(
        argparse.Namespace(
            node_id="demo-biophase7",
            truth="Truth continuous",
            light="Light stable",
            chaos="Next vector",
            write=None,
            i_consent=False,
        )
    )
    fold = cmd_fold(
        argparse.Namespace(
            note="Arweave Turbo folds memory into mycelium (local fold only)",
            prev_hash=seal.get("merkle_root"),
            node_id="demo-biophase7",
            write=None,
            i_consent=False,
        )
    )
    return {"ok": bool(seal.get("ok") and fold.get("ok")), "seal": seal, "fold": fold, "plan": cmd_worker_plan(_ns)}


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="LYGO Immutable Anchor (local CA)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def add_write(p: argparse.ArgumentParser) -> None:
        p.add_argument("--write", default="")
        p.add_argument("--i-consent", action="store_true")

    p = sub.add_parser("seal-geodesic")
    p.add_argument("--node-id", default="NODE_LOCAL")
    p.add_argument("--truth", required=True)
    p.add_argument("--light", required=True)
    p.add_argument("--chaos", default="")
    add_write(p)

    p = sub.add_parser("fold-mycelium")
    p.add_argument("--note", required=True)
    p.add_argument("--prev-hash", default="")
    p.add_argument("--node-id", default="NODE_LOCAL")
    add_write(p)

    p = sub.add_parser("verify")
    p.add_argument("--from-file", required=True)

    p = sub.add_parser("emit-receipt")
    p.add_argument("--from-file", required=True)
    add_write(p)

    p = sub.add_parser("status")
    p.add_argument("--stack-root", default="")

    sub.add_parser("worker-plan")
    sub.add_parser("demo")
    return ap


def main(argv: list[str] | None = None) -> int:
    ns = build_parser().parse_args(argv)
    fn = {
        "seal-geodesic": cmd_seal,
        "fold-mycelium": cmd_fold,
        "verify": cmd_verify,
        "emit-receipt": cmd_receipt,
        "status": cmd_status,
        "worker-plan": cmd_worker_plan,
        "demo": cmd_demo,
    }[ns.cmd]
    out = fn(ns)
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0 if out.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
