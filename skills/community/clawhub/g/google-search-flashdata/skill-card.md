## Description:

Search Google with FlashData and return structured web results with titles, URLs, snippets and positions. Use for web research, SERP data, site-specific searches, document discovery and localized search results. Requires a FlashData API key and paid Credits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flashdatadev](https://clawhub.ai/user/flashdatadev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and research users can search Google for current web sources, site-specific results, documents and localized queries, then use the structured results in an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search requests require a FlashData API key and spend paid Credits; a timed-out paid submission can have an unknown outcome.

Mitigation: Keep the key in protected secret configuration, check pricing and query budgets, and check Jobs before retrying a timed-out submission.

Risk: The security scan had incomplete coverage because two local references could not be resolved.

Mitigation: Review the unresolved references and assess FlashData before enabling the skill in a sensitive environment.

## Reference(s):

- [FlashData Google Search documentation](https://flashdata.dev/docs/sources/google_search?utm_source=clawhub&utm_medium=integration&utm_campaign=intent_gtm_2026q4&utm_content=google_search-task)
- [FlashData MCP endpoint](https://flashdata.dev/mcp?utm_source=clawhub&utm_medium=integration&utm_campaign=intent_gtm_2026q4&utm_content=google_search-task)
- [FlashData pricing](https://flashdata.dev/pricing?utm_source=clawhub&utm_medium=integration&utm_campaign=intent_gtm_2026q4&utm_content=google_search-task)
- [FlashData API key signup](https://flashdata.dev/signup?utm_source=clawhub&utm_medium=integration&utm_campaign=intent_gtm_2026q4&utm_content=google_search-task)
- [ClawHub skill release](https://clawhub.ai/flashdatadev/skills/google-search-flashdata)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured JSON search results with titles, URLs, snippets and positions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returned results and counts may vary by query and search type.]

## Skill Version(s):

1.0.3 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
