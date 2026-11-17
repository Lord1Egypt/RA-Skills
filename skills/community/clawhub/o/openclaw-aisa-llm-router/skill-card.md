## Description:

Unified LLM Gateway - One API for 70+ AI models. Route to GPT, Claude, Gemini, Qwen, Deepseek, Grok and more with a single API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aisadocs](https://clawhub.ai/user/aisadocs)

### License/Terms of Use:


## Use Case:

Developers and external agent builders use this skill to route chat, vision, model comparison, streaming, and function-calling requests through a unified AIsa API using one API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, chat history, image URLs or base64 image data, and tool schemas are routed through api.aisa.one and may be sent to downstream model providers.

Mitigation: Do not send secrets, regulated data, private images, or proprietary documents unless that routing is approved.

Risk: Use of AISA_API_KEY may incur token usage and billing costs across selected models.

Mitigation: Set token limits, choose appropriate models, monitor usage and cost, and use fallback routing intentionally.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aisadocs/skills/openclaw-aisa-llm-router)
- [OpenClaw](https://openclaw.ai)
- [AIsa API Reference](https://aisa.mintlify.app/api-reference/introduction)
- [AIsa Pricing](https://marketplace.aisa.one/pricing)
- [AIsa](https://aisa.one)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, Python code examples, and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl or python3 and an AISA_API_KEY environment variable; routes prompts, images, and tool schemas to the AIsa API.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
