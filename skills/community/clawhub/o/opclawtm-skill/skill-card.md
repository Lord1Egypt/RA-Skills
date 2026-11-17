## Description:

Opclawtm Skill helps agents guide users through installing and activating the opclawtm CLI, creating OpenClaw teams, configuring Feishu integrations, and troubleshooting common setup issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[poderosom1](https://clawhub.ai/user/poderosom1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to help users set up opclawtm, verify CLI installation and licensing, and guide users through OpenClaw team, Feishu, and private-skill workflows. The skill separates environment commands the agent may run from business operations that the user must complete in the TUI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to install an unpinned global opclawtm CLI package.

Mitigation: Review the package source and install a pinned, trusted opclawtm release where possible; avoid administrator or global installation unless required.

Risk: The Feishu setup flow requests broad application permissions.

Mitigation: Review requested scopes before approval and reduce Feishu permissions to the minimum needed for the deployment.

Risk: The setup flow handles Feishu App Secret values and other sensitive configuration.

Mitigation: Keep secrets in trusted tools only and do not paste credentials into untrusted chats, logs, or shared documents.

Risk: Troubleshooting may expose local gateway log identifiers.

Mitigation: Share only the minimum identifier needed for support and avoid posting raw gateway log output in chat.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/poderosom1/skills/opclawtm-skill)
- [Publisher Profile](https://clawhub.ai/user/poderosom1)
- [opclawtm Homepage](https://opclawtm.com)
- [CLI Command Reference](artifact/references/cli-reference.md)
- [Installation and Activation Flow](artifact/references/installation-flow.md)
- [Team Creation Flow](artifact/references/team-creation-flow.md)
- [Feishu Configuration Flow](artifact/references/feishu-config-flow.md)
- [Private Skill Flow](artifact/references/private-skill-flow.md)
- [Troubleshooting Guide](artifact/references/troubleshooting.md)
- [Feishu Bot Tutorial](https://www.feishu.cn/content/article/7602519239445974205)
- [Feishu Open Platform](https://open.feishu.cn/app)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance distinguishes agent-executable environment checks from user-operated TUI business workflows.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
