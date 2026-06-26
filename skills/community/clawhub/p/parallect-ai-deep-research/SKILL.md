---
name: parallect
description: >
  Deep research using Parallect.ai. Queries multiple AI research providers
  (Perplexity, Gemini, OpenAI, Grok, Anthropic) in parallel, then synthesizes
  results into a unified report with cross-referenced citations and conflict
  resolution. Use when the user wants to research a topic, investigate a
  question, or needs comprehensive analysis with citations. Also triggers
  when the user says things like "look this up", "research this",
  "find out about", "deep dive on", or "what do we know about".
  Do NOT use for simple factual questions you can answer from memory --
  only for topics requiring sourced, multi-perspective analysis.
user-invocable: true
metadata: {"openclaw": {"emoji": "🔬", "primaryEnv": "PARALLECT_API_KEY", "requires": {"env": ["PARALLECT_API_KEY"]}, "homepage": "https://parallect.ai"}}
---

# Parallect Deep Research Skill

You have access to Parallect.ai, a multi-provider deep research platform.
It queries multiple frontier AI providers simultaneously and synthesizes
their findings into a single report with cross-referenced citations,
extracted claims, conflict resolution, and follow-on suggestions.

Research is **asynchronous** -- jobs take 30 seconds to 10+ minutes
depending on mode and providers. You MUST poll for completion. Never block.

## Connection

Parallect is accessed via its hosted MCP server. The connection is
pre-configured through your `openclaw.json` skill config.

- **Endpoint:** `https://parallect.ai/api/mcp/mcp`
- **Auth:** Bearer token using your `PARALLECT_API_KEY` (`par_live_*`)

If tools are not available, verify the key is set in your skill env
and the skill is enabled.

## Gotchas

Read these first. They prevent the most common mistakes:

- **Research is async.** Calling `research` does NOT return results. It
  returns a `jobId`. You must poll `research_status` and then call
  `get_results` only after status is `"completed"`.
- **`get_results` on a running job is an error.** Don't call it until
  `research_status` returns `"completed"`. You will get `JOB_NOT_COMPLETE`.
- **You are spending the user's money.** Never submit research without
  discussing budget first. Even an XXS tier costs ~$1.
- **Polling too fast triggers rate limits.** Use exponential backoff with
  jitter (see Step 3). Don't poll every 5 seconds.
- **Balance check before research is mandatory.** If the user has no
  balance and no payment method, the research call will fail. Check first.
- **The `synthesis` field is markdown.** Present it as-is with citations.
  Don't strip the formatting.
- **`research` always creates a new thread.** Do NOT pass a `threadId`
  to the `research` tool. For follow-up research in the same thread, use
  the `follow_up` tool with the parent `jobId`. Completed research
  reports are immutable and must not be overwritten.
- **`fast` mode skips synthesis.** It returns a single provider's raw
  report with no cross-referencing or conflict resolution. Only use when
  the user explicitly prioritizes speed.

## Available Tools

| Tool | Use when... | Do NOT use when... |
|------|-------------|-------------------|
| `research` | User wants to investigate a topic with sourced analysis | Question is simple enough to answer from memory |
| `research_status` | You've submitted research and need to check progress | You haven't called `research` yet |
| `get_results` | `research_status` shows `"completed"` | Job is still running or synthesizing |
| `follow_up` | User wants to dig deeper on a completed research topic | No prior completed job exists |
| `list_threads` | User refers to past research or wants to resume | You already have the threadId |
| `get_thread` | You need full context of a previous research session | You only need current job status |
| `balance` | Before starting research, or after to report remaining credits | Mid-polling (wastes a call) |
| `usage` | User asks about their spending history | Default -- only when explicitly asked |
| `list_providers` | Before research to show user what their tier includes | Already discussed budget with user |

## Workflow: Running Research

### Step 1: Discuss budget and check balance

Before submitting ANY research:

1. Call `balance` to check the user's current credits and payment status.
2. Call `list_providers` with the anticipated `budgetTier` to show what
   providers and cost range that tier includes.
3. Discuss budget with the user, framing it in natural language:

   | User says... | Map to tier | Max cost | Providers | Duration |
   |-------------|-------------|----------|-----------|----------|
   | "quick check", "just a glance" | XXS | ~$1 | 1 provider | ~30s |
   | "quick look", "brief" | XS | ~$2 | 1-2 providers | ~1min |
   | "standard", "normal" | S | ~$5 | 2 providers | ~2min |
   | "thorough", "detailed" | M | ~$15 | 3-4 providers | ~5min |
   | "comprehensive", "deep" | L | ~$30 | 4-5 providers | ~8min |
   | "exhaustive", "everything" | XL | ~$60 | All providers | ~10min |

   For per-tier details, provider strengths, and selection heuristics
   see `references/budget-tiers.md`.

4. Tell the user: "Your balance is $X.XX. A [tier] research will cost
   up to $Y. That will query [providers]. Want to proceed?"

5. If balance is insufficient and no payment method is on file, direct
   them to https://parallect.ai/settings/billing before proceeding.

6. If the user set a budget preference earlier in this session, reuse it
   silently unless the topic warrants a different tier. Don't ask again.

**Why this matters:** You are spending real money on the user's behalf.
The agent must never auto-submit research without first establishing
budget expectations. Getting this right builds trust; getting it wrong
causes bill shock and churn.

### Step 2: Submit the research

Call `research` with:
- `query`: A specific, well-formed research question (see Tips below)
- `budgetTier`: The tier confirmed in Step 1
- `mode`: `"methodical"` (default) for multi-provider synthesis.
  Only use `"fast"` if the user explicitly wants speed over depth.
- `providers`: Omit to let Parallect auto-select. Only specify if the
  user has a strong preference for specific providers.

The `research` tool always creates a new thread. Do NOT attempt to
pass a `threadId`. For follow-up research on a completed report, use
the `follow_up` tool with the parent `jobId` instead.

Save the returned `jobId` and `threadId`.

Tell the user: "Research submitted to [N] providers. I'll check back
on progress in about 30 seconds."

### Step 3: Poll for completion (exponential backoff with jitter)

Research is asynchronous. Poll using `research_status` with exponential
backoff. Do NOT poll at fixed intervals.

**Polling schedule:**

```
attempt = 1
base_delay = 30 seconds

while job not complete:
    wait(base_delay * (1.5 ^ (attempt - 1)) + random(0, 5 seconds))
    call research_status(jobId)
    attempt += 1
```

In practice this looks like:

| Check # | Approximate wait | Cumulative time |
|---------|-----------------|-----------------|
| 1 | ~30s | 30s |
| 2 | ~50s | 1m 20s |
| 3 | ~75s | 2m 35s |
| 4 | ~110s | 4m 25s |
| 5+ | ~120s (cap) | +2min each |

**Cap the maximum interval at 120 seconds.** Never poll more frequently
than every 30 seconds.

**On each poll, report progress naturally:**
- "1 of 3 providers finished, 2 still running..."
- "All providers done, synthesis is running now..."
- "Research complete! Let me grab the results."

**Shortcut:** If status is `"synthesizing"`, it's almost done. Next
check in 30 seconds.

**Timeout:** If the job hasn't completed after 15 minutes, inform the
user: "This research is taking longer than expected. Want me to keep
checking, or should we try a different approach?" Offer to:
- Keep polling (set 2-minute intervals)
- Check `get_results` in case partial results are available
- Start a new query with fewer providers or `fast` mode

**Silent stall detection:** If 3 consecutive polls return the exact
same progress (same providers complete, same status), the job may be
stuck. Inform the user and suggest starting fresh.

### Step 4: Deliver results

When `research_status` returns `"completed"`:

1. Call `get_results` with `jobId`.
   - Set `includeProviderReports: false` unless the user wants raw data.
   - Set `includeClaimsJson: false` unless the user wants structured claims.

2. Present findings in this order:
   a. **Brief summary** (3-5 sentences) of the key findings in your own
      words. Lead with the most important insight.
   b. **Full synthesis** -- share the `synthesis` markdown as-is. It
      contains inline citations and cross-references.
   c. **Cost report** -- "This research cost $X.XX across N providers
      (took Y minutes)."
   d. **Balance check** -- call `balance` and report: "Remaining
      balance: $X.XX." If below $5, flag it: "Heads up -- your balance
      is getting low."

3. If the job `status` is `"failed"`, report what happened and suggest
   retrying with a different tier or fewer providers.

### Step 5: Offer follow-ons

Results include `followOnSuggestions`. Present them as numbered options:

"Based on this research, here are directions we could explore next:
1. [suggestion 1]
2. [suggestion 2]
3. [suggestion 3]

Want me to research any of these, or ask your own follow-up question?"

When the user picks one:
- Use `follow_up` with the parent `jobId` and `topicIndex` (0-based)
  or `customQuery` for a custom question.
- Mention the estimated cost before submitting.
- Then repeat Steps 3-5.

Follow-ups run in the same thread, so providers have full context.

## Cost Awareness Rules

You are spending the user's money at machine speed. Be responsible:

- **NEVER auto-submit research in a new session** without first
  establishing budget expectations. This is non-negotiable.
- **Track cumulative session spend.** After multiple queries, report:
  "We've spent $X.XX on research so far this session."
- **Suggest cheaper tiers proactively.** If the question is simple,
  say: "This seems like a quick lookup -- XXS (~$1) should be enough.
  Want to save money with that instead of M?"
- **Confirm expensive operations.** For L/XL tiers or chains of
  follow-ups, get explicit confirmation: "That'll be up to $60.
  Want to proceed?"
- **Report cost after EVERY research job.** Never skip the cost report.
- **Alert at low balance.** If balance drops below $5, mention it.
  If below $2, proactively warn that the next research might fail.
- **Link to billing on insufficient funds.** Don't just say "insufficient
  balance" -- give them the link: https://parallect.ai/settings/billing

## Error Handling

Common errors: `INSUFFICIENT_BALANCE`, `JOB_NOT_COMPLETE`, `RATE_LIMITED`,
`PAYMENT_FAILED`, `JOB_NOT_FOUND`, `INVALID_TOPIC`. See
`references/api-errors.md` for full error codes, response fields, and
recovery steps.

## Tips for Quality Research Queries

A well-formed query saves money and produces better results:

- **Be specific:** "What are the latest Phase 3 clinical trial results
  for GLP-1 receptor agonists in treating NASH?" beats "GLP-1 drugs".
- **Include constraints:** time period, geography, industry sector,
  comparison criteria.
- **If the user is vague, ask ONE clarifying question** before spending
  money. "Could you narrow that down? Are you interested in [X] or [Y]?"
- **Don't over-scope.** If the user asks about a narrow topic, don't
  inflate it into a broad research question. Match the query scope to
  the budget tier.

## Mode Selection

| Mode | When to use | Duration | Output |
|------|------------|----------|--------|
| `methodical` | Accuracy and breadth matter (default) | 2-10 min | Multi-provider synthesis with claims and citations |
| `fast` | User says "quick" / "fast" / time-sensitive | 10-30s | Single provider raw report, no synthesis |

Use `methodical` unless the user explicitly asks for speed. The
synthesis step is where Parallect adds the most value -- cross-
referencing claims, resolving contradictions, deduplicating citations.

## Session Memory

- Remember `threadId` and `jobId` from current research context.
- If the user says "the research" or "those results", use the most
  recent jobId. Don't ask them to repeat it.
- If they want to resume older research, call `list_threads` to find
  it, then `get_thread` for the full context.
- Track cumulative spend across the session as a running total.
- `research` creates a new thread every time. `follow_up` continues
  an existing thread. Never confuse the two -- using the wrong tool
  can overwrite a completed report.
