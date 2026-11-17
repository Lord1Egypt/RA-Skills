## Description:

Design and generate complete OpenClaw agent workspaces with personas, rules, memory, and heartbeat plans, then iterate on behavior and autonomy efficiently.

This skill is ready for commercial/non-commercial use.

## Publisher:

[godferylindsay](https://clawhub.ai/user/godferylindsay)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and advanced OpenClaw users use this skill to create new agent workspaces or refine existing agents. It helps define persona, operating rules, autonomy boundaries, memory practices, heartbeat behavior, skill roster, guardrails, and acceptance tests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated agent workspace files may allow more autonomy or heartbeat behavior than intended if adopted without review.

Mitigation: Review generated AGENTS.md, MEMORY.md, and HEARTBEAT.md before use, especially when selecting high autonomy or periodic heartbeats.

Risk: Agent workspaces can become risky if users store credentials, session transcripts, or private configuration in generated or committed files.

Mitigation: Keep secrets, OpenClaw credentials, and session transcripts out of the workspace, following the artifact guidance.

## Reference(s):

- [OpenClaw agent workspace cheat sheet](artifact/references/openclaw-workspace.md)
- [OpenClaw agent file templates](artifact/references/templates.md)
- [Agent Architecture Patterns](artifact/references/architecture.md)
- [Agent Builder on ClawHub](https://clawhub.ai/godferylindsay/skills/godfery-agent-builder)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown workspace files, concise prompts, checklists, and targeted diffs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local OpenClaw workspace guidance and file content; it does not show hidden execution, credential access, or data transfer behavior in the security evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
