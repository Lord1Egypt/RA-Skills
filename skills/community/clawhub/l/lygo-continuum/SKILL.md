---
name: lygo-continuum
description: "LYGO Continuum — falsifiable work capsules for AI agents and humans. Seal 'done' as checkable claims (file SHA-256, contains, JSON paths, globs under --base), re-verify, drift, handoff. CLI: pure local stdlib — no network, no subprocess. Paths/globs confined under --base; --out under base or state/ with --i-consent. Optional separate browser portal is NOT opened by the skill. Commands: seal, verify, drift, handoff, card, demo. Install clawhub:@deepseekoracle/lygo-continuum."
version: 1.0.1
license: MIT-0
metadata:
  openclaw:
    emoji: "∞"
    homepage: "https://github.com/DeepSeekOracle/lygo-protocol-stack/tree/main/docs/skills/lygo-continuum"
    requires:
      anyBins: [python, python3]
  lygo: true
  continuum: true
  receipts: true
  handoff: true
  security: true
  signature: "Delta9Phi963-CONTINUUM-v1.0.1"
  publisher: deepseekoracle
  clawhub: "https://clawhub.ai/deepseekoracle/skills/lygo-continuum"
  portal_optional: "https://chatagent.ca/lygo-continuum.html"
  permissions:
    network: false
    shell: false
    subprocess: false
    filesystem:
      read: "claim paths relative to --base only"
      write: "--out under --base; skill state/ with --i-consent; --i-allow-any-out override"
    publish: false
---

# LYGO Continuum v1.0.1

**The work still holds.**

Agents say “done.” Sessions die. Files change. The next human or AI cannot tell what still holds.

**Continuum** seals work as a **falsifiable capsule**: structured claims any script can prove true or false against real files — plus decisions, next actions, and a Merkle-style root hash. Re-verify later. Drift becomes visible. Handoffs become portable.

**Signature:** `Delta9Phi963-CONTINUUM-v1.0.1`  
**ClawHub:** `@deepseekoracle/lygo-continuum`  
**CLI:** pure local · no network · no subprocess

---

## Why this is different

| Approach | Gap | Continuum |
|----------|-----|-----------|
| “Done” in chat | Not checkable | Claims re-run on disk |
| Git commit | Code only; no task semantics | Claims + decisions + next |
| Cloud agent receipts | HMAC secrets / vendor lock | Local stdlib + browser SHA-256 |
| One-shot proofs | No cross-session story | **Drift** + **handoff pack** |

Never made before as a **human+agent lattice product**: seal → verify → drift → handoff + client-side witness portal under LYGO dual-channel.

---

## Install

```bash
npx clawhub@latest install deepseekoracle/lygo-continuum
```

FULL engineer RAW: https://chatagent.ca/lygoskillhub.html#full-lygo

---

## Commands

```bash
cd path/to/lygo-continuum
python scripts/self_check.py
python scripts/continuum.py demo

# Seal claims (auto-fills file_sha256 when expect omitted)
python scripts/continuum.py seal --claims claims.json --task "Ship login fix" --agent grok --base .

# Verify / drift
python scripts/continuum.py verify --capsule capsule.json --base .
python scripts/continuum.py drift --capsule capsule.json --base .

# Handoff pack for the next agent (markdown + embedded JSON)
python scripts/continuum.py handoff --capsule capsule.json --verify --base .

# Witness card HTML
python scripts/continuum.py card --capsule capsule.json --verify
```

| Command | Network | Subprocess | Writes |
|---------|---------|------------|--------|
| seal / verify / drift / handoff / card / demo / kinds | none | none | `--out` under `--base`, or `state/` + `--i-consent` |

**Exit codes:** `0` holds · `10` claims fail / drift · `11` root integrity fail · `2` bad input

---

## Claim kinds

`file_exists` · `file_missing` · `file_sha256` · `file_contains` · `file_not_contains` · `line_count_gte` · `line_count_eq` · `bytes_gte` · `bytes_eq` · `glob_count_gte` · `json_path_eq` · `text_sha256` · `regex_match` · `regex_not_match`

Example `claims.json`:

```json
[
  {"id": "c1", "kind": "file_exists", "path": "src/app.py"},
  {"id": "c2", "kind": "file_sha256", "path": "src/app.py"},
  {"id": "c3", "kind": "file_contains", "path": "src/app.py", "needle": "def login"},
  {"id": "c4", "kind": "json_path_eq", "path": "out/report.json", "jpath": "status", "expect": "ok"},
  {"id": "c5", "kind": "glob_count_gte", "pattern": "tests/test_*.py", "n": 3}
]
```

---

## Agent recipe

```text
1. Finish the task on disk
2. Write claims.json for what MUST still be true
3. continuum.py seal --claims claims.json --task "..." --base .
4. If exit 10 → fix files or claims; do not say "done"
5. continuum.py handoff --capsule capsule.json --verify → paste to next agent/human
6. Later: continuum.py drift --capsule capsule.json  (or portal + drop files)
```

---

## Optional portal (humans only — not part of the CLI)

https://chatagent.ca/lygo-continuum.html is a **separate** web UI.  
This skill **never** opens it or phones home. Use only if you trust that site with the files you drop.

---

## What it does *not* do

- No network, shell, or subprocess **in the CLI**  
- No absolute / `..` claim paths or escaping globs  
- No arbitrary `--out` without `--i-allow-any-out`  
- No cloud signing keys (integrity = root hash of capsule body)  
- No auto-publish / git push  
- Does not replace tests — it seals **what landed** so agents cannot bluff  

---

## Pair with

| Skill | Role |
|-------|------|
| `lygo-mint-walkthrough` | Hash+ledger for prompt packs |
| `lygo-context-guard` | Pack handoff text into budget |
| `lygo-skill-gate` | Scan skills before install |
| `lygo-geodesic-sealer` | Deeper lattice attest |

---

## Security

See `references/SECURITY.md`.  
**Δ9Φ963 — claims over vibes · drift over denial · human remains the publisher.**
