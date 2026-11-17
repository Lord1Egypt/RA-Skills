## Description:

PortEden (porteden.com). Use this skill for ANY PortEden request — reading, creating, updating, and deleting data. Whenever a task involves PortEden, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using a connected PortEden account use this skill to search, read, send, reply to, forward, label, and delete email through connected Gmail or Microsoft 365 accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions can trigger a downloaded installer, and the remote installers were not validated by the security review.

Mitigation: Review setup behavior before installation; install a verified CLI yourself or require separate approval before downloaded installers run, and check whether setup installs additional agent skills.

Risk: Email access and actions depend on the permissions granted to the connected account.

Mitigation: Grant only the needed email permissions and retain confirmation before sending, forwarding, modifying, or deleting messages.

## Reference(s):

- [PortEden API documentation](https://porteden.com/docs/api/authentication/)
- [PortEden](https://porteden.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands target the selected PortEden email action; payload fields follow that action's live schema.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
