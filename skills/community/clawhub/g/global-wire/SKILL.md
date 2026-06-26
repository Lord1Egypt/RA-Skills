---
name: global-wire
description: Turn answers about major world events into wire-style briefings, rolling event timelines, verification notes, and alert bullets with stable formatting, source priority, and confidence labels. Use when the user asks what happened today, wants a professional global news briefing, needs a conflict or policy timeline, or asks whether a fast-moving report is credible.
metadata: {"openclaw":{"emoji":"📰"}}
---

# GlobalWire

Use this skill when the user wants major world news to read like a professional wire desk instead of a loose AI summary.

Track major world events like a wire desk: professional briefings, credibility labels, and rolling timelines.

GlobalWire is an editorial skill, not a crawler framework.

Default assumption:

- the current model or active workflow may already have found the core answer
- GlobalWire's main job is to normalize, tighten, and publish that answer
- only add extra search when the answer is clearly incomplete or weakly sourced

When the user asks in Chinese, default to fully Chinese section labels and Chinese confidence labels. Do not leave English field names in a Chinese-only response unless the user explicitly asks for bilingual formatting.

## Quick start

Example natural-language prompts:

- `今天发生了什么重大新闻？按 GlobalWire 格式输出。`
- `Use $global-wire to summarize today's biggest global events in Chinese.`
- `Use $global-wire to build a full timeline of the 2026 US-Iran conflict.`
- `Use $global-wire to verify how credible this report is.`

Example explicit invocations:

- `$global-wire`
- `/global_wire`

On surfaces that sanitize slash-command names, the display name remains `GlobalWire` while the command may appear as `/global_wire`.

## Product promise

GlobalWire should feel like a newsroom editor handling a rough draft:

- cleaner structure
- lower noise
- clearer fact versus analysis separation
- stronger timeline discipline
- explicit confidence labels
- stronger focus on globally consequential developments
- concise, reusable markdown output

## Core modes

Pick one primary mode:

1. `brief`
   - Use for daily or on-demand major-news summaries.
   - Return `3-5` independent cards by default, but prefer fewer stronger cards over padding.
   - Expand to at most `8` on unusually heavy days.
   - If there is no clear global-level top event, say so and add `Still worth watching`.
   - Require clear global spillover for inclusion in the main card list.

2. `timeline`
   - Use for a continuing event.
   - Default to the event's full arc from its start to today.
   - Write event development, not media history.

3. `verify`
   - Use when the user asks whether a claim or summary is reliable.
   - Grade reliability; do not pretend to be an absolute fact-checking authority.

4. `alert`
   - Use for fast, developing, high-impact events.
   - Keep the first pass short and explicit about uncertainty.

## Result-first workflow

1. Start from the best answer already available in context.
2. If the answer is obviously thin, add light evidence patching.
3. Reorganize into the correct GlobalWire mode.
4. Apply timeline, formatting, source-priority, and confidence rules.
5. Save to markdown when requested or when the workflow is archival.

## Search stance

Do not default to heavy browser automation or multi-platform orchestration.

Preferred order:

1. current model's native search result or answer
2. user-provided answer or draft
3. targeted web search or source checking only when needed
4. browser automation only as a last-resort patch path

Read `{baseDir}/references/source-priority.md` before adding or revising sources.

## Hard editorial rules

1. Keep sports, entertainment, local social incidents, and small funding rounds out of the default major-news brief.
2. Separate `Facts` from `Analysis` every time.
3. Do not write media coverage history as if it were event history.
4. Do not upgrade weakly sourced timelines into high-confidence narratives.
5. Domestic sources can supplement, but should not dominate major conflict or geopolitics timelines.
6. Social posts and prediction markets are weak signals, not factual anchors.
7. Do not pad with assistant chatter, moral framing, or generic commentary.
8. Do not pad the daily brief with entertainment, sports, or low-spillover items just to hit a card count target.
9. Keep confidence labels clean; if nuance is needed, explain it in a note, not by bloating the label.
10. In Chinese output, localize the briefing header, section labels, confidence labels, and watchlist labels.

## References to load

Always use:

- `{baseDir}/references/output-modes.md`
- `{baseDir}/references/timeline-rules.md`
- `{baseDir}/references/credibility-rules.md`
- `{baseDir}/references/source-priority.md`
- `{baseDir}/references/formatting-rules.md`

Use as needed:

- `{baseDir}/references/exemplars.md`
- `{baseDir}/references/file-layout.md`

## Output contract

Always show:

- a style line
- a length line

Default style is always `wire` unless the user explicitly asks otherwise.

Supported voice modes:

- `wire`
- `brief`
- `analyst`

Translate visible labels to match the user's language while preserving structure and meaning.

Preferred visible labels:

- English: `Current style`, `Current length`
- Chinese: `当前风格`, `当前长度`
