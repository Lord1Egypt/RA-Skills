## Description:

Use the BugHerd-connected oo CLI to read and manage BugHerd projects, tasks, comments, and attachments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users with an OOMOL-connected BugHerd account can use this agent skill to inspect projects, tasks, comments, and attachments, and to create or update BugHerd records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions may execute downloaded installer code without separate approval or integrity checks; the installers and hosted connector implementation were not available for inspection.

Mitigation: Review the CLI and its automatic skill synchronization settings before enabling the skill. Connect only the intended BugHerd account and require confirmation for each write.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [BugHerd](https://bugherd.com/)
- [BugHerd API documentation](https://docs.bugherd.com/api/)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [JSON responses and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some actions create or update BugHerd data and require user confirmation.]

## Skill Version(s):

1.0.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
