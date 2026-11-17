## Description:

Atomic node skill to exclusively update the summary (title) of a Google Calendar event.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zvirb](https://clawhub.ai/user/zvirb)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and users who manage Google Calendar events use this skill to rename an existing event by updating only its summary/title through the gog CLI. The skill is intentionally limited to the event summary field and expects the returned JSON to confirm the change.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The command template can create a command-injection risk if calendar IDs, event IDs, or titles are interpolated into a shell command unsafely.

Mitigation: Pass event titles, event IDs, and calendar IDs as literal CLI arguments through a shell-free execution path, or validate and escape them carefully before execution.

Risk: The skill depends on the local gog CLI setup and the agent executing it.

Mitigation: Install only in environments where the gog CLI configuration and executing agent are trusted, and review the returned JSON before treating the update as successful.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zvirb/skills/google-calendar-update-summary)

## Skill Output:

**Output Type(s):** [shell commands, JSON, guidance]

**Output Format:** [Shell command invocation plus JSON response validation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gog CLI and limits updates to the Google Calendar event summary field.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
