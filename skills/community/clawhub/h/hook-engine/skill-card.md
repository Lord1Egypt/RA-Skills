## Description:

Hook Engine is an event-driven behavior guard system that uses configurable rules to inspect and control exec commands and message-sending events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add pre-execution, post-execution, and message-format hooks that warn, block, or log actions according to Markdown-defined rules. It is intended to help review command execution and outbound messages before an agent proceeds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The hook system can observe commands and messages and keep command audit records in the workspace.

Mitigation: Use it only in workspaces where command and message observation is acceptable; define audit-log redaction, retention, and file permissions before deployment.

Risk: The documented protection catalog does not fully match what the included scripts enforce.

Mitigation: Treat warnings and blocks as review assistance until rule coverage is tested against the actual scripts and documented gaps are resolved.

Risk: JSON parsing and escaping limitations can affect decisions, messages, or audit-log content.

Mitigation: Validate hook inputs with representative event JSON, prefer environments with jq available, and review generated JSON output before relying on the hooks.

## Reference(s):

- [Hook API documentation](artifact/references/hook-api.md)
- [Security patterns catalog](artifact/rules/security-patterns.md)
- [ClawHub skill page](https://clawhub.ai/paudyyin/skills/hook-engine)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown documentation, shell scripts, rule configuration, JSON hook responses, and workspace audit-log entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write command audit records to memory/hook-audit.log when integrated.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
