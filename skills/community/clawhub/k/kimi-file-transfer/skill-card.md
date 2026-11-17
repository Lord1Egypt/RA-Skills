## Description:

将本地最多5个文件上传到当前 Kimi 对话中，便于用户在对话内下载和共享文档、图片、PDF 或代码文件。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chongjie-ran](https://clawhub.ai/user/chongjie-ran)

### License/Terms of Use:


## Use Case:

Kimi users and agents use this skill to transfer up to five locally accessible files into the active Kimi conversation for document sharing, asset handoff, or code sharing. Users should review selected paths because uploaded files leave the local machine.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-requested local files leave the local machine when uploaded into a Kimi conversation.

Mitigation: Review each requested path before use, avoid secrets or private documents unless they are intended to be shared, and ask the agent to confirm the exact files before upload.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chongjie-ran/skills/kimi-file-transfer)

## Skill Output:

**Output Type(s):** [files, guidance]

**Output Format:** [Kimi chat file attachments with concise text or Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports up to 5 local file paths per upload request.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
