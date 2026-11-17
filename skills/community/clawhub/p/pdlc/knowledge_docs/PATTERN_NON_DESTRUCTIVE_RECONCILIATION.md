# Pattern: Non-Destructive Reconciliation

**Purpose:** Documents the reusable design pattern where updates to generated artifacts NEVER destroy existing content — proposing changes for human review, preserving team edits, and operating in overlay mode rather than replace mode.

---

## The Pattern

```
EXISTING STATE (generated artifacts + team customizations)
        │
        ▼
CHANGE TRIGGER (architecture revised, steering updated, tier upgraded)
        │
        ▼
┌─────────────────────────────────────────────────────────────────────┐
│  NON-DESTRUCTIVE RECONCILIATION                                      │
│                                                                      │
│  1. DETECT what changed (signal-based or scan)                       │
│  2. MAP impact (which existing artifacts are affected)                │
│  3. PROPOSE changes (show diff, don't auto-apply)                    │
│  4. PRESERVE team edits (ownership-aware merge)                      │
│  5. APPLY only after human approval                                  │
└─────────────────────────────────────────────────────────────────────┘
        │
        ▼
UPDATED STATE (affected files updated + team content intact)
```

**One sentence:** Changes are proposed, not imposed — existing team work is sacred, and nothing is overwritten without explicit approval.

---

## Where It's Used

| Package | Mode | Reconciliation Context |
|---------|------|----------------------|
| **AI-DWG** | Mode 2 (Delta Reconciliation) | Architecture changed → update affected steering files |
| **AI-DWG** | Mode 3 (Brownfield Overlay) | Add governance to existing codebase without touching it |
| **AI-GCE** | Re-derivation | Steering updated → re-derive affected rules/hooks |
| **AI-TGE** | Architecture Reconciliation (Stage 10) | AP changed → update test register |
| **AI-ADLC** | Brownfield extension | Load existing architecture, modify only new parts |

---

## Why This Pattern Exists (Lessons 3, 6, 7)

**The problem it solves:** Real projects change after initial generation. Architecture evolves, teams customize outputs, constraints shift. A generator that only does "full generation" forces teams to:
- Start over (losing all customizations)
- Never re-run (accepting stale governance)
- Maintain shadow copies (working outside the tool)

All three are unacceptable. Non-destructive reconciliation enables evolution without loss.

---

## The Five Guarantees

| Guarantee | Meaning |
|-----------|---------|
| **No source code changes** | Reconciliation writes only to governance/steering folders, never to `src/` |
| **No custom content loss** | `<!-- custom -->` blocks preserved verbatim (see Pattern: Custom Preservation) |
| **No silent overwrites** | Changes are shown to user before application |
| **No surprise deletions** | Obsolete files are flagged for removal, not auto-deleted |
| **No config destruction** | Existing `.eslintrc`, `tsconfig.json`, etc. are never modified |

---

## The Propose-Review-Apply Flow

```
PROPOSED CHANGES
├── Modified: api-standards.md (diff shown)
│   └── Section 3.2: versioning changed from URL to header-based
├── Added: graphql-standards.md (new file — architecture now includes GraphQL)
├── Unchanged: security-rules.md (no impact from this change)
└── Flagged: rest-only-patterns.md (may be obsolete — architecture added GraphQL)

USER REVIEWS
├── api-standards.md changes → ✅ Approve
├── graphql-standards.md addition → ✅ Approve
├── rest-only-patterns.md removal → ❌ Keep (still relevant for legacy endpoints)

APPLIED: only approved changes written
```

**Key principle:** The reconciliation engine proposes a PLAN. The user approves, modifies, or rejects each item. Nothing happens without confirmation.

---

## Reconciliation Modes

| Mode | What's Updated | What's Preserved |
|------|---------------|-----------------|
| **Surgical (targeted)** | Only files affected by the specific change | Everything else untouched |
| **Category-wide** | All files in a category (e.g., all API rules) | Other categories untouched |
| **Full re-derivation** | All generated files | Team customs (via `<!-- custom -->`) + user-owned files |
| **Overlay (brownfield)** | Nothing existing; only NEW files added | 100% of existing workspace preserved |

---

## Impact Mapping

Before proposing changes, reconciliation maps impact:

```
CHANGE: api-standards.md updated (versioning strategy)
        │
        ├── Direct impact: api-standards.md (the file itself)
        │
        ├── Derived impact: .governance/rules/API-02_versioning.md (references this steering)
        │                   .kiro/hooks/api-contract-check.json (enforces this steering)
        │
        └── No impact: security-rules.md, naming-conventions.md, module-structure.md
                       (unrelated to API versioning change)
```

Only directly and derivatively impacted files are touched. Everything else is guaranteed unchanged.

---

## Handling Conflicts

When a change affects content the team has also modified:

| Scenario | Resolution |
|----------|-----------|
| Generated section changed by team (outside custom markers) | Show both versions, let user choose |
| Custom block references something that changed | Preserve custom, flag for team review |
| New generated content conflicts with custom content | Keep custom (team authority wins), log warning |
| File was deleted by team but re-derivation wants it | Don't recreate — respect the deletion |

---

## Implementation Rules

1. **Always show what will change before changing it** — no silent modifications, ever.

2. **Ownership field determines behavior** — `generated` files can be overwritten; `hybrid` files merge; `user` files are never touched.

3. **Flagging ≠ deleting** — when something becomes obsolete, flag it for human review. Only human confirms deletion.

4. **Log every reconciliation action** — compliance log records what changed, what was proposed, what was accepted/rejected.

5. **Partial approval is valid** — user can approve 3 of 5 proposed changes and reject 2. The engine applies only the approved set.

6. **Reconciliation is idempotent** — running the same reconciliation twice (same input, same state) produces the same proposal. No drift from re-runs.

---

## When to Apply This Pattern

Apply when:
- [ ] Generated artifacts are expected to evolve over time
- [ ] Team customizations exist and must survive updates
- [ ] The cost of full regeneration is high (lost customizations, context reset)
- [ ] Changes should be traceable (audit requirement)
- [ ] Human judgment is needed to evaluate proposed changes

Don't apply when:
- Files are 100% generated with no team edits (just overwrite — simpler)
- The artifact is ephemeral (recreated from scratch each time, no persistence)
- Speed matters more than safety (batch automation with no human review)

---

## Related Documents

| Document | Location |
|----------|----------|
| Pattern: Custom Preservation | `knowledge_docs/PATTERN_CUSTOM_PRESERVATION.md` |
| Pattern: Downstream Signaling | `knowledge_docs/PATTERN_DOWNSTREAM_SIGNALING.md` |
| How GCE Rederivation Works | `knowledge_docs/HOW_GCE_REDERIVATION_WORKS.md` |
| How DWG Generation Engine Works | `knowledge_docs/HOW_DWG_GENERATION_ENGINE_WORKS.md` |
| How to Handle Architecture Changes Mid-Project | `knowledge_docs/HOW_TO_HANDLE_ARCHITECTURE_CHANGES_MID_PROJECT.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
