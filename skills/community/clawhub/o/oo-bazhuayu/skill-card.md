## Description:

Provides guidance for reading and managing Bazhuayu tasks and collected data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect Bazhuayu action schemas, read collected data and analytics, and manage task execution through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute unverified remote code and add or update persistent agent skills.

Mitigation: Review the setup source, use a separately verified and pinned oo CLI installation, and check which skills it installs or updates. Consider disabling startup skill synchronization with OO_SKILLS_SYNC_DISABLED.

Risk: Connector requests and linked credentials are handled by OOMOL.

Mitigation: Review the connection and its scopes, and avoid sending unnecessary sensitive content in connector requests.

Risk: Write and destructive actions can change Bazhuayu task state or overwrite data.

Mitigation: Confirm the exact payload and effect before write actions, and get explicit approval for the target before destructive actions.

## Reference(s):

- [Bazhuayu homepage](https://www.bazhuayu.com/)
- [Bazhuayu API documentation](https://openapi.bazhuayu.com/zh-CN/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-bazhuayu)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [JSON action responses with shell command examples and concise textual guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected Bazhuayu account, its plan, and the selected action.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
