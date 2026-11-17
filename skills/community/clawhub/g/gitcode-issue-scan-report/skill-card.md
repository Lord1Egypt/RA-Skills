## Description:

Use when a user asks to scan, audit, classify, reconcile, or report GitCode Issues and linked PR states, including requests for a reviewable Issue-closing script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sun9898](https://clawhub.ai/user/sun9898)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to audit open GitCode Issues, classify them by issue type and linked PR state, reconcile included and excluded counts, and generate a Markdown report. When explicitly requested, it can produce a reviewable Bash or PowerShell script for manually closing eligible Issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated close scripts can be unsafe if attacker-controlled repository, branch, or GitCode command values are included and then run.

Mitigation: Use the read-only report workflow by default, and run generated close scripts only after validating the repository, branch, command values, and listed Issue IDs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sun9898/skills/gitcode-issue-scan-report)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code]

**Output Format:** [Markdown report with optional Bash or PowerShell close script and JSON command summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and either gitcode-npm or gitcode; generated close scripts are for manual review and execution only.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
