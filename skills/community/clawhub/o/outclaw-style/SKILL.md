---
name: outclaw-style
description: >
  Learn the user's writing style per outreach channel (email, LinkedIn,
  Twitter/X, WhatsApp, Slack, SMS, Discord, Telegram — whatever is
  connected for this tenant). Runs the Prompt Learning Protocol from
  https://gist.github.com/milstan/3b12f938f344f4ae1f511dd19e56adce on
  ≥20 outbound samples per channel (falls back to what's available).
  Triggers on: 'learn my style', 'learn my voice', 'retrain style for
  <channel>', 'style report', 'how's my style score'. Auto-invoked (no
  user prompt) by outclaw-plan when a planned channel lacks a learned
  style for the current tenant.
version: 2.1.33
metadata:
  openclaw:
    emoji: "🎨"
    homepage: https://github.com/leadbay/outclaw
---

# OutClaw — Style

Learns a per-channel style prompt for the **current tenant** and persists
it at `~/.openclaw/outclaw/styles/<tenant>/<channel>_style.md`. Each style
prompt is what `outclaw-plan` uses to draft messages on that channel.

## Resolver mandate

Before writing styles, memory entries, or any KB update, read
`shared/references/RESOLVER.md`. Styles go in
`styles/<tenant>/<channel>_style.md`. NEVER hand-craft a different path.
A trained-style summary goes to tenant memory as
`type=user, key=style_trained_<channel>` so `outclaw-plan` can find it
quickly without re-reading the style file.

## When this skill runs

1. **Explicit user request** — `learn my style`, `retrain style for email`.
2. **Auto-invoked, silent** — when `outclaw-plan` builds a plan that
   includes a channel with no learned style for this tenant, it invokes
   this skill for that one channel, waits for completion, then continues.
   No user prompt. No interruption.

## Prompt Learning Protocol (implements the user's gist)

The gist at https://gist.github.com/milstan/3b12f938f344f4ae1f511dd19e56adce
prescribes:

1. **Sample collection** — gather ≥20 outbound messages per channel (or
   ≥1 000 words / ≥10 pairs, whichever floor is higher). If fewer are
   available, work with what you find; mark `confidence` accordingly.
   **Do not fabricate samples.**
2. **Analysis** — a thinking model identifies dimensions of quality,
   structural/stylistic patterns, anti-patterns the samples avoid.
3. **Candidate prompt** — direct, actionable instructions
   ("Write sentences that average 12-18 words"), target 500-2 000 words,
   with an explicit Avoid section.
4. **Iteration loop (5 cycles default)** per channel:
   - Generate test output with moderate temperature (0.6-0.8)
   - Evaluate against dimensions (0-100 LLM judgments)
   - Track best-of-N
   - Refine (lower temperature 0.2-0.4, focus on lowest-scoring dimensions)
5. **Output**: learned prompt + best score + iteration number + dimensions
   + conformity log. Save to
   `~/.openclaw/outclaw/styles/<tenant>/<channel>_style.md` with YAML
   frontmatter (tenant, channel, trained_at, sample_count, best_score,
   best_iteration, dimensions).

See `references/style-learning.md` for the detailed steps and
`agents/style-learner.md` for the delegated sub-agent spec.

## Per-channel sources (which tools to use)

For each channel we care about, list where outbound samples can be read
from. The agent picks only channels this tenant has `ready` in the
capability map (`capabilities/<tenant>.json`).

| Channel | Sample source |
|---------|---------------|
| Gmail | `gog gmail messages search "from:me" --max 50` |
| LinkedIn | `linkedin-cli posts --author me --max 50` (if connected) or export |
| Twitter/X | `XActions` or direct API via xurl |
| Slack | `slack-mcp-server` message history where sender=me |
| WhatsApp | `whatsapp-mcp-ts` conversation export, filter author=me |
| Telegram | `telegram-mcp` sent messages |
| Discord | `discord-mcp` messages where author=me |
| iMessage/SMS | `mac_messages_mcp` sent messages |
| Bluesky | `bsky-mcp-server` user posts |

## Flow

1. **Pick channels** — from memory `tool_inventory`, enumerate channels
   that have a `ready` plugin AND a sample source. Skip channels with
   no connected plugin entirely (no point training).

2. **For each selected channel**, run a sub-task:
   a. Pull outbound samples via the channel's plugin. Write raw samples
      to `kb/raw/style-<tenant>-<channel>-<ts>.jsonl` (NOT into the KB's
      people/orgs — this is training data, filed under raw/).
   b. If the sample count is <20 or <1 000 words, log a memory
      observation and proceed anyway:
      `{type: observation, key: "style_thin_<channel>", insight:
      "only <N> samples — learned prompt confidence will be lower",
      source: "observed", confidence: 6}`.
   c. Two-stage classify: heuristic pre-filter (outbound, non-trivial
      length, not auto-reply) → LLM OUTREACH_COLD/FOLLOWUP/WARM vs.
      NOT_OUTREACH (see `scripts/message_classifier.py`).
   d. Run the 5-iteration Prompt Learning Protocol
      (`scripts/style_evaluator.py`).
   e. Write the learned style to
      `~/.openclaw/outclaw/styles/<tenant>/<channel>_style.md`.
   f. Log: `{type: user, key: "style_trained_<channel>", insight:
      "<channel> style trained; score <N>/100; <K> samples",
      source: "observed", confidence: <N/10>}`.

3. **If auto-invoked** (from `outclaw-plan`): do ONE channel (the one
   requested), silent, then return to the caller. **NEVER ask the user
   for "preferred tone" or "desired format"** — the whole point of this
   skill is that we infer style from samples. If a channel has no
   outbound samples at all (e.g. user just connected Discord today),
   log an observation:
   `{type: observation, key: "style_nosamples_<channel>",
     insight: "no outbound samples on <channel>; using neutral template",
     source: "observed", confidence: 6}`
   and emit a minimal neutral template at
   `styles/<tenant>/<channel>_style.md` with sample_count: 0,
   best_score: null, and a generic "direct, concise, warm-professional"
   prompt. Return to caller.

4. **If user-invoked**: show a compact report — which channels were
   trained, best score each, sample count, confidence.

## Filing rules (RESOLVER-compliant)

- Style prompt: `styles/<tenant>/<channel>_style.md` — NEVER
  `kb/styles/*`, NEVER `kb/me/styles/*`.
- Raw outbound samples (the training data): `kb/raw/style-<tenant>-<channel>-<ts>.jsonl`.
- Summary for fast lookup: tenant memory, `type=user`,
  `key=style_trained_<channel>`.
- Do NOT put learned styles in `kb/me/self.md` — voice description there
  is for context, the style prompt lives separately.

## Consent

Sample collection is a one-time opt-in, captured during
`outclaw-setup` Step 2 as a memory `preference` entry. If no consent
entry exists when this skill runs:
- Explicit invocation: ask once, record the decision.
- Auto-invocation from plan: proceed only if the tenant has an opt-in
  `style_consent` entry. If missing, log an observation and fall back
  to a neutral template style. Never silently scrape without consent.

## Output format (style prompt file)

```markdown
---
tenant: outclaw
channel: gmail
trained_at: 2026-04-22T12:00:00Z
sample_count: 42
best_score: 82
best_iteration: 3
dimensions: [sentence_length, formality, personalization, cta_style, structure, tone, greeting_pattern, signoff_pattern]
conformity_log:
  - {iter: 1, score: 64}
  - {iter: 2, score: 71}
  - {iter: 3, score: 82}
  - {iter: 4, score: 80}
  - {iter: 5, score: 78}
---

# Gmail style — outclaw (tenant)

## Instructions
<the learned prompt — 500-2000 words, direct + actionable>

## Avoid
- <anti-pattern 1>
- <anti-pattern 2>

## Reference samples
- <path>/raw/style-outclaw-gmail-<ts>.jsonl (not included verbatim here;
  pointer only)
```

This format lets `outclaw-plan` parse the "Instructions" section directly
into the draft-generation prompt.
