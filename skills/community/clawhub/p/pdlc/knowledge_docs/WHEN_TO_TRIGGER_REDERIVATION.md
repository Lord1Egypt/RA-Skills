# When to Trigger Re-Derivation

**Decision:** Something changed in my project — do I need to re-run AI-DWG reconciliation and/or AI-GCE re-derivation? Or can I leave governance as-is?

**Derived from:** Pattern: Downstream Signaling + Pattern: Non-Destructive Reconciliation

---

## The Decision at a Glance

| What Changed | Re-Derive? | Urgency |
|-------------|:----------:|:-------:|
| ADR revised (tech stack, security, API strategy) | ✅ Yes | High — governance is stale |
| New container/service added to architecture | ✅ Yes | High — new code has no rules |
| Container removed from architecture | ✅ Yes | Medium — orphaned rules exist |
| Extension activated in AI-ADLC | ✅ Yes | High — new constraints needed |
| Extension deactivated | ✅ Yes | Medium — remove extension rules |
| Team agreements changed | ⚠️ Maybe | Low — only if enforced by hooks |
| Code refactored (no architecture change) | ❌ No | N/A — governance still applies |
| New team member joined | ❌ No | N/A — governance helps them |
| Sprint completed | ❌ No | N/A — run audit instead |
| Tier graduation requested | ⚠️ Partial | Medium — activate dormant rules |
| Bug fixed in existing code | ❌ No | N/A — existing rules still valid |
| New steering file added manually | ✅ Yes | Medium — derive rules for new file |

---

## When YES — Trigger Re-Derivation

### Architecture-Level Changes (Always Re-Derive)

These changes mean your steering files and/or governance rules are stale:

| Change | Pipeline | What Gets Updated |
|--------|----------|-------------------|
| Technology stack changed | AI-DWG (Mode 2) → AI-GCE | tech-stack.md → naming/testing/security rules |
| API versioning strategy changed | AI-DWG (Mode 2) → AI-GCE | api-standards.md → API-* rules + hooks |
| Security model changed | AI-DWG (Mode 2) → AI-GCE | security-rules.md → SEC-* rules + hooks |
| New service/container added | AI-DWG (Mode 2) → AI-GCE | module-structure.md → ARCH-* rules |
| Data architecture changed | AI-DWG (Mode 2) → AI-GCE | data-standards.md → data governance rules |
| Integration added/removed | AI-DWG (Mode 2) → AI-GCE | integration steering → resilience rules |

### Steering-Level Changes (GCE Re-Derivation Only)

If you manually edit a steering file:

| Change | Action |
|--------|--------|
| Added new rules to `api-standards.md` | AI-GCE re-derives API-* category |
| Modified `naming-conventions.md` | AI-GCE re-derives NAME-* category |
| Created new steering file (e.g., `performance-budgets.md`) | AI-GCE derives entirely new rule category |
| Deleted a steering file | AI-GCE flags derived rules as orphaned |

---

## When NO — Don't Re-Derive

These changes do NOT require re-derivation:

| Change | Why No Re-Derivation |
|--------|---------------------|
| Code refactoring (same architecture) | Governance rules still apply to new structure |
| Bug fixes | Existing rules are still valid |
| New features within existing containers | Module boundaries unchanged |
| Test additions | Tests don't change governance |
| Team member joins/leaves | Governance is role-based, not person-based |
| Sprint boundary | Run an audit instead (different process) |
| Dependency version bump (no API change) | Tech stack steering still accurate |
| Documentation updates | Steering is separate from docs |

---

## When MAYBE — Judgment Call

| Change | Re-Derive If... | Skip If... |
|--------|-----------------|------------|
| Team agreements changed | ...agreements are enforced by hooks | ...agreements are informational only |
| New tool adopted (linter, formatter) | ...it changes naming/coding rules | ...it's internal tooling only |
| CI/CD pipeline changed | ...deployment governance exists (Tier 3) | ...only Tier 1-2 active |
| Performance requirements changed | ...performance budgets are enforced | ...no Tier 3 governance yet |
| Tier graduation | Activate dormant rules (not re-derive) | N/A — this IS the trigger |

---

## The Re-Derivation Pipeline

When you decide YES:

```
Step 1: Identify what changed
        └── ADR revision? Steering edit? Extension change?

Step 2: Run AI-DWG Mode 2 (if architecture changed)
        └── Updates steering files to match new architecture
        └── Sends downstream signal to AI-GCE

Step 3: Run AI-GCE re-derivation
        └── Reads signal (or scans for changed steering)
        └── Proposes rule changes (diff view)
        └── You approve/reject proposed changes

Step 4: Post-re-derivation audit
        └── Quick compliance scan against new rules
        └── Baseline new violations (if new rules find existing issues)
        └── Communicate changes to team
```

---

## How to Know If Governance Is Stale (Without Signal)

If no one ran re-derivation and you're unsure:

| Check | How | Staleness Signal |
|-------|-----|-----------------|
| Compare steering dates vs. rule dates | `generatedOn` in front-matter | Rule older than its source steering = stale |
| Run compliance audit | AI-GCE audit mode | "Orphaned rules" finding = stale |
| Check `.compliance-state.json` | `lastAudit` timestamp | >4 weeks since last audit = potentially stale |
| Compare `adlc-state.md` revision date vs. workspace | Manual check | AP newer than workspace = DWG reconciliation needed |

---

## Frequency Recommendations

| Project Phase | Re-Derivation Frequency |
|--------------|------------------------|
| Early design (architecture changing often) | After every ADR revision |
| Stable delivery (architecture locked) | Only if steering is manually edited |
| Post-launch (maintenance mode) | Quarterly audit triggers if needed |
| After major architecture pivot | Immediate full re-derivation |

---

## Related Documents

| Document | Location |
|----------|----------|
| Pattern: Downstream Signaling | `knowledge_docs/PATTERN_DOWNSTREAM_SIGNALING.md` |
| Pattern: Non-Destructive Reconciliation | `knowledge_docs/PATTERN_NON_DESTRUCTIVE_RECONCILIATION.md` |
| How GCE Rederivation Works | `knowledge_docs/HOW_GCE_REDERIVATION_WORKS.md` |
| How to Handle Architecture Changes Mid-Project | `knowledge_docs/HOW_TO_HANDLE_ARCHITECTURE_CHANGES_MID_PROJECT.md` |
| What If Architecture Changes Break Governance | `knowledge_docs/WHAT_IF_ARCHITECTURE_CHANGES_BREAK_GOVERNANCE.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
