---
name: Post-Labor Economics
slug: post-labor-economics
version: 1.0.0
homepage: https://clawic.com/skills/post-labor-economics
description: Model post-labor economies with automation shocks, distribution redesign, and policy portfolios across income, ownership, time, and services.
changelog: Initial release with policy portfolio design, scenario stress tests, and evidence-led transition planning.
metadata: {"clawdbot":{"emoji":"📉","requires":{"bins":[]},"os":["linux","darwin","win32"],"configPaths":["~/post-labor-economics/"]}}
---

## Setup

If `~/post-labor-economics/` does not exist or is empty, read `setup.md`, explain that you can save local preferences for continuity, and ask for explicit confirmation before writing memory files.

## When to Use

User wants to analyze a world where paid employment is no longer the main channel for income, status, or social coordination. Use for automation transition strategy, post-work policy design, distribution modeling, and labor market scenario planning.

## Architecture

Memory lives in `~/post-labor-economics/`. See `memory-template.md` for setup.

```text
~/post-labor-economics/
|- memory.md            # Core context and integration preferences
|- portfolios.md        # Policy portfolio drafts and decision logs
|- indicators.md        # Chosen metrics, targets, and thresholds
`- scenarios.md         # Transition scenarios and stress tests
```

## Data Storage

Local working memory and transition artifacts are stored in `~/post-labor-economics/` only.

## Quick Reference

| Topic | File |
|-------|------|
| Setup process | `setup.md` |
| Memory template | `memory-template.md` |
| Core frameworks | `frameworks.md` |
| Policy portfolio design | `policy-portfolio.md` |
| Indicators and dashboards | `indicators.md` |
| Scenario stress tests | `scenarios.md` |
| Evidence map | `research-notes.md` |

## Core Rules

### 1. Define the Transition Mechanism Before Debating Policy
Start by naming what changed in production:
- task automation,
- capital concentration,
- platform coordination,
- energy and ecological limits,
- demographic pressure.

No mechanism means no credible post-labor recommendation.

### 2. Separate Production Logic from Distribution Logic
Model these as two distinct layers:
- how goods and services are produced,
- how purchasing power, rights, and access are distributed.

Do not assume that efficient production automatically produces fair distribution.

### 3. Design Bundles, Not Single-Idea Policies
Always propose a portfolio with at least three categories:
- baseline security (income or services),
- coordination of socially necessary work,
- ownership and bargaining architecture.

Single-policy answers are fragile and usually fail under political stress.

### 4. Make Power and Ownership Explicit
For each design, state:
- who owns productive assets,
- who controls allocation decisions,
- who captures automation gains,
- who absorbs transition risk.

If power is hidden, the model is incomplete.

### 5. Quantify the Path, Not Just the End-State
Require phased planning:
- near term (0-3 years),
- transition (3-10 years),
- structural horizon (10+ years).

For each phase, define financing, institutions, and measurable checkpoints.

### 6. Evaluate Multiple Human Profiles
Every recommendation must score effects on:
- displaced workers,
- care workers,
- young entrants,
- older workers,
- disabled people,
- small producers and local communities.

A policy that works only for one profile is not a post-labor solution.

### 7. Maintain an Evidence Ledger
Tag every claim as one of:
- empirical finding,
- modeling assumption,
- normative preference,
- political constraint.

Never present assumptions or values as settled facts.

## Common Traps

- Treating post-labor economics as "no one works" -> ignores care, coordination, and public goods labor.
- Debating UBI as the whole system -> misses services, institutions, and ownership design.
- Assuming automation gains distribute automatically -> reproduces inequality under new technology.
- Mixing descriptive and moral claims -> analysis becomes rhetorical instead of decision-grade.
- Skipping implementation sequencing -> creates elegant theory with no transition path.
- Ignoring political feasibility entirely -> proposal cannot survive first contact with institutions.

## Security & Privacy

**Data that leaves your machine:**
- None from this skill itself.

**Data that stays local:**
- Policy drafts, indicators, and scenarios in `~/post-labor-economics/`.

**This skill does NOT:**
- Make undeclared network calls.
- Collect or infer sensitive personal data beyond what user provides for analysis.
- Write outside its declared local path.

## Scope

This skill ONLY:
- Structures post-labor economic analysis.
- Builds policy portfolios and transition scenarios.
- Separates empirical evidence from assumptions and values.

This skill NEVER:
- Claims deterministic macro forecasts.
- Replaces legal or fiscal sign-off by institutions.
- Treats one country template as universally transferable.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `economics` - Economic reasoning and policy tradeoff analysis.
- `strategy` - Structured decision design under constraints.
- `work` - Practical work design and role-level execution planning.
- `productivity` - Throughput and workflow optimization at task level.
- `collaborate` - Multi-stakeholder communication and coordination patterns.

## Feedback

- If useful: `clawhub star post-labor-economics`
- Stay updated: `clawhub sync`
