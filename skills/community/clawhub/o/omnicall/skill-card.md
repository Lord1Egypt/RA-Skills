## Description:

Omnicall helps agents access 248 LLMs, media generation, and live crypto, DeFi, market, web, and research data through a keyless, pay-per-call OpenAI-compatible endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[colinhughes2121](https://clawhub.ai/user/colinhughes2121)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to configure agents, SDKs, or MCP clients to send LLM, media-generation, and live-data requests through Omnicall. It is especially relevant when an agent needs a keyless pay-per-call gateway or OpenClaw default routing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OpenClaw setup can make Omnicall the default route for model traffic.

Mitigation: Use the default route only when you intend all model requests to pass through Omnicall, and test routing behavior before relying on it.

Risk: The paid gateway can automatically spend wallet funds without clearly documented limits.

Mitigation: Use strict wallet spending limits or only connect funds you are prepared to spend.

Risk: Requests may include secrets, private code, personal data, or regulated information.

Mitigation: Do not route sensitive or regulated data through the service unless privacy, retention, downstream-provider, and payment controls have been reviewed.

Risk: Setup commands install packages from external package registries.

Mitigation: Prefer pinned package versions where possible and review installed package behavior before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/colinhughes2121/skills/omnicall)
- [Omnicall API base endpoint](https://omnicall.gocreativeai.com/v1)
- [Omnicall MCP endpoint](https://omnicall.gocreativeai.com/mcp)
- [Omnicall free completion endpoint](https://omnicall.gocreativeai.com/v1/ai/free/{prompt})

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, API calls]

**Output Format:** [Markdown guidance with inline shell commands, code snippets, and endpoint paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May configure an agent or SDK to route model and tool requests through Omnicall.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter and changelog mention 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
