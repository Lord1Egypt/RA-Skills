## Description:

Run GA4 reports, inspect properties, list audiences and data streams, and analyze traffic and conversion data via the Google Analytics Data API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and analytics teams use this skill to connect an agent to Google Analytics through ClawLink, discover GA4 accounts and properties, run standard or realtime reports, inspect metadata, and review traffic, campaign, audience, data stream, and conversion information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables a third-party ClawLink plugin with hosted OAuth credentials and access to Google Analytics properties available to the connected Google account.

Mitigation: Install only after reviewing the requested Google OAuth scopes and GA4 property permissions, and revoke the ClawLink Google connection when it is no longer needed.

Risk: Some available analytics tools can create or update Google Analytics resources.

Mitigation: Preview write-capable actions and approve them only when the proposed operation exactly matches the user's intent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hith3sh/skills/google-analytics-reporting)
- [Google Analytics Data API documentation](https://developers.google.com/analytics/devguides/reporting/data/v1)
- [GA4 dimensions and metrics](https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema)
- [GA4 Realtime API](https://developers.google.com/analytics/devguides/reporting/realtime/v1)
- [ClawLink documentation](https://docs.claw-link.dev/openclaw)
- [ClawLink verification](https://claw-link.dev/verify)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON tool parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes guidance for choosing and confirming Google Analytics tool calls; write-capable actions require explicit user confirmation.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
