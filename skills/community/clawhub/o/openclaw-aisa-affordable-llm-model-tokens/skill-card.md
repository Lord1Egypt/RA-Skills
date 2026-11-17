## Description:

Unified LLM Gateway - One API for 70+ AI models. Route to GPT, Claude, Gemini, Qwen, Deepseek, Grok and more with a single API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xjordansg-yolo](https://clawhub.ai/user/0xjordansg-yolo)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to call AISA's OpenAI-compatible LLM gateway with one API key for chat, streaming, vision analysis, model comparison, and model selection across supported providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, conversation history, image URLs or image data, and tool/function schemas are sent to AISA's external API for model routing.

Mitigation: Use the skill only where that external processing is approved, and avoid sending secrets, regulated data, private screenshots, or internal documents unless approved.

Risk: The AISA_API_KEY can be exposed if copied into code, logs, or shared shell history.

Mitigation: Provide the key through environment configuration and keep it out of source files, logs, and shared command histories.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/0xjordansg-yolo/skills/openclaw-aisa-affordable-llm-model-tokens)
- [OpenClaw homepage](https://openclaw.ai)
- [AISA API reference](https://aisa.mintlify.app/api-reference/introduction)
- [AISA model pricing](https://marketplace.aisa.one/pricing)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands, Python examples, and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY. The included client can return JSON chat responses, stream text chunks, compare models, and list supported model families.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
