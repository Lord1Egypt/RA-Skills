# Pattern: Custom Preservation

**Purpose:** Documents the reusable design pattern where tool-generated files preserve team customizations during re-derivation — using ownership levels and marker comments to separate "safe to overwrite" content from "sacred team edits."

---

## The Pattern

```
ORIGINAL GENERATION
├── Generated content (from steering/AP)
├── <!-- custom -->
├── Team additions (added after generation)
└── <!-- /custom -->

        │
        ▼  (architecture changes → re-derivation triggered)

RE-DERIVATION
├── Generated content ← REGENERATED (updated to match new steering)
├── <!-- custom -->
├── Team additions ← PRESERVED (untouched, verbatim)
└── <!-- /custom -->
```

**One sentence:** Generated content evolves with architecture; team edits survive every regeneration because they're marked and protected.

---

## Where It's Used

| Package | Files With Custom Preservation | What Teams Customize |
|---------|-------------------------------|---------------------|
| **AI-DWG** | `TEAM_AGREEMENTS.md` | Team working norms, meeting schedules, communication preferences |
| **AI-DWG** | `DEFINITION_OF_DONE.md` | Team-specific quality criteria beyond generated ones |
| **AI-DWG** | `.kiro/steering/workspace-rules.md` | Project-specific rules beyond architecture-derived ones |
| **AI-DWG** | `PROJECT_INSTRUCTIONS.md` | Team context, onboarding notes, custom workflows |
| **AI-GCE** | `.governance/COMPLIANCE_README.md` | Team-specific governance notes, override explanations |
| **AI-GCE** | Rule files (`.governance/rules/*.md`) | Team-added verification steps or context |

---

## The Three Ownership Levels

Custom preservation is part of the broader ownership model:

| Level | Marker | Re-Derivation | Custom Preservation? |
|-------|--------|:-------------:|:--------------------:|
| `generated` | `ownership: generated` in front-matter | Full overwrite | ❌ No customs expected |
| `hybrid` | `ownership: hybrid` in front-matter | Merge (regenerate + preserve) | ✅ `<!-- custom -->` blocks preserved |
| `user` | `ownership: user` or no front-matter | Never touched | N/A (entire file is "custom") |

**Custom preservation applies ONLY to `hybrid` ownership files.** Generated files are fully overwritten. User files are never touched.

---

## The Marker Syntax

```markdown
---
generatedBy: AI-DWG
generatedVersion: 1.0.0
source: adlc-output/04_Technology_Stack.md
generatedOn: 2026-06-12
ownership: hybrid
---

# Team Agreements

## Working Hours (Generated)
{Derived from project governance — regenerated on re-derivation}

## Communication Channels (Generated)
{Derived from team structure — regenerated on re-derivation}

<!-- custom -->
## Sprint Ceremonies
- Standup: 9:15 AM daily (15 min max)
- Retro: Every other Friday
- Planning: Monday morning

## Pair Programming Policy
- All security-sensitive code: mandatory pairing
- Everything else: optional but encouraged

## On-Call Rotation
- Week 1: Alice, Bob
- Week 2: Charlie, Diana
<!-- /custom -->
```

**On re-derivation:**
- "Working Hours" section → regenerated from new steering
- "Communication Channels" → regenerated
- Everything between `<!-- custom -->` and `<!-- /custom -->` → preserved verbatim

---

## Why This Pattern Exists

**The problem it solves:** Without custom preservation, teams face a terrible choice:
1. Never re-derive (governance becomes stale when architecture changes)
2. Re-derive and lose all team edits (hours of customization destroyed)

Both options are unacceptable. Custom preservation eliminates the trade-off.

**The anti-pattern it prevents:**
- Teams refusing to allow re-derivation because "it'll delete our stuff"
- Teams making ALL edits in generated sections (overwritten on next re-derive)
- Shadow copies of generated files ("the real team agreements are in Confluence, not here")

---

## Implementation Rules

1. **Markers are literal strings** — `<!-- custom -->` and `<!-- /custom -->` exactly as written. No variations, no extra attributes.

2. **Multiple custom blocks are supported** — a file can have several custom sections between different generated sections.

3. **Empty custom blocks are valid** — `<!-- custom --><!-- /custom -->` means "no team edits yet, but the space is reserved."

4. **Generated content ABOVE first custom block** — the pattern assumes generated content comes first, customs follow. This keeps regeneration simple (replace everything above the marker).

5. **Custom block position is stable** — re-derivation doesn't move the custom block. It stays where the team placed it.

6. **Custom content is never validated** — AI-GCE doesn't check whether custom content conflicts with generated rules. Team authority over their custom sections is absolute.

---

## The Re-Derivation Algorithm

```
For each hybrid file:
  1. Read existing file content
  2. Find <!-- custom --> markers
  3. Extract custom content (everything between markers)
  4. Regenerate the file from new steering/AP
  5. Inject preserved custom content at the same position
  6. Write updated file
  7. Update generatedOn timestamp in front-matter
  8. Log: "Re-derived {file}, custom content preserved ({N} lines)"
```

---

## Edge Cases

| Scenario | Behavior |
|----------|----------|
| File has no custom markers | Treated as fully generated (overwritten completely) |
| File has custom markers but empty content | Markers preserved, empty space maintained |
| Custom content references something generated that changed | Custom content preserved AS-IS (team responsibility to update) |
| File was manually deleted | Re-derivation recreates it (without custom content — it's gone) |
| Custom marker syntax is broken (`<!-- custom` without closing) | File treated as fully generated (preservation skipped, warning logged) |

---

## Communicating to Teams

Teams need to know:
- "Content above `<!-- custom -->` may be regenerated when architecture changes"
- "Content between the markers is YOURS — it will never be touched by automation"
- "Put your additions inside the markers to protect them"
- "If you need to modify generated content, consider whether your change belongs in steering instead (so it persists through re-derivation)"

---

## When to Apply This Pattern

Apply when:
- [ ] A generated file is expected to receive team additions
- [ ] Re-derivation is likely (architecture changes, tier upgrades)
- [ ] Team edits are valuable enough to protect (not just cosmetic)
- [ ] The file has a clear separation between "derived from input" and "added by team"

Don't apply when:
- The file is 100% generated with no expected team edits (`generated` ownership)
- The file is 100% team-owned (`user` ownership — just don't touch it)
- The file is too small for sectioning (single-line configs)
- Custom content would conflict with generated rules (use steering instead)

---

## Related Documents

| Document | Location |
|----------|----------|
| How Provenance Tracking Works | `knowledge_docs/HOW_PROVENANCE_TRACKING_WORKS.md` |
| How GCE Rederivation Works | `knowledge_docs/HOW_GCE_REDERIVATION_WORKS.md` |
| How to Handle Architecture Changes Mid-Project | `knowledge_docs/HOW_TO_HANDLE_ARCHITECTURE_CHANGES_MID_PROJECT.md` |
| How DWG Generation Engine Works | `knowledge_docs/HOW_DWG_GENERATION_ENGINE_WORKS.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
