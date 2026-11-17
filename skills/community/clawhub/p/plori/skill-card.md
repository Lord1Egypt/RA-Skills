## Description:

Runs tasks on Plori cloud agents that continue after the chat ends, such as background or parallel builds, scheduled automations, long jobs and research saved as files. Not for quick tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuchen-plori](https://clawhub.ai/user/yuchen-plori)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to connect an agent to Plori cloud workspaces and delegate long-running, parallel, scheduled, or file-producing tasks. It also guides setup, authentication, approvals, and management of runs and workspace files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project data sent to Plori and its AI providers may include sensitive information.

Mitigation: Share only data you are authorized to send to those services.

Risk: Persistent cloud runs can incur costs and continue operating after the chat ends.

Mitigation: Set spending and runtime limits, and keep external actions and deletion under human control.

Risk: CLI installation or authentication configuration can introduce supply-chain or credential exposure risks.

Mitigation: Prefer the hosted MCP connection when CLI access is unnecessary; otherwise review and pin installation code, and clear authentication when disconnecting.

## Reference(s):

- [Plori MCP connection guide](https://plori.ai/mcp)
- [Plori authentication guide](https://plori.ai/auth.md)
- [Plori CLI documentation](https://plori.ai/docs/cli)

## Skill Output:

**Output Type(s):** [Guidance, Configuration instructions, Shell commands, API calls]

**Output Format:** [Markdown guidance with configuration examples and inline commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Authentication guidance may involve API keys; keep credentials private.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
