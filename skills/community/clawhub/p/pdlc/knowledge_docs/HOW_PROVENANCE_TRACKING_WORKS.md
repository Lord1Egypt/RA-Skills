# How Provenance Tracking Works

**Purpose:** Explains how the AI-* Family tracks the origin and ownership of every generated artifact — the front-matter schema, ownership levels, and how provenance enables safe re-derivation without destroying team customizations.

---

## What Provenance Tracking Is

Provenance tracking means every generated file carries metadata declaring: who generated it, what source produced it, when it was generated, and what ownership level it has. This metadata enables re-derivation (knowing what's safe to overwrite) and audit (knowing where every artifact came from).

```yaml
---
generatedBy: AI-DWG
generatedVersion: 1.0.0
source: adlc-output/04_Technology_Stack.md
generatedOn: 2026-06-12
ownership: hybrid
---
```

---

## The Provenance Schema

Every generated `.md` artifact carries a YAML front-matter block:

| Field | Purpose | Example |
|-------|---------|---------|
| `generatedBy` | Which package produced this file | `AI-DWG`, `AI-GCE`, `AI-TGE` |
| `generatedVersion` | Version of the generating package | `1.0.0` |
| `source` | Which upstream document triggered generation | `adlc-output/07_API_Architecture.md` |
| `generatedOn` | ISO date of generation | `2026-06-12` |
| `ownership` | Who controls this file's content (see below) | `generated`, `hybrid`, `user` |

For hooks (`.json` files):
```json
{
  "generatedBy": "AI-GCE",
  "generatedVersion": "1.0.0",
  "source": ".kiro/steering/api-standards.md"
}
```

---

## Ownership Levels

The `ownership` field determines what happens during re-derivation:

| Level | Meaning | Re-Derivation Behavior |
|-------|---------|------------------------|
| `generated` | Fully tool-owned; no team edits expected | **Overwritten** — regenerated from source |
| `hybrid` | Tool-seeded, team customized | **Merge** — generated parts updated, `<!-- custom -->` blocks preserved |
| `user` | Team-owned; tool doesn't touch | **Never touched** — completely excluded from re-derivation |

### Ownership: `generated`

Files that are 100% derived from upstream sources. No team edits expected or preserved.

**Examples:**
- `.governance/rules/ARCH-01_module-boundaries.md` (derived from steering)
- `.compliance-state.json` (computed by AI-GCE)
- Hook files in `.kiro/hooks/` (derived from steering)

**Re-derivation:** Full overwrite. If steering changes, the file is regenerated completely.

### Ownership: `hybrid`

Files that AI seeds with generated content but the team is expected to customize:

**Examples:**
- `TEAM_AGREEMENTS.md` (AI generates from architecture, team adds working norms)
- `DEFINITION_OF_DONE.md` (AI generates from quality plan, team refines)
- `.kiro/steering/workspace-rules.md` (AI generates, team adds project-specific sections)

**The `<!-- custom -->` preservation pattern:**
```markdown
## Generated Section (ownership: generated portion)
{This content will be regenerated on re-derivation}

<!-- custom -->
## Team Additions
{Everything below this marker is PRESERVED during re-derivation}
{Team edits here are sacred — never overwritten}
<!-- /custom -->
```

**Re-derivation:** Content ABOVE `<!-- custom -->` is regenerated. Content BETWEEN the markers is preserved verbatim.

### Ownership: `user`

Files the team fully owns. AI-* packages never modify them after initial creation (or don't create them at all).

**Examples:**
- Source code files
- Team-authored documentation
- Custom configuration that the team manages
- Files created manually (no provenance front-matter)

**Re-derivation:** Skipped entirely. These files are invisible to the re-derivation process.

---

## How Provenance Enables Re-Derivation

When architecture changes and AI-DWG/AI-GCE re-derive:

```
1. Read all files in governance/steering folders
2. For each file:
   a. Has provenance front-matter? → Check ownership
   b. No front-matter? → Treat as user-owned (never touch)
   c. ownership: generated → Safe to overwrite
   d. ownership: hybrid → Update generated parts, preserve custom
   e. ownership: user → Skip entirely
3. Generate new/updated files
4. Update generatedOn timestamp
5. Log changes in compliance log
```

**Without provenance:** Re-derivation would be dangerous — no way to know which files are safe to overwrite vs. which contain team edits. Provenance makes re-derivation safe and surgical.

---

## Provenance Across the Chain

Each package generates files with its own provenance:

| Package | Files It Generates | Typical Ownership |
|---------|-------------------|:-----------------:|
| **AI-DWG** | Steering files, PROJECT_INSTRUCTIONS, DoD, TEAM_AGREEMENTS | Mix of `generated` and `hybrid` |
| **AI-GCE** | Rules, hooks, agents, compliance-state | Mostly `generated` |
| **AI-TGE** | Test strategy, register, coverage reports | Mostly `generated` |
| **AI-PILC** | PIP artifacts (requirements, charter, etc.) | `hybrid` (team refines) |
| **AI-ADLC** | AP artifacts (architecture docs, ADRs) | `hybrid` (team refines) |

---

## Source Tracing

The `source` field creates a derivation chain:

```
Source: adlc-output/07_API_Architecture.md
    ↓ (AI-DWG reads this)
Generated: .kiro/steering/api-standards.md
    ↓ (AI-GCE reads this)
Generated: .governance/rules/API-01_contract-first.md
    ↓ (AI-GCE derives hook)
Generated: .kiro/hooks/api-contract-check.json
```

For any enforcement hook, you can trace back: "Why does this hook exist?" → because of this rule → because of this steering file → because of this architecture decision. Full traceability from enforcement to intent.

---

## Audit Value

Provenance provides certification evidence:

| Auditor Question | Provenance Answers |
|-----------------|--------------------|
| "Where did this rule come from?" | `source` field traces to architecture decision |
| "When was this last reviewed?" | `generatedOn` + re-derivation log entries |
| "Who controls this file?" | `ownership` field declares responsibility |
| "Has this been tampered with?" | `generated` files match their source — discrepancy = drift |
| "Is enforcement current?" | `generatedVersion` matches installed package version |

---

## Related Documents

| Document | Location |
|----------|----------|
| How GCE Rederivation Works | `knowledge_docs/HOW_GCE_REDERIVATION_WORKS.md` |
| How DWG Generation Engine Works | `knowledge_docs/HOW_DWG_GENERATION_ENGINE_WORKS.md` |
| How to Handle Architecture Changes Mid-Project | `knowledge_docs/HOW_TO_HANDLE_ARCHITECTURE_CHANGES_MID_PROJECT.md` |
| Naming and Ownership Convention | `contracts/NAMING_AND_OWNERSHIP.md` |
| How GCE Compliance Audit Works | `knowledge_docs/HOW_GCE_COMPLIANCE_AUDIT_WORKS.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
