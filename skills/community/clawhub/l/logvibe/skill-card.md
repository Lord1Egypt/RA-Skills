## Description:

Logvibe colorizes HTTP status codes in log files so successes, redirects, client errors, and server errors are easier to identify in a terminal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[albionaiinc-del](https://clawhub.ai/user/albionaiinc-del)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and sysadmins use Logvibe to scan web server logs quickly by highlighting common HTTP status-code classes in file, piped, or single-line log input.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Attacker-controlled logs can contain terminal control sequences that make terminal output misleading.

Mitigation: Use Logvibe with trusted or sanitized logs, and strip or escape control characters before printing untrusted log content.

## Reference(s):

- [Logvibe ClawHub skill page](https://clawhub.ai/albionaiinc-del/skills/logvibe)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Terminal text with ANSI color highlighting and markdown usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads from a log file, stdin, or a single piped line and highlights standalone 2xx, 3xx, 4xx, and 5xx status codes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
