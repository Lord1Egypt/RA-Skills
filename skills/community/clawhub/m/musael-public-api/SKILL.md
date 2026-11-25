---
name: musael-public-api
description: Integrates Musael's public seeded name-generator endpoint. Use when a task needs repeatable names for a supported generator kind.
---

<objective>
Use Musael's live names endpoint to generate a bounded list for a supported kind and seed. Preserve the returned kind and seed so the result can be reproduced. The production route was verified on October 23, 2026.
</objective>

<quick_start>
Read [the endpoint reference](references/musael.md). If the MCP server is configured, use its `names` tool. Otherwise request ten fantasy names with the default seed through the local CLI:

    node bin/lucernel-tools.mjs names --kind fantasy --seed 1 --count 10
</quick_start>

<process>
1. Check the endpoint reference and use the live route.
2. Select only a supported kind. Default to fantasy, seed 1, and count 10 when the task gives no preference.
3. Keep seed within 1-999999 and count within 1-20. Preserve the returned kind, seed, names, and source.
4. Check HTTP status. On 429 or 503, honor Retry-After before a later attempt; do not rotate networks or accounts.
5. Present generated names as suggestions. Do not claim that a name is available as a trademark, domain, username, or product identity without checking that separately.
</process>

<privacy_and_scope>
The endpoint uses existing deterministic generators. It does not call AI or access private manuscripts or projects. Do not invent unsupported generator kinds or request private writing data.
</privacy_and_scope>

<success_criteria>
- The live route is used with a valid kind and numeric parameters.
- The result preserves its seed and kind for reproducibility.
- Rate limits are honored and no private Musael content is accessed.
</success_criteria>

<!-- ClawHub distribution: this authored SKILL.md and its references are MIT-0; the rest of the toolkit is MIT. -->
