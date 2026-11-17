## Description:

Search Referral Rock programs, members, and referrals, and retrieve member sharing, referral, and reward statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using a connected Referral Rock account can ask the agent to find programs, search or list members and referrals, and retrieve a member's sharing, referral, and reward statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can run remote code and can install or synchronize other agent skills without clearly scoped user approval.

Mitigation: Verify the CLI release before installing it, and review or disable automatic skill installation and synchronization unless those changes are intended.

Risk: The bundled instructions were reviewed, but the remote installers and deployed connector implementation were not verified; OOMOL acts as an intermediary for the connected Referral Rock account.

Mitigation: Review the CLI release and OOMOL connection before enabling the skill, and decide whether the intermediary is acceptable for the account.

## Reference(s):

- [Referral Rock API documentation](https://api.referralrock.com/help)
- [Referral Rock](https://referralrock.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured Referral Rock data and natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected account and the selected read action.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
