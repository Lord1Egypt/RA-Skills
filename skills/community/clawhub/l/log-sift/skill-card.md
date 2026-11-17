## Description:

Log Sift filters large log files by keywords and timestamp ranges from files or stdin.

This skill is ready for commercial/non-commercial use.

## Publisher:

[albionaiinc-del](https://clawhub.ai/user/albionaiinc-del)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use Log Sift to inspect application or server logs during troubleshooting, filtering noisy output by keywords and time windows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Logs can contain sensitive data.

Mitigation: Run Log Sift only on files the user intends to inspect and handle filtered output according to the applicable data handling policy.

Risk: Date-only examples may not match the script's default full-timestamp parser.

Mitigation: Use full timestamps or provide a matching --date-format when filtering by date.

## Reference(s):

- [ClawHub Log Sift skill page](https://clawhub.ai/albionaiinc-del/skills/log-sift)
- [albionaiinc-del publisher profile](https://clawhub.ai/user/albionaiinc-del)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline bash examples and plain-text CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local log files or stdin and emits matching log lines; date filters require timestamps matching the configured date format.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
