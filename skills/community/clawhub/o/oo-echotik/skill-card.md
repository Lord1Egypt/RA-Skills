## Description:

Access EchoTik data for product, category, creator, live, video, shop, ranking, and review research through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and commerce researchers use the skill to query EchoTik for TikTok Shop market, product, seller, creator, video, live-session, ranking, and review data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup can execute external CLI installers, and the installed release and exact version have not been verified.

Mitigation: Review the installer and choose a reviewed CLI release before installing it.

Risk: Automatic skill synchronization can introduce broader agent changes than this connector alone.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 if you only want this connector.

Risk: EchoTik credentials and queries pass through OOMOL as disclosed.

Mitigation: Review OOMOL and EchoTik connection and data-handling terms before connecting the service.

## Reference(s):

- [EchoTik API documentation](https://opendocs.echotik.live/introduction)
- [EchoTik service](https://echotik.live/zh/api-service)
- [oo CLI project documentation](https://github.com/oomol-lab/oo-cli)
- [EchoTik ClawHub release](https://clawhub.ai/oomol/skills/oo-echotik)

## Skill Output:

**Output Type(s):** [JSON data, Text, Analysis]

**Output Format:** [JSON action responses with concise natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Data may be offline; category snapshots are T+1 and product trends cover up to 180 days, as described in the skill.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
