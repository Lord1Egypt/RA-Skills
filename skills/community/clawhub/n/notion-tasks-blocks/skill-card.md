## Description:

Manage Notion checklist blocks inside a page (no database required). Use when the user has plain to-do blocks and wants to list tasks, add tasks, and mark tasks done/undone.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luciorenovato](https://clawhub.ai/user/luciorenovato)

### License/Terms of Use:


## Use Case:

Developers and end users use this skill to manage checklist-style Notion page tasks without creating a Notion database. It supports listing top-level to-do blocks, adding new unchecked tasks, and marking listed tasks done or undone.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Notion integration token that can access the configured task page.

Mitigation: Use a dedicated Notion token shared only with that page and rotate it if exposed.

Risk: Local users on a shared system may be able to inspect process command lines or environment details.

Mitigation: Avoid running the skill on shared systems where other local users can inspect command execution details.

Risk: The skill only manages top-level to-do blocks on the configured Notion page.

Mitigation: Run list before changing task state and use the displayed indexes for done and undo operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luciorenovato/skills/notion-tasks-blocks)
- [Notion API endpoint used by the skill](https://api.notion.com/v1)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON responses from the wrapper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires NOTION_TOKEN and NOTION_TASKS_PAGE_ID environment variables and operates on top-level Notion to-do blocks on the configured page.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
