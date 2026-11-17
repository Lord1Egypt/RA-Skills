## Description:

Converts MCP servers into standalone skill packages so agents can call generated Bash-based capabilities without keeping an MCP process running.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jalanchao](https://clawhub.ai/user/jalanchao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to replace a registered or command-based MCP server with a generated skill package. It supports tool-schema extraction, command drafting, configuration and secrets scaffolding, and optional agent registration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may run inferred shell commands or test generated read-only commands against destinations that have not been reviewed.

Mitigation: Inspect each generated command and destination before execution, and test only in a sandbox or controlled environment.

Risk: The inspector can fetch source packages for MCP servers, which may expose the agent to untrusted package content.

Mitigation: Use only trusted MCP servers, pin or verify package sources before fetching, and isolate package inspection from sensitive environments.

Risk: Generated skills may be registered in persistent agent locations before their behavior has been fully reviewed.

Mitigation: Review and scan generated skill files before registration, and require explicit user approval for persistent agent configuration changes.

Risk: Generated plaintext secrets files can create credential handling risk.

Mitigation: Prefer environment variables or a secret manager, keep secrets files out of version control, and commit only sanitized example files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jalanchao/skills/mcp-to-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with inline shell commands and generated package files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce config files, secrets templates, helper scripts, and registration guidance for the generated skill.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
