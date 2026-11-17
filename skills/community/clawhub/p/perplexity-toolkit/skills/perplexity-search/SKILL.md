---
name: perplexity-search
description: "Use when the user asks to use Perplexity search for a quick lookup. Lightweight source-grounding policy alias; deep research goes to perplexity-conversational-research, browser actions to perplexity-web-automation."
---

# Perplexity Quick-Lookup Policy Alias

Lightweight quick-lookup and source-grounding policy. This skill does not select
models or maintain browser state. It defines the canonical anti-hallucination
prompt and source-verification rules, then routes deeper or browser-based work
to the dedicated skills. For a normal Perplexity request with no explicit
browser wording, the execution route is the `perplexity` CLI.

## WebBridge boundary

Any Perplexity action through the user's logged-in Chrome is executed by `perplexity-web-automation` (via `kimi-webbridge`); this skill does not maintain browser operation flows. For repeat browser use in one fixed tab/group, the executor is the resident console (`perplexity console ...`, documented in `perplexity-web-automation`) — trigger it for 「用网页(版)的 Perplexity 搜/问」-style requests as described there.

Keep these concepts separate:

- **Perplexity thread**: the website's search/conversation thread.
- **WebBridge session**: the local task namespace that owns a tab group.
- **Chrome extension connection**: the daemon-to-browser handshake.

A `no extension connected` response means the daemon currently has no extension handshake; it is not evidence that a Perplexity thread limit was reached. A healthy but empty session returns `success: true` with `tabs: []` — confirmed by the 2026-09-05 smoke test as a connection-state transition, not a thread-capacity failure. Reuse the existing daemon/session; never create extra threads or sessions to work around the message, and never stop, restart, or close the user's browser connection automatically.

## Skill stack and routing

This is the lightweight quick-lookup and anti-hallucination policy layer. It is not a second browser driver and should not be loaded as a co-equal full workflow with every Perplexity skill.

- Quick lookup with no multi-turn workflow → use this skill.
- Deep, multi-turn, model-variety, or evidence-ranking research → use `perplexity-conversational-research`.
- Any logged-in Chrome/WebBridge interaction → load `perplexity-web-automation` as the execution layer.

Choose one high-level research path per task, then load the WebBridge layer only when browser execution is explicitly requested; do not run all three as duplicate top-level instructions.

## Route contract

- Explicit `web page`/`网页方式`, `browser`, `Chrome`, `WebBridge`, `Kimi
  WebBridge`, "open Perplexity", or "continue the current browser thread" → use
  `perplexity-web-automation` directly and do not invoke the CLI first.
- Any other Perplexity request → use `perplexity` CLI first. The current CLI
  still uses WebBridge internally, but it remains the CLI-managed route.
- If the CLI is unavailable or fails, report the failure and wait for explicit
  authorization before using the direct browser route or the standalone
  fallback helper.

## When to Use

- User says "perplexity search", "用 perplexity 查"
- Price comparison, technical evaluation, market research with verified citations

## Step 1: Model Policy

Quick lookup does not declare specific models or model capabilities; this skill makes no model-selection claim, and only an actual returned result may be cited for model/quality information. Deep, multi-turn, or model-variety research is handled by `perplexity-conversational-research`.

## Step 2: Anti-Hallucination Prompts

NEVER ask a bare question. Wrap with:

```
{query}
Requirements:
1. Cite sources with URLs
2. If no verified source, say so
3. For pricing: official page URLs only
4. Format as comparison table with Source URL column
```

> **Canonical definition point.** This wrapper block is the single canonical definition of the anti-hallucination prompt shared by all related Perplexity skills. Other Perplexity skills should reference (or apply) this section as-is — do not copy another full definition into them. If an inconsistency appears, resolve it here first.

## Step 3: Verification

**Canonical definition point.** This is the single source of truth for the
candidate-vs-verified boundary and the HEAD-vs-readback rule. Other Perplexity
skills must link here instead of restating it.

- Treat HTTP HEAD on cited URLs as a **transport diagnostic only** — it can surface dead links or redirects, but a `403`/blocked HEAD does **not** mean the page content is unreadable (many sites block HEAD yet serve GET fine).
- Do **not** treat HEAD success/failure as source verification.
- Record the two states **independently**, never collapsed into one verdict:
  - `toolkit-head`: reachability diagnostic (`ok`, `blocked`, or other result)
  - `page-content`: whether the canonical URL was actually read back, and whether it supports the claim
  Never downgrade a readable page to "no evidence" solely because HEAD returned `403`.
- Verify sources by doing an actual **page readback on the canonical URL** (e.g. `web_extract`, or Kimi WebBridge for JS-heavy/anti-bot pages): confirm the cited claim is present in the fetched content, and only then feed that content into the project pipeline. Mark anything not confirmed this way as `not_verified`.
- The toolkit's `verify_result` performs bounded GET readback and records `page_content` / `readback`, but deliberately returns `verification_state: candidate` and `claim_support: not_evaluated`; it does not claim semantic support automatically. Promote a claim only after the canonical content is reviewed.
- The Perplexity answer quality score (0-100) is a **lead/discovery signal only** — never a fact-verification conclusion.
- Red flags: prices without URLs, "studies show" without a link.

## Step 4: Failure Handling

Report lookup failures honestly. Do not change from the CLI route to direct
browser execution without explicit user authorization. The toolkit may perform
bounded transport retries internally; that is different from this policy layer
silently starting a new research route. Escalate to
`perplexity-conversational-research` for deeper research or to
`perplexity-web-automation` only when browser execution is in scope.


