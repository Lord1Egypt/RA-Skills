## Description:

Gift Up (giftup.com). Use this skill for ANY Gift Up request — reading, creating, updating, and deleting data. Whenever a task involves Gift Up, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users with a connected Gift Up account use this skill to inspect company, gift card, item, order, location, promotion, and transaction data, and to make approved gift card changes through OOMOL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI dependency can make broader, persistent changes to installed agent skills that this skill does not explain.

Mitigation: Review the CLI installation separately and consider setting OO_SKILLS_SYNC_DISABLED=1 before first use to prevent automatic changes to other agents' skills. Keep the required approvals for balance changes and voids.

## Reference(s):

- [Gift Up homepage](https://www.giftup.com/)
- [Gift Up API documentation](https://developer.giftup.com/api#authentication)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [ClawHub skill release](https://clawhub.ai/oomol/skills/oo-gift-up)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text, Shell commands, Configuration instructions]

**Output Format:** [JSON data returned by connector actions, with shell command examples and explanatory text in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action inputs must match the live connector schema; the skill instructs users to confirm state-changing and destructive operations.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
