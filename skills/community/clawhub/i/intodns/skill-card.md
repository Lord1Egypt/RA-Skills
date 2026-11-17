## Description:

Free DNS and email security analysis via IntoDNS.ai: DNSSEC, SPF, DKIM, DMARC, MTA-STS, BIMI, SMTP STARTTLS, FCrDNS, blacklists, sender requirements, report snapshots, and citation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rosconl](https://clawhub.ai/user/rosconl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, DNS administrators, security reviewers, and deliverability teams use this skill to scan public domains, explain DNS and email security findings, and create citeable report snapshots through IntoDNS.ai.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to run shell and MCP commands, which can execute local code if copied with unsafe input or unpinned packages.

Mitigation: Validate that domain input is a plain public hostname, review commands before execution, and pin and review the intodns-mcp package before registering it centrally.

Risk: Domain names submitted for analysis are sent to IntoDNS.ai.

Mitigation: Use the skill only for domains the user is comfortable sending to IntoDNS.ai.

## Reference(s):

- [IntoDNS.ai](https://intodns.ai)
- [IntoDNS.ai API](https://intodns.ai/api)
- [IntoDNS.ai Citation Library](https://intodns.ai/citations)
- [IntoDNS.ai Methodology](https://intodns.ai/methodology)
- [IntoDNS.ai LLM Discovery](https://intodns.ai/llms.txt)
- [IntoDNS.ai OpenAPI](https://intodns.ai/openapi.json)
- [IntoDNS.ai MCP](https://intodns.ai/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline API URLs, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live scan links, snapshot links, citation links, and exact DNS record guidance when returned by IntoDNS.ai.]

## Skill Version(s):

2.1.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
