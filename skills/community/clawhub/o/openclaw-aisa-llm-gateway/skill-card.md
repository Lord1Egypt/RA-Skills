## Description: <br>
Unified LLM Gateway - One API for 70+ AI models. Route to GPT, Claude, Gemini, Qwen, Deepseek, Grok and more with a single API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xjordansg-yolo](https://clawhub.ai/user/0xjordansg-yolo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and autonomous agents use this skill to call AIsa's OpenAI-compatible gateway, switch among supported LLM families, stream chat responses, analyze image URLs, compare model outputs, and route requests with one API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, message history, image URLs, and request metadata are sent to AIsa and may be routed through external model providers. <br>
Mitigation: Use only with data approved for those providers; avoid submitting secrets, private documents, internal image links, or regulated personal data unless your organization has approved the workflow. <br>
Risk: The skill depends on an AISA_API_KEY for paid gateway access. <br>
Mitigation: Store the key securely, monitor usage and billing, and set token or model limits where appropriate. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/0xjordansg-yolo/openclaw-aisa-llm-gateway) <br>
- [OpenClaw Homepage](https://openclaw.ai) <br>
- [AIsa Pricing and Model List](https://marketplace.aisa.one/pricing) <br>
- [AIsa API Reference](https://aisa.mintlify.app/api-reference/introduction) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python examples, and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY and network access to AIsa's API; CLI commands may stream text output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
