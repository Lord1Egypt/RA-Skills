## Description:

A CLI skill to manage Microsoft To Do tasks via Microsoft Graph API, including listing, creating, completing, deleting, searching, viewing, and exporting tasks and lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoski](https://clawhub.ai/user/xiaoski)

### License/Terms of Use:

MIT

## Use Case:

External users, employees, and developers use this skill to manage Microsoft To Do lists and tasks from an agent-accessible command line. It supports authenticated task creation, completion, deletion, search, status views, statistics, and JSON export through Microsoft Graph.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Microsoft To Do login material is stored locally without explicit file protections.

Mitigation: Use the skill on a trusted single-user machine and protect or remove ~/.mstodo_token_cache.json and ~/.mstodo_device_flow.json when appropriate.

Risk: Debug output can expose request or response details during troubleshooting.

Mitigation: Avoid --debug unless necessary and treat any debug logs as sensitive.

Risk: The skill can delete tasks and lists through Microsoft To Do.

Mitigation: Review delete actions carefully and use confirmation prompts unless deletion intent is explicit.

Risk: Task exports may contain sensitive personal or work information.

Mitigation: Store exported JSON securely and remove exports when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaoski/skills/ms-todo-sync)
- [Microsoft device login](https://microsoft.com/devicelogin)
- [Microsoft Graph API endpoint](https://graph.microsoft.com/v1.0)
- [uv documentation](https://docs.astral.sh/uv/)
- [Python](https://python.org)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON]

**Output Format:** [Command-line text and optional JSON export, usually presented to the user as concise Markdown with inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Microsoft To Do authentication and network access to Microsoft Graph; destructive delete operations should be confirmed unless user intent is explicit.]

## Skill Version(s):

1.0.2 (source: server release metadata, SKILL.md frontmatter, and pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
