## Description:

意图分类器实时分析用户输入，识别代码、知识、任务和闲聊等意图，并给出对应的处理流程或技能路由建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to classify user requests and choose an appropriate downstream workflow or skill for code, knowledge, task, or chat intents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad intent examples may classify polite requests or common phrases as actionable task intent.

Mitigation: Use classifications as advisory routing signals and require explicit user confirmation before invoking downstream skills that can edit files, run commands, search private data, or store memories.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown intent-classification summary with confidence, triggering features, alternatives, and a routing recommendation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory routing output only; it does not execute downstream actions.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
