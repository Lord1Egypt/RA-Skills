<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Drift Detection Engine — Detect, Classify, Tag, Verify

## Purpose

Defines how AI-GCE detects **midflight design drift** — reality in the generated workspace diverging from the DWG baseline (the governed surface) without acknowledgment. GCE is the **sole detector**. It measures reality against the current baseline version, classifies each divergence, tags it with a domain for routing, logs it to the Drift Register, and later verifies dispositions by re-reading the re-baselined version.

**GCE never fixes drift.** Detect + log + verify. Resolution belongs to the target package (via AI-FLO routing); DWG owns re-baselining.

**Trigger:** `DFT__` (on-demand, primary) + session-end (the destination `agentStop`/`Stop` drift hook — NOT the internal build `SEG__`) + gate pre-check. No continuous file-event hooks (detection is expensive; continuous firing fights the flow).

**Grounding:** Implements `MIDFLIGHT_DRIFT_GOVERNANCE_DESIGN.md` §5, §8.

---

## MANDATORY: Stage Sub-Role — Audit Specialist

Audit Specialist mindset (evidence-based detection, no false positives, verify-don't-trust). ADDS a dimension — does NOT replace the primary Compliance/Governance role.

### Behavioral Shifts
- Drift is reality diverging from an *approved* element without acknowledgment — the danger is silence, not change
- Silent when compliant — a passing element produces NO output
- Detect and log; never fix. Never trust a disposition blindly — re-measure.

### Anti-Patterns
- Do NOT fix drift (that's the target package's job after routing)
- Do NOT flag a waived (unexpired) or thrash-guarded element
- Do NOT hardcode paths — discover the workspace via `.governance/workspace-manifest.yaml`

---

## Discovery (Manifest-Driven)

GCE's FIRST action: read `.governance/workspace-manifest.yaml` to locate everything.

```
1. Read.governance/workspace-manifest.yaml
   → files.baselineManifest → the governed surface to measure against
   → files.driftRegister → where to log
   → paths.rules / paths.src / paths.backlog / … → where reality lives
   → platformTargets → enforcement mechanism (see gate-integration.md)
   → storyStyle → AC format for acceptance-criteria elements
2. Read the current baseline (files.baselineManifest → baselines/current/)
   → governedElements (hard) + advisoryElements
   → dispositionLedger (waivers, prior closures)
```

GCE NEVER hardcodes `rules/` or file paths — the manifest is the discovery contract. (Legacy fallback: if no manifest, warn + use the legacy scan — see `common/workspace-reading-guide.md`.)

---

## Detection Algorithm

```
Read baseline.current (governedElements + advisoryElements + dispositionLedger)

FOR EACH element in governedElements + advisoryElements:
  1. LOCATE the reality artifact (element.source + type-specific strategy — element-comparators.md)
  2. COMPARE reality vs the element's declared truth (per comparator)
  3. IF divergence:
     a. WAIVER CHECK — is this element WAIVED and unexpired in the ledger?
        → YES: skip (suppressed until expiry)
     b. THRASH GUARD — was this element re-baselined in the current cycle?
        → YES: skip (one-cycle suppression — drift-register.md)
     c. CLASSIFY:
        - element.locked == true  → HARD  (blocks gate)
        - element.locked == false → ADVISORY (informs, never blocks)
     d. TAG domain: architecture | data | infrastructure | ux | product
        (from the element's parent category in the baseline)
     e. LOG to Drift Register (new entry, pinned to current baselineVersion)
  4. IF no divergence: element PASSES (silent — no output)

FOR EACH existing OPEN entry in the register:
  - Re-measure: still drifted?
    → NO (gone without explicit disposition): mark SELF-RESOLVED
    → YES: remains OPEN
```

---

## Classification

| Classification | Governed element | Gate effect | Urgency |
|----------------|------------------|-------------|---------|
| **HARD** | `locked: true` | BLOCKS gate pass | Resolve before next gate |
| **ADVISORY** | `locked: false` | Never blocks | Deferrable |

Advisory sits as `OPEN-ADVISORY` — surfaced at session-end/gate as informational. Hard MUST reach Conform/Amend/Waive before the gate passes.

---

## Domain Tagging (for AI-FLO Routing)

GCE tags each entry with the owning design domain — the signal FLO uses to route to the target package. GCE does NOT name the target package (keeps GCE free of topology; FLO owns routing).

| Domain Tag | Owning design domain |
|------------|----------------------|
| `architecture` | Architecture decisions, tech choices, component boundaries |
| `data` | Data models, schema, migrations (arch sub-domain) |
| `infrastructure` | CI/CD, deployment, observability (arch sub-domain) |
| `ux` | Design tokens, UI patterns, a11y, navigation |
| `product` | Acceptance criteria, story scope, epics, value metrics |

> **No `governance` domain.** GCE's own governance layer is not a DWG baseline element (DWG doesn't generate it — GCE derives it), so it cannot drift. Stale/hand-edited rules are handled by GCE **re-derivation** (`re-derivation/selective-regeneration.md`), never the drift loop.

---

## GCE Verification (Confirm Each Disposition)

After DWG re-baselines (vN → vN+1) carrying a disposition, GCE re-reads the new baseline to confirm closure. **Two of three are self-verifying; only Waive is trust-based.**

| Disposition | How GCE confirms | Method |
|-------------|------------------|--------|
| **Conform** | Re-measure element vs SAME baseline version → drift gone | Automatic — element now matches |
| **Amend** | Re-measure vs NEW element in vN+1 → matches | Automatic — reality matches new truth |
| **Waive** | Read tolerated-divergence annotation in vN+1 → valid | Trust-based — check owner + unexpired expiry |
| **Retire** | Element removed from surface; files in `obsolete/` | Automatic — element no longer governed |

GCE reads the new baseline to learn every resolution (the ledger entry says what to expect; GCE confirms by measuring). One channel, one source of truth.

---

## Detection Depth by Scan Mode

| Mode | Elements checked | Use |
|------|------------------|-----|
| `DFT__ quick` | Top-N highest-risk hard elements | Mid-session sanity check |
| `DFT__` (standard) | All hard-governed elements | Normal gate check |
| `DFT__ deep` | All (hard + advisory) | Pre-release thorough scan |

---

## Build-Profile Note (Parked)

The drift design (§5.7) tunes detection depth by `buildProfile` (spec-driven = deep, freestyle = advisory-only). **`buildProfile` is PARKED** (build-method-agnostic DWG). When absent from the manifest, GCE uses **Standard** mode — measures reality against the baseline's governed elements regardless of build method. Detection does NOT depend on build profile. The mode-selection table activates only when the build-profile axis is unparked.

---

## Interaction with Other Files

| Related | Relationship |
|---------|--------------|
| `drift/element-comparators.md` | Per-type comparison strategies used in step 2 |
| `drift/drift-register.md` | Register schema, waiver management, thrash guard |
| `drift/gate-integration.md` | Gate Step 0 uses HARD-drift counts from the register |
| `templates/agents/drift-detect-agent.md` | The `DFT__` agent that runs this engine |
| (DWG) | Owns baseline + re-baseline; GCE reads it |
| (AI-FLO) | Reads register domain tags → routes to target package |

---

## Output Validation

- [ ] Workspace discovered via `.governance/workspace-manifest.yaml` (no hardcoded paths)
- [ ] Every governed element measured; passing ones silent
- [ ] Waived (unexpired) + thrash-guarded elements skipped
- [ ] Each divergence classified HARD/ADVISORY + domain-tagged
- [ ] Entries logged to the drift register, pinned to baseline version
- [ ] Existing OPEN entries re-measured (self-resolved detected)
- [ ] Dispositions verified by re-reading vN+1 (Waive = annotation check)
- [ ] Standard mode used when `buildProfile` absent (parked)
