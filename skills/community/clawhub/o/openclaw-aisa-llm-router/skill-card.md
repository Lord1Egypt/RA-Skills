## Description: <br>
Unified LLM Gateway - One API for 70+ AI models. Route to GPT, Claude, Gemini, Qwen, Deepseek, Grok and more with a single API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIsaDocs](https://clawhub.ai/user/AIsaDocs) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to route chat, vision, comparison, and function-calling requests across multiple LLM providers through AIsa's OpenAI-compatible API with one API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, image URLs, or base64 image data may contain sensitive information and are sent to the AIsa API. <br>
Mitigation: Do not submit secrets, regulated data, private documents, screenshots, or sensitive image URLs unless AIsa's privacy, retention, routing, and billing terms have been reviewed and accepted. <br>
Risk: A shared or long-lived AISA_API_KEY could increase exposure if copied into logs, shells, or agent transcripts. <br>
Mitigation: Use a dedicated, revocable AISA_API_KEY and rotate it if exposure is suspected. <br>
Risk: Multi-model routing can create variable spend across providers and model families. <br>
Mitigation: Set spending limits if available and use max_tokens, model selection, and response usage metadata to control costs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/AIsaDocs/openclaw-aisa-llm-router) <br>
- [OpenClaw homepage](https://openclaw.ai) <br>
- [AIsa API Reference](https://aisa.mintlify.app/api-reference/introduction) <br>
- [AIsa model pricing](https://marketplace.aisa.one/pricing) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, JSON, Text] <br>
**Output Format:** [Markdown guidance with bash, Python, and JSON examples; CLI responses are plain text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY and sends user-provided prompts or image references to AIsa API endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
