## Description:

Agent skill for official cloud and AI documentation via MCP. Covers Microsoft Learn, AWS, Google Cloud, Cloudflare, OpenAI and Anthropic. Use for service limits, APIs, SDKs, CLI commands, regional availability or explicit documentation verification. One HTTP call per lookup; no API key except Google.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ricardodpalmeida](https://clawhub.ai/user/ricardodpalmeida)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical teams use this skill to verify cloud and AI platform details against the relevant vendor's current official documentation, then provide cited answers with preview status and documentation gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and requested documentation URLs are sent to the vendor-hosted service being queried.

Mitigation: Keep secrets, account or customer identifiers, and proprietary code out of queries.

Risk: The security scan was partial and left some local references unresolved, so its evidence is incomplete.

Mitigation: Review unresolved references and scan the skill before installation.

## Reference(s):

- [Setup and recovery](references/setup.md)
- [Microsoft Learn MCP Server](https://github.com/MicrosoftDocs/mcp)
- [AWS Knowledge MCP](https://awslabs.github.io/mcp/servers/aws-knowledge-mcp-server)
- [Google Developer Knowledge MCP](https://developers.google.com/knowledge/mcp)
- [Cloudflare MCP servers](https://developers.cloudflare.com/agents/model-context-protocol/mcp-servers-for-cloudflare)
- [OpenAI Docs MCP](https://developers.openai.com/api/docs/docs-mcp)
- [Claude Platform docs MCP](https://platform.claude.com/docs/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with Answer, Sources, Status, and Gaps sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Cites vendor documentation; searches first and reads up to three pages per vendor unless excerpts lack needed evidence.]

## Skill Version(s):

1.0.4 (source: release metadata and CHANGELOG.md; released 2026-11-16)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
