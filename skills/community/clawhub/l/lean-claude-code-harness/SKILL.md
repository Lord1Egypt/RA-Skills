---
name: lean-claude-code-harness
description: Use when building, auditing, or simplifying an AI coding-agent harness, especially when the current runtime has unclear config precedence, weak tool permissions, hidden product-only behavior, or poor transcriptability.
metadata:
  {
    "openclaw": {
      "emoji": "🪶"
    }
  }
---

# Lean Claude Code Harness

Distill the durable parts of Claude Code into a smaller, auditable harness. The goal is not feature parity. The goal is a runtime another engineer can understand, extend, and verify without reverse-engineering hidden behavior.

## When to Use

Use this skill when a coding-agent runtime shows any of these symptoms:

- config values are hard to trace
- tool permissions are implicit or inconsistent
- the tool surface keeps growing without clear ownership
- session history disappears after a run
- the main loop is hard to sketch from memory
- product-only logic is mixed into the harness core

## Keep These Primitives

- layered configuration
- permission-aware tool execution
- a small explicit tool registry
- markdown skill discovery
- transcript persistence
- a visible query loop

## Remove These By Default

- telemetry
- remote-managed settings
- hidden kill-switches
- private feature flags
- branding-specific branches
- heavyweight UI layers

Only add them back when the user explicitly asks for them and can explain the operational need.

## Quick Audit

If you need a fast harness review, answer these six questions first:

1. Can you explain config precedence without reading three files?
2. Are tool permissions checked before execution?
3. Can you list the built-in tools in one screen?
4. Are skills discovered from visible files instead of hidden registration?
5. Does every run persist a transcript?
6. Can you trace the query loop from prompt to final response?

If two or more answers are "no", the harness is already too opaque.

## Apply This Order

### 1. Freeze the Runtime Boundary

Keep the entrypoint thin. It should only:

- parse commands
- load merged config
- wire services
- print results

Do not hide business logic in the CLI layer.

### 2. Make Config Precedence Explicit

Use a predictable merge order:

1. defaults
2. user config
3. project config
4. local config
5. environment overrides

If a runtime value cannot be traced back to one of these sources, the harness is already drifting into opacity.

### 3. Gate Tools Before Execution

Define permission policy before the query loop runs tools.

Minimum pattern:

- `default` and `plan` expose read-only tools
- write or shell tools require a stronger mode
- `bypassPermissions` should be explicit and rare

Permission checks belong before tool execution, not after damage is already possible.

### 4. Start with a Tiny Tool Surface

Default tool set should be boring and legible:

- `list_files`
- `read_file`
- `grep`
- `bash`

Do not add tools because the upstream product has them. Add tools only when they expand capability without making the harness harder to reason about.

### 5. Keep Skills File-Backed

Discover skills from `SKILL.md` files with frontmatter metadata. Avoid hidden registration layers, magic imports, or remote skill switches.

The discovery rule should be explainable in one sentence: scan configured directories, parse frontmatter, expose name, description, and path.

### 6. Persist Every Session

Save transcripts to disk. Each transcript should include:

- session id
- timestamp
- prompt
- tool steps
- final response

If an agent run cannot be inspected afterward, debugging and trust both degrade.

### 7. Keep the Query Loop Visible

The harness should make this loop easy to trace:

1. receive prompt
2. ask provider for next action
3. validate tool request
4. execute tool
5. append tool result to state
6. repeat until final response
7. persist transcript

If you cannot sketch the loop from memory, the runtime is already too opaque.

## Anti-Patterns

- cloning upstream complexity without upstream context
- mixing config loading, permission logic, and tool execution in one file
- treating remote flags as architecture instead of distribution policy
- adding analytics before the harness can explain itself locally
- claiming a harness is complete without transcript and permission tests

## Minimal Verification

Before calling the harness usable, verify:

- config precedence behaves as documented
- permission modes actually filter tools
- skill discovery finds real `SKILL.md` files
- session persistence writes and reloads transcripts
- the full query loop works with a deterministic provider

The verification standard is simple: no claims about the harness until the config, permission, skills, session, and loop seams are each exercised once.

## Use This Skill To

- design a fresh coding-agent harness
- simplify a bloated Claude Code-style runtime
- review an existing agent runtime for opacity and unnecessary layers
- extract reusable harness patterns from a larger codebase

## Do Not Use This Skill To

- recreate the full Claude Code product surface
- justify hidden behavior with “that is how the upstream does it”
- add cloud control planes, telemetry, or feature flags without a concrete requirement

## Output Standard

When applying this skill, produce:

- the minimal harness shape
- the layers kept vs removed
- the exact config precedence
- the permission model
- the smallest verification plan that proves the harness is real
