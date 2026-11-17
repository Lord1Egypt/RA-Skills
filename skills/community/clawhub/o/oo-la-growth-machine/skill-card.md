## Description:

Connects an agent to La Growth Machine for reading, creating, and updating account data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using a connected La Growth Machine account can look up audiences, members, and leads, or create audiences and add or update leads. Write actions require confirmation of the exact payload and effect.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup runs downloaded CLI code that could not be inspected, and the CLI may make broader changes to installed agent skills.

Mitigation: Review and verify a specific CLI release before installing it. Set OO_SKILLS_SYNC_DISABLED=1 before invoking the CLI if you do not want skills installed or refreshed.

Risk: Account actions can expose or change data in the connected La Growth Machine account.

Mitigation: Connect only the intended account and review every write payload and its effect before execution.

## Reference(s):

- [La Growth Machine](https://lagrowthmachine.com)
- [La Growth Machine API documentation](https://developers.lagrowthmachine.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [La Growth Machine skill release](https://clawhub.ai/oomol/skills/oo-la-growth-machine)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Structured account data and concise guidance; action inputs use JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected account and the selected action.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
