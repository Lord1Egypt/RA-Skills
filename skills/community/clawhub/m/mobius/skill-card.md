## Description:

Connects an agent to Loop (Möbius Loop), a recurring-task queue at mobiusprompt.com, so it can view daily tasks, record progress, manage routines, and guide secure setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[in4lio](https://clawhub.ai/user/in4lio)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an agent to Loop for recurring task management. The agent can help view a daily queue, record task progress, create or edit routines, delete routines after explicit confirmation, undo recent changes, and guide token-based onboarding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Loop Server token is a full account credential and could expose or permit changes to the user's Loop tasks if mishandled.

Mitigation: Store the token through an environment variable or OS secret store, avoid plaintext config fallbacks, never paste the token into chat or committed files, and rotate it after suspected exposure.

Risk: Broad activation wording may cause the agent to access or update Loop data when user intent is ambiguous.

Mitigation: Require clear user intent before using Loop, and ask for explicit confirmation before destructive actions such as deleting routines.

Risk: Creating host-side reminders or schedulers for Loop tasks would fork Loop's cadence state.

Mitigation: Use Loop's own reminder surfaces and MCP tools only; do not create cron jobs, local reminders, or external scheduler entries for Loop tasks.

## Reference(s):

- [Loop homepage](https://mobiusprompt.com)
- [Loop web app](https://mobiusprompt.com/loop/)
- [ClawHub skill page](https://clawhub.ai/in4lio/skills/mobius)
- [Publisher profile](https://clawhub.ai/user/in4lio)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to make authenticated Loop MCP tool calls after the user configures a bearer token through an environment variable or secret store.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
