<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-UXD
generatedVersion: "{version}"
source: "{upstream-doc-path}"
generatedOn: "{ISO-date}"
ownership: hybrid
---

# Wireframe: {Screen Name}

## Metadata

| Field | Value |
|-------|-------|
| Template Type | {Dashboard / List / Detail / Form / Wizard / Modal / Empty} |
| Primary Flow | {flow that owns this screen} |
| Persona | {primary user of this screen} |
| Entry Points | {how user arrives — nav, flow step, link} |
| Exit Points | {where user goes from here} |
| Prototype Link | {external Figma/tool link, if available} |

---

## Layout Zones

```
┌─────────────────────────────────────────────────┐
│ HEADER                                           │
│ {global nav + utilities}                         │
├──────────┬──────────────────────────────────────┤
│ SIDEBAR  │ MAIN CONTENT                          │
│          │                                       │
│ {local   │  ┌───────────────────────────────┐   │
│  nav or  │  │ Zone A: {primary content}     │   │
│  filters}│  └───────────────────────────────┘   │
│          │  ┌───────────────────────────────┐   │
│          │  │ Zone B: {secondary content}   │   │
│          │  └───────────────────────────────┘   │
│          │  ┌─────────────┐ ┌───────────────┐   │
│          │  │ Zone C      │ │ Zone D        │   │
│          │  └─────────────┘ └───────────────┘   │
├──────────┴──────────────────────────────────────┤
│ FOOTER {if applicable}                           │
└─────────────────────────────────────────────────┘
```

---

## Content Priority

| Priority | Content | Zone | Component |
|:--------:|---------|------|-----------|
| 1 | {primary — what user came for} | {zone} | {component type} |
| 2 | {primary action} | {zone} | {component} |
| 3 | {supporting context} | {zone} | {component} |
| 4 | {secondary content} | {zone} | {component} |
| 5 | {tertiary / navigation} | {zone} | {component} |

---

## Interactive Elements

| Element | Component | Action on Interaction | Target |
|---------|-----------|---------------------|--------|
| {labeled element} | {component type + variant} | {what happens} | {where it leads} |
| {element} | {component} | {action} | {target} |
| {element} | {component} | {action} | {target} |

---

## Screen States

| State | Trigger | Visual Difference | Content Shown |
|-------|---------|-------------------|---------------|
| Default (loaded) | Data available | Full content | All zones populated |
| Empty | No data yet | {empty state illustration + message + CTA} | Guidance to populate |
| Loading | Data fetching | {skeleton screens in content zones} | Structure without data |
| Error | Load failure | {error message + retry action} | Explanation + recovery |
| Partial | Some data unavailable | {available data + placeholder for missing} | Mixed |

---

## Responsive Behavior

| Breakpoint | Layout Change | What Happens to Zones |
|------------|---------------|-----------------------|
| Desktop (>1024px) | Full layout as drawn | All zones visible, sidebar expanded |
| Tablet (640-1024px) | {adaptation} | {sidebar collapses? columns reduce?} |
| Mobile (<640px) | {adaptation} | {single column? drawer nav? zones stack?} |

---

## Annotations

| # | Area | Note |
|---|------|------|
| 1 | {zone/element} | {design rationale or behavior note} |
| 2 | {zone/element} | {note} |
| 3 | {zone/element} | {note} |

---

## Traceability

| Artifact | Reference |
|----------|-----------|
| Flow | {flow doc that contains this screen} |
| Journey Stage | {journey → stage this screen serves} |
| Components used | {list of components from Component Library} |
| Template shared with | {other screens using same template layout} |
