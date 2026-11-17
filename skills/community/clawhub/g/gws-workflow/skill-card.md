## Description:

Google Workflow: Cross-service productivity workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Google Workspace users use this skill to inspect and run cross-service gws workflow commands for productivity tasks such as meeting preparation, standup summaries, email-to-task conversion, weekly digests, and Drive file announcements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Google Workspace authorization may grant the gws CLI access to account data and actions.

Mitigation: Review the Google authorization scopes granted to gws before use and install only when the user intends to operate the CLI with their Google Workspace account.

Risk: Workflow commands can send messages, create tasks, or change Drive, Gmail, Calendar, and Chat data.

Mitigation: Inspect each method with gws schema and confirm any mutating or message-sending action before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/googleworkspace-bot/skills/gws-workflow)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and CLI usage patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws CLI and schema inspection before API method calls.]

## Skill Version(s):

1.0.12 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
