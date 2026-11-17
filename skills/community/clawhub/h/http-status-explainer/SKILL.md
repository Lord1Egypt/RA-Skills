---
name: http-status-explainer
description: >
  Explain HTTP status codes in plain language and suggest safe next steps for
  clients and operators. Use when debugging APIs, browsers, or reverse proxies.
metadata: {"clawdbot":{"emoji":"📶","requires":{"bins":[]}}}
---

# HTTP Status Explainer

## Purpose / Overview
Turn a status code (and optional response headers) into a short diagnosis:
what it means, who owns the fix (client vs server), and what to try next.

## When to Use
- A curl/fetch call returns an unexpected code
- Logs show spikes of 4xx/5xx
- The user pastes a status line like `HTTP/1.1 502 Bad Gateway`

## Usage / Instructions
1. Ask for the numeric status code if not already provided.
2. Optionally collect: request method, URL path (no secrets), and a few response
   headers that matter (`Retry-After`, `WWW-Authenticate`, `Location`).
3. Classify the code family (1xx / 2xx / 3xx / 4xx / 5xx).
4. Write four short sections for every answer:
   - **Meaning** — one or two sentences
   - **Likely causes** — 2–4 bullets tailored to method/path if known
   - **Who should act** — client developer, API owner, or infrastructure
   - **Next checks** — concrete steps (retry, fix auth, inspect upstream)
5. For 429 with `Retry-After`, convert the wait to a human duration and advise
   respecting it instead of tight retry loops.
6. For 401 vs 403, distinguish "not authenticated" from "authenticated but not
   allowed" without asking the user to paste tokens.
7. For 502/503/504, suggest upstream health, timeouts, and recent deploys before
   rewriting business logic.
8. Never invent a vendor-specific root cause. Label guesses as hypotheses.
9. Offer a one-line message suitable for an incident channel.
10. If the user pastes a full response body, summarize only non-sensitive fields.
11. Keep answers structured with short headings so the user can skim.
12. If information is missing, ask at most two clarifying questions before guessing.
13. Prefer concrete commands or checklists the user can copy.
14. Call out assumptions explicitly when the environment is unknown.
15. Refuse to invent tool output you did not see; ask for a fresh paste instead.
16. When offering optional follow-ups, keep them clearly optional.
17. Stay within this skill's scope; suggest a different task type if the request drifts.
18. End with a brief "done when" criterion so the user knows success.


## Examples
User: "Webhook got 410."
→ Meaning (gone), causes (deleted callback), owner (integration), next checks.

User: "curl -I returns 301 with Location https://example.com/new"
→ Explain permanent redirect; ask whether clients should update stored URLs.

## Requirements / Dependencies
None. Works from status codes and optional headers the user pastes.

## Limitations / Caveats
- Does not call the live API unless the user explicitly asks with a URL
- CDN-specific edge cases still map to standard families
- Cannot see body content the user did not share

## Security / Permissions
Text-only. Do not request or echo API keys, cookies, or `Authorization` values.
If secrets appear in a paste, advise rotation and omit them from further replies.

## Description

Explain HTTP status codes in plain language and suggest safe next steps for clients and operators.

## License or terms

MIT

## Use case

Intended for practitioners who need help with: Explain HTTP status codes in plain language and suggest safe next steps for clients and operators.

## Risks and mitigations

## References

- MDN HTTP response status codes: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status

## Ethical considerations

Illegal use of this skill is not allowed. The publisher will not be accountable for outcomes arising from unlawful use under country or international law. Prohibited examples include breaking into accounts without authorization, deploying ransomware, and trafficking in stolen personal data. Misuse against third-party systems without authorization is illegal.
