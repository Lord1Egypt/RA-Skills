## Description:

Operate UptimeRobot through your OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use the skill to review account details, monitors, and alert contacts, and to create, update, or delete monitors in a connected UptimeRobot account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Skill setup may introduce broader changes to agent configuration than expected.

Mitigation: Review the CLI setup, prefer a verified release, and set OO_SKILLS_SYNC_DISABLED=1 when only this integration is needed.

Risk: Using the integration entrusts OOMOL with access to the connected UptimeRobot account.

Mitigation: Keep approval requirements for monitor changes and deletions.

Risk: The remote installer and hosted connector implementation are outside the inspected package.

Mitigation: Review the CLI setup before installing and review the connected account permissions.

## Reference(s):

- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [UptimeRobot API documentation](https://help.uptimerobot.com/en/articles/11620152-how-to-use-uptimerobot-s-api)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text, Shell commands]

**Output Format:** [JSON requests and text summaries of UptimeRobot account data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Monitor creation and updates change account state; deletion is destructive.]

## Skill Version(s):

1.0.5 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
