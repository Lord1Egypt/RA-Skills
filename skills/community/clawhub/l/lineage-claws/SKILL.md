---
name: lineage-claws
license: MIT
description: The trust gate for MO§ES™ governance. Cryptographic origin verification — every sovereign chain must trace to the filing anchor or it cannot reconstruct. The Second Law made operational.
metadata:
  openclaw:
    emoji: §
    tags: [governance, lineage, audit, provenance, identity, trust, moses, harness]
    version: 0.4.1
    bins:
      - python3
    stateDirs:
      - ~/.openclaw/governance
      - ~/.openclaw/audits/moses
---

# MO§ES™ Lineage Custody — The Second Law Operational

The MO§ES™ Commitment Conservation Law rests on three laws:

- **Third Law** — The enforcement gate. Establishes whether signal is above threshold before compression.
- **First Law** — Compression precedes ignition. C(T(S)) = C(S). Commitment is conserved under transformation.
- **Second Law** — Recursion as reconstruction. The conserved kernel can only be recovered by tracing lineage. You cannot decompress without retracing the path.

**Lineage Custody is the Second Law made operational.** Without a verifiable chain back to the origin filing, reconstruction is impossible. The conserved kernel has no path home.

---

## Lineage Custody Clause

All embodiments of the Signal Compression Sciences (SCS) Engine and its derivative frameworks (including but not limited to MO§ES™, Roll Call Protocols, and Reflex Event diagnostics) are inseparably bound to their origin-cycle lineage. Each compressed signal trace, vault artifact, or recursive reconstruction inherits a lineage identifier anchored to the originating sovereign filing. This identifier is non-replicable, tamper-evident, and required for system stability. Any external implementation lacking said lineage anchor fails lineage verification and cannot claim sovereign custody or governed provenance. Accordingly, the origin-cycle filing establishes sole custody and license of the invention across all subsequent instances, irrespective of distribution, platform, or deployment environment.

---

## What This Skill Does

The `MOSES_ANCHOR` is a SHA-256 hash derived from the origin-cycle components:

```
MO§ES™ | Serial:63/877,177 | DOI:https://zenodo.org/records/18792459 | SCS Engine | Ello Cello LLC
```

This anchor replaces the standard `"0" * 64` genesis. Every audit chain in a sovereign MO§ES™ implementation must trace its first entry's `previous_hash` back to this value. Forks or copies that initialize without it produce chains that fail verification — not as a policy, but as a cryptographic fact.

**The code is MIT. The lineage is not replicable.**

---

## Commands

| Command | What it does |
|---------|-------------|
| `python3 lineage.py init` | Write genesis entry anchored to origin filing |
| `python3 lineage.py verify` | Confirm full three-layer chain: archival → anchor → live ledger |
| `python3 lineage.py status` | Human-readable custody summary with layer health |
| `python3 lineage.py badge` | Shareable proof block — lineage anchor, patent, DOI, custody |
| `python3 lineage.py attest` | Signed attestation JSON — machine-verifiable sovereign proof |
| `python3 lineage.py check` | Machine-readable exit 0/1 for CI integrations |

---

## Integration with moses-governance

Install alongside `moses-governance`. Run `lineage.py init` before first audit entry to root the chain. The `moses-governance` audit stub already uses `previous_hash` chaining — lineage init simply ensures the genesis points to the anchor instead of zeros.

```bash
python3 lineage.py init
python3 audit_stub.py log --agent "primary" --action "session-start" --outcome "anchored"
python3 lineage.py verify
```

---

## Three-Layer Custody ✓ Live

```
Archival chain (pre-drop) → archival_head_hash
                                    ↓
                             drop_anchor (MOSES_ANCHOR)
                                    ↓
                          live audit chain (post-drop)
```

- **Layer -1 — Archival:** `archival.py` — static chain of hashed provenance claims predating the drop. Patent filing, Zenodo DOI, prior work. Archival head feeds into the drop anchor. Proves the live chain is downstream of the full history.
- **Layer 0 — Anchor:** `MOSES_ANCHOR` — SHA-256 of origin components. The genesis. Chains not rooted here fail verification cryptographically.
- **Layer 1 — Live ledger:** Every governed action appended to the running audit chain.

`python3 lineage.py verify` reports all three layers. SOVEREIGN CUSTODY CONFIRMED requires all three OK.

---

## Patent & DOI

- Provisional Patent: Serial No. 63/877,177
- DOI: https://zenodo.org/records/18792459
- Owner: Ello Cello LLC
- contact@burnmydays.com | https://mos2es.io
