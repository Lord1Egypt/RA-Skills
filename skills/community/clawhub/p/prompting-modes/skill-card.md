## Description:

高级推理模式工具箱，实现 Chain-of-Thought、Self-Consistency、Tree-of-Thought、ReAct 和 Plan-and-Execute 五种提示词工程模式，用于按任务需要选择特定推理策略。

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this Chinese-language skill to guide an agent in selecting and applying structured reasoning modes for explanation, verification, multi-path exploration, tool-assisted work, and multi-step planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can route ordinary requests into tool, file, database, browser, or code-execution workflows without explicit confirmation rules.

Mitigation: Require user confirmation before code execution, database access, file-system reads, browser actions, or any state-changing operation, especially in ReAct and Plan-and-Execute modes.

Risk: Self-Consistency is implemented as simulated multiple reasoning paths in one agent response rather than independent model calls.

Mitigation: Use it as a lightweight verification aid, and require independent checks for high-impact factual, legal, medical, financial, or security decisions.

## Reference(s):

- [Prompting Modes Skill Page](https://clawhub.ai/paudyyin/skills/prompting-modes)
- [Implementation Guide](references/implementation-guide.md)
- [Modes Reference](references/modes-reference.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown or plain text with structured reasoning sections and optional tool/action records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [ReAct guidance limits action loops to five rounds; Self-Consistency is represented as multiple reasoning paths in one response.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
