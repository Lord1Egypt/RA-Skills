## Description:

Connects and disconnects OpenViking long-term memory for eight coding agents, with commands to check integration status and verify the memory service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to integrate or unbind OpenViking memory for supported coding agents, verify connectivity, and check whether an integration is active or requires a restart.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Executable plugins may be downloaded and retained before the confirmation prompt; declining that prompt may not undo downloads.

Mitigation: Review the skill and plugin sources before running it, preview changes with dry-run, and do not rely on declining the prompt to prevent downloads.

Risk: Remote plugin downloads include an unverified module sync path.

Mitigation: Use only audited plugin sources and avoid --yes unless the downloads and their destinations have been reviewed.

Risk: Persistent agent hooks can automatically capture conversation content into OpenViking.

Mitigation: Use a local or trusted endpoint and enable integration only for agents and sessions where memory capture is appropriate.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-openviking-agent-integration)
- [Agent configuration reference](references/agent-configs.md)
- [Integration and safety notes](references/notes.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration guidance, Status reports]

**Output Format:** [Markdown with shell commands; optional JSON status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports dry-run previews and per-agent status checks.]

## Skill Version(s):

1.0.4 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
