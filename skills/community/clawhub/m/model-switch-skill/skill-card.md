## Description:

Switch between configured LLM API providers including MiniMax, SCNET, OpenRouter, and Volcano Engine using OpenClaw CLI commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yzh0916](https://clawhub.ai/user/yzh0916)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to switch among configured LLM API providers, query the active provider, and list available providers for agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts may be sent to the selected third-party LLM provider.

Mitigation: Confirm trusted provider endpoints, API keys, billing terms, and data policies before use.

Risk: Provider configuration uses API keys and endpoint URLs.

Mitigation: Use your own API keys and keep OpenClaw configuration files protected from unintended disclosure.

Risk: Usage examples are mainly Chinese-language invocations.

Mitigation: Adapt invocation phrases for the target operator language before relying on them in routine workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yzh0916/skills/model-switch-skill)
- [Publisher profile](https://clawhub.ai/user/yzh0916)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with command examples and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local OpenClaw configuration and selected provider endpoints.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact _meta.json, SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
