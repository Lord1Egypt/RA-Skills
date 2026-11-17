## Description:

Creates and maintains a persistent personal memory layer for OpenClaw that learns from interactions, extracts patterns, and supports personalized contextual assistance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pathanaawej0-dot](https://clawhub.ai/user/pathanaawej0-dot)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let OpenClaw maintain local long-term memory about user preferences, patterns, context, and interaction history. It supports personalized assistance through structured insights and synthesized profile documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically build a broad long-term personal profile from conversations.

Mitigation: Enable it only with explicit user consent and confirm where memory files are stored before use.

Risk: Personal memory files may retain sensitive or unwanted information over time.

Mitigation: Provide review, edit, deletion, and forgetting workflows, and confirm whether automatic extraction can be disabled.

Risk: The skill may alter AGENTS.md with memory-aware guidelines.

Mitigation: Require user approval before applying persistent agent-behavior changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pathanaawej0-dot/skills/personal-memory-layer)

## Skill Output:

**Output Type(s):** [Markdown, Files, Configuration]

**Output Format:** [Markdown profile and insight files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local memory files, profile documents, and extraction logs.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
