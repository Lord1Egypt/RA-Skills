# AI-DWG — Whitepaper

**AI-Driven Workspace Generator**

**Version:** 1.0.0
**Author:** Maheri — [LinkedIn](https://www.linkedin.com/in/mohammad-maheri-8399565b)
**Date:** 2026-06-07

---

## The Problem

Between "a beautiful architecture document" and "a developer opening their IDE on day one" lies an enormous gap that nobody owns.

The typical pattern: architecture is approved. Then silence. Someone creates a Git repo. Someone else writes a README. A tech lead spends a week hand-crafting coding standards. Another week configuring linting. Another week writing a Definition of Done. By the time a developer joins, half the standards are in someone's head, the wiki is already stale, and the architecture decisions — those carefully-made trade-offs — live in a document nobody links to their IDE.

The result: within two sprints, the codebase drifts from the architecture. Not maliciously — there's simply no mechanism connecting architecture decisions to developer tooling. The architecture exists in one universe; the code exists in another.

---

## The Solution

AI-DWG reads an Architecture Package — every document, every ADR, every conditional decision — and transforms it into a complete, ready-to-code development workspace. Not a starter template. A governed development environment where every rule traces to an architecture decision.

**Architecture in, workspace out. In minutes.**

Every steering file it generates says "MUST" or "MUST NOT" — because "should" doesn't prevent drift. Every rule includes a provenance comment identifying which architecture document justified it. Nothing is arbitrary. Nothing is "best practice because I said so."

---

## How It Works

```
Architecture Package → Read AP → Ask 2-4 Questions → Generate Workspace → Ready to Code
```

**One-shot generation with two ongoing modes:**

| Mode | When | What Happens |
|------|------|--------------|
| Full Generation | First time | Reads AP, asks config questions, generates all workspace files |
| Delta Reconciliation | Architecture changes | Detects what changed, proposes updates, preserves team customizations |
| Brownfield Overlay | Existing codebase | Adds governance files without disturbing existing code |

---

## Who It's For

| Role | Pain Point Solved |
|------|-------------------|
| **Platform Engineer** | No more hand-crafting workspace boilerplate per project — generate from architecture automatically |
| **Tech Lead** | Coding standards and conventions are enforced from day 1, not documented and hoped for |
| **CTO / VP Engineering** | Architecture decisions actually reach developer tooling — zero translation gap |
| **New Team Member** | Opens IDE, reads steering files, knows exactly how to contribute — no "ask around" onboarding |
| **DevOps Engineer** | CI/CD config, Docker setup, CODEOWNERS generated from architecture — not copied from last project |

---

## Key Differentiators

### 1. Architecture-Driven, Not Template-Driven

AI-DWG doesn't apply a generic project template. It reads YOUR architecture decisions and generates workspace rules specific to YOUR system. Multi-tenancy steering only appears if your architecture includes multi-tenancy. API versioning rules only appear if your architecture defines API contracts.

### 2. Conditional Generation

Not every project needs every file. AI-DWG only generates what the architecture justifies:
- Architecture has multi-tenancy? → Generate `multi-tenancy.md` steering
- Architecture has 3+ integrations? → Generate `integration-standards.md`
- Architecture is monolith? → Skip microservices-related files

Zero bloat. Every file earned its existence.

### 3. Provenance Tracking

Every generated steering file includes a metadata comment:
```
<!-- Source: ADR-003 (Technology Stack), API Architecture §4.2 -->
```

Six months later, when someone asks "why does this rule exist?" — the answer is built into the file.

### 4. Non-Destructive Reconciliation

When architecture evolves (it always does), AI-DWG doesn't destroy and rebuild. It:
- Detects what changed in the AP
- Proposes specific workspace updates
- Preserves everything marked `<!-- custom -->` (team additions)
- Signals downstream packages (AI-GCE) to re-derive

### 5. Technology-Adaptive

Output differs based on tech stack. A Node.js workspace gets `package.json`, ESLint config, and Vitest setup. A Python workspace gets `pyproject.toml`, Ruff config, and pytest setup. Same architecture, appropriate tooling.

### 6. Extension-Aware (AI-ADLC v1.1)

Detects active extensions in the Architecture Package (DDD, Microservices, BFF, Event Sourcing, Resilience, Feature Flags) and enriches workspace output accordingly — additional steering rules, technology-specific patterns, module structure refinements.

---

## What You Get

A complete **Development Workspace (DW)** containing:

| Category | Examples |
|----------|----------|
| Steering files (always) | workspace-rules.md, tech-stack.md, api-standards.md, security-rules.md, module-structure.md |
| Steering files (conditional) | multi-tenancy.md, event-driven.md, resilience-standards.md |
| Operational documents | Definition of Done, Contributing Guide, Team Agreements, Architecture Summary |
| Configuration files | docker-compose.yml, .editorconfig, CODEOWNERS, .gitignore |
| Project instructions | Project README, Module READMEs |
| Repository structure | Folder layout matching C4 L3 component architecture |

Typically 30-40 files in one generation pass. Every file ready for immediate use.

---

## Part of AIFLC — the AI-* PDLC Family

AI-DWG is the third node in the AI-* PDLC Family chain. It consumes an Architecture Package from AI-ADLC and produces the Development Workspace that AI-GCE uses for compliance derivation. But it works standalone — if you have architecture documentation from any source (even hand-written), AI-DWG can transform it into a governed workspace.

Learn more: [AI-* Family Whitepaper](../narrative/WHITEPAPER.md)

---

## Getting Started

See [setup/INSTALL.md](./setup/INSTALL.md) for platform-specific installation instructions.

**Activation:** After installation, start a chat and say:
```
Using AI-DWG, generate the development workspace from my architecture package.
The AP is located at: [path]
```

---

*Created by Maheri — because architecture should reach the developer's IDE, not die in a wiki.*
