# How Steering File Loading Works

**Purpose:** Explains how AI-* Family steering files are loaded into AI sessions — the loading modes, precedence rules, conditional inclusion, and how steering files interact with the core workflow to shape AI behavior at runtime.

---

## What Steering Files Are

Steering files are markdown documents placed in `.kiro/steering/` that provide context, rules, and constraints to every AI session in a workspace. They are the runtime bridge between architectural decisions (made during AI-ADLC/AI-DWG) and session-level AI behavior.

```
.kiro/steering/
├── workspace-rules.md         ← Always loaded (project-wide context)
├── tech-stack.md              ← Always loaded (technology constraints)
├── api-standards.md           ← Always loaded (API rules)
├── security-rules.md          ← Always loaded (security constraints)
├── ai-pilc-rules.md           ← File-match: loaded when working in ai-pilc/
├── ai-adlc-rules.md           ← File-match: loaded when working in ai-adlc/
└── persona-cto-architect.md   ← Manual: loaded when user invokes #persona-cto-architect
```

---

## Three Loading Modes

### Mode 1: Always Included (Default)

**Behavior:** Loaded into EVERY AI session in the workspace, automatically.

**Front-matter:** None required (default behavior) — or explicitly:
```yaml
---
inclusion: always
---
```

**Use for:** Project context, technology constraints, coding standards, governance rules — anything the AI should know in EVERY session regardless of what file is being edited.

**Examples:** `workspace-rules.md`, `tech-stack.md`, `api-standards.md`, `security-rules.md`, `naming-conventions.md`

### Mode 2: File-Match (Conditional)

**Behavior:** Loaded ONLY when a file matching the specified pattern is open/active in the editor.

**Front-matter:**
```yaml
---
inclusion: fileMatch
fileMatchPattern: "ai-adlc/**"
---
```

**Use for:** Package-specific rules, folder-specific conventions, module-specific constraints that shouldn't pollute sessions working in other areas.

**Examples:** `ai-adlc-rules.md` (loaded only when editing AI-ADLC files), `frontend-rules.md` (loaded only when editing frontend code)

### Mode 3: Manual (User-Invoked)

**Behavior:** Loaded ONLY when the user explicitly provides it via `#` context key in chat.

**Front-matter:**
```yaml
---
inclusion: manual
---
```

**Use for:** Personas, reference documentation, specialized guides that are useful on-demand but too heavy for always-on loading.

**Examples:** `persona-cto-architect.md` (invoked as `#persona-cto-architect`), `package-builder-rules.md` (invoked when building packages)

---

## Loading Precedence

When multiple steering files provide conflicting guidance:

| Priority | Source | Wins Because |
|:--------:|--------|-------------|
| 1 (highest) | Workspace-level steering | Closest to the project |
| 2 | User-level global steering (`~/.kiro/steering/`) | Personal defaults |
| 3 | Package defaults | Generic, can be overridden |

**Within the same level:** All files are loaded and compose. If two files at the same level conflict, the more specific one (file-match) takes precedence over the general one (always-included).

---

## File References in Steering

Steering files can reference other files using the inclusion syntax:

```markdown
#[[file:../contracts/NAMING_AND_OWNERSHIP.md]]
```

This pulls the referenced file's content into the steering context. Use for:
- OpenAPI specs that inform API standards
- Architecture decisions that inform coding rules
- Contracts that define cross-package behavior

---

## How AI-DWG Generates Steering Files

When AI-DWG runs, it produces steering files with appropriate loading modes:

| Generated File | Loading Mode | Rationale |
|---------------|:------------:|-----------|
| `workspace-rules.md` | Always | Every session needs project context |
| `tech-stack.md` | Always | Technology constraints apply everywhere |
| `api-standards.md` | Always | API rules apply to any endpoint work |
| `security-rules.md` | Always | Security is never optional |
| `module-structure.md` | Always | Boundary rules apply to all code changes |
| `naming-conventions.md` | Always | Naming applies to every file created |
| `testing-strategy.md` | Always | Test requirements apply to all new code |
| `session-governance.md` | Always | Session discipline is universal |
| `multi-tenancy.md` | Always (conditional generation) | Only generated if architecture includes tenancy |
| `frontend-standards.md` | File-match (`src/frontend/**`) | Only when editing frontend code |

---

## The Family Loading Model — One Orchestrator, Manual Cores

A family of injectable packages ships many large workflow files (one "core" per package). If every core were always-loaded, a workspace with the whole family installed would consume most of the AI's context window before the first prompt — and several package workflows would compete for the same session.

The family avoids this with a deliberate split:

| Artifact | Inclusion | Loaded |
|----------|-----------|--------|
| Each package core (`{package}-rules/core-*.md`) | `manual` | Only when you activate that package — by its key (e.g. `_POLC_`) or by referencing it with `#` |
| One `session-orchestrator.md` (deployed to `.kiro/steering/` — top level, so Kiro auto-loads it) | `auto` | Always — it is the family's single always-loaded steering file |

The **session orchestrator** is a small (~120-line) router. On every session it:
1. Reads your intent — an activation key (e.g. `_ADLC_`), a natural-language request, or "resume".
2. Loads exactly ONE package's core on demand.
3. Keeps the rest dormant so the context window stays free.

A fresh session therefore starts with a lightweight orchestrator rather than every package workflow, and only one package is ever active at a time.

**Activating a package:**
- Type its key (e.g. `_UXD_`) — the orchestrator routes to that package.
- Or describe what you want ("work on the backlog") — the orchestrator maps intent to the right package.
- Or say "resume" — the orchestrator scans your `*-state.md` files and reloads the in-progress package.

**Single-package installs** still get the orchestrator; it simply routes to the one package you installed. Either way, the package cores stay `manual` and the orchestrator is the one `auto` file.

---

## Context Budget Management

Steering files consume AI context window. Loading strategy matters:

| Strategy | Impact |
|----------|--------|
| All files always-included | Maximum governance but high token cost |
| Heavy use of file-match | Contextual loading — lighter sessions |
| Manual inclusion for reference docs | Zero cost until invoked |
| File references (`#[[file:...]]`) | Pulls full content — use for specs/contracts only when needed |

**Best practice:** Keep always-included files concise (rules and constraints). Put detailed reference material in manual-inclusion files. Use file-match for folder-specific concerns. For a multi-package family, ship package cores as `manual` and load them through the single `auto` session orchestrator (see "The Family Loading Model" above) — this keeps always-loaded cost flat regardless of how many packages are installed.

---

## Steering File Anatomy

Every steering file follows a consistent structure:

```markdown
---
inclusion: always | fileMatch | manual
fileMatchPattern: "pattern/**"  # only for fileMatch
---

# {Topic} Rules

## Context
{Why these rules exist — one paragraph}

## Rules
1. MUST {rule}
2. MUST NOT {rule}
3. NEVER {rule}

## Examples
{Concrete examples of compliant vs. non-compliant behavior}
```

**Key conventions:**
- Use MUST/MUST NOT/NEVER (prescriptive language — Lesson from AI-DWG Rule 1)
- Keep rules binary (pass/fail, not judgment calls)
- Include examples when a rule might be ambiguous
- Reference source (which AP document or ADR justified this rule)

---

## Steering vs. Hooks vs. Agents

| Mechanism | When Active | Enforcement | Best For |
|-----------|-------------|-------------|----------|
| **Steering files** | During AI session (context) | Advisory — AI follows rules but can be overridden | Coding standards, architecture constraints, project context |
| **Hooks** | On IDE events (triggers) | Blocking — fires automatically, can prevent actions | Pre-commit checks, PR validation, file-edit enforcement |
| **Agents** | At workflow milestones | Active — runs as separate AI invocation | Process governance, architecture review, compliance checks |

Steering sets the CONTEXT. Hooks enforce AUTOMATICALLY. Agents provide ACTIVE GOVERNANCE. All three work together — steering informs hooks and agents.

---

## Related Documents

| Document | Location |
|----------|----------|
| How Package Installation Works | `knowledge_docs/HOW_PACKAGE_INSTALLATION_WORKS.md` |
| How Multi-Platform Support Works | `knowledge_docs/HOW_MULTI_PLATFORM_SUPPORT_WORKS.md` |
| How DWG Generation Engine Works | `knowledge_docs/HOW_DWG_GENERATION_ENGINE_WORKS.md` |
| How GCE Derivation Pipeline Works | `knowledge_docs/HOW_GCE_DERIVATION_PIPELINE_WORKS.md` |
| How to Prepare a Development Workspace | `knowledge_docs/HOW_TO_PREPARE_A_DEVELOPMENT_WORKSPACE.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-24 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
