# prd-for-agents

> A PRD skill that turns your vision or idea into a specification AI agents can build from directly.

[![ClawHub](https://img.shields.io/badge/ClawHub-prd--for--agents-blue)](https://clawhub.ai/sanketsao/prd-for-agents)
[![License: MIT-0](https://img.shields.io/badge/License-MIT--0-green)](https://spdx.org/licenses/MIT-0.html)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-compatible-orange)](https://openclaw.ai)

---

## What This Is

Most PRD templates are written by human product managers for engineering teams. This skill is different — it produces PRDs based on a vision or idea to be directly consumed by AI agents that are building.

The result is a complete, structured PRD that any agent can pick up and execute without needing clarification from the person who had the original idea.

---

## The Problem It Solves

When you tell your vision or idea to an agent, the builder or developer agent needs more detail at specification level. A raw idea is not enough — the agent needs to know what to build, in what order, what assumptions to validate, and what questions to resolve before writing a line of code.

`prd-for-agents` addresses that gap. It takes a vision and produces a specification structured for agent execution — with the sections that generic PRD templates skip but agents critically need.

---

## Key Additions Over Standard PRD Templates

| Section | Why Agents Need It |
|---------|-------------------|
| **Agent Build Order** | Sequenced task list with complexity and dependencies — builder agent executes in order without guessing |
| **Assumptions** | Beliefs embedded in the vision that need confirmation before build starts — prevents silent scope corruption |
| **Open Questions** | Unresolved decisions with owners and deadlines — flags what must be answered before building begins |
| **Phase Map** | For larger ideas — breaks scope into phases so the agent builds Phase 1 only, with sequence validated upfront |
| **Quantitative Metrics** | Every metric has a number, unit, and date — agent or human can verify without subjective judgment |
| **User Stories** | One per feature, independently testable — maps directly to acceptance criteria the agent checks against |

---

## Routing Rules (for Multi-Agent Pipelines)

When using this skill in a pipeline with an orchestrator or approver agent, built-in routing logic handles the review loop:

- **`#CLARIFY`** — if any Open Question is marked "before build starts", or any Assumption has confidence < High, the PRD should route to an approver agent or human for resolution before the builder starts
- **PRD Review Loop** — responses are classified as Confirms / Scoped Change / Broad Change, each triggering a different update depth (no change / section update / full revision)
- **Max 3 loops** — if unresolved after 3 iterations, escalate to the human operator
- **Phase Map gate** — approver validates phase sequence before Phase 1 begins

These rules are baked into the completeness checklist, not just documentation. If you are running a single-agent setup, treat these as self-review checkpoints before starting the build.

---

## File Structure

```
prd-for-agents/
├── SKILL.md                          ← Main skill file (always loaded)
└── references/
    ├── prd-sections.md               ← Detailed guidance for all 16 sections
    └── prd-examples.md               ← Annotated examples using a real project
```

---

## Installation

**Via ClawHub CLI:**
```bash
openclaw skills install prd-for-agents
```

**Manual:**
```bash
git clone https://github.com/sanketsao/prd-for-agents
cp -r prd-for-agents ~/.openclaw/skills/
```

---

## Usage

Once installed, your agent will use this skill automatically when asked to write a PRD. You can also invoke it explicitly:

```
"Write a PRD for [vision or idea]"
"Review this PRD for completeness gaps"
"Is this PRD ready for the builder agent?"
"Write the assumptions section for this PRD"
"Create a phase map for this PRD"
```

---

## PRD Output Structure

Every PRD produced by this skill follows this section order:

1. Header Block
2. Problem Statement
3. Target Users & Jobs-to-be-Done
4. User Stories
5. Feature List (MVP + Post-MVP)
6. Acceptance Criteria
7. Quantitative Success Metrics
8. Data Schema / API Contracts
9. File & Folder Structure
10. Agent Build Order
11. Phase Map *(for projects with >5 features)*
12. Assumptions
13. Open Questions
14. Dependencies
15. Risks
16. Out of Scope

---

## Completeness Checklist

Before any PRD is handed to a Developer agent, it must pass:

- [ ] All assumptions listed with confidence level and impact if wrong
- [ ] All success metrics have a number, unit, and target date
- [ ] Agent build order present and sequenced (no circular dependencies)
- [ ] No Open Question marked "before Developer starts" left unresolved
- [ ] Phase Map present and Main-validated for projects with >5 features
- [ ] Every MVP feature has at least one user story and one acceptance criterion

---

## Who This Is For

- **Anyone using AI agents to build software** — solo builders, indie hackers, small teams
- **OpenClaw users** running multi-agent setups with separate planner and builder agents
- **Product managers and founders** who want to hand a vision to an agent and get a build-ready spec back
- **Anyone tired of agents asking clarifying questions mid-build** because the original brief wasn't detailed enough

---

## Background

Built as part of the [Product Foundry](https://thebuildereconomist.substack.com) — a multi-agent OpenClaw setup for building software products with AI agents. The insight was simple: agents fail mid-build not because they can't code, but because the specification they were handed was missing the details they needed. This skill closes that gap.

---

## License

MIT-0 — free to use, modify, and redistribute. No attribution required.

---

## Author

[Sanket Sao](https://linkedin.com/in/sanketsao) · [The Builder Economist](https://thebuildereconomist.substack.com)
