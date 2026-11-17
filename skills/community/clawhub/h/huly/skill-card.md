## Description:

Drive self-hosted Huly workspaces through the huly CLI for project tracking, scheduling, documents, chat, notifications, approvals, and other workspace automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iamcoder18](https://clawhub.ai/user/iamcoder18)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace operators use this skill to let an agent inspect and automate a self-hosted Huly workspace through CLI commands, including issue tracking, project setup, documents, cards, chat, calendars, time logs, notifications, and approvals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and relies on an unpinned third-party CLI package.

Mitigation: Install only after reviewing and trusting the @iamcoder18/huly-cli package source; prefer a pinned, reviewed CLI version.

Risk: The skill can manage persistent Huly credentials and workspace access.

Mitigation: Use a least-privileged service account and prefer a short-lived HULY_TOKEN over stored passwords.

Risk: The skill can trigger powerful workspace changes, including deletes, DM sends, approvals, raw API calls, and credential resets.

Mitigation: Review and explicitly confirm sensitive actions before allowing the agent to run them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iamcoder18/skills/huly)
- [huly CLI issue tracker](https://github.com/IamCoder18/huly-cli)
- [Auth and setup](references/auth-and-setup.md)
- [Issues and actions](references/issues-and-todos.md)
- [Tracker projects](references/tracker-projects.md)
- [Cards](references/cards.md)
- [Documents](references/documents.md)
- [Chat and collaboration](references/chat-and-collaboration.md)
- [Calendar and schedule](references/calendar-and-schedule.md)
- [Direct SDK access](references/direct-sdk-access.md)
- [Notifications and approvals](references/notifications-and-approvals.md)
- [Spaces, types, and relations](references/spaces-types-and-relations.md)
- [Workspace and user](references/workspace-and-user.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Encourages --json or --ci for programmatic reads, dry-run where available, and explicit confirmation before persistent workspace writes.]

## Skill Version(s):

1.0.6 (source: server release evidence, created 2026-08-27)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
