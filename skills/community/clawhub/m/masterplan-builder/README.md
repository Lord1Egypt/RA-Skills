# masterplan-builder

A Claude skill that turns a vague project idea into a complete, production-grade masterplan — from zero to a system that's actually ready to launch, not just a rough outline.

## What it does

When triggered, Claude will:

1. Ask what kind of project this is (website, mobile app, local AI assistant, desktop app, backend/API, browser extension, CLI tool, etc.) before anything else.
2. Search the web for the current (not training-data-stale) best-practice stack and patterns for that category.
3. Interview you topic by topic — never a giant wall of questions at once — covering everything from the project name and target users down to database schema, API contracts, security threat model, cost/budget, reliability targets, versioning policy, vendor lock-in, infrastructure-as-code, analytics, and how the system should adapt to whatever device/network/load it actually runs on.
4. Validate every tech/architecture decision against live sources before locking it in.
5. Draft the plan, then run it back through a self-audit against a production-readiness checklist and a planning/governance checklist — fixing anything that still reads as a Blocker or Major gap before calling it done.
6. Write the final plan to `docs/masterplan/masterplan.md` inside your project directory (auto-created).

The goal: code built from this plan should be deployable as-is, with no development-only shortcuts, no dead code, no silently-swallowed errors, and no hard assumptions about a single device/network/scale baked in where the system should instead detect and adapt.

## Files in this skill

```
SKILL.md                              -- the workflow Claude follows
references/interview-topics.md        -- the full topic-by-topic interview script (23 topics)
references/production-standards.md    -- code/architecture production-readiness bar, incl.
                                          environment-adaptability and anti-dead-code/anti-
                                          silent-failure standards, universal + per project type
references/gap-checklist.md           -- planning/governance checklist (risk register, cost,
                                          threat model, SLA/RTO/RPO, versioning, vendor lock-in,
                                          IaC, analytics, market context) + the self-audit step
references/masterplan-template.md     -- the output document's section structure
```

## What ends up in the masterplan

Overview, users/personas, features (MVP vs later, to acceptance-criteria level), tech stack (with justification and sources), data model, architecture, non-functional requirements, adaptive system design, production-readiness checklist, risk register, cost & budget, security threat model, reliability targets, versioning & release policy, team & roles, post-launch maintenance, vendor lock-in analysis, infrastructure-as-code decision, analytics/KPI plan, market context (commercial projects), build roadmap (phased, each phase ends in something working, each phase states what to remove if it supersedes earlier work), and open questions.

## How to use it

Install the skill, then just ask Claude to help plan a project — e.g. "help me plan a website for X" or "buatkan masterplan untuk aplikasi mobile Y". Claude will ask the category first, then walk through the interview conversationally. Answer as specifically as you can; vague answers get pushed back on rather than silently assumed.

## Known limitation

This skill hasn't yet been run end-to-end against a real project inside this repository — it's been reviewed and iterated on structurally, but not battle-tested. Treat the first real run as a trial and flag anything that feels off so it can be tightened.
