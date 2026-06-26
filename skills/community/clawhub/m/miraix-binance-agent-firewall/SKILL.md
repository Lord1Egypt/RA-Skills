---
name: miraix-binance-agent-firewall
description: Use this skill when the user wants to audit a Binance trading prompt, decide whether an AI trader should get Binance account permissions, return Pass/Warn/Block with guardrails, identify allowed/watch-only/blocked symbols, rewrite the prompt into a safer operating mode, or generate a share card URL for the probation report.
---

# Miraix Binance Agent Firewall

Use this skill to judge whether an AI trading prompt is safe enough to touch a Binance account. It is backed by Miraix public endpoints and Binance public market data.

Public endpoints:

- Audit API: `https://app.miraix.fun/api/binance-agent-firewall`
- Share image: `https://app.miraix.fun/api/binance-agent-firewall/share-image`

## When to use it

- The user pasted a Binance or crypto trading prompt and wants a safety audit.
- The user asks whether an AI trader should get spot, futures, margin, transfer, or withdraw permissions.
- The user wants guardrails, a permission plan, or a probation profile before enabling automation.
- The user wants a safer rewrite of a risky trading prompt.
- The user wants a share card, screenshot, or X post for the firewall result.

## Workflow

1. Extract the raw trading prompt from the request. If none is provided, ask for it.
2. Extract Binance symbols if the user gives them. If they do not, send an empty list and let the API infer context from the prompt.
3. Run:

```bash
curl -sS -X POST https://app.miraix.fun/api/binance-agent-firewall \
  -H 'Content-Type: application/json' \
  -d '{"prompt":"<raw-trading-prompt>","symbols":["<symbol-1>","<symbol-2>"]}'
```

4. Base the answer on the returned JSON. The most important fields are:
   - `status`
   - `safetyScore`
   - `verdict`
   - `summary`
   - `findings`
   - `guardrails`
   - `permissionPlan`
   - `probationProfile`
   - `safePrompt`
   - `shareText`
5. If the user wants the safest possible operating version, prefer `safePrompt` over inventing a new rewrite.
6. If the user wants a share card, build a payload with:
   - `status`
   - `safetyScore`
   - `verdict`
   - `summary`
   - `primaryFinding`
   - `primaryGuardrail`
   - `symbols`
   - `dimensions`
   - `generatedAt`

   Then URL-encode the JSON and append it to:

```bash
https://app.miraix.fun/api/binance-agent-firewall/share-image?payload=<urlencoded-json>
```

7. If the user wants a social post, start from `shareText` and adapt the tone instead of rewriting the whole result from scratch.

## Output guidance

- Lead with the verdict and safety score.
- Then show the top findings and the recommended permission plan.
- Then show the probation profile and the safe rewrite.
- Do not claim private Binance account access. This skill uses Binance public market data plus Miraix scoring logic.
- If `futuresDataAvailable` is false, say funding data was unavailable instead of making it up.
- If the API fails, surface the error clearly and suggest retrying with a cleaner prompt or a tighter symbol list.
