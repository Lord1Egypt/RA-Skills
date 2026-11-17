## Description:

Build, bootstrap, and maintain a stable OpenClaw default agent identity by interviewing the user, updating IDENTITY.md, and seeding core context files (AGENTS.md, SOUL.md, TOOLS.md, USER.md, HEARTBEAT.md, BOOTSTRAP.md).

This skill is ready for commercial/non-commercial use.

## Publisher:

[msaum](https://clawhub.ai/user/msaum)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to bootstrap a new agent baseline or refresh an existing agent identity through a five-question interview. It creates or updates core workspace context files and memory scaffolding with practical defaults.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is intended to edit long-lived OpenClaw identity, memory, and bootstrap files.

Mitigation: Ask for a preview or diff before applying changes when existing context files contain important content.

Risk: Incorrect or overbroad synthesized defaults could affect future agent behavior.

Mitigation: Review generated context files before relying on them for daily agent use.

## Reference(s):

- [OpenClaw context documentation](https://docs.openclaw.ai/concepts/context)
- [Bootstrap Core Files](references/bootstrap-core-files.md)
- [Ranked Question Bank](references/question-bank.md)
- [ClawHub skill page](https://clawhub.ai/msaum/skills/openclaw-default-agent-backstory)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Configuration, Guidance]

**Output Format:** [Markdown workspace files and concise conversational summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update AGENTS.md, SOUL.md, TOOLS.md, IDENTITY.md, USER.md, HEARTBEAT.md, BOOTSTRAP.md, MEMORY.md, and daily memory notes under memory/.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
