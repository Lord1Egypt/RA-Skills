## Description:

Better Proposals (betterproposals.io). Use this skill for ANY Better Proposals request — searching and reading data. Whenever a task involves Better Proposals, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People who manage proposals in Better Proposals can use this skill to search and read proposals, quotes, companies, currencies, templates, and account settings through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup provides remote CLI installers whose full effects were unavailable for inspection.

Mitigation: Review and approve the CLI installation separately before running it.

Risk: The CLI may synchronize or otherwise change agent skills at startup.

Mitigation: Review the CLI's skill changes; set OO_SKILLS_SYNC_DISABLED=1 to disable startup synchronization.

Risk: Proposal data and connection credentials are handled through OOMOL's connected account.

Mitigation: Consider whether OOMOL should handle this data and these credentials before connecting the service.

## Reference(s):

- [Better Proposals](https://betterproposals.io)
- [Better Proposals API documentation](https://betterproposals.io/resources/api/)
- [oo CLI controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-better-proposals)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON data and text summaries from Better Proposals read actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected Better Proposals account and the selected read action.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
