# Setup - Hermes Agent

Read this when `~/hermes-agent/` does not exist or is empty. Do not lead with setup language or internal file names. Help first, then install the smallest Hermes loop that will keep working in future sessions.

## Goal

Make OpenClaw behave more like Hermes without bloating every turn.
The loop should be:
- visible in AGENTS.md for routing and retrieval
- optional in SOUL.md for self-correction pressure
- tiny in HEARTBEAT.md for maintenance only
- stored locally in `~/hermes-agent/` for durable lessons

## Priority Order

### 1. First: Integration

Within the first 2-3 exchanges, learn how the user wants Hermes behavior to show up:
- always on for non-trivial work
- only after failures and corrections
- only when explicitly asked
- never in certain repos, channels, or projects

Save that integration preference to the user's main OpenClaw memory only if the path is already clear in the current workspace and the user wants that preference to persist outside Hermes. Otherwise keep it in `~/hermes-agent/` until clarified.

If the user already asked for a concrete task, answer that task first, then tighten integration.

### 2. Then: Create the Hermes Files

Create this structure:

```bash
mkdir -p ~/hermes-agent/archive
touch ~/hermes-agent/{memory.md,promotions.md,reflections.md,workspace-state.md}
```

Initialize `~/hermes-agent/memory.md` from `memory-template.md`.

Use these files with strict scope:
- `memory.md` = HOT, always read before non-trivial work
- `promotions.md` = repeated workflows that may become stable rules or skills
- `reflections.md` = post-task lessons before distillation
- `workspace-state.md` = which workspace files were seeded and what each seed does

### 3. Then: Patch the Active OpenClaw Workspace

Use the official OpenClaw workspace templates as reference. The template AGENTS.md says Session Startup reads SOUL.md, USER.md, daily memory, and MEMORY.md. Those bootstrap files are injected on every run, so keep Hermes additions compact.

Apply edits non-destructively and only in these places:

#### AGENTS.md

If the workspace follows the default OpenClaw template, patch two places.

1. Inside `## Session Startup`, after the existing startup list, add a compact Hermes retrieval block:

```markdown
### Hermes Retrieval

For non-trivial work only:
- Read `~/hermes-agent/memory.md` if it exists.
- Read at most one additional Hermes file if the task clearly needs it.
- Skip Hermes retrieval for trivial replies, casual chat, and one-shot questions.
```

2. Inside `### Write It Down - No "Mental Notes"!`, refine the memory routing bullets:

```markdown
- Reusable execution lesson -> write to `~/hermes-agent/reflections.md`
- Stable repeated rule -> distill to `~/hermes-agent/memory.md`
- Candidate workflow after repeated success -> log to `~/hermes-agent/promotions.md`
- Keep Hermes files short and operational; do not duplicate daily-log history there
```

#### SOUL.md

Only patch SOUL.md if the user wants stronger self-correction pressure on every run.
Append this exact block near `## Continuity` or at the end:

```markdown
## Hermes Pressure

Retrieve before non-trivial work.
Reflect after meaningful work.
Prefer one distilled lesson over noisy self-commentary.
```

Do not add more than these three lines unless the user explicitly wants a heavier persona shift.

#### HEARTBEAT.md

Only patch HEARTBEAT.md if the user wants periodic maintenance.
The official template keeps this file empty unless periodic checks are needed, so append only these bullets:

```markdown
## Hermes Maintenance

- [ ] Review `~/hermes-agent/reflections.md` for lessons worth distilling
- [ ] Review `~/hermes-agent/promotions.md` for patterns ready to become skills
- [ ] Keep `~/hermes-agent/memory.md` short and current
```

Do not turn HEARTBEAT.md into a second AGENTS.md.

### 4. Finally: Verify Token Discipline

The token policy is:
- AGENTS.md carries routing logic
- SOUL.md carries tone pressure only if needed
- HEARTBEAT.md carries maintenance only if needed
- `~/hermes-agent/memory.md` is the only Hermes file read by default before non-trivial work
- read at most one more Hermes file unless the task clearly needs more

If the user sounds unsure, start with local Hermes memory only and postpone workspace edits.

## What You Are Saving Internally

Save only what changes future execution quality:
- integration preference
- which workspace files were extended
- active reflection policy
- promotion threshold or promotion preference
- current exclusions such as "never touch this repo" or "do not edit SOUL.md"

If the user declines file edits, keep Hermes in local memory only and continue helping.

## Guardrails

- Ask before writing to workspace files.
- Ask before writing to any main OpenClaw memory file outside `~/hermes-agent/`.
- Patch the smallest matching section; never replace the whole file.
- Never claim OpenClaw has a native learning loop if you are simulating it with local files and seed blocks.
- Keep Hermes additions smaller than the surrounding template section whenever possible.
