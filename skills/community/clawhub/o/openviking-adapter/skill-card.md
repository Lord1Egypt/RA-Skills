## Description:

OpenViking memory adapter for OpenClaw that organizes agent memory into layered summaries and supports on-demand memory search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yyu812707-wq](https://clawhub.ai/user/yyu812707-wq)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to analyze existing agent memory token usage, generate L0/L1 Markdown summaries, and search relevant memories instead of loading the full memory set every time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads OpenClaw memory files that may contain sensitive personal details, secrets, credentials, or untrusted instructions.

Mitigation: Install only when this memory access is acceptable, and avoid running it on memory files that may contain sensitive or untrusted content.

Risk: Generated L0_soul.md and L1_overview.md files persist plaintext summaries that can be loaded into later agent conversations.

Mitigation: Review generated memory summary files before allowing an agent to load them in future sessions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yyu812707-wq/skills/openviking-adapter)
- [ByteDance OpenViking](https://github.com/bytedance/OpenViking)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown and plain-text tool responses, including generated memory summary files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates persistent plaintext summaries under ~/.openclaw/workspace/memory_viking.]

## Skill Version(s):

1.0.0 (source: frontmatter, skill.json, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
