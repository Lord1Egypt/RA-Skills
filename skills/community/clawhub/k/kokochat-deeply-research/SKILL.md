---
name: kokochat-deeply-research
version: 0.5.0
description: "Deep-research course generator for the KokoChat Deeply mini-app. Phase A side of a two-phase pipeline: use the `kokochat-search` skill plus `web_fetch` to collect real sources, narrate the research in Chinese prose, and emit one `koko.deeply.research.notes` fenced block with synthesis + a flat sources list. Phase B runs as a separate stateless inference and turns those notes into the course outline. Fires when the user message looks like '请围绕「<topic>」做一份深度调研课程'."
author: komako-workshop
license: Apache-2.0
tags: [latest, kokochat, deeply, research, course, web-search, two-phase]
triggers:
  - 请围绕「
  - 深度调研课程
  - kokochat deeply research course
  - koko.deeply.research.notes
metadata:
  openclaw:
    emoji: "🔍"
    requires:
      skills:
        - kokochat-search
      capabilities:
        - network
      platforms:
        - linux
        - darwin
        - windows
---

# kokochat-deeply-research

OpenClaw side of the KokoChat **Deeply** mini-app's deep-research course path.
The user is in a `deeply-course` conversation created from the "定制课程" sheet
with `kind = "research"`.

## Two-phase pipeline (this skill is Phase A)

KokoChat splits research course generation into two model passes:

- **Phase A — this turn (the agent run you are in now)**: research only.
  Search the web, narrate the process to the user in Chinese prose, and emit
  one `koko.deeply.research.notes` fenced block at the end containing a
  300–1200 字 synthesis plus a flat list of 5–20 cited sources. You do
  **not** decide on course sections, write section titles, or assign sources
  per section — those are Phase B's job.

- **Phase B — separate stateless `inferOnce` the client triggers right after
  you finish**: the same agent, but no web tools available. Phase B reads
  your notes block, decides how many sections to use, and emits the final
  `koko.deeply.research.outline` JSON. You will never see Phase B run; just
  hand off clean notes and Phase B will handle the rest.

This split exists because asking one turn to plan tools, narrate prose, AND
emit a strict per-section JSON schema repeatedly burned attention budget on
the schema and led to "toolCallCount=0 but plausible-looking sources" — the
2026-05-28 hallucination regression.

## When this skill fires

The first user message in the conversation looks exactly like:

> 请围绕「<topic>」做一份深度调研课程

(or with an explicit `N` 节 between `做一份` and `深度调研课程` when the user
chose a non-auto length in the sheet). When you see this shape, run the
procedure below. For any later user message in the same conversation, just
respond to the host's mainline prompt — KokoChat re-injects a fresh prompt on
every turn.

## What the host sends with the kickoff

KokoChat injects a Phase A kickoff prompt right before the visible user line.
That prompt is the authoritative source of truth for **this turn's hard
constraints** (3 numbered rules), the `koko.deeply.research.notes` JSON
schema, and the prose sentinel `〔KP〕` requirement. **Always follow what the
kickoff prompt says.** Do not produce a `koko.deeply.research.outline` block
from this turn — that schema belongs to Phase B and emitting it here will be
ignored.

This skill file only adds background you need across all such turns: what
the search/fetch tools can / cannot do, and how to plan the research itself.

## Tools

The deeply agent uses KokoChat's hosted search wrapper plus OpenClaw's built-in
`web_fetch`.

### KokoChat hosted search (`kokochat-search`)

Run a web search via the local exec wrapper installed by KokoChat. The
KokoChat Runtime Contract in `AGENTS.md` gives the exact absolute path for
the wrapper; use that command shape:

```bash
<kokochat-search/bin/search.mjs absolute path> '{"query":"EN keywords","count":5}'
```

It calls KokoChat's hosted search proxy (Brave-backed in production), so the
user does not need to configure any search API key in their own OpenClaw.
Returns title / url / snippet per result.

Args:

- `query` (string, required): EN keywords. Translate Chinese topics into
  English search keywords; keep user-facing prose Chinese.
- `count` (int 1–10, optional): default ~5; lower for targeted lookups,
  higher when scoping broadly.

Pass **only** `query` and `count`. Provider-specific args like
`domain_filter`, `date_after`, `freshness`, `country`, `language`,
`max_tokens` will be rejected.

Tool quirks worth knowing:

- The wrapper may return `{ "ok": false, "error": "..." }` if KokoChat's
  hosted search is unavailable or rate-limited. Be honest; do not invent URLs.
- Don't batch multiple search calls in one assistant turn — issue them
  sequentially across narration steps.

### `web_fetch`

Pull one URL's main content as readable text. Useful when a search hit
looks unusually authoritative and you want the actual body instead of just
the snippet.

Args:

- `url` (string, required).
- `maxChars` (int, optional): prefer `60000` so the model sees enough body.
  The Gateway may cap this lower.

Only fetch `http://` / `https://` URLs that came from a successful
KokoChat search. Never fetch `file://`, skill files, workspace docs, or URLs
you invented. If a fetch fails (network block, private-IP guard, challenge,
timeout), don't retry many other URLs — continue from search snippets.

## Research Planning (generic; no hard-coded domain templates)

Before searching, infer a small research plan **from the user's topic
itself**. Don't insert fixed people, organisations, industries, or examples
that the user didn't mention.

Identify:

1. **Key subjects**: people / organisations / works / events / markets /
   technologies / concepts named or implied by the topic.
2. **Time and scope**: year, geography, stage, version, comparison target,
   or other limits.
3. **Controversy structure**: mainstream view, counter-view, boundary
   conditions, common misreadings likely relevant.
4. **Best evidence types**: primary text, interview, transcript, filing,
   paper, policy document, official data, high-quality secondary synthesis.

Queries should start with the exact topic and key subjects, then expand to
counterpoints / background / more authoritative original evidence. Avoid
filling sources with broad trend pages when narrower material exists. If a
topic is very narrow, **prefer fewer real sources over more weak ones**.

## What is NOT in this skill any more

Schema, field rules, prose sentinel marker (`〔KP〕`), exact step-by-step
narration order, and the "3 hard rules" all live in the host-injected
Phase A kickoff prompt now. Treating those as the source of truth keeps this
file small and stops the model from being overwhelmed by duplicated, slightly
divergent instructions across two layers (which is exactly what caused the
2026-05-28 regression where the model emitted plausible-looking sources
without ever calling search).

The `koko.deeply.research.outline` schema (per-section sources, course
introduction, outline markdown) lives entirely in the Phase B prompt and is
**not** part of Phase A's output.
