## Description:

Countly (countly.com). Use this skill for ANY Countly request — searching and reading data. Whenever a task involves Countly, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users with a connected Countly account use the skill to retrieve application and user details and read dashboard, event, and session analytics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute an installer that has not been verified.

Mitigation: Review the CLI installer and prefer a separately reviewed version before installing.

Risk: Setup can introduce persistent changes to agent skills without clear user control.

Mitigation: Review and approve local changes, and disable automatic skill synchronization if it is not wanted.

Risk: Connecting Countly exposes data from the connected account and applications to skill actions.

Mitigation: Connect only the Countly account and applications needed.

## Reference(s):

- [oo CLI project page](https://github.com/oomol-lab/oo-cli)
- [Countly homepage](https://countly.com/)
- [Countly REST API reference](https://api.count.ly/reference/rest-api-reference)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Countly data returned as JSON, with natural-language summaries as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only application, user, dashboard, event, and session data.]

## Skill Version(s):

1.0.4 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
