## Description:

Praesidia helps agents verify AI agent identity, check trust scores, discover marketplace agents, fetch A2A agent cards, and apply guardrails for security and compliance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[msoica](https://clawhub.ai/user/msoica)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to evaluate agent trust, discover suitable public or private agents, and configure or validate guardrails before using agents in security- or compliance-sensitive workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can apply or change live guardrail settings through authenticated Praesidia API requests.

Mitigation: Require explicit user confirmation before applying or modifying guardrails, and use least-privilege keys with separate read and write scopes when available.

Risk: The skill supports configurable API endpoints, including local or custom URLs.

Mitigation: Prefer the default HTTPS production endpoint and avoid sending production API keys to custom or plaintext endpoints.

Risk: Content submitted for guardrail validation is sent to Praesidia or the configured API endpoint.

Mitigation: Treat validation input as data shared with the configured service and avoid submitting sensitive content unless the user has approved that data flow.

## Reference(s):

- [Praesidia homepage](https://praesidia.ai)
- [Praesidia API documentation](https://app.praesidia.ai/docs/api)
- [A2A protocol](https://a2a-protocol.org)
- [ClawHub skill listing](https://clawhub.ai/msoica/skills/praesidia)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with API request examples, JSON configuration snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PRAESIDIA_API_KEY and may use PRAESIDIA_API_URL for a custom API endpoint.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
