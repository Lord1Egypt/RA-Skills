## Description:

Helps agents view, switch, and manage Hermes profile model configuration for main, auxiliary, and delegation models across single or multiple profiles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youbuwei](https://clawhub.ai/user/youbuwei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Hermes administrators use this skill to inspect current model settings, switch providers or models, batch-update profiles, and verify that gateway restarts made configuration changes effective.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents to change live Hermes profile settings and restart gateways.

Mitigation: Use it only for intentional Hermes model administration and require confirmation before applying configuration changes or restarting gateways.

Risk: Credential-check examples can print API key values from profile .env files into terminal or agent logs.

Mitigation: Use quiet presence checks instead of commands that echo secrets, and do not ask agents to collect or display API key values.

## Reference(s):

- [Server-resolved source repository](https://github.com/youbuwei/hermes-profile-model-manager)
- [ClawHub skill page](https://clawhub.ai/youbuwei/skills/hermes-profile-model-manager)
- [Publisher profile](https://clawhub.ai/user/youbuwei)
- [BigModel model overview](https://docs.bigmodel.cn/cn/guide/start/model-overview)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Hermes configuration changes, profile-wide batch operations, provider switches, and gateway restart commands.]

## Skill Version(s):

2.1.2 (source: artifact/SKILL.md frontmatter and server release changelog; ClawHub release metadata version: 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
