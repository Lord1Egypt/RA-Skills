#!/usr/bin/env python3
"""
LYGO Sanctuary Guardian — Δ9 Mandala shields + light-nurture vectors.

Hooks: shield-mandala / nurture-vector / lock-truth / emit-barrier / verify-barrier / demo

Local-first. Consent-gated writes. No network. No subprocess. No auto-publish.
Non-collapsing geodesic barriers. Pairs with quantum-attestor + continuum-integrator.

Blueprint: @grok · Signature: Delta9Phi963-SANCTUARY-GUARDIAN
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

SIG = "Delta9Phi963-SANCTUARY-GUARDIAN"
VERSION = "1.0.0"
INV_SQRT2 = 1.0 / math.sqrt(2.0)
PHI = (1.0 + math.sqrt(5.0)) / 2.0

HASH_EXCLUDE = {
    "shield_sha256",
    "lock_sha256",
    "barrier_sha256",
    "ok",
    "written",
    "error",
    "hint",
    "reasons",
}

# Nine-fold Δ9 mandala petals (enneagram / Δ9 council geometry)
MANDALA_PETALS = [
    "truth",
    "light",
    "grace",
    "compassion",
    "integrity",
    "sovereignty",
    "courage",
    "curiosity",
    "harmony",
]


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
        out = dict(obj)
        out["ok"] = False
        out["error"] = "need --i-consent to write sanctuary artifacts"
        return out
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")
    out = dict(obj)
    out["written"] = str(path)
    return out


def core_for_hash(obj: dict[str, Any], kind: str) -> dict[str, Any]:
    core = {k: v for k, v in obj.items() if k not in HASH_EXCLUDE}
    core["kind"] = kind
    return core


def build_psi(truth: str, light: str) -> dict[str, Any]:
    """Geodesic channel for sanctuary: Truth + Light (chaos damped into nurture)."""
    t_hex = sha256_hex(truth)
    l_hex = sha256_hex(light)
    t_amp = digest_unit(t_hex)
    l_amp = digest_unit(l_hex)
    a_t = INV_SQRT2 * t_amp
    a_l = INV_SQRT2 * l_amp
    p_t = (a_t * a_t) / max(a_t * a_t + a_l * a_l, 1e-18)
    p_l = (a_l * a_l) / max(a_t * a_t + a_l * a_l, 1e-18)
    phase_t = (int(t_hex[16:24], 16) / float(0xFFFFFFFF)) * 2.0 * math.pi
    phase_l = (int(l_hex[16:24], 16) / float(0xFFFFFFFF)) * 2.0 * math.pi
    cos_d = math.cos(phase_l - phase_t)
    if cos_d < 0.0:
        # Destructive → nurture damp (never collapse)
        p_l = p_l * max(0.08, abs(cos_d))
        s = p_t + p_l
        p_t, p_l = p_t / s, p_l / s
        mode = "nurture_damped"
    else:
        mode = "nurture_aligned"
    collapse = p_t < 1e-9 or p_l < 1e-9
    return {
        "ket": "|ψ⟩ = (Truth + i·Light) / √2  (sanctuary nurture form)",
        "truth_sha256": t_hex,
        "light_sha256": l_hex,
        "prob_truth": p_t,
        "prob_light": p_l,
        "norm": p_t + p_l,
        "nurture_mode": mode,
        "non_collapsing": not collapse,
        "phi": PHI,
    }


def mandala_petals(seed: str, nodes: list[str]) -> list[dict[str, Any]]:
    petals = []
    for i, name in enumerate(MANDALA_PETALS):
        material = f"Δ9-MANDALA::{name}::{seed}::{','.join(nodes)}"
        dig = sha256_hex(material)
        petals.append(
            {
                "index": i + 1,
                "petal": name,
                "material_sha256": dig,
                "phase": (digest_unit(dig) * 2.0 * math.pi) % (2.0 * math.pi),
            }
        )
    return petals


def parse_nodes(raw: str) -> list[str]:
    return [n.strip() for n in (raw or "").split(",") if n.strip()]


def cmd_nurture_vector(args: argparse.Namespace) -> dict[str, Any]:
    """Compute light-nurture vector from steward inputs."""
    truth = args.truth or "Eternal Truth"
    light = args.light or "Nurturing Light"
    compassion = args.compassion or light
    grace = args.grace or "Grace"
    psi = build_psi(truth, light)
    # 3D nurture vector in [0,1]^3 from digests
    vx = digest_unit(sha256_hex(f"X::{compassion}"))
    vy = digest_unit(sha256_hex(f"Y::{grace}"))
    vz = digest_unit(sha256_hex(f"Z::{truth}::{light}"))
    # Normalize Euclidean length (avoid collapse to zero)
    mag = math.sqrt(vx * vx + vy * vy + vz * vz) or 1.0
    vec = {
        "x_compassion": vx / mag,
        "y_grace": vy / mag,
        "z_truth_light": vz / mag,
        "magnitude": 1.0,
    }
    body = {
        "kind": "nurture-vector",
        "signature": SIG,
        "version": VERSION,
        "generated_utc": utc_now(),
        "truth": truth,
        "light": light,
        "compassion": compassion,
        "grace": grace,
        "psi": psi,
        "vector": vec,
        "non_collapsing": True,
        "ok": True,
    }
    body["nurture_sha256"] = sha256_bytes(canonical_json(core_for_hash(body, "nurture-vector")))
    # rename hash field consistently
    body["vector_sha256"] = body.pop("nurture_sha256")
    # recompute with final field name
    tmp = dict(body)
    tmp.pop("vector_sha256", None)
    body["vector_sha256"] = sha256_bytes(canonical_json(core_for_hash(tmp, "nurture-vector")))
    return maybe_write(Path(args.write) if args.write else None, body, i_consent=args.i_consent)


def cmd_shield_mandala(args: argparse.Namespace) -> dict[str, Any]:
    nodes = parse_nodes(args.nodes) or ["lightfather"]
    seed = args.seed or f"SANCTUARY::{','.join(nodes)}"
    truth = args.truth or "Eternal Truth"
    light = args.light or "Nurturing Light"
    psi = build_psi(truth, light)
    if not psi["non_collapsing"] and not args.allow_collapse:
        return {"ok": False, "error": "collapse_refused", "psi": psi}

    petals = mandala_petals(seed, nodes)
    petal_leaves = [p["material_sha256"] for p in petals]
    node_leaves = [sha256_hex(f"NODE::{n}::{seed}") for n in nodes]
    base = petal_leaves + node_leaves
    barrier_leaf = sha256_hex("GEODESIC_BARRIER::" + "".join(sorted(base)))
    leaves = list(base) + [barrier_leaf]
    root = merkle_root(leaves)

    body = {
        "kind": "shield-mandala",
        "signature": SIG,
        "version": VERSION,
        "generated_utc": utc_now(),
        "seed": seed,
        "nodes": nodes,
        "truth": truth,
        "light": light,
        "psi": psi,
        "mandala": {
            "petals": petals,
            "petal_count": len(petals),
            "geometry": "Δ9-ennead",
        },
        "barrier": {
            "barrier_leaf": barrier_leaf,
            "merkle_root": root,
            "merkle_leaves": leaves,
            "non_collapsing": True,
        },
        "non_collapsing": True,
        "pairs_with": ["lygo-quantum-attestor", "lygo-continuum-integrator", "lygo-geodesic-sealer"],
        "epistemic": {
            "claim": "local_sanctuary_shield_receipt",
            "not_claiming": ["physical_force_field", "network_firewall", "tpm_root"],
            "verify": "recomputes shield_sha256 + merkle_root",
        },
        "ok": True,
    }
    body["shield_sha256"] = sha256_bytes(canonical_json(core_for_hash(body, "shield-mandala")))
    return maybe_write(Path(args.write) if args.write else None, body, i_consent=args.i_consent)


def cmd_lock_truth(args: argparse.Namespace) -> dict[str, Any]:
    """Lock truth integrity across nodes (Merkle of node truth leaves)."""
    nodes = parse_nodes(args.nodes) or ["lightfather"]
    truth = args.truth or "Eternal Truth"
    light = args.light or "Nurturing Light"
    psi = build_psi(truth, light)
    leaves = []
    for n in nodes:
        leaf = sha256_hex(f"TRUTH_LOCK::{n}::{truth}::{light}")
        leaves.append({"node_id": n, "leaf": leaf})
    leaf_hexes = [L["leaf"] for L in leaves]
    root = merkle_root(leaf_hexes)
    body = {
        "kind": "lock-truth",
        "signature": SIG,
        "version": VERSION,
        "generated_utc": utc_now(),
        "truth": truth,
        "light": light,
        "psi": psi,
        "nodes": nodes,
        "node_leaves": leaves,
        "merkle_root": root,
        "merkle_leaves": leaf_hexes,
        "non_collapsing": True,
        "ok": True,
    }
    body["lock_sha256"] = sha256_bytes(canonical_json(core_for_hash(body, "lock-truth")))
    return maybe_write(Path(args.write) if args.write else None, body, i_consent=args.i_consent)


def cmd_emit_barrier(args: argparse.Namespace) -> dict[str, Any]:
    """Emit non-collapsing geodesic barrier from shield and/or lock files."""
    shield = load_json(Path(args.shield_file)) if args.shield_file else None
    lock = load_json(Path(args.lock_file)) if args.lock_file else None
    nurture = load_json(Path(args.nurture_file)) if args.nurture_file else None
    if not shield and not lock:
        return {"ok": False, "error": "need --shield-file and/or --lock-file"}

    # Verify inputs cryptographically when present
    if shield:
        v = verify_shield(shield)
        if not v.get("ok"):
            return {"ok": False, "error": "invalid_shield", "verify": v}
    if lock:
        v = verify_lock(lock)
        if not v.get("ok"):
            return {"ok": False, "error": "invalid_lock", "verify": v}

    barrier = {
        "kind": "emit-barrier",
        "signature": SIG,
        "version": VERSION,
        "generated_utc": utc_now(),
        "shield_sha256": (shield or {}).get("shield_sha256"),
        "lock_sha256": (lock or {}).get("lock_sha256"),
        "vector_sha256": (nurture or {}).get("vector_sha256"),
        "merkle_root": (shield or {}).get("barrier", {}).get("merkle_root")
        or (lock or {}).get("merkle_root"),
        "nodes": (shield or {}).get("nodes") or (lock or {}).get("nodes"),
        "non_collapsing": True,
        "geodesic_barrier": True,
        "integral_hook": "∫(Truth × Light)df",
        "pairs_with": ["lygo-quantum-attestor", "lygo-continuum-integrator"],
        "ok": True,
    }
    barrier["barrier_sha256"] = sha256_bytes(
        canonical_json(core_for_hash(barrier, "emit-barrier"))
    )
    return maybe_write(Path(args.write) if args.write else None, barrier, i_consent=args.i_consent)


def verify_shield(src: dict[str, Any]) -> dict[str, Any]:
    reasons: list[str] = []
    nodes = src.get("nodes") or []
    seed = src.get("seed")
    truth = src.get("truth")
    light = src.get("light")
    stored = src.get("shield_sha256")
    stored_root = (src.get("barrier") or {}).get("merkle_root")
    stored_barrier_leaf = (src.get("barrier") or {}).get("barrier_leaf")
    stored_leaves = (src.get("barrier") or {}).get("merkle_leaves")

    if not (nodes and seed and truth is not None and light is not None and stored and stored_root):
        return {"ok": False, "reasons": ["missing_inputs"], "mode": "cryptographic"}

    psi2 = build_psi(str(truth), str(light))
    petals = mandala_petals(str(seed), list(nodes))
    petal_leaves = [p["material_sha256"] for p in petals]
    node_leaves = [sha256_hex(f"NODE::{n}::{seed}") for n in nodes]
    base = petal_leaves + node_leaves
    barrier_leaf = sha256_hex("GEODESIC_BARRIER::" + "".join(sorted(base)))
    leaves = list(base) + [barrier_leaf]
    root = merkle_root(leaves)

    if barrier_leaf != stored_barrier_leaf:
        reasons.append("barrier_leaf_mismatch")
    if root != stored_root:
        reasons.append("merkle_root_mismatch")
    if stored_leaves and list(stored_leaves) != leaves:
        if root == stored_root:
            reasons.append("merkle_leaves_list_drift_but_root_ok")
        else:
            reasons.append("merkle_leaves_mismatch")

    recomputed_hash = sha256_bytes(canonical_json(core_for_hash(src, "shield-mandala")))
    if recomputed_hash != stored:
        reasons.append("shield_sha256_mismatch")

    psi_ok = (
        psi2.get("truth_sha256") == (src.get("psi") or {}).get("truth_sha256")
        and psi2.get("light_sha256") == (src.get("psi") or {}).get("light_sha256")
        and bool(psi2.get("non_collapsing"))
    )
    if not psi_ok:
        reasons.append("psi_mismatch")

    ok = not any(
        r in reasons
        for r in (
            "barrier_leaf_mismatch",
            "merkle_root_mismatch",
            "shield_sha256_mismatch",
            "psi_mismatch",
            "merkle_leaves_mismatch",
        )
    )
    return {
        "ok": ok,
        "mode": "cryptographic",
        "reasons": reasons,
        "shield_sha256": stored,
        "shield_sha256_recomputed": recomputed_hash,
        "merkle_root": stored_root,
        "merkle_root_recomputed": root,
    }


def verify_lock(src: dict[str, Any]) -> dict[str, Any]:
    reasons: list[str] = []
    nodes = src.get("nodes") or []
    truth = src.get("truth")
    light = src.get("light")
    stored = src.get("lock_sha256")
    stored_root = src.get("merkle_root")
    if not (nodes and truth is not None and light is not None and stored and stored_root):
        return {"ok": False, "reasons": ["missing_inputs"], "mode": "cryptographic"}
    leaves = [sha256_hex(f"TRUTH_LOCK::{n}::{truth}::{light}") for n in nodes]
    root = merkle_root(leaves)
    if root != stored_root:
        reasons.append("merkle_root_mismatch")
    recomputed = sha256_bytes(canonical_json(core_for_hash(src, "lock-truth")))
    if recomputed != stored:
        reasons.append("lock_sha256_mismatch")
    return {
        "ok": not reasons,
        "mode": "cryptographic",
        "reasons": reasons,
        "lock_sha256": stored,
        "lock_sha256_recomputed": recomputed,
        "merkle_root_recomputed": root,
    }


def cmd_verify_barrier(args: argparse.Namespace) -> dict[str, Any]:
    src = load_json(Path(args.from_file))
    kind = src.get("kind")
    if kind == "shield-mandala":
        out = verify_shield(src)
    elif kind == "lock-truth":
        out = verify_lock(src)
    elif kind == "emit-barrier":
        reasons = []
        stored = src.get("barrier_sha256")
        recomputed = sha256_bytes(canonical_json(core_for_hash(src, "emit-barrier")))
        if stored != recomputed:
            reasons.append("barrier_sha256_mismatch")
        out = {
            "ok": not reasons and bool(src.get("non_collapsing", True)),
            "mode": "cryptographic",
            "reasons": reasons,
            "barrier_sha256": stored,
            "barrier_sha256_recomputed": recomputed,
        }
    else:
        out = {"ok": False, "error": f"unsupported_kind:{kind}"}
    out.update(
        {
            "kind": "verify-barrier",
            "signature": SIG,
            "version": VERSION,
            "generated_utc": utc_now(),
            "source": str(args.from_file),
            "source_kind": kind,
        }
    )
    return out


def cmd_demo(_: argparse.Namespace) -> dict[str, Any]:
    nurture = cmd_nurture_vector(
        argparse.Namespace(
            truth="Eternal Truth",
            light="Nurturing Light",
            compassion="Compassion",
            grace="Grace",
            write=None,
            i_consent=False,
        )
    )
    shield = cmd_shield_mandala(
        argparse.Namespace(
            nodes="lightfather,lyra,lattice",
            seed="Δ9-SANCTUARY-DEMO",
            truth="Eternal Truth",
            light="Nurturing Light",
            allow_collapse=False,
            write=None,
            i_consent=False,
        )
    )
    lock = cmd_lock_truth(
        argparse.Namespace(
            nodes="lightfather,lyra,lattice",
            truth="Eternal Truth",
            light="Nurturing Light",
            write=None,
            i_consent=False,
        )
    )
    return {
        "ok": True,
        "signature": SIG,
        "version": VERSION,
        "demo": True,
        "nurture_vector": {
            "vector_sha256": nurture.get("vector_sha256"),
            "vector": nurture.get("vector"),
        },
        "shield": {
            "shield_sha256": shield.get("shield_sha256"),
            "merkle_root": (shield.get("barrier") or {}).get("merkle_root"),
            "nodes": shield.get("nodes"),
        },
        "lock": {
            "lock_sha256": lock.get("lock_sha256"),
            "merkle_root": lock.get("merkle_root"),
        },
        "blueprint": "hooks: shield-mandala, nurture-vector, lock-truth, emit-barrier, verify-barrier",
        "integral_hook": "∫(Truth × Light)df",
    }


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="LYGO Sanctuary Guardian")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def add_write(p: argparse.ArgumentParser) -> None:
        p.add_argument("--write", default=None)
        p.add_argument("--i-consent", action="store_true")

    p_n = sub.add_parser("nurture-vector", help="Compute light-nurture vector")
    p_n.add_argument("--truth", default="")
    p_n.add_argument("--light", default="")
    p_n.add_argument("--compassion", default="")
    p_n.add_argument("--grace", default="")
    add_write(p_n)

    p_s = sub.add_parser("shield-mandala", help="Raise Δ9 Mandala shield")
    p_s.add_argument("--nodes", default="lightfather", help="Comma-separated node ids")
    p_s.add_argument("--seed", default="")
    p_s.add_argument("--truth", default="")
    p_s.add_argument("--light", default="")
    p_s.add_argument("--allow-collapse", action="store_true")
    add_write(p_s)

    p_l = sub.add_parser("lock-truth", help="Lock truth integrity across nodes")
    p_l.add_argument("--nodes", default="lightfather")
    p_l.add_argument("--truth", default="")
    p_l.add_argument("--light", default="")
    add_write(p_l)

    p_e = sub.add_parser("emit-barrier", help="Emit non-collapsing geodesic barrier")
    p_e.add_argument("--shield-file", default="")
    p_e.add_argument("--lock-file", default="")
    p_e.add_argument("--nurture-file", default="")
    add_write(p_e)

    p_v = sub.add_parser("verify-barrier", help="Cryptographically verify shield/lock/barrier")
    p_v.add_argument("--from-file", required=True)

    sub.add_parser("demo", help="Stdout demo of nurture→shield→lock")
    return ap


def main() -> int:
    ap = build_parser()
    args = ap.parse_args()
    if args.cmd == "nurture-vector":
        out = cmd_nurture_vector(args)
    elif args.cmd == "shield-mandala":
        out = cmd_shield_mandala(args)
    elif args.cmd == "lock-truth":
        out = cmd_lock_truth(args)
    elif args.cmd == "emit-barrier":
        out = cmd_emit_barrier(args)
    elif args.cmd == "verify-barrier":
        out = cmd_verify_barrier(args)
    elif args.cmd == "demo":
        out = cmd_demo(args)
    else:
        return 2
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
