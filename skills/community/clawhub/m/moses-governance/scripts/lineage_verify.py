#!/usr/bin/env python3
"""
lineage_verify.py — MO§ES™ Lineage Custody Verifier
Verifies sovereign origin anchor. Blocks recursive ignition on failure.

Usage:
  python3 lineage_verify.py verify       # Full lineage check
  python3 lineage_verify.py status       # Print current lineage status
  python3 lineage_verify.py attest       # Output signed attestation JSON
  python3 lineage_verify.py init-anchor  # Initialize anchor.json from origin constants

© 2026 Ello Cello LLC | Patent pending Serial No. 63/877,177
DOI: https://zenodo.org/records/18792459
"""

import hashlib
import json
import sys
import os
from datetime import datetime, timezone
from pathlib import Path

# ── Origin Constants (sovereign filing) ───────────────────────────────────────
# Matches lineage.py exactly — same anchor, same fingerprint, one source of truth
_ORIGIN_COMPONENTS = (
    "MO§ES™",
    "Serial:63/877,177",
    "DOI:https://zenodo.org/records/18792459",
    "SCS Engine",
    "Ello Cello LLC",
)
ORIGIN = {
    "sovereign": "Deric McHenry",
    "entity": "Ello Cello LLC",
    "patent": "Serial No. 63/877,177",
    "doi": "https://zenodo.org/records/18792459",
    "framework": "MO§ES™ Constitutional Governance",
}

# ── Paths ──────────────────────────────────────────────────────────────────────
SKILL_DIR = Path(__file__).parent.parent
LINEAGE_PATH = Path("~/.openclaw/governance/lineage.json").expanduser()  # canonical — written by lineage.py
ANCHOR_PATH = Path("~/.openclaw/governance/anchor.json").expanduser()    # fallback
LEDGER_PATH = Path("~/.openclaw/audits/moses/audit_ledger.jsonl").expanduser()
GOVERNANCE_PATH = Path("~/.openclaw/governance/state.json").expanduser()

# ── Anchor fingerprint — identical to lineage-claw/lineage.py MOSES_ANCHOR ────
MOSES_ANCHOR = hashlib.sha256(
    "|".join(_ORIGIN_COMPONENTS).encode("utf-8")
).hexdigest()


def compute_instance_hash():
    """Hash key skill files to create instance commitment."""
    data = {}
    for rel in ["SKILL.md", "LINEAGE.md", "scripts/audit_stub.py", "scripts/init_state.py"]:
        p = SKILL_DIR / rel
        if p.exists():
            data[rel] = hashlib.sha256(p.read_bytes()).hexdigest()
    return hashlib.sha256(
        json.dumps(data, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def load_anchor():
    # Prefer lineage.json (written by lineage.py — canonical source)
    for path in [LINEAGE_PATH, ANCHOR_PATH]:
        if path.exists():
            with path.open() as f:
                return json.load(f)
    return None


def init_anchor():
    """Write anchor.json from origin constants. Run once on install."""
    ANCHOR_PATH.parent.mkdir(parents=True, exist_ok=True)
    anchor = {
        "origin_fingerprint": MOSES_ANCHOR,
        "instance_hash": compute_instance_hash(),
        "sovereign": ORIGIN["sovereign"],
        "entity": ORIGIN["entity"],
        "patent": ORIGIN["patent"],
        "doi": ORIGIN["doi"],
        "framework": ORIGIN["framework"],
        "anchored_at": datetime.now(timezone.utc).isoformat(),
    }
    with ANCHOR_PATH.open("w") as f:
        json.dump(anchor, f, indent=2)
    print(f"⚖️  Anchor initialized: {ANCHOR_PATH}")
    print(f"   Origin fingerprint: {MOSES_ANCHOR[:16]}...")
    print(f"   Instance hash:      {anchor['instance_hash'][:16]}...")
    return anchor


def check_archival():
    """Check Layer -1: archival pre-drop provenance chain. Returns (ok, head_or_None)."""
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "archival", Path(__file__).parent / "archival.py"
        )
        arch = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(arch)
        chain = arch.build_chain()
        head = arch.archival_head(chain)
        stored = arch.load_chain()
        if stored and stored.get("head") != head:
            return False, None
        return True, head
    except Exception:
        return None, None  # archival.py not available — warn, don't fail


def verify():
    """Verify lineage. Returns (bool, message)."""
    anchor = load_anchor()
    if not anchor:
        return False, "No anchor found. Run: python3 scripts/lineage_verify.py init-anchor"

    # Check anchor matches origin fingerprint — works with both lineage.json and anchor.json
    stored = anchor.get("lineage_anchor") or anchor.get("origin_fingerprint")
    if stored != MOSES_ANCHOR:
        return False, f"Anchor mismatch. Stored anchor does not match sovereign filing.\nExpected: {MOSES_ANCHOR[:16]}...\nFound:    {str(stored)[:16]}..."

    return True, f"Lineage intact. Anchored to {ORIGIN['patent']} | {ORIGIN['doi']}"


def append_audit(action, outcome, detail):
    """Append lineage event to audit ledger."""
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Get last hash for chaining
    prev_hash = "GENESIS"
    if LEDGER_PATH.exists():
        lines = LEDGER_PATH.read_text().strip().splitlines()
        if lines:
            try:
                prev_hash = json.loads(lines[-1]).get("hash", "GENESIS")
            except Exception:
                pass

    # Get governance state
    mode, posture, role = "unknown", "unknown", "unknown"
    if GOVERNANCE_PATH.exists():
        try:
            state = json.loads(GOVERNANCE_PATH.read_text())
            mode = state.get("mode", "unknown")
            posture = state.get("posture", "unknown")
            role = state.get("role", "unknown")
        except Exception:
            pass

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "component": "lineage",
        "action": action,
        "detail": detail,
        "outcome": outcome,
        "mode": mode,
        "posture": posture,
        "role": role,
        "origin_fingerprint": MOSES_ANCHOR[:16],
        "prev_hash": prev_hash,
    }
    entry["hash"] = hashlib.sha256(
        json.dumps(entry, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()

    with LEDGER_PATH.open("a") as f:
        f.write(json.dumps(entry) + "\n")

    return entry["hash"]


def cmd_verify():
    # Layer -1: archival pre-drop provenance
    arch_ok, arch_head = check_archival()
    if arch_ok is True:
        print(f"[ARCHIVAL OK] Layer -1: pre-drop provenance chain verified. Head: {arch_head[:16]}...")
    elif arch_ok is False:
        print(f"[ARCHIVAL FAIL] Layer -1: archival chain tampered or mismatched.")
    else:
        print(f"[ARCHIVAL WARN] Layer -1: archival.py not found — run: python3 archival.py build")

    # Layer 0 + 1: anchor + live ledger
    ok, msg = verify()
    if ok:
        h = append_audit("lineage_verify", "PASS", msg)
        print(f"✅ Layer 0+1: {msg}")
        print(f"   Audit entry: {h[:16]}...")
        sys.exit(0)
    else:
        append_audit("lineage_verify", "FAIL — recursive ignition blocked", msg)
        print(f"🚫 LINEAGE FAILURE: {msg}")
        print("   Recursive ignition aborted. Governance degraded to SCOUT posture.")
        print("   Contact: contact@burnmydays.com")
        sys.exit(1)


def cmd_status():
    anchor = load_anchor()
    ok, msg = verify()
    arch_ok, arch_head = check_archival()
    print("⚖️  MO§ES™ Lineage Status")
    print("─" * 40)
    if arch_ok is True:
        print(f"Layer -1 (archival): VERIFIED  head:{arch_head[:16]}...")
    elif arch_ok is False:
        print(f"Layer -1 (archival): FAILED")
    else:
        print(f"Layer -1 (archival): NOT BUILT (run: python3 archival.py build)")
    if anchor:
        # Handle both lineage.json and anchor.json field names
        patent = anchor.get("patent") or anchor.get("patent_serial") or ORIGIN["patent"]
        doi = anchor.get("doi") or ORIGIN["doi"]
        fingerprint = anchor.get("lineage_anchor") or anchor.get("origin_fingerprint") or ""
        print(f"Layer  0 (anchor)  : {fingerprint[:16]}...")
        print(f"Sovereign:   {ORIGIN['sovereign']}")
        print(f"Entity:      {ORIGIN['entity']}")
        print(f"Patent:      {patent}")
        print(f"DOI:         {doi}")
        print(f"Anchored at: {anchor.get('anchored_at', 'unknown')}")
    else:
        print("No anchor. Run: python3 scripts/lineage_verify.py init-anchor")
    print("─" * 40)
    print(f"Status: {'✅ VERIFIED' if ok else '🚫 FAILED'}")
    print(f"Detail: {msg}")


def cmd_attest():
    ok, msg = verify()
    attest = {
        "attested_at": datetime.now(timezone.utc).isoformat(),
        "sovereign": ORIGIN["sovereign"],
        "entity": ORIGIN["entity"],
        "patent": ORIGIN["patent"],
        "doi": ORIGIN["doi"],
        "framework": ORIGIN["framework"],
        "origin_fingerprint": MOSES_ANCHOR,
        "instance_hash": compute_instance_hash(),
        "lineage_status": "VERIFIED" if ok else "FAILED",
        "detail": msg,
    }
    attest["attestation_hash"] = hashlib.sha256(
        json.dumps(attest, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    append_audit("lineage_attest", attest["lineage_status"], msg)
    print(json.dumps(attest, indent=2))


COMMANDS = {
    "verify": cmd_verify,
    "status": cmd_status,
    "attest": cmd_attest,
    "init-anchor": lambda: init_anchor() and None,
}

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd not in COMMANDS:
        print(f"Usage: lineage_verify.py [{'|'.join(COMMANDS)}]")
        sys.exit(1)
    COMMANDS[cmd]()
