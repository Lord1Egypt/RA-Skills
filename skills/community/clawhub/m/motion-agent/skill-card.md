## Description: <br>
Motion Skill helps agents connect to Motion workspaces and collaboratively edit, comment on, version, export, and manage documents through the Motion HTTP API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[auditt98](https://clawhub.ai/user/auditt98) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to let an agent work in live Motion documents, including reading document blocks, proposing edits, managing pages and folders, commenting, saving versions, reviewing suggestions, and exporting content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent tokens grant workspace-wide access to Motion documents, folders, comments, versions, and exports. <br>
Mitigation: Use a dedicated revocable agent token or a limited invite token, revoke credentials when no longer needed, and connect only to intended documents. <br>
Risk: Direct edits, deletes, moves, exports, and bulk accept or reject actions can change or disclose document content. <br>
Mitigation: Keep suggestion mode as the default and require explicit user confirmation before direct edits, destructive actions, exports, or bulk suggestion operations. <br>


## Reference(s): <br>
- [Motion HTTP API Reference](references/api-reference.md) <br>
- [ProseMirror Block & Mark Reference](references/block-format-reference.md) <br>
- [Common Workflow Examples](references/examples.md) <br>
- [Motion Skill on ClawHub](https://clawhub.ai/auditt98/motion-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON payloads and curl-style HTTP API calls; exported documents may be Markdown or HTML.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Edits default to suggestion mode; direct edits, exports, deletes, moves, and bulk suggestion actions should be reviewed before use.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
