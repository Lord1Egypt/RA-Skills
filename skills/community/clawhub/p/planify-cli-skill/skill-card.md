## Description:

Manage tasks and projects via Planify CLI commands to add, list, update, and export tasks with JSON-formatted results for scripting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elzorrorebelde](https://clawhub.ai/user/elzorrorebelde)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Planify users use this skill to ask an agent for Planify CLI commands that create, list, update, and back up tasks and projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent-run Planify CLI commands can change the user's task database when the user asks for add or update actions.

Mitigation: Review proposed commands before execution and use task IDs from prior add, list, or cache results instead of guessed IDs.

Risk: Planify backups export all Planify data as JSON.

Mitigation: Request backups only when an export is intended, choose a controlled output path, and treat the resulting JSON as user data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/elzorrorebelde/skills/planify-cli-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/elzorrorebelde)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash commands and JSON-oriented CLI guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands are intended for Planify CLI and commonly produce JSON output suitable for jq.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
