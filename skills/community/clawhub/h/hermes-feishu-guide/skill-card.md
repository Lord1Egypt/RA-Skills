## Description:

Guides developers through local deployment of a Hermes Agent Feishu/Lark bot in WebSocket mode, including Kimi API setup, Feishu permissions, environment variables, and group chat policy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cindypapa](https://clawhub.ai/user/cindypapa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure and troubleshoot a locally deployed Hermes Agent bot for Feishu/Lark using WebSocket mode without requiring a public domain.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guide uses a remote installer command that executes downloaded shell content.

Mitigation: Review the installer before running it and prefer a pinned release or checksum-verified script.

Risk: The guide configures live API and Feishu application secrets in ~/.hermes/.env.

Mitigation: Protect the environment file with restrictive permissions and rotate secrets if they are exposed.

Risk: Open group chat policy and all-user gateway access can make the bot available more broadly than intended.

Mitigation: Use allowlists or disabled group chat mode unless broad workspace access is explicitly intended.

## Reference(s):

- [Hermes official documentation](https://hermes-agent.nousresearch.com)
- [Feishu Open Platform](https://open.feishu.cn)
- [Hermes installer script](https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash and environment-variable code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes deployment steps, configuration values, verification commands, comparison tables, and troubleshooting guidance.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
