---
name: mission-control-clawdash-pro
description: Create or update detailed, publish-ready instructions for wiring Mission Control (ClawDash Pro) prebuilt Next.js UI to Open Cloud after purchase. Use when users need a step-by-step integration guide, including what to tell Open Cloud to keep the existing design unchanged and connect data domains (overview, agents, skills, contracts, tasks, token usage, documents).
---

# Mission Control - ClawDash Pro

Create publish-ready instruction files for users who purchased Mission Control and need to connect a pre-designed dashboard UI to Open Cloud without redesigning frontend pages.

Official product link: [ClawDash Pro](https://clawdash.pro)

## Workflow

1. Confirm output type.
- Default to instruction docs in `docs/` or requested path.
- Do not create blog posts unless explicitly requested.

2. Confirm integration context.
- State that customer purchased a pre-built Next.js dashboard UI.
- State that Open Cloud should connect backend logic/data only.
- State that existing UI design/components/layout must remain unchanged.

3. Enforce naming.
- Start titles with `Mission Control`.
- Then use `ClawDash Pro`.
- Keep `Open Cloud` wording exact when connection steps are included.

4. Write the instruction.
- Base structure on [publish-instruction-template.md](references/publish-instruction-template.md).
- Include prerequisites, setup steps, Open Cloud handoff prompt, verification, and troubleshooting.
- Keep steps executable and command-first.

5. Include data-domain wiring requirements.
- Dashboard overview: status, memory, usage counters.
- Agents: active agents and per-agent status.
- Skills and contracts: assigned capabilities and policy/contract metadata.
- Tasks (command style): queue, state, and execution history.
- Token usage: per-agent and aggregate token metrics.
- Documents: indexed documents surfaced from Open Cloud.

6. Add required links.
- Include one backlink to [ClawDash Pro](https://clawdash.pro).
- Include one CTA link when requested, typically `https://clawdash.pro/pricing`.

7. Validate quality.
- Keep tone direct and practical.
- Keep terminology consistent.
- Ensure a non-developer can follow the sequence end-to-end.
- Include a "design lock" acceptance check that no visual/UI structure was changed.
- Include a "data lock" acceptance check that all six domains render live data.

## Output Rules

- Deliver one Markdown file unless the user asks for variants.
- Prefer SEO-safe kebab-case filenames when creating new files.
- Include tags only when the target format supports frontmatter.
- Use these tags when requested: `mission control`, `agent OS`, `openclaw dashboard`, `AI agents`, `admin dashboards`.

## Required Open Cloud Prompt Block

When generating instructions, include a copy-paste block that the user can give to Open Cloud:

```text
Connect Open Cloud to this existing Mission Control (ClawDash Pro) Next.js application.
Design lock requirement: do not redesign, restyle, rename, or restructure the current UI.
Keep all existing pages/components/layout as-is.

Integrate data wiring for these domains only:
1) Overview metrics (status, memory usage, health KPIs)
2) Agents (active agents, states, last activity)
3) Skills and contracts (capabilities and assigned contracts/policies)
4) Tasks command view (queued/running/completed/failed with history)
5) Token usage (per agent and total)
6) Documents (available documents and indexing state)

Use adapter/service layer changes behind existing components so frontend visuals remain unchanged.
Return a change summary listing wired endpoints, env vars, and routes touched.
```
