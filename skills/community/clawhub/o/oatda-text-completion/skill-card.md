## Description:

Generate text using OATDA's unified LLM API across supported third-party model providers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devcsde](https://clawhub.ai/user/devcsde)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to route text generation prompts through OATDA's unified LLM API, select a provider or model alias, and return generated text with optional usage and cost details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts are sent to OATDA and the selected external model provider, which can expose sensitive user content.

Mitigation: Use only with approved data transfer paths, and do not send secrets, regulated data, private business data, or proprietary content unless that transfer is authorized.

Risk: The shell examples handle API keys and user prompts in commands that could expose credentials or behave unexpectedly if copied literally.

Mitigation: Keep API keys scoped to the request, avoid printing full credentials, and construct request JSON with structured tooling such as jq --arg before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/devcsde/skills/oatda-text-completion)
- [OATDA](https://oatda.com)
- [OATDA LLM API Endpoint](https://oatda.com/api/v1/llm)
- [OATDA API Keys](https://oatda.com/dashboard/api-keys)
- [OATDA Usage Dashboard](https://oatda.com/dashboard/usage)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include generated text, provider and model identifiers, token usage, and cost details returned by the OATDA API.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
