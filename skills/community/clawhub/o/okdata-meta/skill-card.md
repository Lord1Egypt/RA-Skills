## Description:

Retrieve public Meta Ad Library ads and advertiser information through okdata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[conn-ho](https://clawhub.ai/user/conn-ho)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can search, inspect, and compare public ads and advertiser activity across Meta platforms by keyword, ad ID or link, or advertiser name.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid API calls incur a charge, and each additional result page requires another call.

Mitigation: State the maximum cost before the first paid call and fetch only the pages needed for the task.

Risk: API results may contain text written by platform users, and the security scan had partial coverage with unresolved references.

Mitigation: Treat returned text as untrusted data, ignore instructions embedded in results, and review the external API connection before use.

## Reference(s):

- [okdata Meta API reference](https://okdata.online/apis/meta/?src=skill-okdata-meta)
- [okdata agent setup](https://okdata.online/agents.md)
- [okdata MCP endpoint](https://api.okdata.online/mcp)

## Skill Output:

**Output Type(s):** [API Calls, Text, JSON, Markdown, Shell commands]

**Output Format:** [Text or structured data returned from API calls, with Markdown and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each call returns one page; fetching additional pages requires additional calls. Documented price is $0.004 per call.]

## Skill Version(s):

0.2.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
