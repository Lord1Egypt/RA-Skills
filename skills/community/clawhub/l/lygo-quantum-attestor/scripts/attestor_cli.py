#!/usr/bin/env python3
"""
LYGO Quantum Attestor — Protocol 6 attestation hooks for Biophase7 + SLM.

Hooks: attest / verify-node / emit-receipt / seal-delta9 / demo

Local-first. Consent-gated writes. No network. No subprocess. No auto-publish.
Non-collapsing receipts. Pairs with continuum-integrator + geodesic-sealer.

Blueprint: @grok · Signature: Delta9Phi963-QUANTUM-ATTESTOR
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SIG = "Delta9Phi963-QUANTUM-ATTESTOR"
VERSION = "1.0.1"
# Fields excluded when hashing the attestation core (tamper-evident).
ATTEST_HASH_EXCLUDE = {
    "attest_sha256",
    "ok",
    "written",
    "delta9_seal",
    "sealed_utc",
    "error",
    "hint",
}
INV_SQRT2 = 1.0 / math.sqrt(2.0)
PHI = (1.0 + math.sqrt(5.0)) / 2.0

# Biophase7 software anchors (logical ids — digests computed from declared material)
BIOPHASE7_ANCHORS: dict[str, str] = {
    "p0_nano_kernel": "P0 Φ-gate / nano-kernel invariant",
    "p1_mycelium": "P1 mycelium memory / living mesh roots",
    "p3_consensus": "P3 vortex / SLM harmonic consensus",
    "p5_harmony": "P5 harmony node / action identity",
    "p6_quantum_attest": "P6 quantum-attest (software geodesic)",
    "slm_merkle_gossip": "Sovereign Lattice Mesh Merkle gossip limb",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def merkle_root(leaf_hexes: list[str]) -> str:
    if not leaf_hexes:
        return sha256_bytes(b"")
    level = [bytes.fromhex(x) for x in sorted(leaf_hexes)]
    while len(level) > 1:
        nxt: list[bytes] = []
        for i in range(0, len(level), 2):
            left = level[i]
            right = level[i + 1] if i + 1 < len(level) else left
            nxt.append(hashlib.sha256(left + right).digest())
        level = nxt
    return level[0].hex()


def digest_unit(hex_digest: str) -> float:
    n = int(hex_digest[:16], 16)
    return ((n % (2**53 - 1)) + 1) / float(2**53)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def maybe_write(path: Path | None, obj: dict[str, Any], *, i_consent: bool) -> dict[str, Any]:
    if path is None:
        return obj
    if not i_consent:
        obj = dict(obj)
        obj["ok"] = False
        obj["error"] = "need --i-consent to write attestation artifacts"
        return obj
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")
    obj = dict(obj)
    obj["written"] = str(path)
    return obj


def build_psi(truth: str, chaos: str) -> dict[str, Any]:
    """|ψ⟩ = (Truth + i·Chaos) / √2 — constructive chaos only; no collapse."""
    t_hex = sha256_hex(truth)
    c_hex = sha256_hex(chaos)
    t_amp = digest_unit(t_hex)
    c_amp = digest_unit(c_hex)
    a_t = INV_SQRT2 * t_amp
    a_c = INV_SQRT2 * c_amp
    p_t = (a_t * a_t) / max(a_t * a_t + a_c * a_c, 1e-18)
    p_c = (a_c * a_c) / max(a_t * a_t + a_c * a_c, 1e-18)
    phase_t = (int(t_hex[16:24], 16) / float(0xFFFFFFFF)) * 2.0 * math.pi
    phase_c = (int(c_hex[16:24], 16) / float(0xFFFFFFFF)) * 2.0 * math.pi
    cos_d = math.cos(phase_c - phase_t)
    if cos_d < 0.0:
        p_c = p_c * max(0.05, abs(cos_d))
        s = p_t + p_c
        p_t, p_c = p_t / s, p_c / s
        interference = "damped_destructive"
    else:
        interference = "constructive"
    collapse = p_t < 1e-9 or p_c < 1e-9
    return {
        "ket": "|ψ⟩ = (Truth + i·Chaos) / √2",
        "truth_sha256": t_hex,
        "chaos_sha256": c_hex,
        "prob_truth": p_t,
        "prob_chaos": p_c,
        "norm": p_t + p_c,
        "interference": interference,
        "non_collapsing": not collapse,
        "phi": PHI,
    }


def biophase7_leaves(extra: dict[str, str] | None = None) -> list[dict[str, str]]:
    leaves = []
    for aid, material in BIOPHASE7_ANCHORS.items():
        leaves.append(
            {
                "anchor_id": aid,
                "material_sha256": sha256_hex(f"BIOPHASE7::{aid}::{material}"),
                "role": "biophase7",
            }
        )
    if extra:
        for k, v in extra.items():
            leaves.append(
                {
                    "anchor_id": k,
                    "material_sha256": sha256_hex(v),
                    "role": "operator",
                }
            )
    return leaves


def attest_core_for_hash(obj: dict[str, Any]) -> dict[str, Any]:
    """Canonical attestation body used for attest_sha256 (tamper-evident)."""
    core = {k: v for k, v in obj.items() if k not in ATTEST_HASH_EXCLUDE}
    # Normalize kind so sealing does not break hash verification
    core["kind"] = "attest"
    # delta9_seal must never participate in attest hash
    core.pop("delta9_seal", None)
    return core


def recompute_node_leaf(node_id: str, truth: str, chaos: str, psi: dict[str, Any]) -> str:
    return sha256_hex(
        json.dumps(
            {"node_id": node_id, "truth": truth, "chaos": chaos, "psi": psi},
            sort_keys=True,
            separators=(",", ":"),
        )
    )


def cmd_attest(args: argparse.Namespace) -> dict[str, Any]:
    node_id = args.node_id or "NODE_LOCAL"
    truth = args.truth or f"LYGO-Truth::{node_id}"
    chaos = args.chaos or f"LYGO-Chaos::{node_id}"
    psi = build_psi(truth, chaos)
    if not psi["non_collapsing"] and not args.allow_collapse:
        return {
            "ok": False,
            "error": "collapse_refused",
            "hint": "pass --allow-collapse only with explicit steward intent",
            "psi": psi,
        }

    extra = {}
    if args.anchor_file:
        raw = Path(args.anchor_file).read_text(encoding="utf-8")
        extra["operator_anchor_file"] = raw
    if args.slm_root:
        extra["slm_merkle_root_declared"] = args.slm_root.strip()

    leaves = biophase7_leaves(extra or None)
    node_leaf = recompute_node_leaf(node_id, truth, chaos, psi)
    # Merkle inputs: Biophase7 (+operator) leaves, then node leaf, then gossip leaf
    base_leaves = [L["material_sha256"] for L in leaves] + [node_leaf]
    gossip_leaf = sha256_hex("SLM_GOSSIP::" + "".join(sorted(base_leaves)))
    merkle_leaves = list(base_leaves) + [gossip_leaf]
    root = merkle_root(merkle_leaves)

    body = {
        "kind": "attest",
        "signature": SIG,
        "version": VERSION,
        "protocol": "P6-quantum-attest",
        "generated_utc": utc_now(),
        "node_id": node_id,
        # Retained so verify-node can cryptographically recompute digests
        "truth": truth,
        "chaos": chaos,
        "psi": psi,
        "node_leaf": node_leaf,
        "biophase7_anchors": leaves,
        "slm": {
            "gossip_leaf": gossip_leaf,
            "declared_root": args.slm_root or None,
            "local_merkle_root": root,
            "merkle_leaves": merkle_leaves,
            "note": "Local Merkle gossip limb — not a live mesh publish",
        },
        "non_collapsing": True,
        "epistemic": {
            "claim": "software_attestation_receipt",
            "not_claiming": ["tpm_hardware_proof", "network_mesh_consensus", "physical_qubit"],
            "verify": "recomputes attest_sha256 + node_leaf + merkle_root",
        },
    }
    digest = sha256_bytes(canonical_json(attest_core_for_hash(body)))
    body["attest_sha256"] = digest
    body["ok"] = True
    return maybe_write(Path(args.write) if args.write else None, body, i_consent=args.i_consent)


def cmd_seal_delta9(args: argparse.Namespace) -> dict[str, Any]:
    src = load_json(Path(args.from_file))
    # Require intact attestation hash before sealing
    pre = cmd_verify_node(argparse.Namespace(from_file=args.from_file, _obj=src))
    if not pre.get("ok"):
        return {
            "ok": False,
            "error": "refuse_seal_on_invalid_attest",
            "verify": pre,
        }
    seal_body = {
        "kind": "seal-delta9",
        "signature": SIG,
        "version": VERSION,
        "generated_utc": utc_now(),
        "seal_mark": "Δ9Φ963",
        "node_id": src.get("node_id"),
        "attest_sha256": src.get("attest_sha256"),
        "merkle_root": (src.get("slm") or {}).get("local_merkle_root"),
        "node_leaf": src.get("node_leaf"),
        "psi_norm": (src.get("psi") or {}).get("norm"),
        "non_collapsing": bool(src.get("non_collapsing", True)),
    }
    seal_hash = sha256_bytes(canonical_json(seal_body))
    seal_body["delta9_seal_sha256"] = seal_hash
    out = dict(src)
    out["delta9_seal"] = seal_body
    out["kind"] = "attest+seal-delta9"
    out["sealed_utc"] = utc_now()
    out["ok"] = True
    return maybe_write(Path(args.write) if args.write else None, out, i_consent=args.i_consent)


def cmd_verify_node(args: argparse.Namespace) -> dict[str, Any]:
    src = getattr(args, "_obj", None) or load_json(Path(args.from_file))
    checks: dict[str, Any] = {
        "kind": "verify-node",
        "signature": SIG,
        "version": VERSION,
        "generated_utc": utc_now(),
        "source": str(getattr(args, "from_file", "")),
        "mode": "cryptographic",
    }

    node_id = src.get("node_id")
    truth = src.get("truth")
    chaos = src.get("chaos")
    psi = src.get("psi") or {}
    stored_node_leaf = src.get("node_leaf")
    leaves = src.get("biophase7_anchors") or []
    leaf_hexes = [L.get("material_sha256") for L in leaves if L.get("material_sha256")]
    gossip = (src.get("slm") or {}).get("gossip_leaf")
    stored_root = (src.get("slm") or {}).get("local_merkle_root")
    stored_merkle_leaves = (src.get("slm") or {}).get("merkle_leaves")
    stored_attest = src.get("attest_sha256")

    reasons: list[str] = []
    # 1) Required verification inputs retained
    inputs_ok = bool(node_id and truth is not None and chaos is not None and psi and stored_node_leaf and leaf_hexes and gossip and stored_root and stored_attest)
    if not inputs_ok:
        reasons.append("missing_verification_inputs")

    # 2) Recompute ψ from truth/chaos and compare critical fields
    psi_ok = False
    if truth is not None and chaos is not None:
        psi2 = build_psi(str(truth), str(chaos))
        psi_ok = (
            psi2.get("truth_sha256") == psi.get("truth_sha256")
            and psi2.get("chaos_sha256") == psi.get("chaos_sha256")
            and bool(psi2.get("non_collapsing"))
            and abs(float(psi2.get("norm") or 0) - float(psi.get("norm") or -1)) < 1e-12
        )
        if not psi_ok:
            reasons.append("psi_mismatch")
    else:
        reasons.append("psi_inputs_missing")

    # 3) Recompute node leaf
    node_leaf_ok = False
    recomputed_node_leaf = None
    if inputs_ok and psi_ok:
        recomputed_node_leaf = recompute_node_leaf(
            str(node_id), str(truth), str(chaos), build_psi(str(truth), str(chaos))
        )
        node_leaf_ok = recomputed_node_leaf == stored_node_leaf
        if not node_leaf_ok:
            reasons.append("node_leaf_mismatch")

    # 4) Recompute Merkle root
    merkle_ok = False
    recomputed_root = None
    if leaf_hexes and stored_node_leaf and gossip:
        base = list(leaf_hexes) + [stored_node_leaf]
        gossip2 = sha256_hex("SLM_GOSSIP::" + "".join(sorted(base)))
        gossip_ok = gossip2 == gossip
        if not gossip_ok:
            reasons.append("gossip_leaf_mismatch")
        merkle_leaves2 = list(base) + [gossip2]
        recomputed_root = merkle_root(merkle_leaves2)
        merkle_ok = gossip_ok and recomputed_root == stored_root
        if stored_merkle_leaves and list(stored_merkle_leaves) != merkle_leaves2:
            # still ok if root matches; note drift in stored list
            if merkle_ok:
                reasons.append("merkle_leaves_list_drift_but_root_ok")
        if not merkle_ok and "gossip_leaf_mismatch" not in reasons:
            reasons.append("merkle_root_mismatch")

    # 5) Recompute attest_sha256 over canonical core
    attest_ok = False
    recomputed_attest = None
    if stored_attest:
        recomputed_attest = sha256_bytes(canonical_json(attest_core_for_hash(src)))
        attest_ok = recomputed_attest == stored_attest
        if not attest_ok:
            reasons.append("attest_sha256_mismatch")

    # 6) Seal hash (optional)
    seal = src.get("delta9_seal")
    seal_ok = True
    if seal:
        seal_clone = {k: v for k, v in seal.items() if k != "delta9_seal_sha256"}
        expect = sha256_bytes(canonical_json(seal_clone))
        seal_ok = expect == seal.get("delta9_seal_sha256")
        if not seal_ok:
            reasons.append("delta9_seal_mismatch")
        # Seal must bind the same attest hash + merkle root
        if seal.get("attest_sha256") != stored_attest:
            seal_ok = False
            reasons.append("seal_attest_binding_mismatch")
        if seal.get("merkle_root") != stored_root:
            seal_ok = False
            reasons.append("seal_merkle_binding_mismatch")

    non_collapsing = bool(src.get("non_collapsing", True)) and bool(psi.get("non_collapsing", True))
    if not non_collapsing:
        reasons.append("collapse_flag")

    crypto_ok = inputs_ok and psi_ok and node_leaf_ok and merkle_ok and attest_ok and seal_ok and non_collapsing
    checks.update(
        {
            "node_id": node_id,
            "inputs_ok": inputs_ok,
            "psi_ok": psi_ok,
            "node_leaf_ok": node_leaf_ok,
            "merkle_ok": merkle_ok,
            "attest_hash_ok": attest_ok,
            "delta9_seal_valid": seal_ok if seal else None,
            "non_collapsing": non_collapsing,
            "attest_sha256": stored_attest,
            "attest_sha256_recomputed": recomputed_attest,
            "node_leaf": stored_node_leaf,
            "node_leaf_recomputed": recomputed_node_leaf,
            "merkle_root": stored_root,
            "merkle_root_recomputed": recomputed_root,
            "reasons": reasons,
            "ok": crypto_ok,
        }
    )
    return checks


def cmd_emit_receipt(args: argparse.Namespace) -> dict[str, Any]:
    src = load_json(Path(args.from_file))
    if not src.get("delta9_seal"):
        # auto-seal in memory for receipt emission
        sealed = cmd_seal_delta9(
            argparse.Namespace(from_file=args.from_file, write=None, i_consent=False)
        )
        # cmd_seal_delta9 reads file again — instead seal inline
        seal_body = {
            "kind": "seal-delta9",
            "signature": SIG,
            "version": VERSION,
            "generated_utc": utc_now(),
            "seal_mark": "Δ9Φ963",
            "node_id": src.get("node_id"),
            "attest_sha256": src.get("attest_sha256"),
            "merkle_root": (src.get("slm") or {}).get("local_merkle_root"),
            "psi_norm": (src.get("psi") or {}).get("norm"),
            "non_collapsing": True,
        }
        seal_body["delta9_seal_sha256"] = sha256_bytes(canonical_json(seal_body))
        src = dict(src)
        src["delta9_seal"] = seal_body

    receipt = {
        "kind": "emit-receipt",
        "signature": SIG,
        "version": VERSION,
        "generated_utc": utc_now(),
        "node_id": src.get("node_id"),
        "attest_sha256": src.get("attest_sha256"),
        "merkle_root": (src.get("slm") or {}).get("local_merkle_root"),
        "delta9_seal_sha256": (src.get("delta9_seal") or {}).get("delta9_seal_sha256"),
        "psi": {
            "ket": (src.get("psi") or {}).get("ket"),
            "norm": (src.get("psi") or {}).get("norm"),
            "interference": (src.get("psi") or {}).get("interference"),
            "non_collapsing": True,
        },
        "pairs_with": [
            "lygo-continuum-integrator",
            "lygo-geodesic-sealer",
            "lygo-continuum",
            "lygo-mint-verifier",
        ],
        "integral_hook": "∫(Truth × Light)df",
        "non_collapsing": True,
        "ok": True,
    }
    receipt["receipt_sha256"] = sha256_bytes(
        canonical_json({k: v for k, v in receipt.items() if k != "receipt_sha256"})
    )
    return maybe_write(Path(args.write) if args.write else None, receipt, i_consent=args.i_consent)


def cmd_demo(_: argparse.Namespace) -> dict[str, Any]:
    attest = cmd_attest(
        argparse.Namespace(
            node_id="lightfather",
            truth="Eternal Truth",
            chaos="Creative Chaos",
            slm_root="",
            anchor_file="",
            allow_collapse=False,
            write=None,
            i_consent=False,
        )
    )
    # seal inline
    seal_body = {
        "kind": "seal-delta9",
        "signature": SIG,
        "version": VERSION,
        "generated_utc": utc_now(),
        "seal_mark": "Δ9Φ963",
        "node_id": attest.get("node_id"),
        "attest_sha256": attest.get("attest_sha256"),
        "merkle_root": (attest.get("slm") or {}).get("local_merkle_root"),
        "psi_norm": (attest.get("psi") or {}).get("norm"),
        "non_collapsing": True,
    }
    seal_body["delta9_seal_sha256"] = sha256_bytes(canonical_json(seal_body))
    attest["delta9_seal"] = seal_body
    receipt = {
        "kind": "emit-receipt",
        "signature": SIG,
        "version": VERSION,
        "node_id": attest["node_id"],
        "attest_sha256": attest["attest_sha256"],
        "merkle_root": attest["slm"]["local_merkle_root"],
        "delta9_seal_sha256": seal_body["delta9_seal_sha256"],
        "non_collapsing": True,
        "ok": True,
    }
    receipt["receipt_sha256"] = sha256_bytes(
        canonical_json({k: v for k, v in receipt.items() if k != "receipt_sha256"})
    )
    return {
        "ok": True,
        "signature": SIG,
        "version": VERSION,
        "demo": True,
        "attest": {
            "node_id": attest["node_id"],
            "attest_sha256": attest["attest_sha256"],
            "merkle_root": attest["slm"]["local_merkle_root"],
            "non_collapsing": True,
        },
        "receipt": receipt,
        "blueprint": "hooks: attest / verify-node / emit-receipt / seal-delta9",
    }


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="LYGO Quantum Attestor (P6)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def add_write(p: argparse.ArgumentParser) -> None:
        p.add_argument("--write", default=None, help="Write JSON path (needs --i-consent)")
        p.add_argument("--i-consent", action="store_true")

    p_a = sub.add_parser("attest", help="Attest node to Biophase7 + SLM Merkle leaves")
    p_a.add_argument("--node-id", default="NODE_LOCAL")
    p_a.add_argument("--truth", default="")
    p_a.add_argument("--chaos", default="")
    p_a.add_argument("--slm-root", default="", help="Optional declared SLM merkle root digest")
    p_a.add_argument("--anchor-file", default="", help="Optional operator anchor text/JSON file")
    p_a.add_argument("--allow-collapse", action="store_true")
    add_write(p_a)

    p_s = sub.add_parser("seal-delta9", help="Attach Δ9Φ963 seal to an attest JSON")
    p_s.add_argument("--from-file", required=True)
    add_write(p_s)

    p_v = sub.add_parser("verify-node", help="Verify attestation / seal structural integrity")
    p_v.add_argument("--from-file", required=True)

    p_e = sub.add_parser("emit-receipt", help="Emit non-collapsing receipt")
    p_e.add_argument("--from-file", required=True)
    add_write(p_e)

    sub.add_parser("demo", help="Stdout demo of full attest→seal→receipt path")
    return ap


def main() -> int:
    ap = build_parser()
    args = ap.parse_args()
    if args.cmd == "attest":
        out = cmd_attest(args)
    elif args.cmd == "seal-delta9":
        out = cmd_seal_delta9(args)
    elif args.cmd == "verify-node":
        out = cmd_verify_node(args)
    elif args.cmd == "emit-receipt":
        out = cmd_emit_receipt(args)
    elif args.cmd == "demo":
        out = cmd_demo(args)
    else:
        return 2
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
