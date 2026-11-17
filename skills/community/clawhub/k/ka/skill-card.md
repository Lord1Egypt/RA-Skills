## Description:

Feishu document read/write operations for agents working with Feishu docs, cloud docs, or docx links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kari-code](https://clawhub.ai/user/kari-code)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to read, create, append, replace, and edit Feishu Docx documents, including block-level text changes, table operations, and image or file uploads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents can replace an entire Feishu document or delete blocks, which may remove or overwrite user content.

Mitigation: Require explicit user confirmation before replace-all, delete, or delete-and-rewrite operations.

Risk: The skill can upload local files to Feishu documents.

Mitigation: Allow local file uploads only from task-specific paths explicitly provided by the user.

Risk: Broad document write capabilities may affect documents beyond the user's intent if doc tokens or block IDs are wrong.

Mitigation: Confirm the target document token and relevant block or table IDs before making write, update, or upload calls.

## Reference(s):

- [Feishu Block Types Reference](artifact/references/block-types.md)
- [ClawHub skill page](https://clawhub.ai/kari-code/skills/ka)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration, API calls]

**Output Format:** [Markdown guidance with JSON action examples and YAML configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May result in Feishu document content changes, table updates, block deletions, and image or file uploads through the feishu_doc tool.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
