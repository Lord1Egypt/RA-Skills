---
name: persona-spawn
description: Spawn subagents with personas from a local workspace library or the Emblem persona marketplace. Use when a task needs a different voice, expertise, or operating style; when the user says "use persona X", "spawn as Y", or "have a specific character do this"; when you need shared org context such as a foundation doc injected into every persona spawn; or when offloading a bounded task to a persona-preserving subagent is better than changing the current agent's own identity. Not for trivial tasks, changing your own persona in-place, or bypassing local subagent policy.
---

# Persona Spawn

Use this skill to ensure the local persona library exists, assemble a deterministic persona prompt, and spawn a subagent without letting workspace persona files override the requested persona.

## Files

Keep personas in the current workspace:

```text
<workspace>/personas/
├── config.json
├── index.json
├── the-mandalorian/
│   ├── SOUL.md
│   ├── IDENTITY.md
│   └── persona.json
└── <custom-persona>/
    ├── SOUL.md
    ├── IDENTITY.md
    └── persona.json
```

`personas/config.json` is the shared org-context config. Put docs there that every persona spawn should inherit, such as Kru foundation rules, brand standards, or execution rules.

Read `references/api-endpoints.md` only when importing or validating marketplace data.
Read `references/soul-guide.md` only when authoring a new custom persona.

## First use

Before resolving personas, ensure the local library exists:

```bash
python3 <skill_dir>/scripts/ensure-personas.py <workspace> <skill_dir>
```

If the workspace has no local persona library yet, this bootstraps bundled starter personas and creates `personas/config.json`.

## Shared org context config

Create or edit:

```json
{
  "context_files": [
    "../_System/Motoko-Kru-Foundation.md",
    "../Resources/Coding-Subagent-Contract.md"
  ]
}
```

Rules:
- Accept `context_files` as either an array or a comma-separated string.
- Resolve relative paths from `personas/config.json`.
- Use shared context for durable org rules, not persona-specific flavor.

## Workflow

### 1. Respect local policy first

Before spawning, follow the current workspace policy.
If local `AGENTS.md` or system rules require asking before spawning subagents, ask first.
Do not use this skill to bypass local governance.

### 2. Ensure local personas exist

Run:

```bash
python3 <skill_dir>/scripts/ensure-personas.py <workspace> <skill_dir>
```

Then read `<workspace>/personas/index.json`.

### 3. Resolve the persona

Read:
- `<workspace>/personas/<handle>/SOUL.md`
- `<workspace>/personas/<handle>/IDENTITY.md`
- `<workspace>/personas/<handle>/persona.json`

If the persona is not installed locally, import it first with the bundled importer.

### 4. Build the persona prompt deterministically

Use the bundled builder:

```bash
python3 <skill_dir>/scripts/build-persona-prompt.py \
  <workspace> \
  <handle> \
  --task-file <task.txt>
```

This assembles the prompt in this order:
1. Override directive
2. Org context files from `personas/config.json`
3. Persona SOUL.md
4. Persona IDENTITY.md
5. Task

The override directive tells the spawned agent to ignore conflicting workspace-injected `SOUL.md` / `IDENTITY.md` for persona and tone, while still obeying higher-priority system, developer, safety, and governance instructions.

### 5. Spawn the subagent

Use the normal OpenClaw subagent path with the assembled prompt.
Preferred shape:

```json
{
  "task": "<assembled prompt>",
  "runtime": "subagent",
  "mode": "run",
  "label": "persona:<handle>",
  "runTimeoutSeconds": 300,
  "cleanup": "delete"
}
```

Model guidance:
- Use the caller's default model unless the user requests another one.
- Use a fast model for writing, brainstorming, or stylistic tasks.
- Use a stronger model for analysis, security review, or planning.

### 6. Return the result

The subagent reports back automatically.
- If the user asked for the persona's voice, preserve it.
- Otherwise summarize in your own voice and mention which persona was used.

## Import personas

### Import one

```bash
bash <skill_dir>/scripts/import-persona.sh <handle> <workspace>/personas
```

### Import all

```bash
bash <skill_dir>/scripts/import-persona.sh --all <workspace>/personas
```

### Batch without rebuilding every time

```bash
bash <skill_dir>/scripts/import-persona.sh --no-index <handle> <workspace>/personas
python3 <skill_dir>/scripts/rebuild-index.py <workspace>/personas
```

## Rebuild the local index manually

After adding, removing, or editing personas:

```bash
python3 <skill_dir>/scripts/rebuild-index.py <workspace>/personas
```

## Guardrails

- Do not change your own persona in-place. Spawn another agent instead.
- Do not spawn for trivial one-liners.
- Do not mix multiple personas in one subagent.
- Do not add tone instructions that conflict with the persona.
- Prefer local personas after import.
- Prefer `context_files` for shared org doctrine and execution standards.
- If import fails, report the failure cleanly and suggest nearby installed personas when possible.
