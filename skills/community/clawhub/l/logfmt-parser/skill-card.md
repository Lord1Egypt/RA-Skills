## Description:

Parses and converts log files into clean JSON for analysis, debugging, and forwarding to log aggregators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[albionaiinc-del](https://clawhub.ai/user/albionaiinc-del)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to convert local application or server logs into structured JSON for easier analysis, debugging, and forwarding to log aggregators.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default output includes each original log line, which may expose secrets or personal data contained in logs.

Mitigation: Use --no-log-field or sanitize logs before processing when inputs may contain sensitive information.

## Reference(s):

- [Logfmt Parser ClawHub Skill Page](https://clawhub.ai/albionaiinc-del/skills/logfmt-parser)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [Newline-delimited JSON records with Markdown usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can read from a file or standard input, optionally extract timestamps, and optionally omit the original log line.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
