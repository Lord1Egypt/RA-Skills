## Description:

Prompt Compressor helps OpenClaw users reduce token use by adding SOUL.md guidance for concise agent responses, memory logs, daily logs, and pre-compaction summaries, and by manually compressing prompts on request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckpxgfnksd-max](https://clawhub.ai/user/ckpxgfnksd-max)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to reduce token consumption and API spend by installing concise-response guidance or asking the agent to compress specific prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent concise-mode instructions can change agent behavior across future OpenClaw sessions.

Mitigation: Install only when persistent concise responses are intended; prefer a workspace-scoped SOUL.md for limited scope and keep a backup or uninstall plan.

Risk: The optional hook can rewrite user messages before the model sees them.

Mitigation: Avoid enabling the hook unless pre-model message rewriting is acceptable; use one-off prompt compression or SOUL.md guidance instead.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ckpxgfnksd-max/skills/prompt-token-saver)
- [Project homepage](https://github.com/ckpxgfnksd-max/prompt-compressor-openclaw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and rewritten prompt text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May provide before/after compression examples and installation guidance for SOUL.md or optional hook-based compression.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
