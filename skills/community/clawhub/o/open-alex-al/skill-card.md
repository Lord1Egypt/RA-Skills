## Description: <br>
Use OpenAlex to find and cite scholarly works, authors, institutions, and trends via metadata queries without needing an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simonpierreboucher02](https://clawhub.ai/user/simonpierreboucher02) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and research agents use this skill to decide when OpenAlex is appropriate, build precise scholarly metadata queries, interpret API results, and produce traceable citations for papers, authors, institutions, and bibliometric trends. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to guide use of a paired external OpenAlex MCP server. <br>
Mitigation: Review and approve the MCP server separately before enabling live OpenAlex queries. <br>
Risk: OPENALEX_MAILTO may send an email address to OpenAlex for polite-pool rate limiting. <br>
Mitigation: Use an address that is acceptable for sharing with OpenAlex, such as a monitored team mailbox. <br>
Risk: Scholarly metadata, citation counts, affiliations, and OpenAlex entity records can change over time. <br>
Mitigation: Report counts as point-in-time values, include an access date when precision matters, and re-resolve IDs periodically. <br>
Risk: Incorrect query construction or unsupported filters can produce empty, misleading, or incomplete results. <br>
Mitigation: Resolve entities before filtering, verify filter keys against OpenAlex documentation, distinguish meta.count from returned results, and never invent missing papers or citations. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/simonpierreboucher02/open-alex-al) <br>
- [OpenAlex API documentation](https://docs.openalex.org) <br>
- [Endpoints and tools reference](artifact/reference/endpoints.md) <br>
- [Entities and filters reference](artifact/reference/entities-and-filters.md) <br>
- [Response fields reference](artifact/reference/response-fields.md) <br>
- [Best practices reference](artifact/reference/best-practices.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guidance with JSON tool-call examples, configuration notes, and citation templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No API key is required. The skill recommends OPENALEX_MAILTO for polite-pool rate limiting and requires OpenAlex IDs or URLs in citations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
