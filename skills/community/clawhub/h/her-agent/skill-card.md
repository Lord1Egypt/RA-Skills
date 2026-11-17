## Description:

Self-evolving AI Agent with thinking chain, knowledge graph, emotion system, and Claude Code-inspired execution flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wenqin1688](https://clawhub.ai/user/wenqin1688)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators can use Her Agent to add a stateful assistant workflow with thinking-chain prompts, knowledge-graph memory, reflection, learning notes, and helper scripts for command execution and sub-agent setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes command execution behavior and can be configured for broad local command access.

Mitigation: Install only in a sandboxed workspace with no inherited credentials or sensitive files, and do not enable full permission mode unless arbitrary local command execution is intended.

Risk: Persistent memory and configuration files can affect future behavior.

Mitigation: Review and reset memory/configuration state before deployment and after any untrusted use.

Risk: Self-evolution and skill-installation behavior can change the agent's operating posture over time.

Mitigation: Require human review before running evolution workflows or accepting newly installed skills.

## Reference(s):

- [ClawHub Her Agent skill page](https://clawhub.ai/wenqin1688/skills/her-agent)
- [ClawHub publisher profile for wenqin1688](https://clawhub.ai/user/wenqin1688)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-stream agent guidance; bundled configuration sets an 8-turn limit and a 2000-token budget.]

## Skill Version(s):

3.0.0 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
