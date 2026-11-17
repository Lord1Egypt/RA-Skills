## Description:

创建飞书云文档，将 Lark-flavored Markdown 内容写入新文档，并支持指定文件夹、知识库节点或知识空间。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenfa188](https://clawhub.ai/user/chenfa188)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace users use this skill to create Feishu cloud documents from structured Lark-flavored Markdown, optionally placing the new document in a folder, wiki node, or wiki space.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create documents in a user's Feishu account and upload media fetched from referenced URLs.

Mitigation: Confirm the document title, destination, and content before use, and avoid sensitive, private, authenticated, temporary, or untrusted media URLs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenfa188/skills/openclaw-feishu-create-doc)
- [Publisher profile](https://clawhub.ai/user/chenfa188)

## Skill Output:

**Output Type(s):** [API Calls, Markdown, Guidance]

**Output Format:** [JSON result with document identifiers and a Feishu document URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a Feishu document from supplied Markdown and may fetch referenced media URLs for upload.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
