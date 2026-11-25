---
name: matrice-public-api
description: Integrates the public Matrice del Destino personal and couple matrix endpoints. Use when a task needs to request, explain, or troubleshoot those numerical API results.
---

<objective>
Use the live Matrice del Destino public API for a personal matrix or a couple matrix, preserving the canonical method identifier and returning only the numerical result requested. Production routes were verified on October 23, 2026.
</objective>

<quick_start>
Read [the endpoint reference](references/matrice.md). If the MCP server is configured, use its `matrix` or `couple` tool. Otherwise use the local CLI if it is already available:

    printf '%s' '{"date":"1990-06-15"}' | node bin/lucernel-tools.mjs matrix --stdin-json

Use a sample date only for a demonstration. For a real date, collect JSON through standard input rather than a command argument.
</quick_start>

<process>
1. Check the endpoint reference and choose the matching live route.
2. Choose matrix for one date or couple for two dates. Validate every date as a real YYYY-MM-DD calendar date from 1900 through today in UTC.
3. Send only date, or only first_date and second_date, as JSON. Do not add a name, account identifier, or extra property.
4. Check HTTP status before reading the result. On 429 or 503, honor Retry-After before a later attempt; do not rotate networks or accounts.
5. Preserve version, method, and source when passing structured results downstream. Explain that the output is a numerical matrix, not a personalized reading.
</process>

<privacy_and_scope>
Treat dates of birth as personal data. Prefer CLI JSON from standard input; do not place a real date in a URL, shell history, log, issue, or telemetry. Do not call premium-reading or PDF features, and do not invent interpretations for numeric points.
</privacy_and_scope>

<success_criteria>
- The requested live route and method match the task.
- All dates pass calendar and UTC range validation.
- The response is handled according to its HTTP status and retains its method identifier.
- No personal date or unsupported data is stored or repeated unnecessarily.
</success_criteria>
