## Description:

Fetches a user's personal Oura Ring sleep, readiness, activity, heart-rate, workout, SpO2, stress, body-temperature, and related biometric data through the official Oura API v2 using the local oura-cli Python tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zqchris](https://clawhub.ai/user/zqchris)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an assistant retrieve and interpret their own Oura Ring sleep, readiness, activity, heart-rate, workout, SpO2, stress, ring, and personal-profile data for specific dates or date ranges. It is suited for personal wellness analysis, recovery questions, and guided setup of the local Oura API companion CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run unpinned third-party oura-cli code.

Mitigation: Review or pin the oura-cli revision before use and re-review it before updating.

Risk: Oura OAuth authorization can expose broad biometric and profile data.

Mitigation: Grant only the OAuth scopes needed for the requested data and revoke authorization when the skill is no longer needed.

Risk: Outputs may include sensitive health data, including sleep, readiness, heart-rate, SpO2, stress, and personal-profile fields.

Mitigation: Keep outputs in the user-requested context, avoid sharing them with unrelated tools, and do not echo secrets or unnecessary personal fields.

Risk: Health metrics can be overinterpreted as medical advice.

Mitigation: Report observed data and trends, avoid diagnosis, and direct medical questions to a clinician.

## Reference(s):

- [Oura API v2 Reference](references/api-reference.md)
- [Example Outputs](references/example-outputs.md)
- [Official Oura API v2 Docs](https://cloud.ouraring.com/v2/docs)
- [oura-cli Companion Tool](https://github.com/zqchris/oura-cli)
- [ClawHub Skill Page](https://clawhub.ai/zqchris/skills/oura-data)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain text with inline shell commands and occasional JSON excerpts from Oura API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can contain sensitive personal health data and should be scoped to the user's requested date range.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
