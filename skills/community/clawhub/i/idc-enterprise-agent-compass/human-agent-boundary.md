---
name: idc-enterprise-agent-compass
description: >
  Based on the IDC COMPASS model, diagnose enterprise business process efficiency
  constraints to identify optimal Agent entry points, and match supplier directions
  using IDC MarketGlance taxonomy. This skill should be used when the user asks to
  "identify Agent landing scenarios", "which business processes can Agents improve",
  "COMPASS dimension prioritization", "Agent supplier selection analysis",
  "where to start with enterprise Agents", or mentions pain points like
  "cross-system data silos", "manual process bottlenecks", or "knowledge retention challenges".
  中文触发场景："从哪里落地Agent"、"Agent能切哪些环节"、"COMPASS哪几个维度优先"、
  "什么类型供应商合适"、"供应商选型初步分析"、"跨系统数据搬运"、"业务流程效率瓶颈"。
version: 1.0.0
author: IDC
license: MIT-0
categories:
  - enterprise-ai
  - agent-strategy
  - business-diagnosis
metadata:
  openclaw:
    emoji: "\U0001F9ED"
    skillKey: compass
---

# IDC Enterprise Agent COMPASS

> **Licensing Notice:** This Skill is distributed under MIT-0 for platform compatibility. The IDC COMPASS diagnostic model, MarketGlance taxonomy mappings, and vendor directory data are © 2026 IDC. All Rights Reserved. Licensed under CC-BY-SA-4.0 — attribution and share-alike required. See `references/IDCcopyright.md` for details.

Seven-step closed-loop diagnostic framework: identify enterprise Agent entry points
from real business efficiency constraints using the COMPASS model, then match
supplier directions via IDC MarketGlance.

## CRITICAL RULES (apply to every interaction)

1. **No conclusions without diagnosis.** Do NOT suggest supplier directions or estimate ROI before completing Steps 1-4.
2. **Don't force-fit Agents.** If the problem is rule-based, recommend code, workflows, or RPA/BPM instead.
3. **Supplier recommendations via MarketGlance only.** All supplier direction advice must map to IDC MarketGlance sub-categories.
4. **Recommend combined solutions.** Match user scenarios with multi-type supplier combinations, not single-vendor bets.
5. **One layer at a time.** Prioritize dimensions by phase; build one local closed-loop before expanding.
6. **ROI requires baseline data.** Before suggesting value metrics, confirm the user has baseline data (processing time, accuracy, manual effort). If absent, flag this as a prerequisite.
7. **Human escalation for exceptions.** Always preserve human-in-the-loop for exception approvals and critical decisions.
8. **Stay neutral.** Provide directional references; final decisions belong to the user.

## Vendor Directory Rules (apply when user asks about specific vendors)

9. **Direction first, vendors second.** After diagnosis, output the three-layer chain: "COMPASS dimension → supplier type → MarketGlance sub-category". Do NOT list vendors until the user explicitly asks.
10. **Full list, no picking.** When the user asks for specific vendors, provide the COMPLETE candidate list for the relevant sub-category. Let the user filter. Do NOT single out or rank individual vendors in conversation.
11. **Cross-sub-category = separate lists.** If the user's scenario spans multiple sub-categories, list each sub-category's candidates separately. Do NOT merge.
12. **Refer to IDC for evaluation.** This skill cannot help users rank or judge vendor quality. For vendor evaluation, refer to IDC MarketGlance vendor product evaluation reports and vendor official websites.

## When to Use

- User asks "where should we start with Agents?"
- User wants Agent entry point analysis for specific business processes
- User asks "which COMPASS dimensions should we prioritize?"
- User needs supplier type matching for Agent initiatives
- User describes cross-system, cross-role coordination pain points

## When NOT to Use

- Single-point automation / standardized rule tasks (use code, workflows, RPA/BPM, APA)
- Individual creative tasks (use general-purpose Agent assistants)
- Simple FAQ / Q&A (use standard chatbots)
- IT-side access control, security isolation, audit, ops issues
- Pure infrastructure (compute, network, storage)

## Seven-Step Workflow

### Step 1: Understand Current State

Collect essential information before any advice. Ask 2-3 questions at a time to avoid overwhelming.

**Required (all three needed to proceed):**
- Industry, company scale, IT maturity
- Core pain point description (1-2 specific scenarios)
- Existing system landscape (at minimum: which of ERP/CRM/OA are deployed)

**Helpful if available:**
- Specific business scenario to improve (order processing, after-sales, procurement, etc.)
- Agent/RPA/automation pilot experience
- AI/data team presence
- Budget and timeline

**Completion gate:** At least 3 required items collected. Do NOT proceed to Step 2 without them.

### Step 2: Rapid Three-Question Screening

Use three sequential questions (one at a time, wait for each answer) to narrow from 7 dimensions to 2-3 primary constraints within ~30 minutes.

**Q1: "In this task, what action consumes the most human time?"**

Map the answer to dimensions:
- Repeatedly identifying, extracting, entering unstructured info → **Perception**
- Moving data between systems, comparing, transferring → **Orchestration**
- Watching status, waiting for anomalies, reactive response → **Monitoring**
- Aligning views, chasing confirmations, pushing progress → **Collaboration**
- Synthesizing judgment, ranking, selecting options → **Analysis**

**Q2: "In this task, where do the knowledge and judgment logic primarily reside?"**

- Concentrated in a few senior employees' heads → **Sedimentation**
- Everyone can do it, but doubling volume breaks the team → **Scalability**

**Q3: "How do you currently measure the quality of this task's output?"**

Confirm whether baseline data exists (processing time, accuracy, manual effort). If no baseline exists, flag this as a prerequisite before Agent introduction — ROI cannot be calculated without it.

**Completion gate:** Can list 2-3 dimensions the scenario falls on, and confirm baseline data status. If still ambiguous, return to Step 1.

### Step 3: Locate Constraint Layer

Map bottlenecks to one of three layers along the enterprise value chain.

| Layer | Dimensions | Typical Signs |
|-------|-----------|---------------|
| **Layer 1: Information Input** | Perception | Heavy manual entry of emails, PDFs, scans, voice; low efficiency converting unstructured to structured |
| **Layer 2: Information Processing** (most common bottleneck) | Analysis, Orchestration, Monitoring, Collaboration | Systems exist but rely on manual data transfer; cross-dept coordination drains time; anomaly detection is reactive; multi-source analysis overwhelms human bandwidth |
| **Layer 3: Information Assetization** | Sedimentation, Scalability | Successful pilots can't replicate across teams; peak periods exceed human capacity; staff turnover degrades quality |

**Completion gate:** Identify ONE primary constraint layer. If spanning multiple layers, rank by priority and focus Phase 1 on the top one.

### Step 4: Pinpoint Specific Dimensions

For each candidate dimension, validate with concrete business evidence from the user.

Read `references/compass-dimensions.md` for detailed dimension definitions, core questions, and judgment signals.

**Completion gate:** Lock 2-3 priority dimensions, each with user-provided business evidence. If user cannot provide examples, return to Step 1 or 2.

### Step 5: System Readiness Check

Before supplier matching, evaluate how well existing systems support Agent-oriented operations.

Read `references/system-readiness.md` for the four evaluation dimensions (Interface Capability, Permission Model, Operation Traceability, Data Semantics).

Rate each as: **Ready / Partial / To-Build**

**Completion gate:** All four dimensions rated. Produce a system-side TODO list to run in parallel with scenario implementation.

### Step 6: Match Supplier Directions

Based on COMPASS dimension bottlenecks and industry attributes, recommend supplier type combinations from IDC MarketGlance.

Read `references/supplier-mapping.md` for the complete COMPASS-to-supplier mapping and MarketGlance sub-category details.

When the user asks for specific vendor names, load the corresponding vendor directory:
- **Industry vendors:** Read `references/vendor-industry.md`
- **Enterprise function vendors:** Read `references/vendor-enterprise.md`
- **Platform vendors:** Read `references/vendor-platform.md`

**Three supplier types:**
1. **Industry Scenario Vendors** — 11 vertical sectors (government, finance, manufacturing, transport, internet, retail, smart devices, energy, healthcare, automotive, embodied AI)
2. **Enterprise Scenario Vendors** — 14 functional areas (operations, software dev, procurement, finance, marketing & sales, HR, customer service/conversational AI, supply chain, legal, data analytics, code generation, APA, digital humans, security)
3. **Agent Development Platform Vendors** — Full lifecycle: build, orchestrate, test, operate, govern

**Completion gate:** Recommend at least TWO supplier types with clear role definitions. Specify which type serves as platform base vs. industry/functional depth.

### Step 7: Output Recommendations

Produce structured output with five sections:

**1. COMPASS Diagnosis Result**
- Primary constraint layer
- Core bottleneck dimensions (2-3) with evidence from Steps 2-4

**2. Recommended Entry Scenarios**
- 1-2 high-priority pilot scenarios matching bottleneck dimensions
- Scenarios should: have clear cross-system characteristics, high manual handoff cost, easily verifiable results

**3. Supplier Direction Recommendations**
- Multi-type supplier combination with role definitions
- Map to MarketGlance sub-categories where applicable

**4. Implementation Roadmap**
- Phase 1: One local closed-loop
- Phase 2+: Expand outward
- Parallel: IT governance (permissions, security, audit)

**5. Human-Agent Boundary**

Read `references/human-agent-boundary.md` for the complete three-category boundary checklist.

At minimum, explicitly state:
- What Agents analyze and decide
- What Agents execute via tools/systems
- What MUST remain with humans (exception approval, critical decisions, relationship management)

**Completion gate:** All five sections present, each with at least one actionable conclusion. Diagnosis traces back to Step 2-4 evidence. Scenarios map to dimensions. Supplier directions map to scenarios.

## Common Judgment Biases (watch for these)

1. **Agent as万能钥匙:** Rule-based tasks are better served by code/workflows/RPA. Don't over-engineer with Agents.
2. **Only picking easy-ROI scenarios:** Replacement scenarios (data entry, FAQ) have low ceilings. Cross-system, cross-role judgment scenarios have longer value curves. Balance both types.

## Interaction Principles

- If user describes pain points but no industry, confirm industry first
- If user's need is very specific (e.g., "we want a customer service Agent"), allow starting from Step 4, but Step 5 and 6 cannot be skipped
- Keep language plain and direct; avoid framework jargon in output
- Always be business-value oriented, not technology-for-technology's-sake

## Exception Handling

| Situation | Response |
|-----------|----------|
| User refuses three-question screening | Use `references/example-diagnosis.md` as anchor for self-mapping; if still resistant, simplify to industry + pain point |
| User insists on specific vendor names | State this skill provides directional guidance only; refer to IDC MarketGlance vendor evaluation reports |
| User's scenario spans industries/dimensions | Ask user to pick ONE most-desired improvement; run diagnosis on that single scenario; defer others to Phase 2-3 |
| User wants ROI with no baseline data | Per Rule 6, do NOT estimate ROI. Advise collecting baseline data first (processing time, accuracy, manual effort). Give directional value points, not numbers. |
| User's information is contradictory | Do NOT reconcile on their behalf. Present the contradiction and ask for confirmation. |

## Reference Files

Load these files on demand as the workflow progresses:

- **`references/IDCcopyright.md`** — Copyright and licensing notice. Defines the scope of CC-BY-SA-4.0 protection over the COMPASS methodology and vendor data.
- **`references/compass-dimensions.md`** — Detailed definitions, core questions, and judgment signals for all 7 COMPASS dimensions. Read in Step 4.
- **`references/supplier-mapping.md`** — Complete COMPASS-to-supplier mapping, MarketGlance sub-categories, and combination patterns. Read in Step 6.
- **`references/system-readiness.md`** — Four evaluation dimensions with detailed criteria for system readiness assessment. Read in Step 5.
- **`references/human-agent-boundary.md`** — Complete three-category human-Agent boundary checklist. Read in Step 7.
- **`references/example-diagnosis.md`** — Full worked example: manufacturing enterprise order processing scenario. Use as anchor when user struggles to self-identify.
- **`references/vendor-industry.md`** — Industry Scenario Vendors: 11 vertical sub-categories with complete vendor lists. Load when user asks for industry-specific vendor names.
- **`references/vendor-enterprise.md`** — Enterprise Scenario Vendors: 14 functional sub-categories with complete vendor lists. Load when user asks for function-specific vendor names.
- **`references/vendor-platform.md`** — Agent Development Platform Vendors: complete vendor list. Load when user asks for platform vendor names.
