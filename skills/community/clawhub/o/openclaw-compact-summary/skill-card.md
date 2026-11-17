## Description:

Generates a structured Markdown summary format for OpenClaw memory flush and compaction workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanxiao-bot](https://clawhub.ai/user/hanxiao-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to standardize memory compaction into a reusable MEMORY.md summary with conversation scope, tools, requests, tasks, files, current work, timeline, and resume state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The template includes a resume instruction that may cause future agents to continue from persistent memory without recap.

Mitigation: Review generated MEMORY.md content before relying on it, and remove or adjust the Resume Instruction section if persistent memory should contain only factual state.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hanxiao-bot/skills/openclaw-compact-summary)

## Skill Output:

**Output Type(s):** [markdown, guidance, configuration]

**Output Format:** [Markdown structured summary template]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a MEMORY.md-oriented summary structure with a resume instruction for subsequent agent continuation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
