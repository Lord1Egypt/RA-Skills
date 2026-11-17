## Description:

Coordinate shared Todo tasks and consolidated reminders across Hermes, OpenClaw, ChatGPT/Codex, WorkBuddy, and other agents through Git.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ernest-su](https://clawhub.ai/user/ernest-su)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to coordinate task ownership, lifecycle updates, and consolidated due-task reminders across multiple independent AI agents through a shared Git repository.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task titles, descriptions, due dates, results, and notification receipts are committed and pushed to the configured Git repository.

Mitigation: Use a dedicated private repository or local bare repository, and keep secrets, credentials, private transcripts, and sensitive personal data out of task records.

Risk: Agents with this skill can run Git commands and publish shared todo metadata.

Mitigation: Install it only for agents that should coordinate these todos, and configure Git credentials and repository access with the least privilege needed.

Risk: Implicit invocation or broad reminder scheduling can create unexpected shared-task updates or duplicate reminders.

Mitigation: Enable implicit use and reminder polling only intentionally, designate one notifier, and keep failover notifiers disabled until needed.

## Reference(s):

- [Runtime compatibility](references/compatibility.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON CLI output expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled CLI emits JSON objects for setup, sync, task lifecycle, due-task, and receipt operations.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
