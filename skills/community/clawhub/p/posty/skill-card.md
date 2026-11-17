## Description:

Posty helps agents schedule, publish, and manage social posts across supported channels using the Posty CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[norbertlevente](https://clawhub.ai/user/norbertlevente)

### License/Terms of Use:

MIT-0

## Use Case:

Social media managers and developers use this skill to authenticate to Posty, choose a workspace, prepare media, schedule or publish posts, and review analytics across supported channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commands can publish or delete posts in a connected account or the wrong workspace.

Mitigation: Confirm the account, workspace, channel, and post action with the user before executing it.

Risk: Subscription links or FotoAI generation can incur charges or use credits.

Mitigation: Confirm the plan, payment link, or credit quote before proceeding; leave payment to the user.

Risk: An incorrect timezone can schedule a post at the wrong time.

Mitigation: Use and confirm the user's actual timezone when scheduling.

Risk: Installing an unrelated package could expose the user to unreviewed software.

Mitigation: Install only the documented posty-cli package, not the similarly named posty package.

## Reference(s):

- [Posty skill on ClawHub](https://clawhub.ai/norbertlevente/skills/posty)
- [Posty website](https://posty.hu)
- [Posty MCP endpoint](https://api.posty.hu/mcp-oauth)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance]

**Output Format:** [Markdown with CLI examples and JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Posting, account, billing, and media actions require user authorization where applicable.]

## Skill Version(s):

1.2.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
