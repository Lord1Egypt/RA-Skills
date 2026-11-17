## Description:

OpenAI-compatible LLM gateway for AI agents that lets OpenAI clients use a third-party base URL for chat completions with USDC pay-per-call or funded-key billing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[colinhughes2121](https://clawhub.ai/user/colinhughes2121)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to configure OpenAI-compatible clients for chat completions through a third-party gateway, including x402 pay-per-call and funded-key payment flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and request data are transmitted to api.gocreativeai.com and may be routed to upstream model providers.

Mitigation: Only send data you are allowed to share with the gateway and upstream providers; review privacy, retention, compliance, and billing terms before using confidential or regulated content.

Risk: Funded gateway keys function as credentials and may authorize paid usage.

Mitigation: Store funded keys securely, keep them revocable, and avoid embedding them in public logs, prompts, repositories, or shared transcripts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/colinhughes2121/skills/openai-compatible-llm-gateway)
- [Publisher profile](https://clawhub.ai/user/colinhughes2121)
- [Gateway base URL](https://api.gocreativeai.com/v1)
- [OpenAI-compatible chat completions endpoint](https://api.gocreativeai.com/v1/chat/completions)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Code, Shell commands]

**Output Format:** [Markdown with inline Python and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a base URL, endpoint descriptions, model tier notes, and payment setup guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
