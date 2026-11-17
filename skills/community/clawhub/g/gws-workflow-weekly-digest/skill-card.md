## Description:

Google Workflow: Weekly summary: this week's meetings + unread email count.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and agents working with Google Workspace use this skill to run a read-only weekly digest that combines this week's calendar agenda with Gmail triage and unread email count information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on the separate gws CLI, Google account authorization scopes, and shared-skill behavior outside this artifact.

Mitigation: Install only when the gws CLI and requested Google account scopes are trusted, and review the shared Google Workspace auth behavior before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/gws-workflow-weekly-digest)

## Skill Output:

**Output Type(s):** [shell commands, guidance, text]

**Output Format:** [Markdown guidance with bash commands; command output can be json, table, yaml, or csv.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws CLI and Google Workspace authorization; the documented command is read-only.]

## Skill Version(s):

1.0.12 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
