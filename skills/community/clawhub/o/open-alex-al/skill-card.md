## Description:

Use OpenAlex to find and cite scholarly works, authors, institutions, and trends via metadata queries without needing an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simonpierreboucher02](https://clawhub.ai/user/simonpierreboucher02)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and research-facing agents use this skill to plan OpenAlex metadata queries, resolve scholarly entities, build citations, and summarize bibliographic trends with traceable OpenAlex records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may treat OpenAlex metadata as full text or as evidence for non-academic web facts.

Mitigation: Use OpenAlex for scholarly metadata only; follow open_access.oa_url or separate sources for full text, paywalled content, and non-academic facts.

Risk: OpenAlex records, citation counts, affiliations, and entity identifiers can change over time.

Mitigation: Report figures as point-in-time, include access dates when precision matters, and re-resolve cached IDs periodically.

Risk: Poor query handling can produce fabricated, incomplete, or untraceable scholarly claims.

Mitigation: Report only API-returned records, keep meta.count distinct from listed results, and cite title, authors, year, DOI, and OpenAlex ID/URL.

Risk: Runtime tool calls depend on a separate OpenAlex MCP server and may encounter rate limits.

Mitigation: Review the MCP server before enabling calls, set a non-sensitive OPENALEX_MAILTO for the polite pool, back off on 429 responses, cache stable records, and use cursor paging for traversal.

## Reference(s):

- [Open Alex Skill Release](https://clawhub.ai/simonpierreboucher02/skills/open-alex-al)
- [OpenAlex API Documentation](https://docs.openalex.org)
- [OpenAlex Entities and Filters](reference/entities-and-filters.md)
- [OpenAlex Endpoints and Tools](reference/endpoints.md)
- [OpenAlex Response Fields](reference/response-fields.md)
- [OpenAlex Best Practices](reference/best-practices.md)
- [OpenAlex Common Errors](reference/common-errors.md)

## Skill Output:

**Output Type(s):** [text, guidance, markdown, code, configuration]

**Output Format:** [Markdown guidance with JSON tool-call examples and citation templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces read-only OpenAlex query guidance, citation formats, workflow checklists, and configuration recommendations such as OPENALEX_MAILTO.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
