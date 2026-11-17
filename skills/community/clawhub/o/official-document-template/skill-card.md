## Description:

公文排版工具。将Markdown格式内容转换为符合GB/T 9704-2012标准的Word文档。当用户需要制作通知、请示、报告、批复、意见等公文时触发。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hunkguo](https://clawhub.ai/user/hunkguo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and document authors use this skill to draft and format Chinese official documents from Markdown or plain text into Word documents aligned with GB/T 9704-2012 conventions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Python dependency is installed without a pinned version in the skill guidance.

Mitigation: Use a virtual environment and pin `python-docx` before installation or deployment.

Risk: Generated DOCX layout can vary when required Chinese fonts are unavailable or office software renders styles differently.

Mitigation: Review generated documents in Word or WPS and install required fonts before relying on final formatting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hunkguo/skills/official-document-template)
- [公文排版规范](artifact/公文排版规范.md)
- [模板使用指南](artifact/模板使用指南.md)
- [通知模板](artifact/通知模板.md)
- [请示模板](artifact/请示模板.md)
- [报告模板](artifact/报告模板.md)
- [批复模板](artifact/批复模板.md)
- [意见模板](artifact/意见模板.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance and generated DOCX files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated documents may require final review in Word or WPS for fonts and layout.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
