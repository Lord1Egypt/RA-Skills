## Description:

当用户发送 PDF 文件并要求存入 GetNotes 时触发，执行 PDF 转图片、AI 摘要生成，并创建包含摘要和全页图片的单一 GetNotes 笔记。

This skill is ready for commercial/non-commercial use.

## Publisher:

[pieces201020](https://clawhub.ai/user/pieces201020)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to turn a supplied PDF into a single GetNotes note with a Markdown summary and each PDF page embedded as an image. It is useful when preserving all PDF pages in one note matters more than uploading the original PDF as an attachment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes live-looking GetNotes credentials in reference material.

Mitigation: Revoke the exposed credentials, remove them from the package, and require users to provide credentials only through local configuration before installation.

Risk: Processed PDFs may be uploaded to GetNotes/OSS and may be sent to an AI model for summarization.

Mitigation: Use the skill only with documents approved for those services, and add explicit consent or disclosure before remote upload and model processing.

Risk: The current implementation stores converted page images and URL metadata under temporary paths.

Mitigation: Use secure temporary files, restrict permissions, and clean up generated images and URL records after note creation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pieces201020/skills/pdf-to-getnote)
- [Full SOP](artifact/references/full_sop.md)
- [GetNotes API Behavior](artifact/references/api_behavior.md)
- [GetNotes Open API](https://openapi.biji.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown note content, shell command examples, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces one GetNotes plain_text note; PDF pages are embedded as Markdown image links after upload.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
