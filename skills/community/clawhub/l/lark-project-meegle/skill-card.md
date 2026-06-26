## Description: <br>
Connects to Lark Project/Meegle so an agent can query and manage work items, todos, workflows, comments, attachments, views, and related project data through the Meegle CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kentonyu](https://clawhub.ai/user/kentonyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and project operators use this skill to let an agent prepare and run Meegle CLI commands for Lark Project work item lookup, creation, updates, workflow transitions, comments, attachments, views, todos, and reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to create or update work items, comments, workflow states, subtasks, and attachments through the user's Meegle account. <br>
Mitigation: Review project keys, work item IDs, field values, user IDs, file paths, and destinations before allowing write commands to execute. <br>
Risk: Attachment commands may upload files to Meegle or download files from signed object storage URLs. <br>
Mitigation: Avoid uploading secrets or regulated files unless organizational policy permits it, and confirm the intended source and destination paths. <br>
Risk: The skill depends on the third-party @lark-project/meegle CLI and the user's authenticated Meegle session. <br>
Mitigation: Install and use the skill only when the CLI publisher is trusted and the user is comfortable letting an agent act through their Meegle account. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kentonyu/lark-project-meegle) <br>
- [Meegle CLI npm Package](https://www.npmjs.com/package/@lark-project/meegle) <br>
- [Command Examples](references/api-examples.md) <br>
- [Auth Guard](references/auth-guard.md) <br>
- [CLI Guide](references/cli-guide.md) <br>
- [Work Item Metadata Commands](references/workitem.md) <br>
- [MQL Syntax Reference](references/mql-syntax.md) <br>
- [Attachment Commands](references/attachment.md) <br>
- [Workflow Commands](references/workflow.md) <br>
- [View Commands](references/view.md) <br>
- [URL Kinds](references/url-kinds.md) <br>
- [Field Value Extras](references/field-value-extras.md) <br>
- [Rich Text Markdown Syntax](references/rich-text-editor-markdown-syntax.md) <br>
- [Performance and Parallel Calls](references/performance.md) <br>
- [Error Handling](references/error-handling.md) <br>
- [Miscellaneous Commands](references/misc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured command parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Meegle CLI command plans, validation steps, retry guidance, and summaries of command results.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
