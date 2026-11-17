## Description:

Praesidia guides AI assistants through agent verification, trust scoring, marketplace discovery, A2A card retrieval, and security or compliance guardrail operations using Praesidia APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[msoica](https://clawhub.ai/user/msoica)

### License/Terms of Use:

MIT

## Use Case:

Developers, operators, and AI assistants use this skill to check whether agents are trustworthy, discover suitable agents, retrieve A2A agent cards, and configure or validate guardrails for security, content moderation, and compliance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive content and API credentials may be sent to configurable API endpoints.

Mitigation: Review PRAESIDIA_API_URL before use, prefer the official HTTPS endpoint unless operating a custom deployment, and use a least-privilege Praesidia API key.

Risk: Guardrail operations can affect live agent behavior.

Mitigation: Confirm guardrail changes before applying them, especially when enabling blocking, redaction, replacement, retry, or escalation actions.

Risk: Content submitted for guardrail validation may be shared with Praesidia.

Mitigation: Treat submitted validation content as potentially sent to Praesidia and avoid sending data that the user has not approved for that purpose.

## Reference(s):

- [Praesidia homepage](https://praesidia.ai)
- [Praesidia API documentation](https://app.praesidia.ai/docs/api)
- [A2A protocol](https://a2a-protocol.org)
- [ClawHub skill page](https://clawhub.ai/msoica/skills/praesidia-a2)

## Skill Output:

**Output Type(s):** [guidance, API calls, configuration, shell commands]

**Output Format:** [Markdown guidance with API request examples, configuration snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a PRAESIDIA_API_KEY and may use PRAESIDIA_API_URL to select the Praesidia API endpoint.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
