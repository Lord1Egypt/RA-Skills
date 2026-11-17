## Description:

Omni Tool is a Bash command-line utility for recording task activity, searching recent entries, checking status, and exporting local logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and command-line users use Omni Tool to keep local task logs for runs, checks, analysis, configuration changes, batch work, and reports, then search or export those records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill metadata advertises bookmark or Chrome functionality, while the artifact behaves as a local logging tool.

Mitigation: Review before installing if bookmark or Chrome behavior was expected; evaluate it as a terminal logging utility.

Risk: Command inputs may be persisted in plaintext local logs and later exposed by recent, search, status, or export commands.

Mitigation: Use only for non-sensitive notes or task logs, and avoid entering secrets, credentials, private customer data, or regulated data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bytesagain3/skills/omni-tool)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Plain text command output with local log and export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores command inputs and history in plaintext under ~/.local/share/omni-tool.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
