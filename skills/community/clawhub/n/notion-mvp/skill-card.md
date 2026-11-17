## Description:

Create and list Notion tasks in a single database via Notion API. Use when the user asks to add tasks, list today tasks, or capture quick todos in Notion from chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luciorenovato](https://clawhub.ai/user/luciorenovato)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to capture, list, and search task records in configured Notion databases from an agent chat workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read from and write to multiple configured Notion databases, including sensitive databases if the user maps them.

Mitigation: Use a least-privilege Notion integration and map only the specific task databases intended for this workflow.

Risk: Notion tokens, database identifiers, and task details may be exposed through local process arguments or environment inspection on shared systems.

Mitigation: Run the skill only in trusted local environments and avoid passing sensitive task details where other local users or tooling can inspect process state.

Risk: Adding, querying, and listing tasks contacts Notion and sends task data to the Notion API.

Mitigation: Confirm that task content is appropriate for Notion before using add, today, query, or next commands.

## Reference(s):

- [Notion API](https://api.notion.com/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Notion API responses for task creation, daily task listing, text search, upcoming task lookup, and alias listing.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
