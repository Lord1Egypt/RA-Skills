<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
package: AI-POLC
version: 1.0.0
status: "{in-progress | ready | operating}"
projectId: "{correlation key from pilc-state.md or user-assigned}"
project-name: "{product/project name}"
---

# AI-POLC State — {Product Name}

## Current State

- Phase: {1-6}
- Stage: {1-16}
- Depth: {minimal | standard | comprehensive}
- Mode: {standalone | chain}
- Tier 2: {active | inactive}
- Active Extensions: [{list or "none"}]

## Context Factors

- Architecture Pattern: {monolith | modular | DDD | microservices | "unknown"}
- Team Topology: {stream-aligned | platform | enabling | complicated-subsystem | "unknown"}
- Delivery Methodology: {Scrum | Kanban | SAFe | Shape Up | Hybrid | "unknown"}
- Scale: {single-team | multi-team | enterprise | "unknown"}
- Product Maturity: {new | growth | mature | sunset | "unknown"}
- Market/User Type: {B2C | B2B | internal | platform | "unknown"}
- Regulatory/Compliance: {none | light | heavy | "unknown"}
- Funding Model: {project | product | capacity | "unknown"}
- Stakeholder Density: {low | medium | high | "unknown"}
- Tech Debt Burden: {low | medium | high | "unknown"}
- Data-Driven Capability: {full | limited | none | "unknown"}
- Release Strategy: {continuous | scheduled | feature-flags | big-bang | "unknown"}
- Outsourcing/Distribution: {co-located | distributed | outsourced | "unknown"}

## Backlog Summary

- Total Epics: {N}
- Prioritized: {N}
- In Release Plan: {N}
- Current Priority Model: {WSJF | MoSCoW | value-effort | custom | "not yet selected"}

## Upstream Reads (last timestamps)

- pilc-state.md: {ISO-date or "not detected"}
- adlc-state.md: {ISO-date or "not detected"}
- uxd-state.md: {ISO-date or "not detected"}
- ilc-state.md: {ISO-date or "not detected"}
- aidlc-docs/: {ISO-date or "not detected"}

## DoR/DoD Version

- DoR: {version or "not defined"}
- DoD: {version or "not defined"}

## Dashboard Summary (machine-readable — AI-DFE reads this)

> A small structured block for the dashboard `po` pane (PO tab). Capture the few facts that are otherwise only in free-form docs. AI-DFE reads this when present and falls back to safe defaults otherwise. Keep it current at Governance/Assembly.

```yaml
dashboard-summary:
  vision:
    status: "{draft | approved}"
    statement: "{one-line product vision}"
  velocity:
    trend: "{stable | up | down}"
  acceptance:
    totalCriteria: {N}
    validated: {N}
```

## Pending Decisions

- {List of decisions awaiting user input, or "none"}

## Last Session Summary

- Date: {ISO-date}
- What was done: {brief summary}
- Next action: {what should happen next}
