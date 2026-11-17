## Description:

Operate Walletap to read, create, update, and delete wallet-pass data through the oo CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill for Walletap account tasks such as finding templates, looking up or searching passes, issuing passes, sending notifications, and updating pass details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute a remote CLI installer whose contents and remote service behavior were not audited.

Mitigation: Review the setup process and independently verify and install the CLI version before using the skill.

Risk: The CLI may automatically synchronize agent skills and make broader changes to the agent environment.

Mitigation: Decide whether to allow automatic skill synchronization and use the oo CLI command reference to disable it when appropriate.

## Reference(s):

- [Walletap](https://www.walletap.io/)
- [Walletap API documentation](https://www.walletap.io/docs/api)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-walletap)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON action payloads and Walletap responses with explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action payloads follow the live connector schema; state-changing actions require user confirmation.]

## Skill Version(s):

1.0.2 (source: artifact frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
