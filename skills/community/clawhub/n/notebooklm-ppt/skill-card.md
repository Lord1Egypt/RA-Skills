## Description:

使用 NotebookLM CLI 生成 PPT 演示文稿。从预置风格模板库中选择模板，通过 notebook query 设置风格要求，再生成幻灯片。适用于需要快速将文档转换为演示文稿的场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yenava](https://clawhub.ai/user/yenava)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to turn source documents into Chinese-language PowerPoint presentations with a selected visual style template. It guides setup, NotebookLM notebook creation, source ingestion, slide generation, download, and file handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: NotebookLM CLI setup and authentication may fail or use an unexpected account.

Mitigation: Run nlm doctor before creating notebooks or adding source documents.

Risk: Source documents may contain confidential content that is processed through NotebookLM.

Mitigation: Only add documents that are approved for NotebookLM processing in the user's environment.

Risk: Repeated slide generation can create duplicate or unintended presentation versions.

Mitigation: Run slides create once per intended deck and record the returned artifact ID before downloading.

Risk: The default workflow requests Chinese output and may not match every user's language needs.

Mitigation: Adjust the language flags and prompt text before generation when a different output language is required.

## Reference(s):

- [NotebookLM style prompt templates](references/templates.md)
- [ClawHub skill page](https://clawhub.ai/yenava/skills/notebooklm-ppt)
- [Publisher profile](https://clawhub.ai/user/yenava)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline shell commands and generated PPTX file handoff]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses NotebookLM CLI, requires an authenticated NotebookLM setup, and normally produces a PPTX slide deck.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
