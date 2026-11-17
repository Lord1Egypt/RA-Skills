## Description:

Manage HelpDesk tickets through an OOMOL-connected account, including reading, searching, creating, updating, and deleting records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Support teams can use the skill to inspect HelpDesk tickets and manage ticket updates through their connected HelpDesk account. Creating, updating, and destructive actions require confirmation as documented by the skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup downloads and runs the CLI installer without a separate installation approval step; the installers and hosted implementation were not verified.

Mitigation: Review and approve installation separately, and prefer an inspected, version-pinned CLI installation.

Risk: Ticket creation, updates, and destructive actions can change HelpDesk data.

Mitigation: Confirm the exact write payload or destructive target and effect before running the action; connect only the intended HelpDesk account.

## Reference(s):

- [HelpDesk homepage](https://www.helpdesk.com)
- [HelpDesk API documentation](https://api.helpdesk.com/docs)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [HelpDesk records and action results, with concise natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read, write, and destructive actions are distinguished in the skill; writes and destructive actions require user confirmation.]

## Skill Version(s):

1.0.5 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
