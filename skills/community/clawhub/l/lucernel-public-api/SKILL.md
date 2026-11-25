---
name: lucernel-public-api
description: Integrates Lucernel's public daily World English Bible verse endpoint. Use when a task needs today's verse or a verse for a specified calendar date.
---

<objective>
Retrieve the date-selected verse from Lucernel's live daily-verse endpoint and preserve its reference, text, translation, and source. The production route was verified on October 23, 2026.
</objective>

<quick_start>
Read [the endpoint reference](references/lucernel.md). If the MCP server is configured, use its `verse` tool. Otherwise request today's verse with no query parameter or use the local CLI:

    node bin/lucernel-tools.mjs verse
</quick_start>

<process>
1. Check the endpoint reference and use the live route.
2. Use the current UTC date by omitting date, or provide one valid YYYY-MM-DD date from 1900 through 2100.
3. Check HTTP status and preserve version, date, reference, text, translation, and source.
4. On 429 or 503, honor Retry-After before a later attempt; use bounded retries only.
5. Attribute the text to the World English Bible and link to the source page when presenting it.
</process>

<privacy_and_scope>
This endpoint returns one daily verse from existing data. It does not accept birth dates or account data and does not call an external Bible service. Do not imply that the selected verse is personalized or generated for an individual.
</privacy_and_scope>

<success_criteria>
- The live route is used with a valid requested date.
- The response keeps its reference and World English Bible attribution.
- Any transient error respects Retry-After.
</success_criteria>

<!-- ClawHub distribution: this authored SKILL.md and its references are MIT-0; the rest of the toolkit is MIT. -->
