---
name: paperzilla-monitor
description: Monitor and discuss research papers from one Paperzilla project using the `pz` CLI inside OpenClaw. Use when users want recent papers, metadata, markdown-based summaries, why a paper matters for current work, a recurring weekday brief, or Paperzilla feed triage in chat.
version: 1.1.4
homepage: https://docs.paperzilla.ai/guides/cli
license: MIT
allowed-tools: [exec, message]
metadata:
  skill-author: "Paperzilla Inc"
  openclaw:
    requires:
      bins: ["pz"]
      config:
        - "Paperzilla CLI already authenticated locally"
        - "OpenClaw message routing already configured by host"
    homepage: "https://docs.paperzilla.ai/guides/cli"
---

# Paperzilla research briefs

Use this skill when the user wants one of these two workflows:

- `on_demand_discussion`: discuss the latest papers from one Paperzilla project, inspect one paper, fetch markdown, summarize it, explain why it matters for "our work", and continue the discussion
- `weekday_brief`: produce one concise weekday research brief for one Paperzilla project

This is a workflow skill built on top of the same Paperzilla access layer as the core `paperzilla` skill. It should feel opinionated and repeatable.

## Prerequisites

- Ensure `pz` CLI is installed and authenticated (`pz login` already done).
- Use OpenClaw tools:
  - `exec` for `pz` commands
  - `message` only when the user explicitly asks to deliver a digest/summary to a chat, or when the current profile explicitly requires scheduled external delivery

If `pz` is missing, run `which pz` and tell the user setup is required before continuing.

## Security model

- This skill is primarily a **Paperzilla read/triage** skill.
- It may use the `message` tool only for profile-approved delivery behavior or explicit user-requested delivery.
- It must **not** send unsolicited or proactive messages outside the profile's delivery rules.
- It must **not** read arbitrary system files, unrelated environment variables, or unrelated credentials.
- It assumes `pz` is already installed and authenticated by the human via `pz login`.
- It assumes OpenClaw messaging is already configured by the host platform. The skill does not acquire, mint, or modify credentials.

## What this skill needs

- One Paperzilla project
- One short sentence for "our work" if that context is not already known

If either is missing, ask once and then reuse it for the rest of the workflow.

Examples:

- `Project: Agents evaluation`
- `Our work: we build evaluation infrastructure for coding agents.`

## Transport rules

Follow the transport required by the current profile.

### CLI profiles

Use the Paperzilla CLI (`pz`).

Core commands:

```bash
pz project list
pz project <project-id>
pz feed <project-id> --limit 20 --json
pz rec <project-paper-id> --json
pz rec <project-paper-id> --markdown
pz paper <paper-id> --json
pz paper <paper-id> --markdown
pz paper <paper-id> --project <project-id>
pz feedback <project-paper-id> upvote
pz feedback <project-paper-id> star
pz feedback <project-paper-id> downvote --reason not_relevant
pz feedback <project-paper-id> downvote --reason low_quality
pz feedback clear <project-paper-id>
```

Use `--json` whenever you need structured feed or metadata parsing.

Keep the Paperzilla object model straight:
- `pz paper <paper-ref>` = canonical paper
- `pz rec <project-paper-ref>` = recommendation inside one project
- `pz feedback <project-paper-ref> ...` = project-specific feedback on that recommendation

When an item comes from `pz feed --json`, prefer `pz rec` and `pz feedback` over `pz paper`.

CLI markdown behavior differs by command:

- `pz rec --markdown` can queue markdown generation and prints a friendly retry message when it is still being prepared
- `pz paper --markdown` only returns markdown when it is already ready

### MCP profiles

Use the Paperzilla MCP tools directly.

Core tools:

- `projects_list`
- `projects_get`
- `feed_get`
- `paper_get`
- `paper_markdown`

Preferred sequence:

1. `projects_list` when the project is missing or ambiguous
2. `projects_get` to confirm project identity when needed
3. `feed_get` to pull the latest feed items
4. `paper_get` for one paper's metadata
5. `paper_markdown` for markdown-backed analysis

Handle `paper_markdown` statuses correctly:

- `ready`: use the markdown
- `queued`: tell the user it is still being prepared and suggest retrying shortly
- `unavailable`: report that markdown is not currently available

## Shared behavior rules

- Treat Paperzilla relevance and ranking as a strong prior, not the final answer.
- Use Paperzilla terms exactly: `project`, `feed`, `Must Read`, `Related`.
- Name the exact paper or recommendation identifier you used when you inspect one paper.
- Separate metadata from interpretation.
- Explain relevance in terms of the user's actual work, not generic importance.
- Do not dump full markdown unless the user explicitly asks for it.
- Do not switch to arXiv HTML/abs links as the default fallback when the request was specifically for Paperzilla markdown.

## Mode 1: on-demand discussion

Use this mode when the user wants an interactive paper conversation in chat.

### Workflow

1. Resolve the project and the "our work" context.
2. Pull the latest papers from that project's feed.
3. Show a short list of the newest or strongest candidates.
4. When the user picks one paper, return metadata first.
5. Fetch markdown for that paper or recommendation.
6. Summarize:
   - contribution
   - method
   - results
   - limits
   - why it matters for our work
7. Continue the discussion and make a recommendation such as:
   - read now
   - keep as Related
   - ignore this week

### Output contract

For the first feed reply, include:

- project name
- the papers you checked
- per paper: title, date, source, and whether it looks `Must Read` or `Related`

For the metadata reply, include:

- title
- authors
- publication date
- source
- URL
- the exact Paperzilla paper ID or project-paper ID used

For the markdown reply, include:

- contribution
- method
- results
- limits
- why it matters for our work

## Mode 2: weekday brief

Use this mode when the user wants one concise recurring brief for one project.

### Workflow

1. Resolve the project and the "our work" context.
2. Load the per-project history of papers already proposed in earlier weekday briefs.
3. Pull the newest papers from the feed.
4. Exclude papers that were already proposed in earlier weekday briefs unless the user explicitly asked to revisit them.
5. Select the remaining papers worth mentioning.
6. For each selected paper, give:
   - one short summary
   - one sentence on why it is relevant to our work
7. After drafting or sending the brief, append the exact Paperzilla IDs used for the selected papers to that project's proposed-paper history.
8. If no new papers qualify, say that explicitly.

### Output contract

Every weekday brief should include:

- project name
- date
- how many new papers were checked
- for each selected paper:
  - title
  - one short summary
  - one sentence on why it is relevant to our work
- a clear `No new papers today.` line when nothing new qualifies

Keep the brief concise and easy to scan.

For recurring runs, the agent must keep a persistent per-project record of the exact Paperzilla IDs already proposed in earlier briefs. Do not propose the same paper again in a later recurring brief unless the user explicitly asked to revisit it.

## Feedback loop on request

If the user wants to tune future recommendations:
1. Use `pz feedback ...` on the recommendation ID.
2. Explain that feedback is project-specific.
3. Use:
   - `upvote` for positive signal
   - `star` for strongest positive signal
   - `downvote --reason not_relevant` for topical mismatch
   - `downvote --reason low_quality` for weak paper quality
   - `feedback clear` to remove prior signal

## Edge cases

- **No project given:** ask once, then continue.
- **No "our work" context:** ask once for one short sentence, then reuse it.
- **No prior brief history:** treat the run as the first brief for that project, initialize an empty proposed-paper history, and persist the papers selected this time.
- **No new papers:** report that clearly instead of padding the brief.
- **Large feed:** use a sensible limit first, then expand only if needed.
- **Markdown delay:** retry more than once when the user explicitly asked for markdown. Prefer a short polling loop over an immediate fallback.
- **Ambiguous paper ID:** fall back to the full UUID or clearly restate the paper you selected.
- **External delivery requests:** if the user did not explicitly ask for delivery and the profile does not require delivery, do not use the `message` tool.
- **Canonical vs recommendation confusion:** if an ID came from `pz feed --json`, assume it is a recommendation ID unless shown otherwise.

## Agent-specific rules

Read and follow any packaged `AGENT.md` file for the current profile. The profile file defines the chat surface, delivery surface, and scheduling behavior.
