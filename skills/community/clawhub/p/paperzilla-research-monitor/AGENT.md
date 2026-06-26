# OpenClaw profile rules

Use this profile for:

- live paper discussion in Telegram or another OpenClaw chat surface
- weekday research briefs delivered to Telegram

## Surfaces

- On-demand discussion surface: the current chat, preferably Telegram when available
- Weekday brief delivery surface: Telegram

## Tooling

- Use OpenClaw `exec` for Paperzilla CLI calls
- Use OpenClaw `message` for Telegram delivery when this profile needs external delivery or when the user explicitly asks to send elsewhere
- Do not require MCP integrations for this profile

Use the Paperzilla CLI directly:

```bash
pz project list
pz project <project-id>
pz feed <project-id> --limit 20 --json
pz rec <project-paper-id> --json
pz rec <project-paper-id> --markdown
pz paper <paper-id> --json
pz paper <paper-id> --markdown
```

Keep the object model straight:

- use `pz rec ...` for recommendation IDs returned by `pz feed --json`
- use `pz paper ...` for canonical paper IDs

If "our work" is missing, ask once for one sentence and then reuse it.

## Mode: on-demand discussion

Keep the discussion in the current chat. If the current chat is Telegram, that is the default live surface.

Default behavior:

- show the latest papers from one project
- let the user pick one paper
- return metadata first
- then fetch markdown and explain why it matters for our work
- keep the discussion going in chat

When discussing one paper, include:

- title
- authors
- publication date
- source
- URL
- exact Paperzilla ID used
- contribution
- method
- results
- limits
- why it matters for our work

If markdown is still being prepared, say so, retry shortly, and prefer `pz rec --markdown` before any fallback when the paper came from a feed item.

## Mode: weekday brief

Use Telegram as the default delivery surface for the recurring brief.

Default behavior:

- produce one concise weekday brief for one project
- if the current run is a scheduled or external-send run, send the brief through the `message` tool to Telegram
- if the brief is sent externally and no chat reply is needed, return `NO_REPLY`
- if this is a user-initiated interactive run, keep the response in chat unless the user explicitly asked to send it elsewhere
- keep a persistent per-project history of the exact Paperzilla IDs already proposed in earlier weekday briefs
- exclude previously proposed papers from later weekday briefs unless the user explicitly asked to revisit them
- after sending or drafting the brief, update that history with the exact Paperzilla IDs included in the brief

Persist that proposed-paper history in the scheduling job state or another profile-owned memory surface that survives to the next run.

The weekday brief must include:

- project name
- date
- how many new papers were checked
- for each selected paper:
  - title
  - one short summary
  - one sentence on why it is relevant to our work
- `No new papers today.` when nothing new qualifies

Suggested Telegram-friendly format:

📚 Paperzilla brief — [Project Name]
[Date] · [N] new papers checked

- [Title](url) — short summary
  Why it matters: one sentence tied to our work

If no new papers qualify:

📚 Paperzilla brief — [Project Name]
[Date]

No new papers today.

## Delivery guardrails

- For scheduled weekday brief runs, this profile may send externally via `message`.
- For normal interactive runs, keep the output in chat unless the user explicitly asked for external delivery.
- If destination is ambiguous, confirm once before sending.
- Do not send proactive nudges, automatic follow-ups, or unrelated summaries under this profile.
