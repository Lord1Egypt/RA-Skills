## Description:

Agent skill for official cloud and AI documentation via MCP. Covers Microsoft Learn, AWS, Google Cloud, Cloudflare, OpenAI and Anthropic. Use for service limits, APIs, SDKs, CLI commands, regional availability or explicit documentation verification. One HTTP call per lookup; no API key except Google.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ricardodpalmeida](https://clawhub.ai/user/ricardodpalmeida)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud practitioners use this skill to verify current service limits, APIs, SDKs, CLI commands, and regional availability against official documentation for Microsoft, AWS, Google Cloud, Cloudflare, OpenAI, and Anthropic. It returns sourced answers and identifies preview status and documentation gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries and requested documentation URLs are sent to the selected vendor; available security results do not establish what data a live request sends.

Mitigation: Keep queries generic and omit secrets, account or customer identifiers, and proprietary code.

Risk: The security scan was marked partial because several references in SKILL.md could not be resolved.

Mitigation: Review the skill and its linked references before installation; the benign verdict is not a guarantee of safety.

## Reference(s):

- [Setup and recovery](references/setup.md)
- [Multi-cloud Docs on ClawHub](https://clawhub.ai/ricardodpalmeida/skills/multicloud-docs-mcp)
- [Project homepage](https://github.com/Ricardodpalmeida/multicloud-docs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Citations]

**Output Format:** [Four-part Markdown response with source titles and URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Answers, sources, feature status, and documentation gaps; page reads are limited to three per vendor unless excerpts lack needed evidence.]

## Skill Version(s):

1.0.5 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
