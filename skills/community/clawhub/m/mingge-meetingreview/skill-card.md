## Description:

内训课内容加工工作流，从飞书文档读取课程素材并生成蒸馏版、总结版、复盘版和 3 点改进稿四类派生文档。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cheney77zhao-cmd](https://clawhub.ai/user/cheney77zhao-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Training operators, course reviewers, and content teams use this skill to process Feishu course materials containing participant lists, comments, and transcripts into four review and improvement documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads Feishu course materials that may include participant names, comments, or private training transcripts.

Mitigation: Use it only on documents the operator is authorized to access, process, and share.

Risk: The skill creates four derived child documents from the source material.

Mitigation: Confirm the destination workspace and sharing permissions before publishing or distributing generated documents.

## Reference(s):

- [六个办公室主任框架详解](references/six-brains.md)
- [ClawHub skill page](https://clawhub.ai/cheney77zhao-cmd/skills/mingge-meetingreview)

## Skill Output:

**Output Type(s):** [Markdown, Files, Guidance]

**Output Format:** [Markdown documents written to Feishu child documents, plus a concise completion summary with document links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces four derived documents: distilled notes, core summary, course review, and three targeted transcript improvements.]

## Skill Version(s):

3.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
