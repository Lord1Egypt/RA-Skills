## Description:

Manage a connected NetEase Enterprise Mail account through OOMOL, including reading, searching, sending, replying to, forwarding, moving, and deleting messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and external users use this skill to find and manage messages in a connected NetEase Enterprise Mail account. It supports read actions as well as sending and other mailbox changes through OOMOL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup uses remote software that has not been verified; documented startup behavior may also write to other agents' skill directories.

Mitigation: Review the CLI installation and use a verified release. Set OO_SKILLS_SYNC_DISABLED=1 to prevent the documented startup writes.

Risk: Mailbox data passes through OOMOL.

Mitigation: Review organizational data-handling requirements before connecting a mailbox.

## Reference(s):

- [NetEase Enterprise Mail](https://qiye.163.com/)
- [NetEase Enterprise Mail API documentation](https://office.163.com/helpCenter/mail/d/1892504942861234178.html?anchorTitle=mm4bctg9fyy)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API calls, Text, Guidance]

**Output Format:** [Structured connector data and text summaries or responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected mailbox and selected action.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
