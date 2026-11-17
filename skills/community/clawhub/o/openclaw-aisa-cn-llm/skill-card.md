## Description:

China LLM Gateway - Unified interface for Chinese LLMs including Qwen, DeepSeek, GLM, Baichuan. OpenAI compatible, one API Key for all models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaimengphp](https://clawhub.ai/user/chaimengphp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to route chat, coding, reasoning, translation, vision, and model-comparison requests to Chinese LLMs through AIsa's OpenAI-compatible API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, code snippets, image URLs, and related metadata may be sent to AIsa and downstream model providers.

Mitigation: Do not send secrets, regulated data, or proprietary code unless your organization has approved the provider and its retention terms.

Risk: Live API calls require AISA_API_KEY and depend on provider availability, account balance, model availability, and rate limits.

Mitigation: Store the API key securely, monitor quota and rate-limit errors, and handle failed responses before relying on generated output.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chaimengphp/skills/openclaw-aisa-cn-llm)
- [OpenClaw Homepage](https://openclaw.ai)
- [AIsa API Reference](https://docs.aisa.one/reference/)
- [AIsa Pricing](https://marketplace.aisa.one/pricing)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash, Python, and JSON examples; CLI responses may be JSON or streamed text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 or curl and an AISA_API_KEY for live API calls.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
