## Description:

Hermes 与本地 OpenClaw 协同工作方案 — 共享记忆、API互调、任务分工

This skill is ready for commercial/non-commercial use.

## Publisher:

[fish1981bimmer](https://clawhub.ai/user/fish1981bimmer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to coordinate Hermes with a local OpenClaw setup for shared memory, local agent calls, task routing, and operational troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide workspace writes, configuration edits, gateway restarts, log access, OpenClaw agent calls, and external message delivery.

Mitigation: Keep use read-only by default and require explicit human approval before any workspace write, config edit, gateway restart, log inspection, or Feishu delivery.

Risk: Operational guidance may affect a local OpenClaw setup or running tasks.

Mitigation: Use trusted or sandboxed environments first, back up ~/.openclaw before maintenance, set reasonable command timeouts, and retain operation logs for audit.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance includes approval, backup, audit, and read-only defaults for higher-risk local OpenClaw operations.]

## Skill Version(s):

1.1.0 (source: server release metadata; source skill version history: v1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
