## Description:

Runs long or continuous shell commands with file-backed logs, truncated previews, and fast log scanning. Invoke when shell output may be large, ongoing, or hard to inspect directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qipengguo](https://clawhub.ai/user/qipengguo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run and monitor long-running shell commands, inspect compact status cards, scan logs for likely failures, and stop background sessions without dumping full output into the agent context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commands run with broad local shell authority and normal user privileges.

Mitigation: Review each command before execution and require explicit approval for destructive, privilege-escalating, reboot, disk-formatting, or mass-deletion commands.

Risk: Command output is persisted to local log files and may contain sensitive data.

Mitigation: Avoid commands that print secrets, avoid passing sensitive files through logPath, and remove temporary logs when they are no longer needed.

Risk: Continuous or background commands can keep running after the initial status card returns.

Mitigation: Use the stop tool to end monitoring sessions and clean up background processes once inspection is complete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qipengguo/skills/long-context-shell)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands]

**Output Format:** [Structured status cards with truncated text previews and file-backed logs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns session identifiers, log paths, process status, exit codes, line and byte counts, severity-ranked scan matches, and timestamp-filtered previews.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
