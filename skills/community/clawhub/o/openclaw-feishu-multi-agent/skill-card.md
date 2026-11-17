## Description:

Build and troubleshoot OpenClaw multi-agent workflows on Feishu by combining visible `<at>` mentions with `sessions_send` delivery for reliable delegation, handoffs, and multi-hop group-chat discussions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ccharlesmeng](https://clawhub.ai/user/ccharlesmeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to design, scaffold, audit, and repair OpenClaw coordinator and specialist agent workflows for Feishu group chats. It helps users produce role-driven configuration, identity, protocol, and troubleshooting artifacts for reliable agent-to-agent handoffs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make broad persistent changes to OpenClaw routing, identity, protocol, and session files.

Mitigation: Use dry-run mode first, inspect every planned path and diff, and enable write mode only after confirming the target OpenClaw state directory and role mapping.

Risk: Roles files may contain Feishu app secrets, account bindings, workspaces, and agent directories.

Mitigation: Keep roles files trusted, use placeholders in shared artifacts, and remove real `appSecret` values from generated or published files.

Risk: Repairing session metadata for the wrong Feishu group or agent can disrupt unrelated OpenClaw sessions.

Mitigation: Provide the exact group ID, isolate this setup from unrelated sessions where possible, and create backups before applying repair operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ccharlesmeng/skills/openclaw-feishu-multi-agent)
- [OpenClaw + Feishu multi-agent reference](reference.md)
- [Reusable templates](templates.md)
- [Example role definition](roles.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration, generated files, and reusable role templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run-first workflows are documented for configuration application and session repair.]

## Skill Version(s):

1.0.1 (source: server release metadata and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
