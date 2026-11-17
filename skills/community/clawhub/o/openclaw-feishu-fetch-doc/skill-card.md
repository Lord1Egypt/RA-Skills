## Description:

获取飞书云文档内容。返回文档的 Markdown 内容，支持处理文档中的图片、文件和画板（需配合 feishu_doc_media 工具）。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenfa188](https://clawhub.ai/user/chenfa188)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to fetch Feishu/Lark cloud document content as Markdown and identify referenced images, files, and whiteboards that require separate media download handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private Feishu/Lark document links and downloaded media can contain sensitive content.

Mitigation: Install only when the agent should access configured Feishu/Lark documents, treat document links and media as sensitive, and confirm attachment save locations before downloading.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenfa188/skills/openclaw-feishu-fetch-doc)

## Skill Output:

**Output Type(s):** [markdown, guidance]

**Output Format:** [Markdown with Feishu/Lark media token references and tool-use guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Media items such as images, files, and whiteboards are represented as tokens and require a separate download tool.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
