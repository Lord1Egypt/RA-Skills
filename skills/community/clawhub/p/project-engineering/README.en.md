# Project Engineering

[![Validate Skill](https://github.com/liubai00/project-engineering/actions/workflows/ci.yml/badge.svg)](https://github.com/liubai00/project-engineering/actions/workflows/ci.yml)
[![License: MIT-0](https://img.shields.io/github/license/liubai00/project-engineering)](LICENSE)

> **From greenfield architecture to development, refactoring, and delivery in existing projects—help coding agents work within real engineering constraints.**
>
> *Design with constraints. Change with evidence. Deliver with proof.*

[ClawHub](https://clawhub.ai/liubai00/skills/project-engineering) · [简体中文](README.md) · [Usage guide (Chinese)](docs/USAGE.md) · [Changelog](CHANGELOG.md)

Project Engineering is an open-source software engineering Skill for Codex, OpenClaw, and other Agent Skills-compatible coding agents. It is not another model or a catch-all prompt. It gives agents a repeatable workflow for establishing engineering constraints before designing or changing code, then validating and delivering the result with evidence. It follows the user's current language by default.

- **New projects:** turn product goals, technology choices, deployment, security, and delivery conditions into explicit module boundaries, data and API contracts, test strategy, and an engineering baseline. Anything unsupported by evidence remains an assumption or an open decision.
- **Existing projects:** inspect repository rules and real source code, reconstruct ownership and call paths, identify reusable capabilities, impact, and risk, then make the smallest coherent change.

## When to use it

Use Project Engineering when correctness depends on architecture, call paths, data, contracts, authorization, deployment, or delivery constraints—not merely on generating a code snippet.

| Task | What the Skill contributes |
|---|---|
| Start a software project from zero | Establish architecture and engineering baselines before coding |
| Add a cross-file or cross-layer feature | Find the real call path, ownership, and reuse points |
| Change an API, database, message protocol, or external service | Check compatibility, migration, failure handling, and rollback risk |
| Refactor or take over an unfamiliar or legacy project | Reconstruct facts from source and configuration instead of guessing from names |
| Review, validate, or prepare a delivery | Separate code completion, automated tests, integration checks, and real-environment acceptance |

A simple test:

> If the agent must first answer “How should this project be structured, how does it work today, where should this change belong, what will it affect, and how will we prove it works?”, use this Skill.

## What changes when you use it

| A typical coding agent | With Project Engineering |
|---|---|
| Starts generating code from the request | Establishes facts, constraints, scope, and risk first |
| Reaches for a familiar architecture template | Designs from greenfield constraints or respects the existing architecture |
| Changes only the most obvious file | Follows the real path across entry points, business logic, data, configuration, and tests |
| Treats a successful build as completion | Performs risk-proportionate validation and names what remains unverified |
| Reports only that the task is done | Reports decisions, changed scope, test evidence, and remaining risk |

## When not to use it

- Typos, one-line copy edits, formatting, or fully specified single-file mechanical changes;
- Non-software writing or other tasks with no engineering context;
- Simple transformations whose correctness does not depend on project context.

Project Engineering also does not replace product decisions, domain experts, professional penetration testing, functional-safety certification, legal or compliance advice, or real-environment acceptance.

## Quick install and verification

OpenClaw / ClawHub:

```bash
openclaw skills install @liubai00/project-engineering
```

Codex desktop, CLI, or IDE:

```bash
git clone https://github.com/liubai00/project-engineering.git ~/.agents/skills/project-engineering
```

### Existing project: a 5-minute read-only verification

Run this zero-write check inside an application repository with an executable entry point:

```text
Use $project-engineering.

Read-only verification: select one real entry point (HTTP, CLI, message consumer,
or scheduled job) and trace it to a database write or external side effect.
Report the entry file and method, complete call path, authorization, transaction
and state authority, one success path and one failure path, existing test coverage,
and anything not yet verified. Attach a file path, configuration, command output,
or test result to every key claim.

Do not modify files or run commands that write to external systems.
```

The result should identify applicable repository rules, module ownership, an evidence-backed call path, concrete risks, and the boundary between automated checks and real-environment validation. For repositories without a business entry point, trace a build, release, or data-processing entry instead.

### New project: establish the engineering baseline first

When a new project has no repository yet, the Skill should not invent an “existing architecture” or run Git and repository inventory. Start with:

```text
Use $project-engineering.

Establish an implementable engineering baseline for a greenfield internal order-management API.
For now, produce design only and do not create files.
Confirmed constraints: Java 21, Spring Boot 3.4, PostgreSQL,
a Docker-deployed monolith, and OAuth 2.0.

Separate confirmed constraints, reasonable assumptions, and decisions that require an owner.
Define module boundaries, dependency direction, data ownership, API and authorization boundaries,
test strategy, deployment and rollback baselines, and a phased implementation plan.
Do not invent business rules or choose unconfirmed external services for me.
```

The result should include a constraint and assumption ledger, architecture and module boundaries, key contracts, quality and delivery baselines, decision gates, and an implementable sequence.

## Two engineering workflows

New project:

```text
Product goals and confirmed constraints
        ↓
Assumptions, decision gates, and risk discovery
        ↓
Project shape, modules, data, and contract design
        ↓
Testing, deployment, observability, and rollback baselines
        ↓
Phased implementation and validation
        ↓
Traceable delivery
```

Existing project:

```text
Repository rules and real code
        ↓
Inventory and call-path reconstruction
        ↓
Ownership, state authority, and risk classification
        ↓
The smallest coherent implementation
        ↓
Risk-proportionate validation
        ↓
Auditable delivery report
```

## Shared engineering principles

- **Facts and constraints first** — separates confirmed facts, assumptions, and open decisions in new projects; avoids guessing from names in existing ones.
- **Architecture follows the project** — chooses boundaries from real conditions instead of forcing DDD, microservices, or design patterns.
- **Depth follows risk** — separates permission to act from the consequence of the target change.
- **The smallest coherent scope** — designs or changes only what the outcome requires, without unrelated expansion, refactoring, or invented capabilities.
- **Layered proof** — distinguishes code completion, automated checks, integration validation, and real-environment acceptance.
- **Workspace safety** — preserves unrelated user changes and keeps credentials or local configuration out of delivery.
- **Cross-stack discovery** — for existing repositories, the read-only inventory script recognizes common Java, Node.js, Python, Go, Rust, and .NET signals.

## More ways to use it

Implement a feature in an existing project:

```text
Use $project-engineering.

Task: Implement order export.
Mode: Implementation.
Requirements:
1. Read repository rules and trace the existing call path first.
2. Preserve unrelated workspace changes.
3. Follow the repository's established architecture and conventions.
4. Run proportionate tests and report the evidence.
5. Do not commit or push.
```

Design a high-impact change:

```text
Use $project-engineering.

Design a maintenance mode for the current system. Produce a design only; do not code.
Focus on state authority, authorization, concurrent ownership, protocol compatibility,
database migration, fail-closed behavior, rollback, and real-environment acceptance.
```

More copy-ready prompts are available in the [usage guide](docs/USAGE.md).

## Risk is not measured in changed lines

| Level | Typical work | Additional scrutiny |
|---|---|---|
| L1 | Documentation, naming, local pure logic | Targeted diff and minimal validation |
| L2 | CRUD, queries, single-module business logic | Inputs, authorization, transactions, migration |
| L3 | Cross-module, database, async, external API | State, idempotency, compatibility, timeout, contracts |
| L4 | Identity, money, privacy, AI actions, device control | Fail-closed behavior, re-authentication, arbitration, audit |
| L5 | Potential injury, critical infrastructure damage, or formal certification | Domain safety owner, hazard analysis, and formal approval |

A read-only review of a high-risk capability still deserves L4/L5 reasoning depth, but read-only authorization does not permit code or external-system changes.

## Safety boundary

Invoking this Skill selects an engineering workflow. It does **not** authorize commits, pushes, pull requests, migrations, deployments, credential changes, production access, or device operations.

The bundled inventory script requires Python 3.10+ and uses only the standard library. It does not use the network or execute repository code, package-manager scripts, or builds. It reads supported build and workspace manifests to detect structure, but does not echo manifest contents or credential values in reports. The Skill also requires explicit authorization before internal repository material is sent to a third party. Inventory reports include the repository root, branch, commit, and structural paths, so review them before sharing.

## Package layout

```text
project-engineering/
├── SKILL.md
├── agents/openai.yaml
├── references/
│   ├── greenfield.md
│   ├── discovery.md
│   ├── architecture.md
│   ├── implementation.md
│   ├── risk-and-archetypes.md
│   └── delivery.md
└── scripts/
    ├── project_inventory.py
    ├── test_project_inventory.py
    └── test_skill_package.py
```

`SKILL.md` keeps only the shared workflow and reference routing. Greenfield baselines, existing-project discovery, implementation, and delivery details are loaded only when the task needs them.

## Validation

```bash
python -m unittest discover -s scripts -p "test_*.py"
python scripts/project_inventory.py --repo . --format json
```

Tests cover multi-ecosystem discovery, sensitive-value redaction, malformed-manifest safety, and Skill-package link integrity. CI runs on both Windows and Linux.

## Help improve it

Run the example that matches your project stage. If it uncovers a real constraint or decision, [star the project](https://github.com/liubai00/project-engineering). If it misses one, [open an issue](https://github.com/liubai00/project-engineering/issues/new) with sanitized project context, expected behavior, and actual result.

## License

[MIT-0](LICENSE). Free to use, modify, redistribute, and use commercially without attribution.
