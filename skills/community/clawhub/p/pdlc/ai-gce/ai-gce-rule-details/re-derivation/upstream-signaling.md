<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Upstream Signaling — How AI-DWG Triggers AI-GCE Re-Derivation

## Purpose

Defines the signaling mechanism between AI-DWG (upstream) and AI-GCE (downstream). When AI-DWG reconciles its workspace output (Mode 2: Delta Reconciliation), it signals AI-GCE to re-derive affected compliance artifacts.

---

## MANDATORY: Stage Sub-Role — Systems Engineer

During THIS activity, ALSO adopt the mindset of a **Systems Engineer**. This does NOT replace your primary role (Compliance Officer + Platform Engineer + AI-DLC v1 Engineer) — it ADDS a thinking dimension.

### Behavioral Shifts
- Think in inter-system contracts: the upstream signal is a formal interface between AI-DWG and AI-GCE — its format must be precise and reliable
- Evaluate signal reliability: same-session signals are immediate, cross-session requires timestamp fallback, manual triggers need disambiguation
- Map signal events to correct AI-GCE mode: `workspace-generated` → Mode 1, `steering-files-updated` → Mode 2
- Consider edge cases: signal arrives but AI-GCE never ran (→ Mode 1, not Mode 2), or signal mentions removed files (→ cleanup flow)
- Ensure AI-GCE logs every re-derivation event for traceability — compliance enforcement changes must be auditable

### Anti-Patterns for This Activity
- Do NOT assume signals persist across sessions (they don't — use timestamp fallback for cross-session scenarios)
- Do NOT enter Mode 2 when AI-GCE has never run on this workspace (empty .governance/hooks/ = Mode 1 territory)
- Do NOT modify .compliance-state.json score/tier fields during re-derivation (only audit updates those)

### Quality Check
A good output from this activity sounds like:
- "Signal received: steering-files-updated, affected=[api-standards.md, testing-strategy.md]. Entering Mode 2. Impact: 2 rule files + 2 hooks to re-derive. Logging REDERIVATION event with rulesUpdated:2, hooksUpdated:2."
- "Edge case: signal says 'workspace-generated' but .governance/hooks/ is empty. Correct response: enter Mode 1 (full generation), not Mode 2. This is first-time AI-GCE activation."

---

## The Signal Format

AI-DWG emits this structured signal after any reconciliation:

```
⚡ DOWNSTREAM SIGNAL
   From: AI-DWG
   To: AI-GCE
   Event: {workspace-generated | steering-files-updated}
   Workspace root: {path}
   Steering files: rules/ ({n} files)
   Affected files: {list of changed steering file paths}
   Change type: {content-update | file-added | file-removed}
   Triggered by: {ADR reference or user action}
   Action required: Re-derive compliance hooks/rules for changed files
```

---

## How AI-GCE Receives the Signal

### Scenario A: Same Session

If AI-DWG reconciliation and AI-GCE re-derivation happen in the same Kiro session:
- The signal is part of the conversation context
- AI-GCE reads the signal directly and enters Mode 2

### Scenario B: Separate Sessions

If the team runs AI-DWG reconciliation in one session and AI-GCE later:
- The signal doesn't persist across sessions
- AI-GCE uses **Method 3 (timestamp comparison)** from `change-detection.md`
- AI-GCE detects that steering files are newer than last audit date

### Scenario C: User Triggers Manually

User says: "Steering files were updated — re-derive compliance"
- This IS the signal. No formal structure needed.
- AI-GCE asks: "Which files changed?" or scans for recent modifications.

---

## Signal Events and AI-GCE Response

| Event | AI-GCE Response |
|-------|----------------|
| `workspace-generated` (first time) | This is Mode 1 territory — full generation, not re-derivation |
| `steering-files-updated` (content changed) | Mode 2: Re-derive affected rules + hooks |
| `steering-files-updated` (new file added) | Mode 2: Generate new rule category + hook (conditional file appeared) |
| `steering-files-updated` (file removed) | Mode 2: Remove corresponding rule category + hook (conditional deactivated) |

---

## What Triggers AI-DWG to Signal

AI-DWG sends a downstream signal when:

| AI-DWG Action | Signal Sent |
|---------------|-------------|
| Delta Reconciliation (Mode 2) — architecture changed | ✅ Always: "steering-files-updated" with affected list |
| Brownfield Overlay (Mode 3) — governance added to existing project | ✅ Always: "workspace-generated" (first-time signal for this project) |
| Manual steering file edit by team (not through AI-DWG) | ❌ AI-DWG doesn't send — AI-GCE detects via timestamp or user notification |

---

## Signal → Re-Derivation Scope

The signal's `Affected files` list directly determines re-derivation scope:

```
Signal says: Affected files: [api-standards.md, testing-strategy.md]

AI-GCE does:
  1. Load change-detection.md → map files to affected artifacts
  2. api-standards.md → re-derive api-first-compliance.md + api-contract-check.json
  3. testing-strategy.md → re-derive cicd-gates.md + coverage-check.json
  4. Run selective-regeneration.md for these 4 artifacts only
  5. Log REDERIVATION event
  6. Present summary
```

---

## AI-GCE Does NOT Signal Downstream

AI-GCE runs as a **continuous compliance companion alongside AI-DLC v1** — no package we own consumes its output downstream. AI-DLC v1 (external) consumes hooks from the filesystem at trigger time. No signal is needed — updated hooks take effect automatically on next IDE event.

However: AI-GCE DOES log a `REDERIVATION` event in `compliance-log/events/{date}.jsonl` so the team knows enforcement changed:

```json
{"timestamp": "{ISO-8601-UTC}", "type": "rederivation", "id": "rdr-{date}-{time}-001",
 "trigger": "api-standards.md, testing-strategy.md",
 "rulesUpdated": 2, "hooksUpdated": 2, "newArtifacts": 0,
 "reason": "AI-DWG downstream signal after architecture change"}
```

---

## Edge Case: Signal Arrives But AI-GCE Hasn't Run Yet

If AI-DWG signals "steering updated" but `.governance/hooks/` is empty (AI-GCE was never run):
- AI-GCE should enter **Mode 1 (Full Generation)** — not Mode 2
- The signal means: "the workspace exists and is ready for compliance derivation"
- This is the normal first-time trigger for AI-GCE in a chain workflow

---

## Integration with `.compliance-state.json`

After re-derivation completes:
- `.compliance-state.json` is NOT modified (re-derivation doesn't change tier or score)
- The `lastAudit` field stays unchanged (re-derivation ≠ audit)
- A new audit should be recommended: "Compliance rules updated. Run audit to see new score?"
