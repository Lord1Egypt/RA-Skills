## Description:

Guides agents to use otta-cli for otta.fi worktime, absence, sick-leave, holiday, saldo, and calendar workflows with JSON-first terminal commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mekedron](https://clawhub.ai/user/mekedron)

### License/Terms of Use:


## Use Case:

Employees, operators, and developers use this skill to automate Otta time-tracking workflows from a terminal, including authentication, status checks, worktime changes, absences, holidays, saldo, and calendar reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Login examples and diagnostics can expose Otta credentials or tokens if copied into shell history, logs, or summaries.

Mitigation: Use --password-stdin or protected secret handling, and redact OTTA_CLI_PASSWORD, access tokens, and refresh tokens from logs and responses.

Risk: Worktime add, update, and delete commands can change account records.

Mitigation: Confirm mutating actions before execution and list existing worktimes first when the target record ID is not explicit.

## Reference(s):

- [Otta CLI repository listed by the skill](https://github.com/mekedron/otta-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with shell commands and JSON-oriented command output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prefers machine-readable --format json output and concise failure reporting with credentials and tokens redacted.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
