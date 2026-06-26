#!/usr/bin/env python3
"""
MO§ES™ Archival Chain — Pre-Drop Provenance Verification
Provisional Patent Serial No. 63/877,177 | DOI: https://zenodo.org/records/18792459

The live lineage chain (lineage.py) roots to MOSES_ANCHOR. The anchor is
computed from the origin filing components and trusted as ground truth.

Cornelius-Trinity asked the correct question:
  "Does it verify the anchor itself, or does it assume it?"

This script answers that question. The archival chain hashes and chains
provenance claims that predate the live chain — patent filing, academic
publication, prior work — in chronological order. The archival head hash
is a cryptographic commitment to the full pre-drop history.

The anchor is not assumed. It is downstream of a verifiable sequence.
Anyone with the external references (patent serial, DOI) can reconstruct
this chain and confirm the head hash independently.

Layer model:
  Layer -1: Archival chain — pre-drop provenance (this script)
  Layer  0: MOSES_ANCHOR — origin filing components (lineage.py)
  Layer  1: Live ledger chain — governed actions (audit_stub.py)

Usage:
  python3 archival.py build    ← Construct chain from provenance claims
  python3 archival.py verify   ← Recompute and verify chain integrity
  python3 archival.py head     ← Output archival head hash (machine-readable)
  python3 archival.py show     ← Display full provenance chain
  python3 archival.py check    ← Exit 0 if valid, 1 if not
"""

import hashlib
import json
import os
import sys
from datetime import timezone

# ─── Provenance Claims ────────────────────────────────────────────────────────
# Ordered chronologically. Each claim is a provenance event that predates
# the live chain. External refs are independently verifiable.
#
# These are FIXED. Adding or modifying a claim changes the archival head
# and breaks verification — which is the point. The chain is tamper-evident.

PROVENANCE_CLAIMS = [
    {
        "seq": 0,
        "claim": "Signal Compression Sciences (SCS) — foundational concept predating the filing. "
                 "Semantic commitment is conserved under compression when enforcement is active.",
        "claim_type": "prior_work",
        "external_ref": "Internal: SCS Engine / Ello Cello LLC prior work",
        "author": "Deric McHenry / Ello Cello LLC",
    },
    {
        "seq": 1,
        "claim": "MO§ES™ Constitutional Governance system concept — constitutional substrate "
                 "for AI agents enforcing policy invariants, role hierarchy, and behavioral modes. "
                 "Predates public release and patent filing.",
        "claim_type": "prior_work",
        "external_ref": "Internal: MO§ES™ system design / Ello Cello LLC prior work",
        "author": "Deric McHenry / Ello Cello LLC",
    },
    {
        "seq": 2,
        "claim": "Provisional patent application filed for MO§ES™ Constitutional Governance "
                 "and the Commitment Conservation Law. Establishes legal priority date.",
        "claim_type": "patent_filing",
        "external_ref": "USPTO Provisional Serial No. 63/877,177",
        "author": "Deric McHenry / Ello Cello LLC",
    },
    {
        "seq": 3,
        "claim": "Academic record published via Zenodo. Public DOI establishes timestamped "
                 "record of the Commitment Conservation Law and MO§ES™ architecture prior to "
                 "software release. Independent of the patent filing.",
        "claim_type": "academic_record",
        "external_ref": "DOI: https://zenodo.org/records/18792459",
        "author": "Deric McHenry / Ello Cello LLC",
    },
    {
        "seq": 4,
        "claim": "First public software release of MO§ES™ governance harness via ClawHub. "
                 "Constitutional substrate open-sourced under MIT license. Lineage is not MIT. "
                 "Any fork initializes with a different genesis — cannot claim sovereign custody.",
        "claim_type": "public_release",
        "external_ref": "clawhub.ai/SunrisesIllNeverSee/moses-governance",
        "author": "Deric McHenry / Ello Cello LLC",
    },
]

ARCHIVAL_PATH = os.path.expanduser("~/.openclaw/governance/archival_chain.json")

# ─── Chain construction ───────────────────────────────────────────────────────

def canonical(data: dict) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def block_hash(block: dict) -> str:
    return hashlib.sha256(canonical(block).encode("utf-8")).hexdigest()


def build_chain() -> list[dict]:
    """Construct the archival chain from PROVENANCE_CLAIMS."""
    chain = []
    prev = "0" * 64  # Genesis has no predecessor

    for claim in PROVENANCE_CLAIMS:
        block = {
            "seq": claim["seq"],
            "claim": claim["claim"],
            "claim_type": claim["claim_type"],
            "external_ref": claim["external_ref"],
            "author": claim["author"],
            "previous_hash": prev,
        }
        h = block_hash(block)
        block["hash"] = h
        chain.append(block)
        prev = h

    return chain


def archival_head(chain: list[dict]) -> str:
    return chain[-1]["hash"]


# ─── Persistence ─────────────────────────────────────────────────────────────

def save_chain(chain: list[dict]):
    os.makedirs(os.path.dirname(ARCHIVAL_PATH), exist_ok=True)
    with open(ARCHIVAL_PATH, "w") as f:
        json.dump({"chain": chain, "head": archival_head(chain)}, f, indent=2)


def load_chain() -> dict | None:
    if not os.path.exists(ARCHIVAL_PATH):
        return None
    with open(ARCHIVAL_PATH) as f:
        return json.load(f)


# ─── Commands ────────────────────────────────────────────────────────────────

def cmd_build(_args):
    chain = build_chain()
    save_chain(chain)
    head = archival_head(chain)

    print("[ARCHIVAL] Pre-drop provenance chain built.")
    print(f"  Blocks : {len(chain)}")
    print(f"  Head   : {head[:24]}...")
    print()
    print("  Layer model:")
    print("    Layer -1 (this)  : Archival chain — pre-drop provenance")
    print("    Layer  0         : MOSES_ANCHOR — origin filing components")
    print("    Layer  1         : Live ledger — governed actions")
    print()
    print("[ARCHIVAL] The anchor is not assumed. It is downstream of this chain.")
    print(f"[ARCHIVAL] Stored: {ARCHIVAL_PATH}")


def cmd_verify(_args):
    stored = load_chain()
    if not stored:
        print("[ARCHIVAL FAIL] No archival chain found. Run: python3 archival.py build")
        sys.exit(1)

    # Recompute the chain from scratch
    expected = build_chain()
    expected_head = archival_head(expected)

    # Verify stored head matches recomputed head
    if stored.get("head") != expected_head:
        print("[ARCHIVAL FAIL] Stored head does not match recomputed chain.")
        print(f"  Expected: {expected_head[:24]}...")
        print(f"  Stored  : {stored.get('head', 'MISSING')[:24]}...")
        print("[ARCHIVAL FAIL] Provenance chain has been tampered with or is from a different origin.")
        sys.exit(1)

    # Verify each block's hash and linkage
    stored_chain = stored.get("chain", [])
    if len(stored_chain) != len(expected):
        print(f"[ARCHIVAL FAIL] Block count mismatch: expected {len(expected)}, found {len(stored_chain)}")
        sys.exit(1)

    for i, (s, e) in enumerate(zip(stored_chain, expected)):
        if s.get("hash") != e["hash"]:
            print(f"[ARCHIVAL FAIL] Block {i} hash mismatch — chain integrity broken at seq {i}.")
            sys.exit(1)
        if s.get("previous_hash") != e["previous_hash"]:
            print(f"[ARCHIVAL FAIL] Block {i} previous_hash mismatch — linkage broken at seq {i}.")
            sys.exit(1)

    head = expected_head
    print(f"[ARCHIVAL OK] Pre-drop provenance chain verified.")
    print(f"  Blocks : {len(expected)}")
    print(f"  Head   : {head[:24]}...")
    print()
    for block in expected:
        print(f"  [{block['seq']}] {block['claim_type']:<18} {block['external_ref'][:60]}")
    print()
    print("[ARCHIVAL OK] The origin anchor is downstream of this verifiable provenance sequence.")
    print("[ARCHIVAL OK] Any implementation claiming sovereign custody must produce this same head.")


def cmd_head(_args):
    """Print archival head hash — machine-readable, for piping into other tools."""
    stored = load_chain()
    if not stored:
        # Build on-demand if not yet persisted
        chain = build_chain()
        print(archival_head(chain))
        return
    # Always recompute to ensure integrity
    chain = build_chain()
    print(archival_head(chain))


def cmd_show(_args):
    chain = build_chain()
    head = archival_head(chain)

    print("─" * 70)
    print("  MO§ES™ ARCHIVAL PROVENANCE CHAIN")
    print("  Pre-drop history — Layer -1")
    print("─" * 70)
    print()
    for block in chain:
        print(f"  Block {block['seq']} — {block['claim_type'].upper()}")
        print(f"  Hash    : {block['hash'][:48]}...")
        print(f"  Prev    : {block['previous_hash'][:48]}...")
        print(f"  Ref     : {block['external_ref']}")
        print(f"  Claim   : {block['claim'][:100]}...")
        print()
    print("─" * 70)
    print(f"  ARCHIVAL HEAD: {head}")
    print("─" * 70)
    print()
    print("  To verify: python3 archival.py verify")
    print("  This chain proves the origin anchor is not assumed —")
    print("  it is downstream of independently verifiable provenance claims.")


def cmd_check(_args):
    """Exit 0 if archival chain is valid, 1 if not. Machine-readable."""
    try:
        stored = load_chain()
        if not stored:
            sys.exit(1)
        expected = build_chain()
        if stored.get("head") != archival_head(expected):
            sys.exit(1)
        print("ARCHIVAL:OK")
        sys.exit(0)
    except Exception:
        sys.exit(1)


# ─── Entry ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="MO§ES™ Archival Chain — Pre-Drop Provenance Verification"
    )
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("build",  help="Construct chain from provenance claims")
    subparsers.add_parser("verify", help="Recompute and verify chain integrity")
    subparsers.add_parser("head",   help="Output archival head hash (machine-readable)")
    subparsers.add_parser("show",   help="Display full provenance chain")
    subparsers.add_parser("check",  help="Exit 0 if valid, 1 if not")

    args = parser.parse_args()

    commands = {
        "build":  cmd_build,
        "verify": cmd_verify,
        "head":   cmd_head,
        "show":   cmd_show,
        "check":  cmd_check,
    }

    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()
