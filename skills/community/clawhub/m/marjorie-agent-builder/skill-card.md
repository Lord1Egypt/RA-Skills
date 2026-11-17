## Description:

Build high-performing OpenClaw agents end-to-end. Use when you want to design a new agent (persona + operating rules) and generate the required OpenClaw workspace files (SOUL.md, IDENTITY.md, AGENTS.md, USER.md, HEARTBEAT.md, optional MEMORY.md + memory/YYYY-MM-DD.md). Also use to iterate on an existing agent's behavior, guardrails, autonomy model, heartbeat plan, and skill roster.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marjoriebroad](https://clawhub.ai/user/marjoriebroad)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and advanced OpenClaw users use this skill to design new agent workspaces, generate core workspace files, and refine an existing agent's behavior, guardrails, autonomy model, heartbeat plan, and skill roster.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated AGENTS.md, MEMORY.md, and HEARTBEAT.md content can shape future agent behavior.

Mitigation: Review generated workspace files before use and keep core safety rules in AGENTS.md.

Risk: Memory files may contain private user or workspace information if populated carelessly.

Mitigation: Keep memory files private and avoid storing secrets, credentials, or sensitive session transcripts.

Risk: Autopilot or heartbeat behavior can increase agent autonomy and token use.

Mitigation: Enable autopilot or heartbeat behavior only after reviewing the generated instructions and confirming the desired autonomy level.

## Reference(s):

- [OpenClaw agent workspace](references/openclaw-workspace.md)
- [OpenClaw agent file templates](references/templates.md)
- [Agent Architecture Patterns](references/architecture.md)
- [Complete setup guide](https://skillboss.co/skill.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with file templates, checklists, scenario prompts, and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces tailored OpenClaw workspace file content and review guidance; users should review generated agent instructions before deployment.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
