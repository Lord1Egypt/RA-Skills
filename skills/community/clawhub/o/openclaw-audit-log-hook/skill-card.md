## Description:

Records OpenClaw tool calls before and after execution for audit logging, debugging, usage statistics, and error tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanxiao-bot](https://clawhub.ai/user/hanxiao-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to add audit logging around OpenClaw tool execution so they can investigate tool usage, failures, and session-level activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audit logs may record sensitive tool inputs, outputs, and user or session identifiers without effective redaction.

Mitigation: Before installing, add mandatory recursive redaction, minimize logged fields, pseudonymize identifiers, and define log retention and access controls.

Risk: Using the sample as-is with credentials, private files, user messages, or production tools could expose sensitive information.

Mitigation: Use only in environments where complete tool-call auditing is intended and logs are tightly controlled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hanxiao-bot/skills/openclaw-audit-log-hook)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JavaScript, JSON, and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes audit log record examples and commands for basic log statistics.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
