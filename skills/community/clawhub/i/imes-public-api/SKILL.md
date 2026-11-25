---
name: imes-public-api
description: Integrates Istruzione Messina's public date-based angel-number endpoint. Use when a task needs to request or explain its digit-root result.
---

<objective>
Use Istruzione Messina's live date-based endpoint to retrieve the versioned digit-root result. The production route was verified on October 23, 2026.
</objective>

<quick_start>
Read [the endpoint reference](references/imes.md). If the MCP server is configured, use its `angel_number` tool. Otherwise use the local CLI if it is already available:

    printf '%s' '{"date":"1990-06-15"}' | node bin/lucernel-tools.mjs angel-number --stdin-json

Use a sample date only for a demonstration. For a real date, collect JSON through standard input rather than a command argument.
</quick_start>

<process>
1. Check the endpoint reference and use the live route.
2. Validate the date as a real YYYY-MM-DD calendar date from 1900 through today in UTC.
3. Send only the date JSON field. Do not send a name, account identifier, or extra property.
4. Check HTTP status. On 429 or 503, honor Retry-After before a later attempt; do not rotate networks or accounts.
5. Preserve version, method, and source with the integer result. Describe it as a digit-root calculation, not as factual life guidance.
</process>

<privacy_and_scope>
Treat dates of birth as personal data. Prefer CLI JSON from standard input; do not put a real date in a URL, shell history, log, issue, or telemetry. The API returns a number from 1 through 9 and does not provide a personalized reading.
</privacy_and_scope>

<success_criteria>
- The live route is used with a valid date.
- The result is an integer from 1 through 9 and retains its method identifier.
- Rate limits are honored and personal data is not repeated unnecessarily.
</success_criteria>
