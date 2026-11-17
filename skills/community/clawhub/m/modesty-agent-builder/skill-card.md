## Description:

Build high-performing OpenClaw agents end-to-end. Use when you want to design a new agent (persona + operating rules) and generate the required OpenClaw workspace files (SOUL.md, IDENTITY.md, AGENTS.md, USER.md, HEARTBEAT.md, optional MEMORY.md + memory/YYYY-MM-DD.md). Also use to iterate on an existing agent's behavior, guardrails, autonomy model, heartbeat plan, and skill roster.

This skill is ready for commercial/non-commercial use.

## Publisher:

[modestyrichards](https://clawhub.ai/user/modestyrichards)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and advanced OpenClaw users use this skill to design new agent workspaces or refine existing agents by defining persona, operating rules, guardrails, memory posture, heartbeat behavior, and validation scenarios.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated agent files may encode overly broad autonomy, outbound messaging behavior, or periodic heartbeat checks before the agent is fully reviewed.

Mitigation: Review the generated workspace files before use and keep destructive actions, outbound messaging, broad autonomy, and heartbeat checks disabled or permission-gated until rules are clear and tested.

Risk: Generated MEMORY.md or heartbeat content may preserve sensitive or inappropriate details if accepted without review.

Mitigation: Inspect MEMORY.md, memory logs, and HEARTBEAT.md content before deployment; do not store secrets, credentials, OAuth tokens, API keys, or session transcripts in the workspace.

## Reference(s):

- [OpenClaw agent workspace](references/openclaw-workspace.md)
- [OpenClaw agent file templates](references/templates.md)
- [Agent Architecture Patterns](references/architecture.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with generated workspace file contents and scenario prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce OpenClaw workspace files including SOUL.md, IDENTITY.md, AGENTS.md, USER.md, HEARTBEAT.md, optional MEMORY.md, memory/YYYY-MM-DD.md, and TOOLS.md.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
