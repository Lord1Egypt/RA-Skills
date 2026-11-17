## Description:

OpenCode Remote helps an agent manage remote OpenCode sessions over HTTP, including session tracking, message sending, status monitoring, and task execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[entropy-xcy](https://clawhub.ai/user/entropy-xcy)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to operate remote OpenCode servers, continue work in existing sessions, create new sessions, send prompts, and monitor task progress.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control remote OpenCode servers and includes high-impact operations such as remote shell execution, destructive session actions, configuration changes, PTY access, and file-content access.

Mitigation: Use it only with OpenCode servers you control, preferably behind HTTPS or a trusted private network with real authentication, and avoid high-impact endpoints unless that authority is explicitly intended.

Risk: Prompts, session outputs, and monitoring summaries may contain sensitive information.

Mitigation: Review prompts before sending, limit what is repeated or stored, and avoid sending secrets or private data to remote sessions.

Risk: The skill may store session identifiers locally and create ongoing monitoring.

Mitigation: Treat session IDs as sensitive, periodically remove stale local session records, and cancel monitoring when tasks complete.

## Reference(s):

- [OpenCode API Reference](references/api_reference.md)
- [ClawHub Skill Page](https://clawhub.ai/entropy-xcy/skills/opencode-remote)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, API examples, and helper-script usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local session records and monitoring workflows when used by an agent.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
