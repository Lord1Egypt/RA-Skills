> **Copyright (c) 2026 IDC. All Rights Reserved. Licensed under CC-BY-SA-4.0.** See `IDCcopyright.md` for details.

# System Readiness Check — Detailed Framework

Four evaluation dimensions for assessing how well existing business systems support Agent-oriented operations. Use this reference during Step 5.

---

## Overview

Existing core systems (ERP, CRM, OA, MES, etc.) don't need to be replaced, but their service orientation must expand from "human-facing" to "human + Agent-facing." This assessment identifies what foundational capabilities need to be added.

---

## Dimension 1: Interface Capability (接口能力)

**What to evaluate:** Whether MCP, API, event stream, and other integration mechanisms cover core business actions — not just reading data, but also initiating execution.

**Assessment criteria:**

| Level | Criteria |
|-------|----------|
| **Ready** | Core business actions (create order, update inventory, approve request, etc.) are accessible via well-documented APIs or event streams. Both read and write operations are supported. Rate limits and error handling are defined. |
| **Partial** | Some core actions have APIs, but coverage is incomplete. Key processes still require manual UI interaction. API documentation may be outdated or inconsistent. |
| **To-Build** | Most business actions are only accessible through the UI. No API layer exists. System-to-system integration relies on file exports/imports or manual data entry. |

**Key questions to ask the user:**
- "Can your core systems be accessed programmatically today?"
- "If an Agent needed to create an order in your ERP, could it do so via API, or would someone need to do it manually?"
- "Do you have documentation for the available interfaces?"

**Implications for Agent scenarios:**
- Orchestration scenarios require **Ready** or at minimum **Partial** interface capability
- Perception scenarios are less dependent on system interfaces (input-side focus)
- Collaboration scenarios need at minimum read APIs for status aggregation

---

## Dimension 2: Permission Model (权限模型)

**What to evaluate:** Whether the permission system has provisions for Agent identities — what identity Agents access under, what actions they can perform, which actions require human confirmation.

**Assessment criteria:**

| Level | Criteria |
|-------|----------|
| **Ready** | Dedicated service accounts or API identities exist for automated processes. Role-based access control (RBAC) defines what automated agents can and cannot do. Approval workflows can distinguish between human-initiated and Agent-initiated actions. |
| **Partial** | Service accounts exist but were not designed with Agent use in mind. No clear separation between human and Agent permissions. Approval workflows treat all actions the same regardless of initiator. |
| **To-Build** | All access is tied to individual user accounts. No concept of service accounts or automated process identities. No way to audit or control what an Agent might do if granted access. |

**Key questions to ask the user:**
- "Do your systems have service accounts or API-specific identities?"
- "Is there a way to limit what an automated process can do, separate from what a human user can do?"
- "Can your approval workflows distinguish between human and automated initiators?"

**Implications for Agent scenarios:**
- **Critical** for any scenario involving system writes (Orchestration, Monitoring response)
- Less critical for read-only scenarios (Analysis, Perception)
- Human-Agent boundary enforcement depends on this capability

---

## Dimension 3: Operation Traceability (操作留痕)

**What to evaluate:** Whether every Agent action — API call, judgment basis, execution result — can be traced to satisfy audit requirements and enable retrospective analysis.

**Assessment criteria:**

| Level | Criteria |
|-------|----------|
| **Ready** | Comprehensive audit logging exists for all system actions. Logs capture who/what initiated the action, when, with what parameters, and what the outcome was. Log retention policies meet regulatory requirements. |
| **Partial** | Audit logs exist but may not capture all relevant context (e.g., missing input parameters or decision rationale). Log format may be inconsistent across systems. Retention policies may be undefined. |
| **To-Build** | No systematic audit logging. Actions are logged at application level only, if at all. No way to reconstruct what happened in a process after the fact. |

**Key questions to ask the user:**
- "Can you trace back through a process and see every action that was taken, by whom or what, and why?"
- "Do your systems have audit logs that capture the full context of each action?"
- "How long are logs retained, and do they meet your compliance requirements?"

**Implications for Agent scenarios:**
- **Essential** for regulated industries (finance, healthcare, energy)
- **Important** for any scenario where Agent decisions affect business outcomes
- Enables continuous improvement through retrospective analysis

---

## Dimension 4: Data Semantics (数据语义)

**What to evaluate:** Whether field meanings, business rules, status transitions, and other context previously understood only by humans have been captured in machine-readable form.

**Assessment criteria:**

| Level | Criteria |
|-------|----------|
| **Ready** | Data dictionaries and business rule repositories exist and are maintained. Status machines and transition rules are formally defined. Field-level documentation is current and accessible programmatically. |
| **Partial** | Some documentation exists (e.g., for core entities) but is incomplete or outdated. Business rules are documented in wikis or documents but not in machine-readable format. Status transitions are understood implicitly by experienced staff. |
| **To-Build** | Field meanings, business rules, and status transitions exist only in the heads of experienced employees. No formal documentation. New team members learn entirely through on-the-job training. |

**Key questions to ask the user:**
- "Is there a data dictionary that documents what each field means in your core systems?"
- "Are your business rules (e.g., approval thresholds, pricing rules) documented somewhere an Agent could reference?"
- "If a new developer joined, could they understand your order status flow from documentation alone?"

**Implications for Agent scenarios:**
- **Critical** for Analysis and Orchestration scenarios (Agent needs to understand data to make decisions)
- **Important** for Monitoring (Agent needs to understand what constitutes an anomaly)
- Less critical for Perception (input-side, pre-system)
- Directly impacts Sedimentation (this dimension IS the foundation for knowledge capture)

---

## Assessment Output Template

After evaluating all four dimensions, produce the following summary:

```
System Readiness Assessment
═══════════════════════════════════════════════
Interface Capability:    [Ready / Partial / To-Build]
Permission Model:        [Ready / Partial / To-Build]
Operation Traceability:  [Ready / Partial / To-Build]
Data Semantics:          [Ready / Partial / To-Build]

Priority Actions (parallel with scenario implementation):
1. [Highest priority item based on target scenario needs]
2. [Second priority]
3. [Third priority]
```

**Prioritization principle:** System improvements should be scheduled in parallel with scenario implementation. Whichever scenario is targeted first, the related system interfaces and semantic supplements should be prioritized accordingly.
