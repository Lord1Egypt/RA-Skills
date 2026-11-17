## Description:

Analyze and optimize OpenClaw system prompt token usage by compressing workspace files (AGENTS.md, SOUL.md, USER.md, TOOLS.md, IDENTITY.md, HEARTBEAT.md, MEMORY.md).

This skill is ready for commercial/non-commercial use.

## Publisher:

[dgkim311](https://clawhub.ai/user/dgkim311)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to audit workspace prompt files, identify token-heavy areas, and apply only approved compression changes that preserve agent behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect sensitive workspace prompt, user, tool, and memory Markdown files.

Mitigation: Run it only against intended directories and review proposed changes before approval, especially for MEMORY.md and tool-related files.

Risk: Exact token counts may depend on optional tokenizer availability and may differ from the target model tokenizer.

Mitigation: Use a pinned or isolated tiktoken install when exact counts are needed and treat estimates as audit guidance.

## Reference(s):

- [Compression Rules by File Type](references/compression-rules.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with plain-text tables and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON token-count output when the bundled script is run with --format json]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
