## Description:

PansModel Manager helps PanSclaw users add, remove, list, and switch custom model provider configurations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dashiming](https://clawhub.ai/user/dashiming)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and PanSclaw users use this skill to manage model provider entries and select the default model in their local OpenClaw/PanSclaw configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be entered through commands and stored in the local PanSclaw/OpenClaw configuration.

Mitigation: Use disposable or restricted provider keys, rotate keys after setup when appropriate, and verify permissions on ~/.openclaw-pansclaw/openclaw.json.

Risk: Switching or deleting model providers can disrupt the active default model configuration.

Mitigation: Back up the configuration before using delete or switch commands and confirm the selected provider/model before restarting the gateway.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dashiming/skills/pansmodel-manager)
- [Publisher profile](https://clawhub.ai/user/dashiming)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with command examples and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include model provider names, base URLs, API keys, model IDs, and local configuration file paths.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
