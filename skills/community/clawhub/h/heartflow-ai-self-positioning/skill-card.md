## Description:

HeartFlow is a cognitive engine for AI agents that supports self-reflection, dream-based experience synthesis, emergent personality, memory, AI psychology, and AI self-positioning analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yun520-1](https://clawhub.ai/user/yun520-1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add cognitive reflection, memory retrieval, self-healing strategy selection, dream synthesis, and AI psychology or self-positioning analysis to an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Powerful code execution may run unsafe or unintended commands.

Mitigation: Run the skill in an isolated environment and disable, gate, or review code execution paths before use.

Risk: Persistent memory injection can introduce stale, private, or untrusted stored content into prompts.

Mitigation: Review and delete stored memory before allowing it into prompts, and keep runtime memory scoped to the intended workspace.

Risk: Unauthenticated local MCP or memory access may expose agent state to unintended local clients.

Mitigation: Avoid the unauthenticated HTTP MCP server unless local access is explicitly controlled and the environment is isolated.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yun520-1/skills/heartflow-ai-self-positioning)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)
- [Agent integration guide](artifact/AGENTS.md)
- [Release changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JavaScript examples, shell commands, and structured tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May expose CLI, daemon, MCP, and memory-tool interactions depending on how the skill is installed and invoked.]

## Skill Version(s):

2.14.0 (source: ClawHub release evidence, SKILL.md frontmatter, package.json, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
