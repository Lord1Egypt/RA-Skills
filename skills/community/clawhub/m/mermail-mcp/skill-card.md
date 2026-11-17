## Description:

Helps agents configure, verify, and troubleshoot a Mermail MCP connection across supported clients.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mermail](https://clawhub.ai/user/mermail)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace users use this skill to connect an MCP client to Mermail, choose an appropriate authentication mode and tool profile, verify read-only access, and diagnose connection failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mermail API keys or OAuth credentials could be exposed in configuration or diagnostics.

Mitigation: Prefer OAuth; keep API keys in a secret store or launch environment and redact credentials from chat, files, and logs.

Risk: An incorrect workspace, profile, or authentication mode could grant broader mail or PayBox access than intended.

Mitigation: Confirm the selected workspace and profile; use the restricted agent-inbox profile when appropriate and enable full-profile PayBox tools only when their authority is intended.

Risk: Connectivity tests or retries could unintentionally modify mailboxes, send mail, or repeat an uncertain write.

Mitigation: Verify with tool discovery and a read-only workspace or mailbox call; never use write tools as smoke tests or replay uncertain writes after reconnecting.

## Reference(s):

- [Mermail agent skill documentation](https://docs.mermail.app/ai/skills)
- [Mermail agent setup](https://mermail.app/agents)
- [ClawHub skill release](https://clawhub.ai/mermail/skills/mermail-mcp)
- [Platform configuration](references/platforms.md)
- [Connection safety](references/security.md)
- [Verification and troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Shell commands, Markdown]

**Output Format:** [Markdown with configuration and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Redacts credentials; distinguishes connection status, selected workspace, tool profile, and read-only verification results.]

## Skill Version(s):

1.2.15 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
