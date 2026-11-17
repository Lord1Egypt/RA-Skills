# Lifecycle of a Governance Rule

**Purpose:** Traces the complete lifecycle of an AI-GCE governance rule from birth to retirement — every state transition, what triggers each transition, and who decides.

---

## The Complete Lifecycle

```
BORN ──→ DORMANT ──→ ACTIVE ──→ ┬── REDERIVED ──→ ACTIVE (updated)
                                  ├── DISABLED ──→ (may reactivate)
                                  ├── OVERRIDDEN ──→ (documented exception)
                                  └── DEPRECATED ──→ REMOVED
```

---

## States

### 1. Born (Derived)

**Trigger:** AI-GCE reads a steering file and derives a rule from it.

**What happens:**
- Rule file created in `.governance/rules/`
- Rule assigned to a tier (1, 2, or 3)
- Rule assigned to a category (ARCH, SEC, API, NAME, TEST, GOV, SESSION)
- Provenance recorded (`source: .kiro/steering/{file}`)
- Corresponding hook generated (if enforcement is automatable)

**State:** Exists as a file — but may be dormant if its tier is above the current active tier.

### 2. Dormant (Tier Not Yet Active)

**Trigger:** Rule's tier is higher than the project's current governance tier.

**What happens:**
- Rule exists in `.governance/rules/` (visible, documented)
- Hook exists but doesn't fire (disabled state)
- Rule is NOT counted in compliance scoring
- Team can read it (previewing what the next tier adds)

**Duration:** Until the team graduates to the rule's tier.

### 3. Active (Enforcing)

**Trigger:** Project's governance tier reaches or exceeds the rule's tier.

**What happens:**
- Hook fires on relevant events
- Violations are detected and logged
- Rule counts toward compliance score
- Grace period may apply (advisory before blocking)

**Duration:** Indefinite — until re-derivation, disabling, or deprecation.

### 4. Re-Derived (Updated)

**Trigger:** Source steering file changed → AI-GCE re-derivation runs.

**What happens:**
- Rule content regenerated from new steering
- Rule ID preserved (continuity)
- Severity may change
- Hook updated to match new rule content
- Compliance log entry: `rule-rederived`
- Previous violations against old rule text: reassessed

**Result:** Rule returns to Active state with updated content.

### 5. Disabled (Turned Off)

**Trigger:** Team or lead explicitly disables a rule with documented rationale.

**What happens:**
- Rule remains in `.governance/rules/` (not deleted)
- Status field: `disabled`
- Hook stops firing
- Rule excluded from compliance score
- Compliance log entry: `rule-disabled` with rationale

**Can be reversed:** Re-enable at any time (status → `active`).

### 6. Overridden (Specific Exception)

**Trigger:** A specific violation is exempted (not the whole rule — just one case).

**What happens:**
- Rule remains active for all other cases
- Specific file/module gets documented exception
- Override has: rationale, approver, expiry date, ticket reference
- Compliance log entry: `violation-overridden`
- Score excludes the overridden instance

**Duration:** Until expiry date or manual removal.

### 7. Deprecated (Source Removed)

**Trigger:** Source steering file deleted or the architectural decision it enforces no longer exists.

**What happens:**
- Rule flagged as `deprecated` (not auto-deleted)
- Hook stops firing
- Rule excluded from compliance score
- Flagged in next audit as "orphaned" for human review

**Next step:** Human confirms removal (→ Removed) or recognizes the rule still has value (→ reassign to different source or convert to baseline).

### 8. Removed (End of Life)

**Trigger:** Human confirms deprecated rule should be deleted.

**What happens:**
- Rule file deleted from `.governance/rules/`
- Hook file deleted from `.kiro/hooks/`
- Compliance log entry: `rule-removed`
- Historical log entries preserved (the rule existed — audit trail intact)

**Irreversible:** Once removed, re-derivation from the same source would create a NEW rule (new ID).

---

## Lifecycle Duration Examples

| Rule | Typical Lifecycle |
|------|------------------|
| GOV-01 (author ≠ approver) | Born → Active → (never deprecated — universal) |
| ARCH-03 (module boundary for service X) | Born → Active → Re-derived (boundary changed) → Active → Deprecated (service merged) → Removed |
| SEC-05 (JWT validation) | Born → Active → Disabled (migration to OAuth) → Re-derived (new auth steering) → Active |
| PERF-01 (bundle size budget) | Born → Dormant (Tier 3) → Active (tier graduation) → Active indefinitely |

---

## Related Documents

| Document | Location |
|----------|----------|
| How Tiered Governance Works | `knowledge_docs/HOW_TIERED_GOVERNANCE_WORKS.md` |
| How GCE Rederivation Works | `knowledge_docs/HOW_GCE_REDERIVATION_WORKS.md` |
| How Compliance Logging Works | `knowledge_docs/HOW_COMPLIANCE_LOGGING_WORKS.md` |
| Pattern: Progressive Activation | `knowledge_docs/PATTERN_PROGRESSIVE_ACTIVATION.md` |
| Pattern: Two-Source Model | `knowledge_docs/PATTERN_TWO_SOURCE_MODEL.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
