<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-UXD
generatedVersion: "{version}"
source: "{upstream-doc-path}"
generatedOn: "{ISO-date}"
ownership: hybrid
---

# Information Architecture

## Organization System

| Section | Scheme | Rationale |
|---------|--------|-----------|
| {main area} | {Topic / Task / Audience / Hybrid} | {why this organization} |
| {area 2} | {scheme} | {rationale} |
| {area 3} | {scheme} | {rationale} |

---

## Site Map

```
├── {L1: Section}
│   ├── {L2: Sub-section}
│   │   ├── {L3: Page/Feature}
│   │   └── {L3: Page/Feature}
│   └── {L2: Sub-section}
├── {L1: Section}
│   ├── {L2: Sub-section}
│   └── {L2: Sub-section}
├── {L1: Section}
└── {L1: Utility}
    ├── {L2: Settings}
    ├── {L2: Help}
    └── {L2: Account}
```

---

## Navigation Model

| Type | Content | Behavior | Mobile Adaptation |
|------|---------|----------|-------------------|
| **Global** | {items} | Persistent, always visible | {drawer / bottom bar / hamburger} |
| **Local** | {items} | Changes per section | {tabs / nested menu} |
| **Contextual** | {items} | Inline, context-sensitive | {same / collapsed} |
| **Utility** | {items} | Secondary (top-right / footer) | {avatar menu / drawer section} |
| **Breadcrumb** | Auto-generated path | Shows hierarchy location | {hidden / simplified} |
| **Search** | {scope} | {global / section-scoped} | {icon → expand} |

---

## Labeling System

### Navigation Labels

| Location | Label | Meaning | Alternatives Rejected |
|----------|-------|---------|----------------------|
| Global nav | {label} | {what it contains} | {rejected + why} |
| Global nav | {label} | {what it contains} | {rejected + why} |
| Utility | {label} | {what it contains} | {rejected + why} |

### Terminology Glossary

| Term | Definition | Where Used |
|------|-----------|-----------|
| {product-specific term} | {plain definition} | {UI locations} |
| {term} | {definition} | {locations} |
| {term} | {definition} | {locations} |

### Labeling Rules

1. Actions use verbs: "Create Report" not "Report Creation"
2. Navigation uses nouns: "Reports" not "View Reports"
3. Collections are plural: "Projects" not "Project"
4. Items are singular: "Project Details" not "Projects Details"
5. {Project-specific rule}
6. {Project-specific rule}

---

## Search Strategy

| Aspect | Decision |
|--------|----------|
| Scope | {Global / Section-scoped / Both with toggle} |
| Auto-suggest | {Yes / No — with rationale} |
| Filters available | {list} |
| Result grouping | {by type / by section / flat} |
| Empty state | {message + suggestions} |
| Minimum query length | {N characters} |

---

## Persona Validation

| Persona | Top Goal | Path Through IA | Steps | Friction? |
|---------|----------|-----------------|:-----:|-----------|
| {persona 1} | {goal} | {Nav > Section > Page} | {N} | {none / description} |
| {persona 2} | {goal} | {path} | {N} | {friction if any} |
| {persona 3} | {goal} | {path} | {N} | {friction if any} |

### Friction Resolution

| Persona | Friction | Resolution |
|---------|----------|-----------|
| {name} | {>3 steps / confusing label / buried deep} | {shortcut / dashboard widget / contextual link} |

---

## Cross-References

| Artifact | Connection |
|----------|-----------|
| Personas | IA validated against all primary persona goals |
| Journeys | Journey stages map to IA sections |
| Flows (Stage 6) | Flows navigate through this IA structure |
| Navigation components (Stage 9) | Component specs implement this nav model |
