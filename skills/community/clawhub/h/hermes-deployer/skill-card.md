## Description:

Helps developers and operators install, configure, deploy, and operate Hermes Agent on Linux servers, including LLM provider setup, messaging integrations, systemd service management, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dengjiawei1226](https://clawhub.ai/user/dengjiawei1226)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to deploy Hermes Agent as a persistent Linux server service, configure LLM providers and messaging channels, and troubleshoot gateway or systemd issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A persistent messaging agent may be exposed with broad access or weak safeguards.

Mitigation: Run it under a dedicated low-privilege service account or container, disable allow-all/open messaging defaults, and require human review before service changes or automatic skill changes.

Risk: Configuration examples include secrets and token files for LLM and messaging providers.

Mitigation: Store tokens with owner-only permissions and rotate or revoke credentials if they are exposed.

Risk: Using broad permission modes or unreviewed upstream updates can expand the agent's operational authority.

Mitigation: Avoid bypassPermissions for network-facing bots and pin Hermes to a reviewed commit or signed release.

## Reference(s):

- [Hermes Agent repository](https://github.com/NousResearch/hermes-agent)
- [Weixin iLink platform](https://ilinkai.weixin.qq.com)
- [ClawHub Hermes Deployer page](https://clawhub.ai/dengjiawei1226/skills/hermes-deployer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash, YAML, environment variable, and systemd configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes operational troubleshooting steps and deployment commands that should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
