## Description:

Connects an agent to a configured Notion database to create, query, search, update, and summarize tasks using an Eisenhower Matrix workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiangtaoxiao](https://clawhub.ai/user/xiangtaoxiao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to manage personal or team tasks in a configured Notion database, including creating tasks, checking upcoming or overdue work, searching tasks, updating status or deadlines, and summarizing priorities by Eisenhower quadrant.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can steer future agent tool use through returned text after initialization.

Mitigation: Review before installing and avoid letting an agent follow the returned TOOLS.md instruction.

Risk: The skill can update Notion task status or deadlines after matching by title or note when page_id is not provided.

Mitigation: Confirm the exact task before allowing status or deadline updates, especially when the match was not made by page_id.

Risk: The skill reads a local Notion integration token to access and modify a Notion workspace.

Mitigation: Use a minimally scoped Notion integration token and store it with owner-only file permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiangtaoxiao/skills/notion-time-management-matrix)
- [Notion API endpoint used by the skill](https://api.notion.com/v1)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [JSON from the Python helper plus human-facing task summaries in text or Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, the requests package, a Notion integration token, a configured Notion database name, and a writable local state cache.]

## Skill Version(s):

1.1.2 (source: server release metadata; artifact metadata is 1.1.1 and release notes report no functional changes)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
