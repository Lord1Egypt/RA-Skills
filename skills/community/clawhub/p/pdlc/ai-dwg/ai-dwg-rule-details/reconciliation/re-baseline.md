<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Re-Baseline — Version Bump, Stamp Refresh, Obsolescence (Mode 2)

## Purpose

Defines how AI-DWG re-versions the baseline during Mode 2 (Delta Reconciliation) or when a drift disposition resolves. Re-baseline is the DWG-only operation that bumps the baseline version, refreshes per-document stamps, regenerates the manifest + context/relevance maps, and applies obsolescence for dropped files. DWG is the **sole writer** of the baseline (drift design D1).

**Trigger:** Mode 2 fires (peer input changed / platform or story-style changed / drift disposition requested / file retirement needed).

**Grounding:** Implements `MIDFLIGHT_DRIFT_GOVERNANCE_DESIGN.md` §4.4 + §8; complements `baseline/baseline-generation.md`, `baseline/document-stamping.md`, `baseline/workspace-manifest-generation.md`.

---

## MANDATORY: Stage Sub-Role — Audit Specialist + Automation Engineer

Audit Specialist (version integrity) + Automation Engineer (deterministic regeneration). ADDS a dimension — does NOT replace the primary role.

### Anti-Patterns
- Do NOT skip the version bump — every re-baseline is a new monotonic version
- Do NOT hard-delete dropped files — obsolescence protocol only
- Do NOT overwrite `<!-- custom -->` content — merge-strategy preserves it

---

## Re-Version Triggers

| Trigger | Source | What re-baseline does |
|---------|--------|-----------------------|
| Platform target change | Config Gate Q2 re-run | Re-render adapters through new platform; bump version |
| Story style change | `polc-state.md` `Story Style:` changed | Re-format story cluster; recheck advisory; bump |
| AP updated | `adlc-state.md` delta | Delta reconciliation + update governed elements; bump |
| PBP updated | `polc-state.md` delta | Update product governed elements; bump |
| UXP updated | `uxd-state.md` delta | Update UX governed elements; bump |
| Drift disposition: Conform | FLO pickup → package restored reality | Carry ledger entry (design unchanged); bump |
| Drift disposition: Amend | FLO pickup → package changed design artifact | Update governed element + ledger; bump |
| Drift disposition: Waive | FLO pickup → package produced waiver | Add tolerated-divergence annotation + ledger; bump |
| File retirement | peer input dropped a file | Obsolescence (move to local `obsolete/`) + `retire` ledger; bump |

---

## Re-Baseline Procedure (vN → vN+1)

```
0. PICKUP DIGEST-READY DISPOSITIONS (drift-triggered re-baseline only — pull via FLO)
   - DWG → FLO: "Any digested drift ready in packages?"
   - FLO returns an ADDRESS list only: [ { driftId, package, dispositionType, output-address } ]
     (FLO polls each package's "digest ready" signal read-only; carries no payload)
   - DWG reads each disposition DIRECTLY from the package's own output at that address
   - DWG never reads the drift register and never reads FLO's routing-log for content —
     it consumes only the pointers FLO hands over, then reads package output (INV-L4-006)
   - Skip this step for non-drift triggers (platform/story/peer-input delta)

1. DETECT DELTA (reconciliation/diff-strategy.md)
   - What peer-input content changed since baseline vN?
   - Classify: add / modify / remove per affected workspace file

2. ARCHIVE CURRENT
   - Copy baselines/current/ → baselines/v{N}/ (immutable snapshot)

3. APPLY CHANGES (reconciliation/merge-strategy.md — preserves <!-- custom -->)
   - Added files: generate + stamp v{N+1} (confirmed v{N+1})
   - Modified files: re-generate + stamp v{N+1} (confirmed v{N+1})
   - Unchanged files: bump ONLY confirmed → (confirmed v{N+1}) [single-line edit]
   - Removed files: OBSOLESCENCE (baseline/document-stamping.md Part 2)

4. UPDATE GOVERNED SURFACE (baseline/baseline-generation.md)
   - Add/modify/retire governed elements per the delta
   - Append disposition ledger entry (amend / conform / waive / retire)
   - Write baselines/v{N+1}/baseline-manifest.yaml + snapshot-meta.yaml

5. REGENERATE DERIVED ARTIFACTS
   - .governance/workspace-manifest.yaml (bump baselineVersion, refresh entries)
   - WORKSPACE_CONTEXT_MAP.md + folder READMEs (fresh from manifest)
   - rules/relevance-map.md (re-derive; preserve <!-- custom --> rows)

6. THRASH GUARD (drift design D15)
   - For each element changed in v{N+1}: suppress drift detection on it for ONE scan cycle
   - Prevents Amend → detect → Amend loop

7. SIGNAL DOWNSTREAM (reconciliation/downstream-signaling.md)
   - Notify AI-GCE the workspace changed (steering-files-updated / workspace-generated)
   - GCE reads v{N+1} to verify dispositions + re-scan
```

---

## Stamp Refresh Rules (Approach C)

| File state in this re-baseline | Primary version | Confirmed version |
|--------------------------------|:---------------:|:-----------------:|
| Added | v{N+1} | v{N+1} |
| Modified | v{N+1} | v{N+1} |
| Unchanged | unchanged (v{prior}) | → v{N+1} (single-line bump) |
| Retired | frozen at v{N} | frozen at v{N} (moved to `obsolete/`) |

See `baseline/document-stamping.md` for format per file type.

---

## Disposition Handling (Drift Closure)

When re-baseline is triggered by a drift disposition, the ledger entry records how GCE will verify closure:

| Disposition | Ledger records | GCE verification (next scan of v{N+1}) |
|-------------|----------------|----------------------------------------|
| Conform | element unchanged, drift resolved | Re-measure vs same element → drift gone |
| Amend | updated governed element | Re-measure vs new element → matches |
| Waive | tolerated-divergence annotation + owner + expiry | Annotation present + unexpired |
| Retire | retired element + `retiredFiles` | Element removed from surface; files in `obsolete/` |

**How DWG learns of a disposition (pull, not push):** DWG asks FLO for digest-ready items (Procedure Step 0). FLO returns pointers only; DWG reads the disposition from each package's own output, then bakes it into v{N+1}. GCE reads v{N+1} to confirm (drift design §8.2). DWG never reads the drift register; the baseline is the only channel back to GCE.

---

## Interaction with Other Files

| Related | Relationship |
|---------|--------------|
| (AI-FLO `route/drift-routing.md`) | DWG pulls digest-ready dispositions from FLO (Step 0); FLO returns addresses only |
| `reconciliation/diff-strategy.md` | Detects the delta that triggers re-baseline |
| `reconciliation/merge-strategy.md` | Preserves `<!-- custom -->` during re-generation |
| `reconciliation/downstream-signaling.md` | Notifies GCE after re-baseline |
| `baseline/baseline-generation.md` | Governed surface + versioning + archive |
| `baseline/document-stamping.md` | Stamp refresh + obsolescence mechanics |
| `baseline/workspace-manifest-generation.md` | Manifest regenerated with new version |

---

## Output Validation

- [ ] Drift-triggered re-baseline pulls digest-ready dispositions via FLO (Step 0), reads payload from package output (not the register)
- [ ] Monotonic version bump (v{N} → v{N+1}); prior archived immutably
- [ ] Added/modified files stamped v{N+1} (both); unchanged bump confirmed only
- [ ] Retired files → local `obsolete/` + `retire` ledger entry (never hard-deleted)
- [ ] Disposition ledger entry appended
- [ ] Manifest + context map + relevance map regenerated (`<!-- custom -->` preserved)
- [ ] Thrash-guard suppression applied to changed elements for one cycle
- [ ] Downstream signal sent to AI-GCE
