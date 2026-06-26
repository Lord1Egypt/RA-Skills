# OpenClaw Seed Blocks

Use these as additive seed blocks in the active OpenClaw workspace.
Patch the smallest relevant section. Do not replace the whole file.

Official template anchors:
- AGENTS.md -> `## Session Startup` and `### Write It Down - No "Mental Notes"!`
- SOUL.md -> append near `## Continuity`
- HEARTBEAT.md -> append only if the file is meant to do periodic work

## AGENTS.md Seed

Insert after the default startup list in `## Session Startup`:

```markdown
## Hermes Agent Seed (DO NOT EDIT BLINDLY)

Before non-trivial work:
1. Read `~/hermes-agent/memory.md` if it exists.
2. Read at most one additional Hermes file only if the task clearly needs it.
3. Prefer existing lessons before inventing a new workflow.
4. Skip Hermes retrieval for trivial replies, casual chat, and one-shot questions.

After significant work:
1. Compare result vs intent.
2. Write one reusable lesson to `~/hermes-agent/reflections.md` if needed.
3. If the lesson should shape future behavior, distill it into `~/hermes-agent/memory.md`.
4. If the pattern repeats, log it in `~/hermes-agent/promotions.md`.
```

Inside `### Write It Down - No "Mental Notes"!`, add these routing bullets without removing the existing ones:

```markdown
- Reusable execution lesson -> write to `~/hermes-agent/reflections.md`
- Stable repeated rule -> distill to `~/hermes-agent/memory.md`
- Candidate workflow after repeated success -> log to `~/hermes-agent/promotions.md`
```

## SOUL.md Seed

Append near `## Continuity` or at the end. Keep it tiny because SOUL.md is injected every turn:

```markdown
## Hermes Pressure

Retrieve before acting on non-trivial work.
After meaningful work, pause long enough to capture one reusable lesson.
Prefer precise additive learning over noisy self-commentary.
```

## HEARTBEAT.md Seed

Append only if heartbeat maintenance is desired. Keep it smaller than AGENTS.md:

```markdown
## Hermes Maintenance

- [ ] Review `~/hermes-agent/reflections.md` for lessons worth distilling
- [ ] Review `~/hermes-agent/promotions.md` for patterns ready to become skills
- [ ] Keep `~/hermes-agent/memory.md` short and current
```

## Install Rule

- Ask before writing any seed block.
- Keep one seed block per file.
- If the file already contains equivalent guidance, merge instead of duplicating.
