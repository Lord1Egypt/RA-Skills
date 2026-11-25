## Description:

Use Obscurify.ai as a model provider through its OpenAI-compatible API (200+ models, an account code instead of email). Use when asked to add, configure or troubleshoot Obscurify.ai in an agent or tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[obscurify](https://clawhub.ai/user/obscurify)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to configure or troubleshoot Obscurify.ai as a model provider in compatible agents and tools. It provides setup guidance, model selection details, and account, authentication, and plan troubleshooting steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions use an unpinned CLI that may change between security reviews when handling account credentials.

Mitigation: Prefer obtaining the API key through the account interface. If the CLI is needed, verify and pin an exact version before running it, and keep account codes and API keys in a secret store.

## Reference(s):

- [Obscurify.ai agent setup](https://obscurify.ai/agents)
- [OpenAPI specification](https://obscurify.ai/api-docs/openapi.json)
- [Model catalog and pricing](https://obscurify.ai/models)
- [Privacy policy](https://obscurify.ai/privacy)
- [Secret scrubbing guide](https://obscurify.ai/tutorials/secret_scrubbing)
- [Private sessions guide](https://obscurify.ai/tutorials/private_sessions)

## Skill Output:

**Output Type(s):** [Configuration instructions, Shell commands, API calls, Troubleshooting guidance]

**Output Format:** [Markdown with inline shell commands, configuration guidance, and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.1.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
