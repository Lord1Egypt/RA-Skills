## Description:

Integrates local Ollama AI model workflows with custom prompts and automatic mode for agent-assisted conversation and task automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to connect an AI agent workflow with local Ollama-style model operations, custom prompts, and automated task handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the local-only framing conflicts with API key and network guidance while requesting read, write, and command execution authority.

Mitigation: Review the skill before installing and use it only when the agent is intentionally allowed to run local Ollama-related commands and manage files.

Risk: The security guidance warns against providing real API keys unless the publisher clarifies what service receives them, which endpoints are contacted, and when prompts or files leave the machine.

Mitigation: Do not provide real API keys or sensitive prompts/files until the data flow and endpoints are clear.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/ollama-toolkit)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May provide execution guidance that involves local commands and file access.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
