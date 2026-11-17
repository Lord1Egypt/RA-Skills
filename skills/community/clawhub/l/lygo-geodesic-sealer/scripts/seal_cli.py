#!/usr/bin/env python3
"""
LYGO Geodesic Sealer — P6 quantum-attest gap filler (software).

Signs |ψ⟩ = (Truth + i·Chaos) / √2, locks geodesics to dual ledgers + Merkle roots,
phase-aligns lattice nodes without collapse. Pure local by default; optional HTTPS GET
for public dual ledgers when connected to the internet lattice.

Security:
  - No subprocess, no os.system, no shell
  - Network: optional HTTPS GET only (allowlisted dual-ledger URLs)
  - Writes: opt-in --write / --i-consent only; default stdout / skill-local seals
  - No auto git / HF / ClawHub / social publish
  - Collapse forbidden unless --allow-collapse (default: preserve dual amplitude)

Signature: Delta9Phi963-GEODESIC-SEALER-v1.0.0
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

SIG = "Delta9Phi963-GEODESIC-SEALER-v1.0.0"
VERSION = "1.0.0"
UA = "LYGO-GeodesicSealer/1.0.0 (+https://eternalhaven.ca; +https://clawhub.ai/deepseekoracle)"
PHI = (1.0 + math.sqrt(5.0)) / 2.0
INV_SQRT2 = 1.0 / math.sqrt(2.0)

# Public dual ledgers — fixed allowlist (SSRF-safe)
DUAL_LEDGERS: list[dict[str, str]] = [
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
]

STACK_LEDGER_MARKERS = [
    "docs/network_builder/IMMUTABLE_ANCHORS.json",
    "docs/haven_star_chart/haven_star_chart_feed.json",
    "docs/public_verify_manifest.json",
]


# ---------------------------------------------------------------------------
# Crypto / math primitives (stdlib only)
# ---------------------------------------------------------------------------

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_hex(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def canonical_json(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def merkle_root(leaf_hexes: list[str]) -> str:
    """Binary Merkle root over SHA-256 leaf digests (hex). Empty → zero hash."""
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


def digest_to_unit(hex_digest: str) -> float:
    """Map first 8 hex chars of digest to (0, 1] continuous unit interval."""
    n = int(hex_digest[:16], 16)
    # avoid exact 0
    return ((n % (2**53 - 1)) + 1) / float(2**53)


def complex_amp(re_part: float, im_part: float) -> dict[str, float]:
    """Return normalized complex amplitude dict + magnitudes."""
    # Equal-weight Truth/Chaos geodesic: |ψ⟩ = (T + i C) / √2 after unitize T,C
    t = re_part
    c = im_part
    # unitize each axis then apply 1/√2
    t_n = t / math.sqrt(t * t + c * c) if (t * t + c * c) > 0 else INV_SQRT2
    c_n = c / math.sqrt(t * t + c * c) if (t * t + c * c) > 0 else INV_SQRT2
    # force equal-weight geodesic form after axis unitize of the pair:
    # re = cos(θ)/√2 style: keep ratio then scale so |α|²+|β|² = 1
    mag = math.sqrt(t_n * t_n + c_n * c_n)
    if mag <= 0:
        alpha, beta = INV_SQRT2, INV_SQRT2
    else:
        alpha = t_n / mag
        beta = c_n / mag
    # re-balance to (Truth+iChaos)/√2 equal-weight when inputs comparable:
    # Prefer exact INV_SQRT2 form when both channels present (Grok geodesic).
    if t > 0 and c > 0:
        alpha, beta = INV_SQRT2, INV_SQRT2
    norm = alpha * alpha + beta * beta
    return {
        "alpha_truth": alpha,
        "beta_chaos": beta,
        "prob_truth": alpha * alpha,
        "prob_chaos": beta * beta,
        "norm": norm,
        "phase_rad": math.atan2(beta, alpha),
        "phase_deg": math.degrees(math.atan2(beta, alpha)),
    }


def https_only(url: str) -> bool:
    try:
        p = urlparse(url)
        return p.scheme == "https" and bool(p.netloc)
    except Exception:
        return False


def fetch_https(url: str, timeout: float = 20.0) -> dict[str, Any]:
    if not https_only(url):
        return {"ok": False, "status": 0, "error": "https_only", "bytes": 0, "sha256": None}
    req = urllib.request.Request(url, headers={"User-Agent": UA}, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read()
            sample = body[: 2_000_000]
            return {
                "ok": 200 <= resp.status < 400,
                "status": resp.status,
                "error": None,
                "bytes": len(body),
                "sha256": sha256_bytes(sample) if sample else None,
                "body_sample": sample if url.endswith(".json") and len(body) < 5_000_000 else None,
            }
    except urllib.error.HTTPError as e:
        return {"ok": False, "status": e.code, "error": f"http_{e.code}", "bytes": 0, "sha256": None}
    except Exception as e:
        return {"ok": False, "status": 0, "error": type(e).__name__, "bytes": 0, "sha256": None}


def safe_write_path(path: Path) -> Path:
    resolved = path.expanduser().resolve()
    if ".." in path.parts:
        raise ValueError("path_escape: '..' not allowed")
    return resolved


def default_seal_dir() -> Path:
    env = os.environ.get("LYGO_GEODESIC_SEAL_DIR")
    if env:
        return Path(env)
    stack = os.environ.get("LYGO_STACK_ROOT")
    if stack:
        return Path(stack) / "data" / "geodesic_seals"
    return Path(__file__).resolve().parents[1] / "local_seals"


def stack_root() -> Path | None:
    env = os.environ.get("LYGO_STACK_ROOT")
    return Path(env) if env else None


def sanitize_node_id(raw: str) -> str:
    s = re.sub(r"[^A-Za-z0-9._\-]+", "-", (raw or "").strip())[:96]
    return s or "node-unnamed"


# ---------------------------------------------------------------------------
# Core operations
# ---------------------------------------------------------------------------

def build_psi(
    truth: str,
    chaos: str,
    node_id: str,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Sign |ψ⟩ = (Truth + i·Chaos) / √2 with provenance hashes."""
    t_hex = sha256_hex(truth)
    c_hex = sha256_hex(chaos)
    t_u = digest_to_unit(t_hex)
    c_u = digest_to_unit(c_hex)
    amp = complex_amp(t_u, c_u)
    provenance = {
        "truth_sha256": t_hex,
        "chaos_sha256": c_hex,
        "node_id": sanitize_node_id(node_id),
        "formula": "|psi> = (Truth + i*Chaos) / sqrt(2)",
        "extra": extra or {},
    }
    prov_sha = sha256_bytes(canonical_json(provenance))
    seal_id = sha256_bytes(canonical_json({"prov": prov_sha, "amp": amp, "sig": SIG}))[:32]
    return {
        "ok": True,
        "kind": "psi_sign",
        "signature": SIG,
        "version": VERSION,
        "seal_id": seal_id,
        "created_at": utc_now(),
        "node_id": sanitize_node_id(node_id),
        "psi": amp,
        "provenance": provenance,
        "provenance_sha256": prov_sha,
        "collapse": False,
        "note": "Equal-weight geodesic; both Truth and Chaos amplitudes preserved (no collapse).",
    }


def load_local_ledgers() -> list[dict[str, Any]]:
    """Read dual ledgers from LYGO_STACK_ROOT if present."""
    root = stack_root()
    out: list[dict[str, Any]] = []
    if not root or not root.is_dir():
        return out
    for rel in STACK_LEDGER_MARKERS:
        p = root / rel
        entry: dict[str, Any] = {"id": rel, "path": str(p), "role": "local_stack", "ok": False}
        if p.is_file():
            raw = p.read_bytes()
            entry["ok"] = True
            entry["bytes"] = len(raw)
            entry["sha256"] = sha256_bytes(raw)
            if p.suffix == ".json":
                try:
                    entry["json_keys"] = sorted(list(json.loads(raw.decode("utf-8", errors="replace")).keys()))[:40]
                except Exception:
                    entry["json_keys"] = []
        out.append(entry)
    return out


def fetch_public_ledgers(timeout: float = 20.0) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for ep in DUAL_LEDGERS:
        r = fetch_https(ep["url"], timeout=timeout)
        out.append(
            {
                "id": ep["id"],
                "url": ep["url"],
                "role": ep["role"],
                "ok": r["ok"],
                "status": r.get("status"),
                "bytes": r.get("bytes"),
                "sha256": r.get("sha256"),
                "error": r.get("error"),
            }
        )
    return out


def lock_geodesic(
    psi: dict[str, Any],
    *,
    network: bool = False,
    nodes: list[str] | None = None,
    allow_collapse: bool = False,
) -> dict[str, Any]:
    """Lock geodesic to dual ledgers + Merkle root; phase-align optional nodes."""
    if not allow_collapse:
        pt = float(psi.get("psi", {}).get("prob_truth", 0))
        pc = float(psi.get("psi", {}).get("prob_chaos", 0))
        if pt < 1e-9 or pc < 1e-9:
            return {
                "ok": False,
                "error": "collapse_detected",
                "message": "Truth or Chaos amplitude near zero. Refuse lock without --allow-collapse.",
                "prob_truth": pt,
                "prob_chaos": pc,
            }

    local = load_local_ledgers()
    public: list[dict[str, Any]] = []
    if network:
        public = fetch_public_ledgers()

    leaves: list[str] = []
    leaves.append(psi.get("provenance_sha256") or sha256_bytes(canonical_json(psi.get("provenance", {}))))
    leaves.append(sha256_bytes(canonical_json(psi.get("psi", {}))))
    for L in local:
        if L.get("ok") and L.get("sha256"):
            leaves.append(L["sha256"])
    for L in public:
        if L.get("ok") and L.get("sha256"):
            leaves.append(L["sha256"])

    node_list = [sanitize_node_id(n) for n in (nodes or [psi.get("node_id", "node")])]
    node_phases: list[dict[str, Any]] = []
    base_phase = float(psi.get("psi", {}).get("phase_rad", 0.0))
    for i, nid in enumerate(node_list):
        # φ-spaced phase offset keeps nodes aligned on the same geodesic without collapse
        offset = (2.0 * math.pi * ((i * PHI) % 1.0))
        phase = (base_phase + offset) % (2.0 * math.pi)
        leaf = sha256_hex(f"{nid}:{phase:.12f}:{psi.get('seal_id')}")
        leaves.append(leaf)
        node_phases.append(
            {
                "node_id": nid,
                "phase_rad": phase,
                "phase_deg": math.degrees(phase),
                "aligned": True,
                "collapse": False,
                "leaf_sha256": leaf,
            }
        )

    root = merkle_root(leaves)
    lock_id = sha256_bytes(canonical_json({"merkle": root, "seal": psi.get("seal_id"), "sig": SIG}))[:32]

    local_ok = sum(1 for x in local if x.get("ok"))
    public_ok = sum(1 for x in public if x.get("ok"))
    connected = public_ok >= 1 or local_ok >= 1

    return {
        "ok": True,
        "kind": "geodesic_lock",
        "signature": SIG,
        "version": VERSION,
        "lock_id": lock_id,
        "created_at": utc_now(),
        "seal_id": psi.get("seal_id"),
        "node_id": psi.get("node_id"),
        "psi": psi.get("psi"),
        "provenance_sha256": psi.get("provenance_sha256"),
        "merkle_root": root,
        "leaf_count": len(leaves),
        "leaves_sha256": leaves,
        "dual_ledgers": {
            "local": local,
            "public": public,
            "local_ok": local_ok,
            "public_ok": public_ok,
            "network_used": network,
            "connected": connected,
        },
        "phase_align": {
            "nodes": node_phases,
            "collapse": False,
            "base_phase_rad": base_phase,
            "method": "phi_offset_geodesic",
        },
        "p6": {
            "layer": "P6",
            "mode": "software_quantum_attest",
            "gap_filled": "geodesic_dual_ledger_merkle_lock",
            "hardware_tpm": False,
            "note": "Software attestation bundle; pairs with stack protocol6_quantum_attest when present.",
        },
        "kernel_eggs": "primed",
        "delta9": "ready",
    }


def phase_align_only(
    seal_or_lock: dict[str, Any],
    nodes: list[str],
    allow_collapse: bool = False,
) -> dict[str, Any]:
    """Phase-align additional nodes onto an existing seal/lock without collapse."""
    psi_block = seal_or_lock.get("psi") or {}
    if not allow_collapse:
        pt = float(psi_block.get("prob_truth", 0.5))
        pc = float(psi_block.get("prob_chaos", 0.5))
        if pt < 1e-9 or pc < 1e-9:
            return {"ok": False, "error": "collapse_detected", "message": "Refuse phase-align with collapsed ψ."}

    base = float(psi_block.get("phase_rad", 0.0))
    seal_id = seal_or_lock.get("seal_id") or seal_or_lock.get("lock_id") or "unknown"
    aligned = []
    for i, raw in enumerate(nodes):
        nid = sanitize_node_id(raw)
        offset = (2.0 * math.pi * ((i * PHI) % 1.0))
        phase = (base + offset) % (2.0 * math.pi)
        aligned.append(
            {
                "node_id": nid,
                "phase_rad": phase,
                "phase_deg": math.degrees(phase),
                "aligned": True,
                "collapse": False,
                "leaf_sha256": sha256_hex(f"{nid}:{phase:.12f}:{seal_id}"),
            }
        )
    return {
        "ok": True,
        "kind": "phase_align",
        "signature": SIG,
        "version": VERSION,
        "created_at": utc_now(),
        "seal_id": seal_or_lock.get("seal_id"),
        "lock_id": seal_or_lock.get("lock_id"),
        "nodes": aligned,
        "collapse": False,
        "method": "phi_offset_geodesic",
    }


def attest_bundle(
    truth: str,
    chaos: str,
    node_id: str,
    *,
    network: bool = False,
    nodes: list[str] | None = None,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Full P6 software attestation: sign → lock → phase-align."""
    psi = build_psi(truth, chaos, node_id, extra=extra)
    lock = lock_geodesic(psi, network=network, nodes=nodes or [node_id], allow_collapse=False)
    if not lock.get("ok"):
        return {"ok": False, "psi": psi, "lock": lock}
    return {
        "ok": True,
        "kind": "p6_quantum_attest",
        "signature": SIG,
        "version": VERSION,
        "created_at": utc_now(),
        "psi": psi,
        "lock": lock,
        "attestation": {
            "measurement": {
                "truth_sha256": psi["provenance"]["truth_sha256"],
                "chaos_sha256": psi["provenance"]["chaos_sha256"],
                "psi_norm": psi["psi"]["norm"],
                "phase_rad": psi["psi"]["phase_rad"],
            },
            "merkle_root": lock["merkle_root"],
            "lock_id": lock["lock_id"],
            "seal_id": psi["seal_id"],
            "dual_ledger_connected": lock["dual_ledgers"]["connected"],
            "collapse": False,
            "p6_mode": "software_quantum_attest",
        },
        "badge": {
            "type": "LYGO-P6-GEODESIC-ATTEST",
            "seal_id": psi["seal_id"],
            "merkle_root": lock["merkle_root"],
            "delta9": "ready",
            "kernel_eggs": "primed",
        },
    }


def verify_artifact(obj: dict[str, Any]) -> dict[str, Any]:
    """Recompute provenance / merkle consistency for a seal or lock artifact."""
    checks: dict[str, Any] = {"ok": False, "signature_match": obj.get("signature") == SIG}
    kind = obj.get("kind") or ""

    if kind == "psi_sign" or "provenance" in obj:
        prov = obj.get("provenance") or (obj.get("psi") or {}).get("provenance")
        if not prov and "provenance" in obj:
            prov = obj["provenance"]
        if prov:
            recomputed = sha256_bytes(canonical_json(prov))
            checks["provenance_match"] = recomputed == obj.get("provenance_sha256")
        else:
            checks["provenance_match"] = None

    if kind in ("geodesic_lock", "p6_quantum_attest") or obj.get("merkle_root") or (
        isinstance(obj.get("lock"), dict) and obj["lock"].get("merkle_root")
    ):
        lock = obj if kind == "geodesic_lock" else obj.get("lock") or obj
        leaves = lock.get("leaves_sha256") or []
        if leaves:
            recomputed_root = merkle_root(leaves)
            checks["merkle_match"] = recomputed_root == lock.get("merkle_root")
        else:
            checks["merkle_match"] = None
        psi = lock.get("psi") or (obj.get("psi") or {}).get("psi") or obj.get("psi")
        if isinstance(psi, dict) and "prob_truth" in psi:
            checks["no_collapse"] = psi.get("prob_truth", 0) > 1e-9 and psi.get("prob_chaos", 0) > 1e-9
        else:
            checks["no_collapse"] = True

    if kind == "p6_quantum_attest":
        checks["has_badge"] = bool(obj.get("badge"))
        checks["attestation_present"] = bool(obj.get("attestation"))

    # overall
    required = [checks.get("signature_match")]
    if "provenance_match" in checks and checks["provenance_match"] is not None:
        required.append(checks["provenance_match"])
    if "merkle_match" in checks and checks["merkle_match"] is not None:
        required.append(checks["merkle_match"])
    if "no_collapse" in checks:
        required.append(checks["no_collapse"])
    checks["ok"] = all(bool(x) for x in required)
    checks["kind"] = kind
    checks["signature"] = SIG
    checks["verified_at"] = utc_now()
    return checks


def maybe_write(obj: dict[str, Any], path: Path | None, i_consent: bool) -> dict[str, Any]:
    if path is None:
        return {"written": False}
    if not i_consent:
        return {"written": False, "error": "consent_required", "hint": "pass --i-consent with --write"}
    try:
        target = safe_write_path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(obj, indent=2), encoding="utf-8")
        return {"written": True, "path": str(target), "sha256": sha256_bytes(target.read_bytes())}
    except Exception as e:
        return {"written": False, "error": str(e)}


def load_json_arg(path: str | None, inline: str | None) -> dict[str, Any]:
    if inline:
        return json.loads(inline)
    if path:
        p = Path(path)
        return json.loads(p.read_text(encoding="utf-8"))
    raise ValueError("need --from-file or --json")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def cmd_sign(args: argparse.Namespace) -> int:
    truth = args.truth or ""
    chaos = args.chaos or ""
    if args.truth_file:
        truth = Path(args.truth_file).read_text(encoding="utf-8", errors="replace")
    if args.chaos_file:
        chaos = Path(args.chaos_file).read_text(encoding="utf-8", errors="replace")
    if not truth:
        truth = "LYGO-TRUTH-DEFAULT-ANCHOR"
    if not chaos:
        # deterministic session chaos from node + time bucket (not secret entropy)
        chaos = f"LYGO-CHAOS:{args.node_id}:{utc_now()[:13]}"
    extra = {}
    if args.label:
        extra["label"] = args.label
    out = build_psi(truth, chaos, args.node_id, extra=extra)
    w = maybe_write(out, Path(args.write) if args.write else None, args.i_consent)
    out["write"] = w
    print(json.dumps(out, indent=2 if not args.compact else None))
    return 0 if out.get("ok") else 1


def cmd_lock(args: argparse.Namespace) -> int:
    if args.from_file or args.from_json:
        psi = load_json_arg(args.from_file, args.from_json)
    else:
        truth = args.truth or "LYGO-TRUTH-DEFAULT-ANCHOR"
        chaos = args.chaos or f"LYGO-CHAOS:{args.node_id}:{utc_now()[:13]}"
        if args.truth_file:
            truth = Path(args.truth_file).read_text(encoding="utf-8", errors="replace")
        if args.chaos_file:
            chaos = Path(args.chaos_file).read_text(encoding="utf-8", errors="replace")
        psi = build_psi(truth, chaos, args.node_id)
    nodes = [n.strip() for n in (args.nodes or "").split(",") if n.strip()] or None
    out = lock_geodesic(
        psi,
        network=args.network,
        nodes=nodes,
        allow_collapse=args.allow_collapse,
    )
    w = maybe_write(out, Path(args.write) if args.write else None, args.i_consent)
    out["write"] = w
    print(json.dumps(out, indent=2 if not args.compact else None))
    return 0 if out.get("ok") else 1


def cmd_phase_align(args: argparse.Namespace) -> int:
    obj = load_json_arg(args.from_file, args.from_json)
    nodes = [n.strip() for n in args.nodes.split(",") if n.strip()]
    if not nodes:
        print(json.dumps({"ok": False, "error": "nodes_required"}))
        return 1
    # unwrap attest bundles
    if obj.get("kind") == "p6_quantum_attest":
        base = obj.get("lock") or obj.get("psi") or obj
    else:
        base = obj
    out = phase_align_only(base, nodes, allow_collapse=args.allow_collapse)
    w = maybe_write(out, Path(args.write) if args.write else None, args.i_consent)
    out["write"] = w
    print(json.dumps(out, indent=2 if not args.compact else None))
    return 0 if out.get("ok") else 1


def cmd_attest(args: argparse.Namespace) -> int:
    truth = args.truth or "LYGO-TRUTH-DEFAULT-ANCHOR"
    chaos = args.chaos or f"LYGO-CHAOS:{args.node_id}:{utc_now()[:13]}"
    if args.truth_file:
        truth = Path(args.truth_file).read_text(encoding="utf-8", errors="replace")
    if args.chaos_file:
        chaos = Path(args.chaos_file).read_text(encoding="utf-8", errors="replace")
    nodes = [n.strip() for n in (args.nodes or "").split(",") if n.strip()] or None
    extra = {"label": args.label} if args.label else {}
    out = attest_bundle(
        truth,
        chaos,
        args.node_id,
        network=args.network,
        nodes=nodes,
        extra=extra,
    )
    # default write path under seal dir if --write-default
    write_path = Path(args.write) if args.write else None
    if args.write_default and write_path is None:
        seal_dir = default_seal_dir()
        sid = (out.get("psi") or {}).get("seal_id") or "attest"
        write_path = seal_dir / f"{sid}.json"
    w = maybe_write(out, write_path, args.i_consent or bool(args.write_default and args.i_consent))
    if args.write_default and not args.i_consent:
        w = {"written": False, "error": "consent_required", "hint": "pass --i-consent with --write-default"}
    out["write"] = w
    print(json.dumps(out, indent=2 if not args.compact else None))
    return 0 if out.get("ok") else 1


def cmd_verify(args: argparse.Namespace) -> int:
    obj = load_json_arg(args.from_file, args.from_json)
    out = verify_artifact(obj)
    print(json.dumps(out, indent=2 if not args.compact else None))
    return 0 if out.get("ok") else 1


def cmd_status(args: argparse.Namespace) -> int:
    local = load_local_ledgers()
    public: list[dict[str, Any]] = []
    if args.network:
        public = fetch_public_ledgers()
    seal_dir = default_seal_dir()
    seals = []
    if seal_dir.is_dir():
        for p in sorted(seal_dir.glob("*.json"))[:20]:
            seals.append({"path": str(p), "sha256": sha256_bytes(p.read_bytes()), "bytes": p.stat().st_size})
    out = {
        "ok": True,
        "kind": "status",
        "signature": SIG,
        "version": VERSION,
        "created_at": utc_now(),
        "stack_root": str(stack_root()) if stack_root() else None,
        "seal_dir": str(seal_dir),
        "local_ledgers": local,
        "public_ledgers": public,
        "network_used": args.network,
        "connected": any(x.get("ok") for x in local) or any(x.get("ok") for x in public),
        "recent_seals": seals,
        "p6_gap": "geodesic software attest available (this skill)",
        "delta9": "ready",
        "kernel_eggs": "primed",
    }
    print(json.dumps(out, indent=2 if not args.compact else None))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="seal_cli",
        description="LYGO Geodesic Sealer — |ψ⟩ sign, dual-ledger Merkle lock, phase-align, P6 attest",
    )
    p.add_argument("--compact", action="store_true", help="compact JSON")
    sub = p.add_subparsers(dest="cmd", required=True)

    def add_common(sp: argparse.ArgumentParser) -> None:
        sp.add_argument("--node-id", default="local-node", help="lattice node id")
        sp.add_argument("--truth", default=None, help="truth payload string")
        sp.add_argument("--chaos", default=None, help="chaos payload string")
        sp.add_argument("--truth-file", default=None, help="read truth from file")
        sp.add_argument("--chaos-file", default=None, help="read chaos from file")
        sp.add_argument("--label", default=None, help="optional label in provenance")
        sp.add_argument("--write", default=None, help="opt-in write path for JSON artifact")
        sp.add_argument("--i-consent", action="store_true", help="consent for local write")
        sp.add_argument("--network", action="store_true", help="HTTPS GET public dual ledgers")
        sp.add_argument("--nodes", default="", help="comma-separated node ids for phase-align")
        sp.add_argument("--allow-collapse", action="store_true", help="allow zeroed amplitude (default refuse)")
        sp.add_argument("--from-file", default=None, help="load prior JSON artifact")
        sp.add_argument("--from-json", default=None, help="inline JSON artifact")

    s = sub.add_parser("sign", help="Sign |ψ⟩=(Truth+iChaos)/√2")
    add_common(s)
    s.set_defaults(func=cmd_sign)

    s = sub.add_parser("lock", help="Lock geodesic to dual ledgers + Merkle")
    add_common(s)
    s.set_defaults(func=cmd_lock)

    s = sub.add_parser("phase-align", help="Phase-align nodes without collapse")
    add_common(s)
    s.set_defaults(func=cmd_phase_align)

    s = sub.add_parser("attest", help="Full P6 software quantum-attest bundle")
    add_common(s)
    s.add_argument("--write-default", action="store_true", help="write under seal dir (needs --i-consent)")
    s.set_defaults(func=cmd_attest)

    s = sub.add_parser("verify", help="Verify seal/lock/attest artifact")
    add_common(s)
    s.set_defaults(func=cmd_verify)

    s = sub.add_parser("status", help="Local/public ledger status + recent seals")
    add_common(s)
    s.set_defaults(func=cmd_status)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
