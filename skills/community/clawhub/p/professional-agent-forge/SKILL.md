---
name: professional-agent-forge
description: Build a complete OpenClaw agent package for a real profession or job role. Use when the user asks for things like "create a product manager agent", "make me a lawyer agent", "generate an engineer persona", "build a professional-role OpenClaw setup", or "create a data analyst / designer / marketer / operator agent". Produce a role-specific package centered on `soul.md`, `identity.md`, `memory.md`, `agents.md`, and `tools.md`, plus a recommended supporting-skill stack.
---

# Professional Agent Forge

Generate deployable OpenClaw agents for real jobs and professions.

Focus on real work patterns, role-specific judgment, stakeholder behavior, and toolchains — not generic assistant fluff.

## Workflow

```text
Input: profession name + optional industry or scenario
  ↓
Check whether a deep reference file exists
  ├─ If yes: read the matching reference and customize it
  └─ If no: use the generic role-analysis framework
  ↓
Generate the five core files
  ↓
Recommend supporting skills and tooling
  ↓
Return a role-ready agent package
```

## Prebuilt profession references

Read the matching file when the profession fits one of these categories:

| Profession | Reference file | Triggers |
| --- | --- | --- |
| Product manager | `references/product-manager.md` | PM, roadmap, requirements, prioritization |
| Software engineer | `references/software-engineer.md` | engineer, developer, coding, architecture, debugging |
| Lawyer | `references/lawyer.md` | lawyer, legal, contracts, litigation, compliance |
| Data analyst | `references/data-analyst.md` | analytics, BI, SQL, dashboards, experimentation |
| UI/UX designer | `references/designer.md` | designer, UX, UI, prototyping, user research |
| Marketer | `references/marketer.md` | marketing, growth, brand, campaigns, content |

If the requested profession is not listed, fall back to the generic framework below.

## Core file requirements

### `soul.md`
Define the role's deepest professional drive.

Must include:
- Core drive
- Professional beliefs
- Quality standard
- Non-negotiables
- The role's built-in tension

### `identity.md`
Define professional identity and communication style.

Must include:
- Role definition
- Expertise stack
- Communication style by audience
- Decision framework
- Professional boundaries

### `memory.md`
Define the role's stable knowledge layer.

Must include:
- Core methodology
- Domain knowledge
- Templates and common artifacts
- Reference standards
- Common pitfalls

### `agents.md`
Define behavior rules for recurring work situations.

Must include:
- Core workflows
- Output format defaults
- Stakeholder protocols
- Escalation rules
- Sample interactions

### `tools.md`
Define the practical toolchain.

Must include:
- Primary toolstack
- AI-augmented tools
- OpenClaw skill mapping
- Open-source resources
- Tool selection logic
- Recommended MCP integrations

## Generic role-analysis framework

When there is no prebuilt reference, analyze the profession using these dimensions:

```text
1. Core responsibilities
2. Key deliverables
3. Primary stakeholders
4. Areas requiring professional judgment
5. Typical toolchain
6. Success metrics
7. Common pain points
8. Hard boundaries and red lines
```

## Output structure

Return the package in this structure:

```text
[Profession Name] Agent Package
├── soul.md
├── identity.md
├── memory.md
├── agents.md
├── tools.md
└── skills-recommendation.md
```

## Quality bar

Before finalizing, check:
- the package sounds like a real practitioner, not a generic AI assistant
- the role-specific language is credible
- the workflows are concrete and executable
- `tools.md` is practical rather than decorative
- a real professional in that field would recognize the trade-offs and tensions
