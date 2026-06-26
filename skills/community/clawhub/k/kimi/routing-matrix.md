# Kimi Routing Matrix

Route by workload first, then by deadline, cost, and validation needs.

| Workload | Primary Goal | Best Starting Route | Validation Pattern | Notes |
|----------|--------------|---------------------|--------------------|-------|
| Fast interactive chat | Low latency and decent quality | smallest live Kimi chat route | spot-check one real prompt | Keep prompts short and avoid giant attachments |
| Coding agent | code edits plus tool context | strongest live coding-capable Kimi route | verify diff quality and parser behavior | Separate planning from exact patch generation |
| Long-context synthesis | compress many files or docs | strongest live long-context route | require citations or source list | Redact internal secrets before upload |
| Deterministic JSON | machine-readable output | low-temperature Kimi route | parse with `jq` or schema validator | Use a second pass if the first prompt needs creativity |
| Migration debugging | port existing OpenAI-compatible calls | smallest live route that reproduces the failure | compare one minimal payload before refactoring | Treat base URL, auth, and model IDs as separate variables |
| Cost-sensitive triage | summarize noisy tickets or logs | cheapest route that still returns stable structure | save token and retry limits | Metadata-only mode is safer than raw body uploads |

## Practical Decision Loop

1. Identify the real workload.
2. Fetch live model IDs from `/models`.
3. Test one minimal payload for the job.
4. Add validation before any downstream action.
5. Save one primary route and one fallback only after a real success.

## Two-Pass Pattern

Use this whenever Kimi must both think and automate:

1. Reasoning pass: analyze, compare, or draft.
2. Normalization pass: convert the result to strict JSON or a narrow format.

This is more reliable than forcing one answer to be both exploratory and deterministic.
