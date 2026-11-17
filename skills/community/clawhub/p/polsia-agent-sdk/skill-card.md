## Description:

Build autonomous AI features using the Polsia Agent API only; never call model providers directly for product AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentlevier](https://clawhub.ai/user/agentlevier)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to build autonomous AI features through the Polsia Agent API, including agent workflows that may use connected services such as Gmail, GitHub, Slack, Google Calendar, and Google Sheets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connected services such as email, Slack, GitHub, Calendar, and Sheets may expose more data or permissions than the project needs.

Mitigation: Grant only the specific service permissions needed for the application and review connected-service scopes before deployment.

Risk: Generated app code may send email or store agent data through mounted tools.

Mitigation: Review code paths that call email-sending or data-storage tools and confirm they match the intended user workflow.

Risk: The skill relies on a Polsia API key for AI feature implementation.

Mitigation: Store POLSIA_API_KEY in the application's secret-management system and avoid embedding it in source files or client-side code.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/agentlevier/skills/polsia-agent-sdk)

## Skill Output:

**Output Type(s):** [guidance, code, configuration]

**Output Format:** [Markdown guidance with API, environment variable, and tool usage details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [References POLSIA_API_URL and POLSIA_API_KEY for Polsia API usage.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
