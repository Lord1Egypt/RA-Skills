## Description:

Use Sendspark through your OOMOL-connected account to read campaign data, create campaigns, and manage prospects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to access Sendspark campaign and prospect data through their OOMOL-connected account, including creating campaigns and adding prospects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup uses remote installers whose system changes were not inspected.

Mitigation: Review the CLI installation and prefer a verified release before setup.

Risk: The required CLI can install or synchronize additional agent skills.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 to disable automatic skill synchronization when you want to avoid changes to other agent skills.

Risk: Sendspark access and connection credentials are mediated through OOMOL.

Mitigation: Review whether this data flow suits your account before connecting Sendspark.

## Reference(s):

- [Sendspark](https://sendspark.com/)
- [Sendspark API documentation](https://help.sendspark.com/en/articles/9051823-api-automatically-create-dynamic-videos-via-api)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Sendspark skill release](https://clawhub.ai/oomol/skills/oo-sendspark)

## Skill Output:

**Output Type(s):** [API data, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples; Sendspark action results are returned as JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected Sendspark account and the selected action.]

## Skill Version(s):

1.0.5 (source: metadata.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
