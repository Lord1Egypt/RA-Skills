---
name: team-builder
description: Discover, compose, and activate specialist teams from 3 rosters — OpenClaw Core (CEO/IG/Artist), Agency Division (55+ specialists), and Research Lab (autonomous experiment loops). Planner proposes optimal teams; Reviewer validates deliverables.
---

# Team Builder

Compose the right team for any job by drawing from three rosters of specialists. The Planner analyzes incoming work and proposes an optimal team; the Reviewer validates deliverables before sign-off.

## Quick Start

1. **Receive a task** — any job, project, or request
2. **Read `PLANNER.md`** in this skill folder — follow the workflow to classify the domain and propose a team
3. **Activate specialists** — load the relevant agent definition from the reference files listed below
4. **Execute** — hand off work through the team using the handoff templates
5. **Review** — read `REVIEWER.md` and run the QA workflow before final delivery

## The Three Rosters

### 1. Core Team (`TEAM-CORE.md`)
The permanent OpenClaw agents. Always available, always running.

| Agent | Role | Workspace |
|-------|------|-----------|
| **CEO** | Leader, orchestrator, final authority | `.openclaw/workspace/` |
| **IG** | Trading specialist, market operations | `.openclaw/workspace-ig/` |
| **Artist** | Image generation, visual analysis | `.openclaw/workspace-artist/` |

### 2. Agency Division (`TEAM-AGENCY.md`)
55+ specialist agents across 9 divisions. Activated on demand from `reference/agency-agents-main/`.

| Division | Agents | Key Specialists |
|----------|--------|-----------------|
| Engineering | 7 | Frontend Developer, Backend Architect, AI Engineer, DevOps |
| Design | 7 | UI Designer, UX Architect, Image Prompt Engineer |
| Marketing | 8 | Growth Hacker, Content Creator, Social Media |
| Product | 3 | Sprint Prioritizer, Trend Researcher, Feedback Synthesizer |
| Project Management | 5 | Senior PM, Studio Producer, Experiment Tracker |
| Testing | 7 | Evidence Collector, Reality Checker, API Tester |
| Support | 6 | Analytics Reporter, Finance Tracker, Legal Compliance |
| Spatial Computing | 6 | XR Architect, visionOS Engineer |
| Specialized | 7 | Agents Orchestrator, Data Analytics, LSP Engineer |

### 3. Research Lab (`TEAM-RESEARCH.md`)
Autonomous experiment methodology adapted from Karpathy's autoresearch. Run iterative experiment loops on any measurable problem.

Applicable to: trading strategy optimization, image analysis pipelines, model tuning, data analysis, any domain with a measurable metric.

## Cross-Team Workflows

The real power is mixing specialists across rosters. Here are proven combinations:

### Trading Strategy Optimization
```
IG (market context) + Research Lab (experiment loop) + AI Engineer (model tuning)
→ IG provides live market data and strategy parameters
→ Research Lab runs 5-min experiment iterations on backtests
→ AI Engineer tunes neural network parameters
→ Reviewer validates with evidence before deploying to live
```

### Visual Content Pipeline
```
Artist (image generation) + Image Prompt Engineer (prompt crafting) + Visual Storyteller (narrative)
→ Image Prompt Engineer crafts detailed, structured prompts
→ Artist generates via xAI grok-imagine-image-pro
→ Visual Storyteller evaluates narrative quality
→ Iterate until quality threshold met
```

### Astronomy / Image Analysis
```
Artist (image capture/generation) + Research Lab (analysis loop) + AI Engineer (classification)
→ Artist handles image acquisition and enhancement
→ Research Lab runs iterative analysis (feature detection, classification)
→ AI Engineer builds/tunes detection models
→ Results feed back for next iteration
```

### Dashboard / UI Feature Build
```
Senior PM (scope) + Frontend Developer (build) + Evidence Collector (QA) + Reality Checker (sign-off)
→ PM breaks spec into tasks with acceptance criteria
→ Frontend Developer implements mobile-first
→ Evidence Collector screenshots and validates each task
→ Reality Checker gives final production-readiness verdict
```

### Full Product Launch
```
CEO (orchestrate) + Engineering (build) + Design (UX) + Marketing (launch) + Testing (validate)
→ CEO activates Planner to scope the project
→ Engineering + Design work in parallel (Dev↔QA loops)
→ Marketing prepares launch materials
→ Reviewer signs off before go-live
```

## Activating a Specialist

To activate any Agency specialist, load their definition file:

```
Read the agent definition at:
reference/agency-agents-main/[division]/[agent-file].md

Then adopt that agent's:
- Identity and personality
- Core mission and rules
- Workflow process
- Success metrics
```

File paths follow the pattern:
- `reference/agency-agents-main/engineering/engineering-frontend-developer.md`
- `reference/agency-agents-main/design/design-image-prompt-engineer.md`
- `reference/agency-agents-main/testing/testing-evidence-collector.md`

See `TEAM-AGENCY.md` for the complete index with all file paths.

## Handoff Protocol

When passing work between specialists, use this template:

```
## Handoff
| Field | Value |
|-------|-------|
| From | [Agent Name] |
| To | [Agent Name] |
| Task | [What needs to be done] |
| Priority | [Critical / High / Medium / Low] |

## Context
- Current state: [What's been done]
- Relevant files: [File paths]
- Constraints: [Limits, requirements]

## Deliverable
- What is needed: [Specific output]
- Acceptance criteria:
  - [ ] [Criterion 1]
  - [ ] [Criterion 2]

## Quality
- Evidence required: [What proof of completion looks like]
- Reviewer: [Who validates this deliverable]
```

For complete handoff templates (QA pass/fail, escalation, phase gates), see:
`reference/agency-agents-main/strategy/coordination/handoff-templates.md`

## NEXUS Pipeline Modes

For larger projects, use the NEXUS pipeline from the Agency framework:

| Mode | Scale | Agents | Timeline |
|------|-------|--------|----------|
| **Micro** | Single task/fix | 5-10 | 1-5 days |
| **Sprint** | Feature or MVP | 15-25 | 2-6 weeks |
| **Full** | Complete product | All | 12-24 weeks |

Pipeline phases: Discover → Strategize → Scaffold → Build → Harden → Launch → Operate

Quality gates between every phase. Evidence required for all assessments.

For full NEXUS strategy: `reference/agency-agents-main/strategy/nexus-strategy.md`
For activation prompts: `reference/agency-agents-main/strategy/coordination/agent-activation-prompts.md`
For quickstart: `reference/agency-agents-main/strategy/QUICKSTART.md`

## Reference Files in This Skill

| File | Contents |
|------|----------|
| `SKILL.md` | This file — overview and quick start |
| `TEAM-CORE.md` | CEO/IG/Artist trio — roles, routing, interactions |
| `TEAM-AGENCY.md` | All 55+ Agency specialists indexed by division |
| `TEAM-RESEARCH.md` | Autonomous experiment methodology |
| `PLANNER.md` | Job analysis → team proposal workflow |
| `REVIEWER.md` | QA validation workflow with quality gates |
