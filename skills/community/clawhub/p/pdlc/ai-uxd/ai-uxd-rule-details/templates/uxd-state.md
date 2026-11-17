<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
package: AI-UXD
version: 1.0.0
projectId: "{correlation key PRJ-{ABBREV}-{YYYY}-{NNN} — adopted from pilc-state.md/polc-state.md, or minted if UXD originates}"
projectHandle: "PRJ-{ABBREV}"
projectRoot: "pdlc-ws/projects/PRJ-{ABBREV}-{slug}/"
outputRoot: "pdlc-ws/projects/PRJ-{ABBREV}-{slug}/ux/"
created: "{ISO-date}"
last_updated: "{ISO-date}"
---

# AI-UXD — Workflow State

## Workflow State

| Field | Value |
|-------|-------|
| Mode | {A / B / C / D} |
| Depth | {Minimal / Standard / Comprehensive} |
| Current Phase | {Discover / Define / Design / Validate / Assemble} |
| Current Stage | {1-16} |
| Status | {In Progress / Complete} |

---

## Progress

| # | Stage | Status | Completed | Artifacts Produced |
|---|-------|:------:|:---------:|-------------------|
| 1 | Workspace Detection | 🔄 Active | — | uxd-state.md |
| 2 | Research Planning | ⏳ Pending | — | |
| 3 | Persona Definition | ⏳ Pending | — | |
| 4 | Journey Mapping | ⏳ Pending | — | |
| 5 | Information Architecture | ⏳ Pending | — | |
| 6 | User Flow Design | ⏳ Pending | — | |
| 7 | Wireframe & Screen Inventory | ⏳ Pending | — | |
| 8 | Design System Foundation | ⏳ Pending | — | |
| 9 | Component Library | ⏳ Pending | — | |
| 10 | Multi-Brand Theming | ⏳ Pending | — | Conditional |
| 11 | Accessibility Baseline | ⏳ Pending | — | |
| 12 | Usability Validation | ⏳ Pending | — | |
| 13 | Design QA Framework | ⏳ Pending | — | |
| 14 | AI-POLC Handoff | ⏳ Pending | — | |
| 15 | AI-DWG/GCE Handoff | ⏳ Pending | — | |
| 16 | Package Assembly | ⏳ Pending | — | |

---

## Conditional Features

| Feature | Active | Trigger |
|---------|:------:|---------|
| Multi-Brand Theming | {Yes / No} | {>1 brand / color modes / "not triggered"} |
| i18n/RTL | {Yes / No} | {>1 locale / "single locale"} |
| Service Blueprints | {Yes / No} | {Comprehensive + service / "not triggered"} |
| Empathy Maps | {Yes / No} | {Comprehensive / "not Comprehensive"} |

---

## Downstream Signals

| Consumer | Artifact | Status | Path |
|----------|----------|--------|------|
| AI-POLC | Personas + Journeys | {Pending / Handed Off} | {path} |
| AI-DWG | Design System + Tokens | {Pending / Handed Off} | {path} |
| AI-GCE | Accessibility Baseline | {Pending / Handed Off} | {path} |

---

## Key Metrics

| Metric | Value |
|--------|:-----:|
| Personas | {N} |
| Journeys | {N} |
| Flows | {N} |
| Screens | {N} |
| Components | {N} |
| Design Tokens | {N} |
| WCAG Target | Level {AA/AAA} |

---

## Dashboard Summary (machine-readable — AI-DFE reads this)

> Roll-up counts for the dashboard `ux` pane (UX tab). AI-DFE reads this when present and falls back to scanning/zeros otherwise. Keep current at Design/Validate/Assemble.

```yaml
dashboard-summary:
  designSystem:
    tokens:     { total: {N}, defined: {N} }
    components: { total: {N}, specified: {N} }
  wireframes:   { total: {N}, approved: {N}, inReview: {N}, pending: {N} }
  componentLibrary: { total: {N}, atoms: {N}, molecules: {N}, organisms: {N} }
  informationArchitecture: { status: "{in-progress | complete}", pages: {N} }
  accessibility: { wcagLevel: "{AA | AAA}", criteria: {N}, met: {N}, baselineDefined: {true|false} }
```

---

## Enabled Extensions (for downstream detection)

| Extension | Status |
|-----------|--------|
| Multi-Brand Theming | {Active / Inactive} |
| i18n/RTL | {Active / Inactive} |

---

## Input Sources

| Source | Path | Mode |
|--------|------|------|
| PIP | {path to pilc-state.md} | {A/B} |
| PBP | {path to polc-state.md} | {A only} |
| AP | {path to adlc-state.md} | {if present — adaptive constraint read} |
| Brief | {path or "verbal"} | {C} |
| Existing Design | {path} | {D} |

---

## Upstream Signals (same-layer peer reads — for re-entry detection)

| Peer | Signal | Last Seen | Notes |
|------|--------|-----------|-------|
| AI-POLC (`polc-state.md`) | Value goals / OKRs (focus research — OI-096) | {timestamp or "none"} | {value-goal summary used to focus research, or "absent"} |
| AI-ADLC (`adlc-state.md`) | `lastApStateSeen` — architecture constraints (Architecture→UX loop — OI-099) | {timestamp/hash or "none"} | On change after flows exist → trigger non-destructive constraint re-entry review |

> These track what each concurrent peer had produced when UXD last read it, so a later change (e.g., a late AP latency/data constraint, or updated POLC value goals) can be detected and reconciled. Absence never blocks.
