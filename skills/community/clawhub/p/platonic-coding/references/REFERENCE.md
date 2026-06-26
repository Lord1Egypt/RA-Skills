# Platonic Coding — Complete Reference

Detailed operation guide for Platonic Coding skill.

## Operations (23 total)

### INITIALIZATION (`references/INIT/`)
| Operation | Purpose |
|-----------|---------|
| `init-scaffold` | Create directories, config, templates |
| `init-scan` | Analyze existing codebase |
| `init-plan-modular-specs` | Propose RFC dependency graph |
| `init-recover-conceptual` | Generate conceptual RFC from code |
| `init-recover-architecture` | Generate architecture RFCs from code |
| `init-recover-impl-interface` | Generate impl interface RFCs (optional) |

### SPECIFICATION (`references/SPECS/`)
| Operation | Purpose |
|-----------|---------|
| `specs-refine` | Comprehensive validation + update |
| `specs-generate-history` | Update change history |
| `specs-generate-index` | Update RFC index |
| `specs-generate-namings` | Update terminology reference |
| `specs-validate-consistency` | Check cross-references |
| `specs-check-taxonomy` | Verify terminology usage |
| `specs-check-compliance` | Validate against RFC standard |

### IMPLEMENTATION (`references/IMPL/`)
| Operation | Purpose |
|-----------|---------|
| `impl-full` | End-to-end: spec → guide → plan → code + tests |
| `impl-create-guide` | Create guide from RFC |
| `impl-code` | Implement from existing guide |
| `impl-validate-guide` | Check guide vs RFC contradictions |
| `impl-update-guide` | Sync guide with RFC changes |

### REVIEW (`references/REVIEW/`)
| Operation | Purpose |
|-----------|---------|
| `review` | Spec compliance review (6-step, report-only) |

### WORKFLOW (`references/WORKFLOW/`)
| Phase | Activities |
|-------|------------|
| 1 | Optional brainstorming → draft → RFC → `specs-refine` |
| 2 | Optional brainstorming → `impl-full` |
| 3 | `review` → compliance report |

---

## Auto-Detection Decision Tree

```
No .platonic.yml?
  → Has code? → recovery flow (init-scan → recover)
  → No code? → init-scaffold

Has specs but no RFCs?
  → Has drafts? → Phase 1 (draft → RFC)
  → No drafts? → Phase 1 (start fresh, optional brainstorming)

Has RFCs but no guides?
  → Phase 2 (impl-full or impl-create-guide)

Has RFCs + guides?
  → In progress? → resume Phase 2
  → Complete? → Phase 3 (review)

Ambiguous? → Ask or resume current phase
```

**Override**: Use canonical operations (`init-scaffold`, `specs-refine`, `impl-full`, `review`, `workflow --phase <N>`).

---

## Template Variables

Templates use `{{PLACEHOLDER}}` syntax. Common variables:

### Project-Level
- `{{PROJECT_NAME}}` — Project name
- `{{LANGUAGE}}` — Programming language
- `{{FRAMEWORK}}` — Framework or stack

### RFC-Level
- `{{RFC_NUMBER}}` — RFC identifier (e.g., "001")
- `{{RFC_TITLE}}` — RFC title
- `{{RFC_STATUS}}` — Status (Draft, Active, Deprecated, Superseded)
- `{{RFC_KIND}}` — Kind (Conceptual Design, Architecture Design, Impl Interface Design)
- `{{DATE}}` — Current date
- `{{AUTHOR}}` — Author name

### Paths
- `{{SPECS_PATH}}` — Specs directory path (from `.platonic.yml`)
- `{{IMPL_PATH}}` — Implementation guides path
- `{{DRAFTS_PATH}}` — Design drafts path

---

## File Structure

```
<project-root>/
├── .platonic.yml                   # Project config
├── docs/
│   ├── specs/                      # RFC specifications
│   │   ├── rfc-standard.md          # RFC process & conventions
│   │   ├── rfc-history.md           # Change history
│   │   ├── rfc-index.md             # Spec index
│   │   ├── rfc-namings.md           # Terminology reference
│   │   ├── RFC-001-world-view.md   # Individual RFC
│   │   ├── RFC-002-message-queue.md
│   │   └── templates/               # Templates for future RFCs
│   │       ├── rfc-template.md
│   │       ├── conceptual-design.md
│   │       ├── architecture-design.md
│   │       └── impl-interface-design.md
│   │
│   ├── impl/                       # Implementation guides
│   │   ├── README.md
│   │   ├── IG-001-user-authentication.md         # Impl guide for RFC-001-user-auth
│   │   └── IG-002-data-storage.md                # Impl guide for RFC-002-data-storage
│   │
│   └── drafts/                     # Phase 1 design drafts
│       ├── README.md
│       └── user-auth-design.md
│
└── <source-code>/                  # Your implementation
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Wrong auto-detection | Use explicit operations (`init-scaffold`, `specs-refine`, `impl-full`, `review`) |
| Wrong placeholders | Check `.platonic.yml` paths match template values |
| Guide contradicts RFC | Run `impl-validate-guide`, then update guide or modify RFC |
| Specs not in index | Check `RFC-NNN-<name>.md` naming, run `specs-generate-index` |
| Missing terminology | Check term format in RFCs, run `specs-generate-namings` |
| Missing code refs in review | Use specific search terms, check naming conventions |
| Workflow stops at gate | Expected—say "no confirmations" to skip |

---

## Reference Files

- `references/INIT/` — Initialization
- `references/SPECS/` — Specification management
- `references/IMPL/` — Implementation
- `references/REVIEW/` — Review
- `references/WORKFLOW/` — Workflow orchestration