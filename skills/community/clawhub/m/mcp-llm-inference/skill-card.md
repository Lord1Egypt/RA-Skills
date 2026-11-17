## Description:

Anonymous LLM inference via L402 micropayments for chat completions, text generation, and model discovery without API keys, signups, or KYC.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haveblue997](https://clawhub.ai/user/haveblue997)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this MCP server to request chat completions, single-prompt text generation, and model listings through an L402 micropayment API when they need accountless, pay-per-request LLM access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, conversation history, and model requests are sent to a remote L402 API.

Mitigation: Do not send secrets, regulated data, proprietary context, or hidden system instructions; review the provider's privacy, logging, and retention terms before use.

Risk: Installation and provider claims need review before use.

Mitigation: Use a pinned, verified package version and confirm the package name, environment variable, and provider documentation match the intended release.

Risk: L402 micropayment handling can introduce per-request costs and payment workflow risk.

Mitigation: Confirm pricing, invoice handling, budget limits, and payment policy before enabling agent access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/haveblue997/skills/mcp-llm-inference)
- [Publisher profile](https://clawhub.ai/user/haveblue997)
- [Nautdev API base URL](https://api.nautdev.com)
- [Blue-Trianon-Ventures GitHub profile](https://github.com/Blue-Trianon-Ventures)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [MCP tool responses as text content, usually JSON strings from the remote API.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool inputs include model identifiers, chat messages or prompts, and optional streaming behavior where supported by the packaged implementation.]

## Skill Version(s):

1.0.0 (source: server release evidence, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
