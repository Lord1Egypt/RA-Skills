## Description:

Control and query Hive Home smart heating, hot water, lights, and devices through Pyhiveapi and bundled helper commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[m0nkmaster](https://clawhub.ai/user/m0nkmaster)

### License/Terms of Use:

MIT-0

## Use Case:

Hive Home users and automation-focused agents use this skill to check device status and control heating, hot water, and related smart-home devices for accounts and devices they control.

### Deployment Geography for Use:

United Kingdom

## Known Risks and Mitigations:

Risk: Hive account credentials and reusable device login material could be exposed through chat, logs, or agent-visible output.

Mitigation: Provide credentials through environment variables or a secret store, run first-time authentication in a private local terminal, and avoid printing device login material into agent-visible output.

Risk: Commands can change real heating and hot-water state.

Mitigation: Use the skill only with Hive accounts and devices the user controls, and review requested mode, temperature, and boost changes before execution.

Risk: The skill relies on an unofficial Hive API through Pyhiveapi, which may change or fail outside the skill author's control.

Mitigation: Pin a reviewed Pyhiveapi version for automation and review upgrades before granting access to live devices.

## Reference(s):

- [ClawHub Hive Home listing](https://clawhub.ai/m0nkmaster/skills/hivehome)
- [Hive Home](https://www.hivehome.com)
- [Hive API reference](references/REFERENCE.md)
- [Credentials reference](references/CREDENTIALS.md)
- [Pyhiveapi](https://github.com/Pyhass/Pyhiveapi)
- [Pyhiveapi session examples](https://pyhass.github.io/pyhiveapi.docs/docs/examples/session/)
- [Home Assistant Hive integration](https://www.home-assistant.io/integrations/hive/)
- [Hive account portal](https://my.hivehome.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and Python examples; bundled script output is plain text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Hive credentials in environment variables and network access to Hive services through Pyhiveapi.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
