## Description:

Unified LLM Gateway - One API for 70+ AI models. Route to GPT, Claude, Gemini, Qwen, Deepseek, Grok and more with a single API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xjordansg-yolo](https://clawhub.ai/user/0xjordansg-yolo)

### License/Terms of Use:


## Use Case:

Developers and external agent builders use this skill to route chat, vision, comparison, streaming, and model-selection workflows through the AIsa unified LLM gateway with one API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, conversation history, image URLs or base64 image data, and tool schemas may be sent to AIsa and downstream model providers.

Mitigation: Avoid secrets, regulated data, private screenshots, and proprietary schemas unless the data path is approved.

Risk: Model usage may incur billing charges and vary by selected model.

Mitigation: Review AIsa pricing and control cost with model selection, max token limits, streaming where appropriate, and usage monitoring.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0xjordansg-yolo/skills/openclaw-aisa-llm-gateway)
- [OpenClaw homepage](https://openclaw.ai)
- [AIsa API reference](https://aisa.mintlify.app/api-reference/introduction)
- [AIsa pricing and model list](https://marketplace.aisa.one/pricing)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, Python code examples, and JSON API payloads or responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses AISA_API_KEY and sends selected prompts, conversation history, image references, and tool schemas to AIsa and possibly downstream model providers.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
