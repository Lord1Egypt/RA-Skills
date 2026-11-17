## Description:

Operates Mattermost through an OOMOL-connected account for reading data and creating posts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using Mattermost through an OOMOL-connected account can retrieve channel, team, and user information, list posts and channels, and create posts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute downloaded code that has not been verified.

Mitigation: Review and approve CLI installation separately before running its installer.

Risk: The required CLI may change other installed agent skills during startup synchronization.

Mitigation: Review any skill changes and use OO_SKILLS_SYNC_DISABLED to disable startup synchronization when appropriate.

Risk: The hosted connector implementation is unverified and OOMOL handles the Mattermost connection and task data.

Mitigation: Confirm OOMOL is an acceptable handler for the connection and task data, and retain the skill's confirmation step before posting.

## Reference(s):

- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Mattermost API documentation](https://api.mattermost.com/)
- [Mattermost on ClawHub](https://clawhub.ai/oomol/skills/oo-mattermost)
- [OOMOL publisher profile](https://clawhub.ai/user/oomol)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [oo CLI commands with JSON request and response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available results depend on the selected Mattermost action; creating posts changes Mattermost state and requires user confirmation.]

## Skill Version(s):

1.0.5 (source: skill frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
