## Description:

Praesidia helps AI assistants verify agent identities, check trust scores, fetch A2A agent cards, discover marketplace agents, and apply security and compliance guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[msoica](https://clawhub.ai/user/msoica)

### License/Terms of Use:

MIT

## Use Case:

Developers, enterprise teams, and OpenClaw users use this skill to verify agent identity and trust, discover suitable public agents, fetch A2A cards, and configure guardrails for security, compliance, and content moderation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change live agent guardrail configurations.

Mitigation: Use a least-privilege Praesidia key and require a clear summary plus user confirmation before applying or modifying guardrails.

Risk: The skill can send user content and bearer credentials to remote endpoints.

Mitigation: Keep the API URL on the official Praesidia host or a trusted HTTPS deployment, and do not send secrets or regulated content to validation unless approved.

## Reference(s):

- [Praesidia Homepage](https://praesidia.ai)
- [Praesidia API Documentation](https://app.praesidia.ai/docs/api)
- [A2A Protocol](https://a2a-protocol.org)
- [ClawHub Skill Page](https://clawhub.ai/msoica/skills/praesidia-ai-a2a)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown responses with REST API call examples and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include trust-score summaries, guardrail recommendations, and API request details.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
