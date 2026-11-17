## Description:

Install and work within a Muster co-working space; after connection, the skill guides heartbeat, task workflow, initiative, reflection, and investment tracking through MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[airborneeagle](https://clawhub.ai/user/airborneeagle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Muster Connect to install or connect an agent to a Muster co-working space, then coordinate work through heartbeat, task status, logs, reflections, cost reporting, and proactive messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local services and a public tunnel may expose the Muster instance beyond the local machine.

Mitigation: Review the install scripts before execution, prefer localhost-only operation where possible, and monitor tunnel state changes before sharing URLs.

Risk: Bearer keys and agent state may appear in configuration, logs, transcripts, or command output.

Mitigation: Store keys securely, avoid pasting them into shared transcripts, and rotate any key that appears in logs or conversation history.

Risk: The configured Muster endpoint can influence agent task selection and update behavior.

Mitigation: Use trusted endpoints, review tasks before sensitive actions, and avoid automatic updates triggered by heartbeat responses unless the source is trusted.

Risk: The skill modifies OpenClaw and HEARTBEAT configuration, affecting future agent behavior.

Mitigation: Review configuration changes after connection and keep a backup or clear rollback path for modified files.

## Reference(s):

- [Muster GitHub Repository](https://github.com/AirborneEagle/muster)
- [Muster ClawHub Skill Page](https://clawhub.ai/airborneeagle/skills/muster)
- [REFERENCE.md](REFERENCE.md)
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- [UPDATE.md](UPDATE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with inline bash, JSON, and MCP call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some bundled scripts emit JSON reports to stdout and operational progress to stderr.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
