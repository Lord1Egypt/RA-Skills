# When to Customize Generated Files vs. Update Steering

**Decision:** I want to change something in a generated file — should I edit the file directly (custom block) or change the steering file that produces it?

**Derived from:** Pattern: Custom Preservation + Pattern: Two-Source Model + Pattern: Downstream Signaling

---

## The Decision at a Glance

| What You Want to Change | Where to Change It |
|------------------------|-------------------|
| Add team-specific info (schedules, agreements, processes) | ✅ Custom block in the generated file |
| Change a governance rule's threshold or scope | ✅ Steering file (re-derive) |
| Add a project-specific convention not in architecture | ✅ Steering file (re-derive) |
| Add a one-off exception for a specific file/module | ✅ Custom block (or governance override) |
| Change the format/structure of a generated file | ❌ Neither — file a package issue |
| Disable a rule that doesn't apply to your project | ✅ Steering file (remove/modify the source) |

---

## The Core Rule

**If the change should SURVIVE re-derivation → use the right mechanism:**

| Mechanism | Survives Re-Derivation? | When to Use |
|-----------|:-----------------------:|-------------|
| Edit inside `<!-- custom -->` block | ✅ Always preserved | Team-specific additions (schedules, processes, notes) |
| Edit steering file → re-derive | ✅ Becomes the new source of truth | Rule changes, threshold changes, convention changes |
| Edit generated section (outside custom block) | ❌ LOST on next re-derive | Never — this is the anti-pattern |
| Override in `.compliance-state.json` | ✅ Logged as exception | Specific violation exemptions with rationale |

---

## Customize (Custom Block): When and How

### Use custom blocks when:

- Adding team-specific info that NO architecture decision produces
- Adding operational context (meeting times, rotation schedules)
- Adding clarifying notes for the team
- Adding temporary instructions ("until migration completes, also check X")
- Content is team-owned, not architecture-derived

### Examples of good custom content:

```markdown
<!-- custom -->
## Team-Specific Processes
- Code reviews: must be completed within 4 hours during business hours
- Emergency hotfix: can bypass normal PR process with tech-lead approval + post-mortem

## On-Call Rotation
- Week A: Alice (primary), Bob (secondary)
- Week B: Charlie (primary), Diana (secondary)
<!-- /custom -->
```

### What happens on re-derivation:
- Generated sections above the markers: regenerated from updated steering
- Your custom sections: preserved verbatim, untouched

---

## Update Steering: When and How

### Use steering changes when:

- You want to change a RULE (not add context)
- The change should affect derived governance (hooks, rules)
- The change is permanent (not a temporary exception)
- Other generated files should also reflect this change
- The change is architectural or convention-level

### Examples of steering-level changes:

| What You Want | Change This Steering File |
|--------------|--------------------------|
| Different naming convention | `naming-conventions.md` |
| Higher test coverage threshold | `testing-strategy.md` |
| New API versioning rule | `api-standards.md` |
| Additional security requirement | `security-rules.md` |
| New module boundary | `module-structure.md` |
| Change session governance rules | `session-governance.md` |

### What happens after steering change:
1. Edit the steering file
2. AI-GCE re-derives affected rules and hooks
3. New governance reflects your change
4. All generated files that source from that steering: updated on next re-derive

---

## The Anti-Pattern: Editing Generated Sections

**Never do this:**
```markdown
## API Standards (Generated section)
- All endpoints MUST have OpenAPI spec entries
- Versioning MUST use header-based strategy  ← ORIGINAL
+ Versioning MUST use URL-based strategy     ← YOUR EDIT (will be lost!)
```

**Why it fails:** Next re-derivation regenerates this section from `api-standards.md`. Your edit disappears silently. You won't know it's gone until someone violates the rule you thought you changed.

**Instead:** Edit `api-standards.md` (the steering source) → re-derive → the generated file now says what you want, and it STAYS that way through future re-derivations.

---

## Decision Flowchart

```
"I want to change something in a generated file"
        │
        ├── Is it adding NEW content (not modifying existing)?
        │   └── YES → Add inside <!-- custom --> block
        │
        ├── Is it changing a RULE or THRESHOLD?
        │   └── YES → Change the steering file → re-derive
        │
        ├── Is it a one-time EXCEPTION for one file/module?
        │   └── YES → Add governance override (with rationale + expiry)
        │
        ├── Is it changing the STRUCTURE/FORMAT of the generated file?
        │   └── YES → File an issue against the package (structure is package-owned)
        │
        └── Is it fixing a MISTAKE in the generated content?
            └── YES → Fix the steering source → re-derive (or fix AP → reconcile full chain)
```

---

## Hybrid Files: Both Mechanisms Work Together

A single file can have both generated and custom content:

```markdown
---
ownership: hybrid
---

## Naming Conventions (GENERATED — from naming-conventions.md steering)
- Files MUST use kebab-case
- Classes MUST use PascalCase
- Constants MUST use UPPER_SNAKE_CASE

← If you want to change these: edit naming-conventions.md → re-derive

<!-- custom -->
## Team Exceptions
- Legacy module `src/old-auth/` exempt from kebab-case (migration planned Q3)
- Test fixtures can use any naming (not production code)

← These survive every re-derivation
<!-- /custom -->
```

---

## Related Documents

| Document | Location |
|----------|----------|
| Pattern: Custom Preservation | `knowledge_docs/PATTERN_CUSTOM_PRESERVATION.md` |
| Pattern: Two-Source Model | `knowledge_docs/PATTERN_TWO_SOURCE_MODEL.md` |
| Pattern: Downstream Signaling | `knowledge_docs/PATTERN_DOWNSTREAM_SIGNALING.md` |
| How Provenance Tracking Works | `knowledge_docs/HOW_PROVENANCE_TRACKING_WORKS.md` |
| How GCE Rederivation Works | `knowledge_docs/HOW_GCE_REDERIVATION_WORKS.md` |
| When to Trigger Re-Derivation | `knowledge_docs/WHEN_TO_TRIGGER_REDERIVATION.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
