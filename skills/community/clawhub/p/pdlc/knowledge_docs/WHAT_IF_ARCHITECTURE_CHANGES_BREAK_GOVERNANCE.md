# What If Architecture Changes Break Governance?

**Scenario:** You changed the architecture (new ADR, removed a container, switched technology), ran reconciliation through AI-DWG → AI-GCE, and now governance is broken — conflicting rules, hooks that reference deleted steering, or compliance score crashed overnight.

---

## Symptoms

- Hooks fire on patterns that no longer exist in the architecture
- Rules reference a steering file that was removed during reconciliation
- Two rules contradict each other (old rule + new rule both active)
- Compliance score dropped 20%+ immediately after re-derivation
- Developers get errors like "rule ARCH-03 references module-structure.md §4 — section not found"

---

## Diagnosis: What Went Wrong?

| Cause | Signal | Root Problem |
|-------|--------|-------------|
| **Stale rules not cleaned** | Old rules still reference removed steering | Re-derivation didn't remove obsolete rules |
| **Partial re-derivation** | Some rules updated, some not | Only affected files were re-derived, but impact was broader |
| **Conflicting rules** | Rule A says "must use REST", Rule B says "must use GraphQL" | Architecture changed but old rule wasn't superseded |
| **Hook targets deleted files** | Hook fires on file patterns that no longer exist in the project | AI-DWG removed containers → folder patterns stale |
| **Tier mismatch** | Re-derivation activated rules at wrong tier | Tier state wasn't preserved during re-derivation |
| **Baseline + new rules overlap** | Same concern enforced by both baseline and new derived rule | Deduplication missed during re-derivation |

---

## Immediate Actions (Stop the Bleeding)

### Step 1: Identify Broken Rules

Check `.governance/rules/` for rules that reference missing content:
- Search for file references that point to deleted steering files
- Look for rules whose `source` field points to something that no longer exists
- Check hook patterns against actual folder structure

### Step 2: Disable Broken Rules (Not Delete)

For each broken rule:
```json
{
  "status": "disabled",
  "disabledReason": "Source steering file removed during architecture change — pending re-derivation",
  "disabledOn": "2026-06-12"
}
```

Disabling is reversible. Deleting loses the rule ID and audit trail.

### Step 3: Notify the Team

"Governance temporarily reduced — some rules disabled while we fix the architecture-to-governance alignment. Core rules (Tier 1) unaffected."

---

## Recovery: Full Re-Derivation

When partial re-derivation caused the problem, run FULL re-derivation:

### Option A: Clean Re-Derivation (Recommended)

1. **Back up current governance** — copy `.governance/` and `.kiro/hooks/` 
2. **Run AI-GCE fresh** against the CURRENT steering files (post-reconciliation)
3. AI-GCE re-derives ALL rules from scratch against current state
4. **Compare** new derivation against backup — what changed, what was removed?
5. **Restore custom content** — check backup for `<!-- custom -->` blocks, reapply to new files
6. **Verify** compliance score makes sense for current architecture

### Option B: Targeted Fix

If the problem is limited to specific rule categories:

1. Identify affected category (e.g., `ARCH-*` rules broken because module-structure changed)
2. Delete ONLY rules in that category that reference stale content
3. Run AI-GCE focused re-derivation: "Re-derive ARCH rules from current module-structure.md"
4. New rules generated for current architecture
5. Other categories unaffected

---

## Prevention: The Reconciliation Checklist

Before running AI-DWG → AI-GCE reconciliation, check:

| Step | What to Verify |
|------|---------------|
| 1 | AP change is finalized (not mid-revision) |
| 2 | ADR for the change exists (rationale documented) |
| 3 | AI-DWG ran in Mode 2 (Delta), not Mode 1 (Full — would overwrite customs) |
| 4 | Steering file diff reviewed (what changed, what was removed) |
| 5 | AI-GCE signal received with COMPLETE list of affected files |
| 6 | Re-derivation scope matches the change scope (not too narrow, not full rebuild) |
| 7 | Post-re-derivation audit run immediately (catch issues before team hits them) |

---

## Common Architecture Changes and Their Governance Impact

| Architecture Change | Governance Impact | Required Action |
|--------------------|-------------------|-----------------|
| Container removed | Module boundary rules reference dead module | Remove/update ARCH rules for that module |
| Tech stack changed | tech-stack.md updated → naming/testing rules may change | Full re-derive for affected categories |
| New container added | New module needs boundary rules | Re-derive ARCH rules (additive) |
| Extension activated | New steering file generated | Re-derive for new category (additive) |
| Extension deactivated | Steering file removed | Remove rules that reference that extension's steering |
| Security model changed | security-rules.md updated | Re-derive SEC rules |
| API versioning changed | api-standards.md updated | Re-derive API rules |

---

## The "Compliance Score Crashed" Scenario

If score drops 20%+ after re-derivation:

1. **Check: are there new rules?** New rules find new violations in existing code → expected score dip
2. **Check: are old rules broken?** Rules that can't evaluate (missing reference) may count as violations
3. **Check: was baseline reset?** If baseline was accidentally cleared, all existing violations now count

**Response by cause:**
- New rules finding real violations → use baseline pattern (enforce forward, not backward)
- Broken rules → disable them (see Step 2 above)
- Baseline reset → restore baseline from `.compliance-state.json` backup or re-run baseline scan

---

## When to Start Over (Nuclear Option)

Consider full governance rebuild when:
- More than 50% of rules are broken
- Three partial fixes haven't resolved the issues
- Architecture changed so fundamentally that old governance is irrelevant
- Team trust in governance is damaged by repeated breakage

**How:** 
1. Archive current `.governance/` and `.kiro/hooks/`
2. Run AI-GCE fresh against current workspace
3. Start at Tier 1 (rebuild trust)
4. Graduate quickly (team already knows the rules)

---

## Related Documents

| Document | Location |
|----------|----------|
| How to Handle Architecture Changes Mid-Project | `knowledge_docs/HOW_TO_HANDLE_ARCHITECTURE_CHANGES_MID_PROJECT.md` |
| How GCE Rederivation Works | `knowledge_docs/HOW_GCE_REDERIVATION_WORKS.md` |
| How Tiered Governance Works | `knowledge_docs/HOW_TIERED_GOVERNANCE_WORKS.md` |
| How Compliance Logging Works | `knowledge_docs/HOW_COMPLIANCE_LOGGING_WORKS.md` |
| What If Team Rejects Governance | `knowledge_docs/WHAT_IF_TEAM_REJECTS_GOVERNANCE.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
