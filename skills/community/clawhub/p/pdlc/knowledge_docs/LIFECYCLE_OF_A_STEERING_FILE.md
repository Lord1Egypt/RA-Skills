# Lifecycle of a Steering File

**Purpose:** Traces the complete lifecycle of a steering file from generation through customization, reconciliation, and eventual obsolescence — every state it passes through and who triggers each transition.

---

## The Complete Lifecycle

```
GENERATED ──→ ACTIVE ──→ CUSTOMIZED ──→ ┬── RECONCILED ──→ ACTIVE (updated + customs preserved)
                                          ├── MANUALLY EDITED ──→ re-derive needed
                                          └── OBSOLETE ──→ FLAGGED ──→ REMOVED
```

---

## States

### 1. Generated (Creation)

**Trigger:** AI-DWG runs (Mode 1 or Mode 3) and produces steering files from the Architecture Package.

**What happens:**
- File created in `.kiro/steering/`
- Front-matter set: `generatedBy`, `source`, `generatedOn`, `ownership`
- Content derived from specific AP artifact(s)
- Conditional generation evaluated (file only created if trigger met)
- `<!-- custom -->` markers placed (for hybrid ownership files)

**Ownership assigned:**
- `generated` — fully tool-owned (e.g., internal technical references)
- `hybrid` — tool-seeded, team may customize (e.g., `workspace-rules.md`)

### 2. Active (In Use)

**Trigger:** Immediately after generation — file is loaded into every qualifying session.

**What happens:**
- AI sessions read the file (based on inclusion mode: always/fileMatch/manual)
- AI-GCE derives rules and hooks from it
- Developers experience the constraints it defines
- File is the runtime expression of architecture decisions

**Duration:** Indefinite — until architecture changes, team customizes, or file becomes obsolete.

### 3. Customized (Team Additions)

**Trigger:** Team adds content inside `<!-- custom -->` blocks.

**What happens:**
- Team-specific rules, exceptions, or context added between markers
- File's effective content = generated + custom
- Ownership remains `hybrid` (both parts coexist)
- AI sessions see both generated and custom content

**Key property:** Custom content is sacred — re-derivation preserves it.

### 4. Reconciled (Architecture Changed)

**Trigger:** AI-DWG Mode 2 (Delta Reconciliation) after architecture change.

**What happens:**
- Generated sections regenerated from updated AP/steering source
- Custom sections preserved verbatim (between markers)
- `generatedOn` timestamp updated
- If source AP artifact changed significantly → content changes significantly
- If source AP artifact had minor changes → content changes minimally

**Result:** File returns to Active state with updated generated content + preserved customs.

### 5. Manually Edited (User Changed Generated Sections)

**Trigger:** Developer edits generated sections (outside custom markers).

**What happens:**
- Edit works immediately (AI sees the change)
- BUT: next re-derivation will OVERWRITE the edit (it's in the generated section)
- This is the anti-pattern described in `WHEN_TO_CUSTOMIZE_VS_USE_STEERING.md`

**Correct action:** Move the edit into a custom block, OR change the source (AP/ADR) and re-derive.

### 6. Obsolete (Architecture No Longer Justifies It)

**Trigger:** Architecture change removed the concern this file addresses.
- Multi-tenancy removed from architecture → `multi-tenancy.md` is obsolete
- Microservices extension deactivated → `microservices.md` is obsolete

**What happens:**
- AI-DWG reconciliation flags the file: "source no longer justifies this file"
- File is NOT auto-deleted (non-destructive reconciliation)
- Flagged for human review in reconciliation proposal

### 7. Removed (End of Life)

**Trigger:** Human confirms removal after flagging.

**What happens:**
- File deleted from `.kiro/steering/`
- AI-GCE re-derivation runs → rules derived from this file become `deprecated`
- Hooks referencing this file stop firing
- Compliance log entry: steering file removed

**Cascade:** Removal triggers downstream re-derivation (rules become orphaned → flagged → removed).

---

## Conditional Steering Files (Special Case)

Some steering files have a conditional lifecycle:

```
TRIGGER NOT MET → file never created (doesn't exist)
    │
    ▼ (architecture changes, trigger now met)
TRIGGER MET → file generated (enters lifecycle at "Generated")
    │
    ▼ (architecture changes again, trigger no longer met)
TRIGGER REMOVED → file flagged obsolete
```

**Examples:**
- `multi-tenancy.md`: exists only if AP contains tenancy architecture
- `resilience-standards.md`: exists only if ≥3 integrations or Resilience extension
- `event-sourcing.md`: exists only if Event Sourcing extension active

---

## Typical Lifecycle Durations

| Steering File | Typical Lifecycle |
|--------------|-------------------|
| `workspace-rules.md` | Generated → Customized → Reconciled (many times) → never obsolete |
| `tech-stack.md` | Generated → Active → Reconciled (on tech changes) → rarely obsolete |
| `multi-tenancy.md` | Not generated → Generated (if tenancy added) → Active → Obsolete (if tenancy removed) |
| `api-standards.md` | Generated → Customized → Reconciled frequently → Active indefinitely |

---

## Related Documents

| Document | Location |
|----------|----------|
| How Steering File Loading Works | `knowledge_docs/HOW_STEERING_FILE_LOADING_WORKS.md` |
| Anatomy of a Steering File | `knowledge_docs/ANATOMY_OF_A_STEERING_FILE.md` |
| Pattern: Custom Preservation | `knowledge_docs/PATTERN_CUSTOM_PRESERVATION.md` |
| Pattern: Conditional Generation | `knowledge_docs/PATTERN_CONDITIONAL_GENERATION.md` |
| Pattern: Non-Destructive Reconciliation | `knowledge_docs/PATTERN_NON_DESTRUCTIVE_RECONCILIATION.md` |
| When to Customize vs Use Steering | `knowledge_docs/WHEN_TO_CUSTOMIZE_VS_USE_STEERING.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
