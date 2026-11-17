## Description:

Use the OOMOL-connected Home Assistant account to read, create, update, and delete Home Assistant data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Home Assistant users and developers can inspect instance state, history, logs, and configuration, and manage entities, automations, scenes, scripts, and events through their OOMOL connection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup can execute downloaded code without separate approval, and the connected service can access the user's Home Assistant account.

Mitigation: Review and approve CLI installation separately, preferably from a fixed, verified release; consider its skill-installation behavior and account access, and require confirmation before device-control or configuration changes.

## Reference(s):

- [Home Assistant](https://www.home-assistant.io)
- [Home Assistant API documentation](https://developers.home-assistant.io/docs/api/rest)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON, Configuration]

**Output Format:** [Natural-language guidance with shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.8 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
