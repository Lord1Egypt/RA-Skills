<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-UXD
generatedVersion: "{version}"
source: "{upstream-doc-path}"
generatedOn: "{ISO-date}"
ownership: hybrid
---

# Flow: {Task/Goal Name}

## Metadata

| Field | Value |
|-------|-------|
| Persona | {owning persona} |
| Journey | {source journey + stage reference} |
| Type | {Task Flow / User Flow / Wireflow} |
| Entry Point | {where/how user enters this flow} |
| Success Exit | {what "done" looks like} |
| Failure Exit | {what failure leads to} |
| Estimated Steps | {N} |
| Frequency | {how often this flow is executed} |

---

## Preconditions

- {What must be true before this flow starts}
- {Authentication state required}
- {Data that must exist}
- {Permissions needed}

---

## Happy Path

| Step | User Action | System Response | Screen | Component | Notes |
|:----:|-------------|-----------------|--------|-----------|-------|
| 1 | {action} | {response} | {screen name} | {key component} | {notes} |
| 2 | {action} | {response} | {screen} | {component} | {notes} |
| 3 | {action} | {response} | {screen} | {component} | {notes} |
| 4 | {action} | {response} | {screen} | {component} | {notes} |
| ✓ | — | {success confirmation} | {final screen} | {Toast/Modal} | Flow complete |

---

## Decision Points

| At Step | Question | Option A | Option B |
|:-------:|----------|----------|----------|
| {#} | {what user decides} | → Step {N}: {path A} | → Step {M}: {path B} |
| {#} | {decision} | → {path} | → {path} |

---

## Error Paths

| At Step | Error Condition | User Sees | Recovery Action |
|:-------:|-----------------|-----------|-----------------|
| {#} | {what goes wrong} | {error message/state} | {how to fix + where it returns to} |
| {#} | {error} | {message} | {recovery} |

---

## Edge Cases

| Condition | Behavior | Affected Steps |
|-----------|----------|:-------------:|
| Empty state (no data) | {what user sees + how to populate} | {steps} |
| First-time use | {onboarding hint / guided setup} | {steps} |
| Bulk operation | {how the flow adapts for many items} | {steps} |
| Interrupted (user leaves mid-flow) | {state preserved? resume point?} | {steps} |
| Concurrent modification | {conflict handling} | {steps} |
| Offline / connectivity loss | {behavior + recovery} | {steps} |

---

## State Changes

| Before Flow | After Flow (Success) | After Flow (Failure) |
|-------------|---------------------|---------------------|
| {system/data state} | {new state} | {state on failure — rolled back?} |

---

## Flow Diagram

<!-- Dashboard contract: DFE extracts the content between ```mermaid and ``` fences.
     The dashboard renders it via mermaid.js. Use `graph TD` or `flowchart TD` (both supported).
     Do NOT nest additional code fences inside. Keep to a single mermaid block per flow file. -->

```mermaid
flowchart TD
    A([Start: {entry point}]) --> B[{Step 1 action}]
    B --> C[{Step 2 action}]
    C --> D{Decision?}
    D -->|Yes| E[{Path A}]
    D -->|No| F[{Path B}]
    E --> G([Success])
    F --> H[{Alternative step}]
    H --> G
    C -->|Error| I[Error State]
    I --> J[Recovery]
    J --> C
```

---

## Traceability

| Artifact | Reference |
|----------|-----------|
| Persona | {persona doc link} |
| Journey | {journey doc} → Stage {#} |
| Screens touched | {Screen_01, Screen_02, ...} |
| Components used | {Button, Form Field, Modal, Toast, ...} |
| Tokens relevant | {any tokens specifically critical to this flow} |
