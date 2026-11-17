## Description:

Keep an OpenClaw-style local runtime on the snapshot-first, thin-BFF-first, read-only Campus Copilot path.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaojiou176](https://clawhub.ai/user/xiaojiou176)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to keep OpenClaw-style local runtimes on a read-only Campus Copilot consumption path. It helps agents choose snapshot-first, thin-BFF-first command and configuration flows without browser takeover or write-capable operation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill references local Campus Copilot commands and MCP configuration that may not exist or may behave differently outside a compatible repo.

Mitigation: Run the referenced commands only in repos that contain the expected Campus Copilot packages, and review repo-local documentation before adapting MCP configuration.

Risk: Snapshot paths can expose local data to the consuming runtime.

Mitigation: Point the snapshot path only at data intended for local runtime use, and keep claims snapshot-scoped and read-only.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaojiou176/skills/openclaw-readonly-consumer)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and configuration references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only, snapshot-scoped operational guidance]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
