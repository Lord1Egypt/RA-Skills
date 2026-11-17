## Description:

Plunk (useplunk.com). Use this skill for ANY Plunk request — reading, creating, updating, and deleting data. Whenever a task involves Plunk, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to work with Plunk contacts, transactional email, events, and email verification through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup executes unpinned remote code, and the required CLI may automatically install additional persistent agent skills.

Mitigation: Review and verify the CLI installer before setup; consider disabling startup skill synchronization with OO_SKILLS_SYNC_DISABLED.

Risk: The skill can send email, change contacts, and delete contacts; the CLI installer and hosted service are outside the inspected artifact.

Mitigation: Retain the skill's confirmation requirements for email, contact changes, and deletion, and account for the remote installer and hosted service during review.

## Reference(s):

- [Plunk documentation](https://docs.useplunk.com/)
- [Plunk homepage](https://www.useplunk.com)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-plunk)

## Skill Output:

**Output Type(s):** [API Calls, JSON data, Shell commands, Guidance]

**Output Format:** [JSON requests and responses with shell commands and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Plunk actions are performed through the oo CLI.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
