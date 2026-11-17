## Description:

Operate BotStar through an OOMOL-connected account to read, create, update, delete, and publish bots and related data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and BotStar administrators use this skill with an OOMOL-connected account to inspect bots, users, attributes, and CMS data, or to create, update, delete, and publish BotStar content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented CLI installation runs downloaded code whose full effects were not verified.

Mitigation: Review and approve installation separately, preferably using a verified fixed release, and check automatic skill synchronization before running it.

Risk: BotStar write, publish, and delete actions can change connected account data.

Mitigation: Use an appropriately limited connected account and confirm the exact target and effect before these actions.

## Reference(s):

- [BotStar homepage](https://botstar.com)
- [BotStar API documentation](https://apis.botstar.com/docs/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance, Shell commands]

**Output Format:** [BotStar action results and data, with concise Markdown guidance and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output depends on the requested BotStar action.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
