## Description:

Free DNS and email security analysis via IntoDNS.ai: DNSSEC, SPF, DKIM, DMARC, MTA-STS, BIMI, SMTP STARTTLS, FCrDNS, blacklists, sender requirements, report snapshots, and citation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rosconl](https://clawhub.ai/user/rosconl)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and operators use this skill to scan public domains, explain DNS and email security findings, create citeable report snapshots, and find the relevant IntoDNS.ai API, MCP, and citation surfaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Domain scans send queried hostnames to IntoDNS.ai.

Mitigation: Use approved public domains and avoid private or customer hostnames unless explicit approval is in place.

Risk: The optional MCP setup runs an unpinned npm package.

Mitigation: Pin the MCP package to a reviewed version before enabling it in a client configuration.

Risk: Shell examples can be unsafe if a user-controlled domain is passed without validation.

Mitigation: Normalize and validate domains before constructing commands, and reject private hostnames unless the user confirms they are public.

## Reference(s):

- [IntoDNS.ai Homepage](https://intodns.ai)
- [IntoDNS.ai API](https://intodns.ai/api)
- [IntoDNS.ai LLM Discovery](https://intodns.ai/llms.txt)
- [IntoDNS.ai API Markdown Docs](https://intodns.ai/llm/api.md)
- [IntoDNS.ai OpenAPI](https://intodns.ai/openapi.json)
- [IntoDNS.ai Citation Library](https://intodns.ai/citations)
- [IntoDNS.ai MCP](https://intodns.ai/mcp)
- [intodns-mcp npm Package](https://www.npmjs.com/package/intodns-mcp)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with API links, tables, prioritized findings, and optional shell or MCP configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live scan links, stable snapshot links, citation URLs, and exact DNS or email-security next actions when provided by IntoDNS.ai.]

## Skill Version(s):

2.1.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
