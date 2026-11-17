## Description:

Manage Microsoft To Do lists and tasks through a local Python CLI backed by Microsoft Graph OAuth, including inspecting, adding, completing, deleting, searching, exporting, and summarizing tasks with priorities, due dates, reminders, recurrence, and list selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nathanatgit](https://clawhub.ai/user/nathanatgit)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to manage Microsoft To Do tasks and lists from a local Python CLI after Microsoft Graph OAuth setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release ships a reusable OAuth client secret.

Mitigation: Use a caller-controlled Azure app registration and provide fresh credentials through environment variables or global options before use.

Risk: The local token cache can contain sensitive Microsoft account tokens.

Mitigation: Restrict or remove the token cache when the session is complete, and run logout or reauthentication when switching accounts.

Risk: Client secrets passed on the command line can be exposed through shell history or process listings.

Mitigation: Prefer environment variables or a secure local secret workflow instead of placing secrets directly in commands.

Risk: Exported task JSON can contain private task names, notes, dates, and list metadata.

Mitigation: Treat exported files as private data and store, share, or delete them according to the user's data handling requirements.

Risk: Delete-list and delete-task actions can remove Microsoft To Do data.

Mitigation: Confirm the exact list or task with the user before allowing an agent to run destructive commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nathanatgit/skills/ms-todo-oauth)
- [Publisher profile](https://clawhub.ai/user/nathanatgit)
- [Microsoft Graph API endpoint](https://graph.microsoft.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance, CLI text, and optional JSON export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local Python dependencies, Microsoft Graph network access, and interactive OAuth on first use.]

## Skill Version(s):

1.0.5 (source: evidence release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
