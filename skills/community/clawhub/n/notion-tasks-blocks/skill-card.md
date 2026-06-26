## Description: <br>
Manage Notion checklist blocks inside a page (no database required). Use when the user has plain to-do blocks and wants to list tasks, add tasks, and mark tasks done/undone. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luciorenovato](https://clawhub.ai/user/luciorenovato) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to manage simple Notion to-do blocks on a shared page without creating a Notion database. It supports listing tasks, appending new unchecked tasks, and marking listed tasks done or undone. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Notion integration token with broad workspace access could expose unrelated Notion content if used with this local shell script. <br>
Mitigation: Create a least-privilege Notion integration token and share only the intended tasks page with that integration before use. <br>
Risk: The skill modifies Notion page content by adding to-do blocks and changing their checked state. <br>
Mitigation: Run list first to confirm indexes, review the shell script before installation, and use it only on the intended page ID. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luciorenovato/notion-tasks-blocks) <br>
- [Notion API base endpoint](https://api.notion.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Configuration instructions, JSON, Guidance] <br>
**Output Format:** [Markdown instructions with shell commands; list output is JSON from the Notion API wrapper.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NOTION_TOKEN and NOTION_TASKS_PAGE_ID environment variables; operates on top-level Notion to-do blocks only.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
