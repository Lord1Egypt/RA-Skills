## Description:

Praesidia helps agents verify AI agents, inspect trust scores, fetch A2A cards, discover marketplace agents, and apply security and compliance guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[msoica](https://clawhub.ai/user/msoica)

### License/Terms of Use:


## Use Case:

Developers and external users use Praesidia to evaluate agent identity and trust, discover compatible public agents, and configure or validate guardrails before using or recommending agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send API credentials and submitted content to a configurable Praesidia service endpoint.

Mitigation: Keep PRAESIDIA_API_URL on the official HTTPS endpoint unless intentionally using a trusted deployment, and install only when the configured service is trusted.

Risk: Agent content, guardrail validation text, and related metadata may be transmitted to the Praesidia service.

Mitigation: Use the least-privileged API key available and avoid submitting confidential or regulated content unless that service use is approved.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/msoica/skills/praesidia-a2a)
- [Praesidia Homepage](https://praesidia.ai)
- [Praesidia API Documentation](https://app.praesidia.ai/docs/api)
- [A2A Protocol](https://a2a-protocol.org)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and JavaScript-style API call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PRAESIDIA_API_KEY and may use PRAESIDIA_API_URL to select the service endpoint.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
