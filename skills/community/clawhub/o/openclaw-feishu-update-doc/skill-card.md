## Description:

更新飞书云文档，支持追加、覆盖、定位替换、全文替换、前插入、后插入和删除 7 种更新模式。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenfa188](https://clawhub.ai/user/chenfa188)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to modify Feishu cloud documents by appending content, replacing selected text or sections, inserting before or after matched content, deleting selected ranges, overwriting full documents, and updating document titles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents can remove or replace content in shared Feishu documents when using delete_range, replace_all, or overwrite.

Mitigation: Review document IDs, selected ranges, and replacement Markdown before execution; prefer targeted modes such as append, insert_before, insert_after, or replace_range when they fit the task.

Risk: Full overwrite can clear the document and may lose images, comments, or other non-text content.

Mitigation: Use overwrite only when the document must be rebuilt, and avoid selecting regions containing images, whiteboards, spreadsheets, tables, tasks, comments, or other content that cannot be reconstructed from Markdown.

Risk: Ambiguous text or title selections can update the wrong section when repeated content appears in a document.

Mitigation: Use specific selection_with_ellipsis context or selection_by_title values and confirm insert_before or insert_after boundaries before running update modes.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown guidance with JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides document update requests that return JSON success, asynchronous task, warning, or error payloads.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
