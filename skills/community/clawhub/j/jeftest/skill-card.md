## Description:

Connects agents to 100+ third-party APIs through Maton managed OAuth so they can make authenticated native API calls to services such as Google Workspace, Microsoft 365, GitHub, Notion, Slack, Airtable, and HubSpot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hjcloud](https://clawhub.ai/user/hjcloud)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to call external SaaS APIs through a unified Maton gateway after the user has authorized each service connection. It is suited for workflows that need API requests, connection management, troubleshooting, and service-specific endpoint guidance across many providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A single MATON_API_KEY can enable the agent to operate a broad API gateway.

Mitigation: Treat MATON_API_KEY as a high-value secret, keep it out of logs and shared transcripts, and install the skill only where broad gateway access is intended.

Risk: Authorized service connections may permit high-impact external actions such as deletes, public posts, payment or customer changes, admin changes, webhooks, or bulk updates.

Mitigation: Require explicit user confirmation before high-impact actions and review the request target, method, payload, and expected effect before execution.

Risk: Overbroad OAuth scopes or the wrong active connection can expand the effect of an API call.

Mitigation: Review and limit each service connection's scopes and specify the intended Maton connection when multiple connections exist.

## Reference(s):

- [Maton homepage](https://maton.ai)
- [Maton API Reference](https://www.maton.ai/docs/api-reference)
- [Slack API gateway reference](references/slack/README.md)
- [Google Mail API gateway reference](references/google-mail/README.md)
- [Stripe API gateway reference](references/stripe/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with API request examples and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes gateway URLs, request headers, connection-management steps, troubleshooting guidance, and service-specific references; credentials are supplied by the user environment.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
