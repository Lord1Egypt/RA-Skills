<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-GCE
generatedVersion: "{version}"
source: "DWG baseline (.governance/baseline-manifest.yaml) + workspace-manifest.yaml"
generatedOn: "{generation-date}"
ownership: generated
---
# Drift Detection Agent — Template

## Purpose

A custom agent specification that measures the current workspace reality against the DWG **baseline** (the governed surface), detects and classifies divergence, tags it by domain, logs it to the Drift Register, and verifies dispositions after re-baseline. Makes design drift **impossible to do silently** — every hard drift must resolve to Conform / Amend / Waive before a gate passes.

**ID:** GCE-AG-10 · **Type:** Audit · **Tier:** 1 (always present) · **Producer:** AI-GCE

---

## Trigger

- **Shortcut:** `DFT__` (typed anywhere in a prompt) — primary mechanism
- **Session-end:** a generated **session-end hook** (Kiro `agentStop` / Claude Code `Stop`) invokes this agent at session close — **silent when clean**. On advisory platforms (Cursor / Codex / Generic) session-end drift is manual (`DFT__`) or a CI step. *(This is the destination-workspace session-end; it is NOT the internal build `SEG__` trigger.)*
- **Pre-gate:** before any gate pass (mandatory for hard-governed workspaces)
- **Sub-commands:**
  - `DFT__` — full scan (detect + classify + log)
  - `DFT__ quick` — top-N highest-risk hard elements only
  - `DFT__ deep` — all elements (hard + advisory)
  - `DFT__ route` — AI-FLO brokers OPEN entries (envelope→target) so owning packages can pull their drift address (FLO never writes the register)
  - `DFT__ status` — summary (counts by classification/status)
  - `DFT__ history` — disposition ledger (resolved entries)
  - `DFT__ element {id}` — detail view of one governed element + its drift history

---

## When to Invoke

- Before any gate pass (mandatory for hard-governed workspaces)
- At session end (recommended — safety net)
- On demand whenever implementation feels "off-design"
- After any significant refactor or technology change

---

## Behavior (Steps)

### Step 1: Discover (Manifest-Driven)
- Read `.governance/workspace-manifest.yaml`
- Resolve: `files.baselineManifest`, `files.driftRegister`, `paths.*`, `platformTargets`, `storyStyle`
- NEVER hardcode paths. (Legacy fallback: no manifest → warn + legacy scan.)

### Step 2: Load Baseline + Register
- Read current baseline governed surface (`baselines/current/baseline-manifest.yaml`)
- Read existing Drift Register (open/closed/waived entries + `lastScanTimestamp`)

### Step 3: Detect
- For each governed element: locate reality artifact + compare (per `drift/element-comparators.md`)
- Apply waiver check (skip unexpired waived) + thrash guard (skip elements re-baselined this cycle)
- Classify HARD/ADVISORY; tag domain (architecture/data/infrastructure/ux/product — no `governance`;)
- Log new entries to the register (pinned to current baseline version, with evidence)

### Step 4: Re-verify Existing
- Re-measure each OPEN entry — still drifted? → keep OPEN; gone? → SELF-RESOLVED
- Read latest re-baseline ledger → CLOSE entries whose disposition is confirmed (Conform/Amend/Retire self-verify; Waive = annotation + unexpired check)
- Check waiver expiry → expired waivers auto-reopen as DETECTED + re-measure

### Step 5: Report
- Update `.governance/drift-register.md` (`lastScanTimestamp`)
- Console summary (silent when compliant):
  ```
  Drift scan vs baseline v{N}:
    🆕 {new} new ({H} hard, {A} advisory)
    ✅ {resolved} resolved   ⏳ {open} open ({openHard} hard)
    🔕 {waived} waived ({expiringSoon} expiring ≤7d)
  ```
- IF `openHard > 0`: `⛔ Gate blocked: {openHard} unresolved hard drift(s).`
- IF `openHard == 0`: `✅ Gate clear — all governed elements pass.`

---

## Consequences of Skipping

- Design debt accumulates silently — the design artifacts become fiction
- Gate evaluation (FLO advance) will detect hard drift anyway, but later = more expensive
- Advisory drift has no consequence of skipping (informational)

---

## Recovery

- Run `DFT__` to produce a current register
- For each HARD entry: `DFT__ route` → AI-FLO routes to the owning package → package disposes (Conform/Amend/Waive) → DWG re-baselines → re-run `DFT__` to confirm closure

---

## Checks Performed

- Every governed element measured against reality (per element type)
- Existing OPEN entries re-verified (self-resolved detection)
- Waiver expiry enforced (auto-reopen)
- Thrash guard applied (one-cycle suppression on just-changed elements)
- Dispositions verified by re-reading the re-baselined version

---

## Output

- Updated `.governance/drift-register.md`
- Console scan summary + gate status
- On HARD drift: block signal (platform-specific — see `drift/gate-integration.md`)

---

## Platform Enforcement

Enforcement mechanism per `manifest.platformTargets`:
- **Kiro / Claude Code:** agent + hook — automatic gate blocking
- **Cursor / Codex:** advisory + CI/CD gate
- **Generic:** CI/CD script fails on hard drift

Disclosed in `PLATFORM_NOTES.md` when editor-level blocking isn't available.

---

## Related

- Engine: `drift/drift-detection-engine.md` · Comparators: `drift/element-comparators.md`
- Register: `drift/drift-register.md` · Gate: `drift/gate-integration.md`
- Contract: `AGENT_GOVERNANCE_CONTRACT.md` §4
- Registered in `.governance/AGENT_REGISTRY.md` + documented in `.governance/AGENT-GUIDE.md`

---

## DFT__ Shortcut Registration

AI-GCE registers `DFT__` in the destination workspace's entry-point rules (`rules/workspace-rules.md`) and in `.governance/AGENT_REGISTRY.md`. Because `DFT__` is a **destination-workspace** trigger (not an internal build trigger), it belongs in the family's published `TRIGGER_KEYS_REFERENCE.md` — NOT the internal build reference (workspace Rule 19).
