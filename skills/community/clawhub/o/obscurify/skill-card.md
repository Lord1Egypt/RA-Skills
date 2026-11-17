## Description:

Use Obscurify.ai as a model provider through its OpenAI-compatible API (200+ models, account number instead of email). Use when asked to add, configure or troubleshoot Obscurify.ai in an agent or tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[obscurify](https://clawhub.ai/user/obscurify)

### License/Terms of Use:

MIT-0

## Use Case:

External developers use this skill to configure or troubleshoot Obscurify.ai as a model provider in an AI agent or compatible tool, including choosing a model and handling common API errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API key and account number provide access to the user's Obscurify account.

Mitigation: Keep credentials in a secure environment variable or secret store; never print, log, or commit them.

Risk: Prompts and included file contents are sent through Obscurify to upstream providers, and model use may incur costs.

Mitigation: Review privacy terms and usage costs before switching providers, and keep account creation and purchases under user approval.

## Reference(s):

- [Obscurify agent setup guides](https://obscurify.ai/agents)
- [Obscurify OpenAPI specification](https://obscurify.ai/api-docs/openapi.json)
- [Obscurify model cards and pricing](https://obscurify.ai/model_cards)
- [Obscurify privacy information](https://obscurify.ai/privacy)

## Skill Output:

**Output Type(s):** [Configuration instructions, Shell commands, API calls, Guidance]

**Output Format:** [Markdown with inline shell commands and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
