## Description:

Use the connected Check account to search and read data, including tax agencies and US address validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query Check through their connected OOMOL account, retrieve tax-agency data, and validate US addresses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Initial CLI setup can execute a downloaded installer whose exact local effects were not inspected.

Mitigation: Review and approve the CLI installation separately before automatic setup.

Risk: OOMOL mediates Check requests and receives the submitted inputs.

Mitigation: Send only information appropriate to share with OOMOL for this integration.

Risk: The CLI's skill synchronization can make broader persistent changes to agent skills.

Mitigation: Review or disable broader synchronization with OO_SKILLS_SYNC_DISABLED when only the Check integration is needed.

## Reference(s):

- [OO CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [OO CLI repository](https://github.com/oomol-lab/oo-cli)
- [Check homepage](https://www.checkhq.com)
- [Check API quickstart](https://docs.checkhq.com/docs/quickstart)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON request payloads and action responses, with Markdown guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Inputs follow the selected action's schema.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
