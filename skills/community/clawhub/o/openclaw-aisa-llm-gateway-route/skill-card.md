## Description:

Unified LLM Gateway - One API for 70+ AI models. Route to GPT, Claude, Gemini, Grok and more with a single API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaimengphp](https://clawhub.ai/user/chaimengphp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to send chat, streaming, vision, and model-comparison requests through AIsa's OpenAI-compatible LLM gateway with one API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, conversation history, and image URLs or base64 content may be sent to AIsa and routed model providers.

Mitigation: Avoid submitting secrets, regulated data, or sensitive personal images unless AIsa's data handling and pricing have been reviewed.

Risk: Compare and fallback examples may send the same prompt to multiple models.

Mitigation: Use compare and fallback workflows only when multi-model transmission is acceptable for the data being processed.

## Reference(s):

- [OpenClaw homepage](https://openclaw.ai)
- [AIsa API reference](https://docs.aisa.one/reference/)
- [AIsa model pricing](https://marketplace.aisa.one/pricing)
- [ClawHub skill page](https://clawhub.ai/chaimengphp/skills/openclaw-aisa-llm-gateway-route)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions, shell commands, Python code, and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY; chat and compare commands return JSON, while streaming chat emits text chunks.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
