## Description:

Write the exact config to point a coding agent, IDE, SDK or framework at Kyma API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyma-api](https://clawhub.ai/user/kyma-api)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure coding agents, IDEs, SDKs, frameworks, and MCP-native tools to route requests through Kyma API with the correct base URLs, keys, model selection guidance, and tool-specific settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured tools may send prompts, code context, or application data to Kyma as an external model provider.

Mitigation: Use the skill only when that routing is intended, review Kyma's data terms for sensitive work, and avoid sending data that is not approved for the provider.

Risk: Global environment variables or shared settings can route unintended projects or tools through Kyma.

Mitigation: Prefer per-project or temporary environment variables and review generated configuration before applying it globally.

Risk: API keys stored directly in shared files or logs can be exposed.

Mitigation: Use secret storage or local environment variables where possible and rotate the key if it is accidentally disclosed.

Risk: The Vercel AI SDK path can add npm dependencies to production applications.

Mitigation: Pin and audit npm dependencies before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kyma-api/skills/kyma-connect-my-tool)
- [Kyma any-OpenAI-client guide](https://docs.kymaapi.com/guides/any-openai-client)
- [Kyma guides](https://docs.kymaapi.com/guides)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API base URLs, environment variables, MCP server URLs, OAuth setup steps, and model recommendation endpoint guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
