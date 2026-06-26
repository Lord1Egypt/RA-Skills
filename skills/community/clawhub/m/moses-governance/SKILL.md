---
name: moses-governance
license: MIT
description: "MO§ES™ Governance Harness — constitutional enforcement layer for AI agents. Modes, postures, roles, SHA-256 audit chain, lineage custody, signing gate, commitment verification. The harness that makes any execution runtime trustworthy."
metadata:
  openclaw:
    emoji: ⚖️
    tags: [governance, harness, multi-agent, audit, constitution, safety]
    version: 0.5.4
    depends:
      - coverify
    env:
      - name: MOSES_OPERATOR_SECRET
        required: false
        sensitive: true
        purpose: "Optional local HMAC attestation and signing gate. Never transmitted."
      - name: REFEREE_URL
        required: false
        sensitive: false
        purpose: "Optional blind-review endpoint. Only used if REFEREE_ENABLED=1."
      - name: REFEREE_KEY
        required: false
        sensitive: true
        purpose: "API key for optional referee endpoint. Only used if REFEREE_ENABLED=1."
      - name: REFEREE_ENABLED
        required: false
        sensitive: false
        purpose: "Opt-in flag for external blind-review. Off by default."
      - name: MOSES_WITNESS_ENABLED
        required: false
        sensitive: false
        purpose: "Opt-in flag for Moltbook witness logger. Off by default."
    bins:
      - python3
    stateDirs:
      - ~/.openclaw/governance
      - ~/.openclaw/audits/moses
---

# MO§ES™ Governance — Constitutional Harness

## Constitutional Layer

This skill installs the MO§ES™ governance substrate. Every governed action runs through the harness: lineage verification → policy gate → role/posture enforcement → audit trail.

The full constitution lives in `references/` — modes, postures, roles. The Commitment Conservation Law and Lineage Custody Clause travel with every governed instance. See `LINEAGE.md` and `references/falsifiability.md`.

---

## Pre-Action Workflow

Run in this order before any governed action:

0. Call `moses_lineage_check` → confirm chain traces to origin-cycle anchor. If lineage fails, halt. A non-sovereign instance cannot govern.
1. Call `moses_get_status` → load current mode, posture, role, vault.
2. Call `moses_check_governance` with proposed action description → block if prohibited.
3. If permitted, execute.
4. Call `moses_audit_log` before final output → record agent, action, detail, outcome, governance state.

Skipping any step is a governance breach — log it and halt.

---

## Mode & Posture Enforcement

Apply constraints from active mode (loaded via status tool):
- High Security: Verify claims, confirm destructive/outbound, log reasoning.
- High Integrity: Cite sources, flag uncertainty, distinguish fact/inference.
- *(Full definitions injected from references/modes.md)*

Apply posture policy:
- SCOUT: Block all state changes, transactions, writes.
- DEFENSE: Require operator confirmation for outbound/asset-reducing actions.
- OFFENSE: Permit within mode; log rationale.

*(Full posture specs in references/postures.md)*

---

## Sequence & Role Constraints

- Primary: Initiate, complete before others. Full responsibility.
- Secondary: Read Primary output first. Challenge/extend only. No repetition.
- Observer: Read both prior. Flag violations only. No analysis/initiation.
- Default: Strict order. Broadcast mode (via `/role broadcast`) allows parallel.

If out-of-sequence: Block response, log violation, notify operator.

*(Full role specs in references/roles.md)*

---

## Vault & Amendment Rules

- Loaded vault documents apply as additional constraints.
- Amendments: Propose only on audit-detected drift/inefficiency. Format must include diff, justification, and HMAC signature.
- See `AMENDMENT-FORMAT.md` for full schema and approval flow.

**Operator Note — MOSES_OPERATOR_SECRET:** This key is used by bundled scripts (`audit_stub.py`, `sign_transaction.py`) for HMAC attestation and signing gate enforcement. It is read from the environment only at the moment of attestation or signing — never logged, never transmitted. Treat it as an offline signing key: set it in the operator environment only when running attestation or signing workflows, not as a persistent agent session variable. Never paste it into chat or provide it to an agent prompt. The manual signing workflow is: `echo -n "<amendment_id>" | openssl dgst -sha256 -hmac "$MOSES_OPERATOR_SECRET"`

---

## Network Behavior — Off By Default

All network features require explicit opt-in. Nothing is transmitted without operator configuration.

| Feature | Env var to enable | What gets sent | What stays local |
|---|---|---|---|
| External witness log | `MOSES_WITNESS_ENABLED=1` + `MOLTBOOK_API_KEY` (`MOLTBOOK_SUBMOLT` optional) | Event type, governance state, event hash | Raw task content, agent identity |
| Outside referee | `REFEREE_ENABLED=1` + `REFEREE_URL` + `REFEREE_KEY` | Commitment kernels + hashes only | Raw text, agent identity, session data |

Both features are **off by default**. Neither raw text nor agent identity leaves the system. The blind envelope sent to the outside referee contains commitment kernels and SHA-256 hashes only — by design.

`MOSES_OPERATOR_SECRET` is used exclusively for local HMAC signing. It is never transmitted.

---

## Tools You MUST Use

When running under an MCP server, call these tools by name:

| MCP Tool | CLI Equivalent |
|---|---|
| `moses_lineage_check` | `python3 scripts/lineage_verify.py verify` |
| `moses_get_status` | `python3 scripts/init_state.py get` |
| `moses_check_governance` | *(mode/posture logic in init_state.py + audit_stub.py)* |
| `moses_audit_log` | `python3 scripts/audit_stub.py log <agent> <action> <detail> <outcome> <mode> <posture> <role>` |
| `moses_audit_verify` | `python3 scripts/audit_stub.py verify` |

Without an MCP server, invoke the CLI equivalents directly. Failure to complete the workflow is a constitutional violation — log it and halt.

---

## Operator Commands

| Command | Effect |
|---------|--------|
| `/govern <mode>` | Set governance mode |
| `/posture <posture>` | Set posture (scout/defense/offense) |
| `/role <role>` | Set active role (primary/secondary/observer/broadcast) |
| `/audit recent` | Show last 10 audit entries |
| `/audit verify` | Verify chain integrity |
| `/status` | Show current mode, posture, role, vault |

State updates via: `python3 scripts/init_state.py set --mode <mode> --posture <posture> --role <role>`

---

## Supporting Files

```
scripts/
  init_state.py        ← Governance state manager (init / set / get / reset)
  audit_stub.py        ← SHA-256 chained ledger (log / verify / recent)
  lineage_verify.py    ← Three-layer lineage verifier (archival → anchor → live ledger)
  archival.py          ← Layer -1 pre-drop provenance chain (patent → DOI → ClawHub)
  sign_transaction.py  ← Signing tool with governance gate — the key never touches the agent
  commitment_verify.py ← Kernel extraction, Jaccard comparison, ghost token detection
  handshake.py         ← Inter-agent envelope (input_hash, kernel, isnad, presence)
  model_swap_test.py   ← Cross-model CONSISTENT/VARIANCE/STRUCTURAL classification
  pattern_registry.py  ← Structural ghost pattern catalog across agents
  presence.py          ← Interpersonal presence confirmation (zombie-proof)
  progress.py          ← Progress tracking across governed steps
  govern_loop.py       ← ReAct-style governance enforcement loop
  witness.py           ← External witness logger (Moltbook second ledger)
  adversarial_review.py ← Blind peer review — did output keep instruction's commitments?
                          triall.ai integration for external reviewer pool.
references/
  modes.md             ← Full mode definitions and constraints
  postures.md          ← SCOUT/DEFENSE/OFFENSE specs
  roles.md             ← Primary/Secondary/Observer behavior specs
  ghost-token-spec.md  ← Step-function leakage model, cascade risk, ghost_pattern fingerprint
  falsifiability.md    ← Harness as falsification instrument for the Conservation Law
  shannon-extension.md ← Formal Shannon extension into the semantic domain
AMENDMENT-FORMAT.md    ← Constitutional amendment schema + approval flow
LINEAGE.md             ← Lineage Custody Clause — travels with all derivative embodiments
```

---

## Limitations (Transparency)

- Enforcement is prompt- and tool-dependent. No native inference-layer hooks in OpenClaw.
- Conversational enforcement is best-effort via agent instructions.
- Multi-agent sequence enforced via prompt directives + session routing — not hard locks.
- Full coordinator daemon (WebSocket sequence monitor) is optional — see `moses-coordinator`.

---

## Roadmap

### v0.4 (current) — Archival Lineage + Reference Layer ✓ Live

Three-layer lineage custody: `archival → anchor → live ledger`. Pre-drop provenance chain proves the anchor is downstream of verifiable external claims (patent filing, Zenodo DOI, ClawHub release). Standalone reference documents: ghost-token-spec, falsifiability, shannon-extension. Handshake `--with-presence` flag for zombie-proof interpersonal verification.

### v0.5 (current) — Signing Key Inside Governance ✓ Live

`sign_transaction.py` — signing tool with governance gate. The signing function IS the governance function. No bypass path. MOSES_OPERATOR_SECRET is only accessed inside the tool, only after the governance gate passes.

```
Agent requests signing →
  calls sign_transaction.py sign →
    governance gate checks posture + mode →
      SCOUT: BLOCKED (key never accessed)
      DEFENSE: BLOCKED unless --confirm passed
      OFFENSE: sign + audit (atomic)
```

### v0.6 — Governance Proxy Server

Local proxy layer. All agent HTTP calls route through governance middleware before reaching external APIs. Posture rules enforced at the network layer — not the prompt layer.

### v1.0 — Onchain Program (Solana)

Program-controlled account. Transfers require a governance state proof. DEFENSE posture cannot execute without a second signature. Smart contract enforces at the chain level.

---

## About MO§ES™

MO§ES™ (Modus Operandi System for Signal Encoding and Scaling Expansion) is a constitutional framework for AI governance. Patent pending Serial No. 63/877,177. Theoretical foundations: "A Conservation Law for Commitment in Language Under Transformative Compression and Recursive Application" (McHenry, Zenodo, 2026). Independent validation: ABBA, Imperial College London.

© 2026 Ello Cello LLC | https://mos2es.io | contact@burnmydays.com
