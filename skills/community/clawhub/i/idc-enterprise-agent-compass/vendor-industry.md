> **Copyright (c) 2026 IDC. All Rights Reserved. Licensed under CC-BY-SA-4.0.** See `IDCcopyright.md` for details.

# Human-Agent Boundary — Complete Checklist

Three-category work division between Agents and humans. Use this reference during Step 7 to define clear boundaries.

---

## Category 1: Suitable for Agent Analysis and Reasoning

Agents excel at processing large volumes of information, identifying patterns, and generating options. These tasks benefit from Agent involvement in the thinking/analysis phase.

- Understanding unstructured inputs: emails, chat messages, attachments, voice transcripts
- Processing vague expressions and implicit intent
- Generating natural language explanations, summaries, and candidate options
- Making preliminary judgments when rules are incomplete
- Identifying anomalies and exceptional cases
- Planning task steps and execution paths
- Handling time-sensitive analysis with complex data dimensions:
  - Multi-supplier price comparison
  - Dynamic inventory allocation
  - Customer credit risk assessment
- Pattern recognition and trend analysis on unstructured data
- Assisting employees with document creation:
  - Writing proposals, reports, and standard documents
  - Pulling data and materials from multiple systems
  - Generating first drafts
- Collaborative document editing:
  - Merging different versions
  - Consolidating review comments
  - Unifying formatting

---

## Category 2: Suitable for Agent Execution via Tools/Systems

These are deterministic or semi-deterministic operations where Agents can reliably execute through tool calls, API invocations, or system integrations.

- Data validation and format checking
- Amount calculation and price matching
- Inventory query and availability confirmation
- Statistical analysis and report generation on structured data
- Permission verification and compliance checking
- Fixed-format system writes
- Status updates and notification distribution
- High-frequency stable batch operations
- Audit log recording
- Risk scoring and credit calculation based on deterministic rules

---

## Category 3: Must Remain with Humans

These tasks require human judgment, accountability, ethical consideration, or relationship management. They should NEVER be fully delegated to Agents.

- **Exception approval and risk backstop** — When scenarios fall outside defined rules, a human must decide
- **Ambiguous responsibility judgment** — When accountability is unclear, human arbitration is required
- **Major customer communication and relationship maintenance** — Trust-building cannot be delegated
- **Policy and ethical decisions** — Regulatory, compliance, and moral judgments require human ownership
- **Final confirmation of Agent output** — Especially during the trust-building phase of Agent adoption
- **Cross-department political and negotiation decisions** — Organizational dynamics require human nuance

---

## Boundary Definition Template

When defining boundaries for a specific scenario, use this structure:

```
Scenario: [Scenario Name]
═══════════════════════════════════════════════

Agent Analyzes:
  - [Specific analysis tasks for this scenario]
  - [Specific pattern recognition tasks]

Agent Executes:
  - [Specific system operations]
  - [Specific tool invocations]
  - [Specific automated actions]

Human Decides:
  - [Specific approval gates]
  - [Specific exception handling]
  - [Specific relationship/communication tasks]

Escalation Rules:
  - When [condition], escalate to [role]
  - When [condition], require human confirmation before Agent proceeds
  - When [condition], pause and notify [role]
```

---

## Implementation Guidance

### Trust-Building Phase (Initial 1-3 months)
- Human confirms ALL Agent decisions before execution
- Agent operates in "recommend only" mode for high-impact decisions
- Broad escalation rules; err on the side of human involvement

### Expansion Phase (3-6 months)
- Human confirms only exception cases and high-impact decisions
- Agent operates in "auto-execute with notification" mode for routine tasks
- Narrow escalation rules based on accumulated trust data

### Maturity Phase (6+ months)
- Human confirms only explicitly defined exception categories
- Agent operates autonomously within defined boundaries
- Continuous monitoring of Agent performance with periodic human audit

### Non-Negotiable (All Phases)
- Exception approval ALWAYS requires human involvement
- Policy and ethical decisions ALWAYS require human involvement
- Major customer relationship decisions ALWAYS require human involvement
- Audit trail of all Agent actions must be reviewable by humans at any time
