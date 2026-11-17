# How AI-GCE Re-Derivation Works

**Purpose:** Explains how AI-GCE selectively updates its rules and hooks when steering files change — the change detection, impact mapping, selective regeneration, and customization preservation mechanics of Mode 2.

---

## What Re-Derivation Is

When architecture changes and AI-DWG reconciles the workspace (updating steering files), AI-GCE's existing rules and hooks may become stale. Re-derivation is the surgical update process that regenerates ONLY the affected artifacts while preserving everything else — including team customizations.

```
STEERING FILE CHANGED (e.g., api-standards.md updated)
        │
        ▼
┌─────────────────────────────────────────────────────────────────────┐
│  AI-GCE RE-DERIVATION (Mode 2)                                       │
│                                                                      │
│  DETECT    →    MAP IMPACT    →    PROPOSE    →    REGENERATE        │
│  (what       (which rules/      (show user      (surgical update     │
│   changed)    hooks affected)    the impact)     preserving custom)  │
└─────────────────────────────────────────────────────────────────────┘
        │
        ▼
AFFECTED RULES + HOOKS UPDATED (custom content preserved)
```

**Key principle:** Selective, not full. Touch ONLY what's affected. Leave everything else exactly as-is.

---

## How Change Is Detected (Three Methods)

### Method 1: AI-DWG Downstream Signal (Preferred)

When AI-DWG reconciles workspace steering, it sends a structured signal:

```
⚡ DOWNSTREAM SIGNAL
   From: AI-DWG
   Event: steering-files-updated
   Affected files: [api-standards.md, testing-strategy.md]
   Action required: Re-derive compliance for changed files
```

AI-GCE uses the `Affected files` list directly — no scanning needed.

### Method 2: User Specifies

User says: "Re-derive compliance — I updated api-standards.md"

AI-GCE uses the named files directly.

### Method 3: Timestamp Comparison (Fallback)

If no signal and user doesn't specify:
1. Read `.compliance-state.json` → `lastAudit` timestamp
2. Scan `.kiro/steering/*.md` for files modified after that timestamp
3. Present findings for user confirmation before proceeding

---

## Impact Mapping: Changed File → Affected Artifacts

Each steering file has a known set of downstream artifacts. Key mappings:

| Steering File Changed | Rules Affected | Hooks Affected |
|----------------------|----------------|----------------|
| `api-standards.md` | `api-first-compliance.md` | `api-contract-check.json` |
| `security-rules.md` | `security-compliance.md` | `security-gate-check.json` |
| `module-structure.md` | `module-boundaries.md`, `team-topology.md` | `module-boundary-check.json`, `domain-layer-purity.json` |
| `testing-strategy.md` | `cicd-gates.md` | `coverage-check.json` |
| `database-rules.md` | `data-governance.md` | `migration-safety.json` |
| `naming-conventions.md` | `naming-conventions.md` | `naming-check.json` |
| `session-governance.md` | `session-governance.md` | `session-discipline.json` |
| `role-isolation.md` | `role-isolation.md`, `team-topology.md` | `segregation-check.json` |
| `git-workflow.md` | `devops-deployment.md`, `pr-governance.md` | `pre-pr-checklist.json` |
| `TEAM_AGREEMENTS.md` | `pr-governance.md`, `role-isolation.md` | `pre-pr-checklist.json`, `segregation-check.json` |
| `CODEOWNERS` | `role-isolation.md`, `team-topology.md` | `module-boundary-check.json` |

### Special Case: `tech-stack.md` Changed

Technology changes affect ALL hooks (file patterns are tech-derived):
- If it's a version bump → update patterns selectively
- If it's a framework switch (NestJS → Django) → recommend Mode 1 full regeneration

### Special Case: New Conditional File Appears

When a conditional steering file is CREATED (e.g., `multi-tenancy.md` added):
- Generate NEW rule file (`tenant-isolation.md`)
- Generate NEW hook (`tenant-isolation-check.json`)
- Update COMPLIANCE_README, ENFORCEMENT-GUIDE, knowledge-map

### Special Case: Conditional File Removed

When a conditional steering file is DELETED:
- Remove the corresponding rule file and hook
- Update supporting documentation
- Log the removal

---

## The Re-Derivation Flow

### Step 1: Detect Changes

Use the best available method (signal → user → timestamps). Produce a list of changed steering files.

### Step 2: Present Impact Report

Before regenerating, show the user what will change:

```
🔄 RE-DERIVATION IMPACT ANALYSIS

Changed steering files: 2
  • api-standards.md (modified 2026-06-10)
  • testing-strategy.md (modified 2026-06-10)

Impact:
┌────────────────────────────────────┬──────────────────────────────────┐
│ Affected Artifact                  │ Action                           │
├────────────────────────────────────┼──────────────────────────────────┤
│ .governance/rules/api-first-*.md   │ Re-derive rules from steering    │
│ .governance/rules/cicd-gates.md    │ Re-derive coverage thresholds    │
│ .kiro/hooks/api-contract-check.json│ Update rule references           │
│ .kiro/hooks/coverage-check.json    │ Update threshold in prompt       │
└────────────────────────────────────┴──────────────────────────────────┘

Proceed? (Custom content marked <!-- custom --> will be preserved.)
```

### Step 3: Selective Regeneration

For each affected rule file:
1. Read current file — identify all `<!-- custom -->` tagged rules
2. Extract custom rules (store temporarily)
3. Re-derive from updated steering using the appropriate generator
4. Merge custom rules back after a separator
5. Write the updated file

**Merge pattern:**
```
[Header with updated metadata + derivation date]
[Re-derived rules from updated steering]
---
## Custom Rules (Team-Added)
[Preserved custom rules — unchanged]
```

### Step 4: Update Affected Hooks

For hooks impacted by the change:
- Update prompt text (rule IDs, thresholds may have changed)
- Update `patterns` field if module paths or tech stack changed
- Increment hook version (1.0.0 → 1.1.0)
- Preserve any `## Custom Instructions` section in the prompt

### Step 5: Update Supporting Artifacts

- Knowledge map (updated source references)
- COMPLIANCE_README (if categories added/removed)
- ENFORCEMENT-GUIDE (if hooks added/removed)

### Step 6: Validate

Run V2 (traceability), V3 (consistency), V5 (hook integrity) on affected artifacts only.

---

## Customization Preservation

The core guarantee of re-derivation: team additions survive.

| Custom Content Type | Marker | Preserved During Re-Derivation |
|--------------------|--------|:------------------------------:|
| Team-added rules | `<!-- custom -->` tag | ✅ Always preserved |
| Team-added hook instructions | `## Custom Instructions` section | ✅ Always preserved |
| Team-renamed hooks | `name` field modified | ✅ Kept as-is |
| Team-changed event types | `when.type` modified | ✅ Kept as-is |

---

## What Re-Derivation Does NOT Do

| Action | Why Not |
|--------|---------|
| Touch unaffected rule files | Selective means selective |
| Reset compliance tier or score | Re-derivation ≠ audit |
| Remove hooks (even if conditional removed) | Removal is a separate flow in change-detection |
| Change hook event types | Debounce tier is stable once set |
| Re-run the compliance audit | Audit is a separate action |
| Update `.compliance-state.json` score fields | Only audit updates scores |

---

## Related Documents

| Document | Location |
|----------|----------|
| Change detection logic | `ai-gce/ai-gce-rule-details/re-derivation/change-detection.md` |
| Selective regeneration | `ai-gce/ai-gce-rule-details/re-derivation/selective-regeneration.md` |
| Upstream signaling | `ai-gce/ai-gce-rule-details/re-derivation/upstream-signaling.md` |
| Core generator (Mode 2) | `ai-gce/ai-gce-rules/core-generator.md` |
| AI-DWG reconciliation (signal source) | `ai-dwg/ai-dwg-rules/core-generator.md` (Mode 2) |

*Knowledge Document | Created: 2026-06-11 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
