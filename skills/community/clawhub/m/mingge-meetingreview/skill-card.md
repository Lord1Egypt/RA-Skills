## Description: <br>
内训课内容加工工作流，从飞书文档读取课程素材并生成蒸馏版、总结版、复盘版和 3 点改进稿四类文档。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cheney77zhao-cmd](https://clawhub.ai/user/cheney77zhao-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, course operators, and content teams use this skill to process Feishu course materials that contain participant lists, timestamped comments, and transcripts. It generates four derived Feishu documents for distilled notes, summary, professional review, and targeted transcript improvements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes persistent content into the user's Feishu workspace. <br>
Mitigation: Confirm source and destination sharing permissions before running, and review the created child documents after generation. <br>
Risk: Course source documents may contain confidential, personal, or otherwise sensitive material. <br>
Mitigation: Use the skill only on documents the user is authorized to process, and avoid confidential or personal data unless that processing is approved. <br>
Risk: The review and improvement outputs can include persuasion-oriented recommendations. <br>
Mitigation: Review generated recommendations before sharing or using them in training, sales, or communication workflows. <br>


## Reference(s): <br>
- [六个办公室主任框架详解](references/six-brains.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/cheney77zhao-cmd/mingge-meetingreview) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, API Calls, Files, Guidance] <br>
**Output Format:** [Markdown documents written to Feishu child documents, plus a concise completion summary with document links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates four persistent Feishu child documents when the required Feishu access and source document structure are available.] <br>

## Skill Version(s): <br>
3.4.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
