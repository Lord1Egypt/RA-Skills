## Description:

Plausible Analytics Agent helps agents track Plausible pageviews and custom events and query analytics data from self-hosted or plausible.io sites.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kryzl19](https://clawhub.ai/user/kryzl19)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site operators use this skill to send Plausible pageview or custom-event data and retrieve analytics summaries, top pages, and realtime visitors for hosted or self-hosted Plausible sites.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Analytics data and API credentials can be sent to any configured Plausible base URL.

Mitigation: Keep PLAUSIBLE_BASE_URL and any --base-url value restricted to a trusted HTTPS Plausible instance.

Risk: API keys or personal data may be exposed through command-line arguments, tracked URLs, referrers, or custom event properties.

Mitigation: Prefer PLAUSIBLE_API_KEY from a protected environment variable and avoid including secrets or personal data in analytics payload fields.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kryzl19/skills/plausible-analytics-agent)
- [Plausible Analytics](https://plausible.io)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands; scripts return JSON or plain text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PLAUSIBLE_SITE_DOMAIN and PLAUSIBLE_API_KEY; PLAUSIBLE_BASE_URL is optional for self-hosted instances.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
