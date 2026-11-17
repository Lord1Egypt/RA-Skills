## Description:

Use when creating OpenClaw agents, configuring workspaces, multi-agent routing, session isolation, or channel bindings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a12591771](https://clawhub.ai/user/a12591771)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to create and configure OpenClaw agents, including workspace setup, session isolation, channel routing, model selection, tool restrictions, and skill integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated agent configuration may enable hooks, heartbeat checks, memory, or session cleanup that affect what an agent runs, remembers, or deletes.

Mitigation: Review those settings before installation or deployment, and confirm they match the intended operational and data-retention policy.

Risk: Copied channel bindings, mention requirements, sandbox settings, or tool allow/deny lists may route messages or grant tool access differently than intended.

Mitigation: Validate bindings, channel identifiers, sandbox mode, and tool permissions against the intended users and channels before applying the configuration.

## Reference(s):

- [OpenClaw Agent Runtime](https://docs.openclaw.ai/concepts/agent.md)
- [OpenClaw Documentation](https://docs.openclaw.ai/)
- [OpenClaw Skills](https://docs.openclaw.ai/tools/skills.md)
- [OpenClaw Agent Workspace](https://docs.openclaw.ai/concepts/agent-workspace.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON5 configuration examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides setup workflows, configuration patterns, and deployment checklists; the skill itself is documentation-only.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
