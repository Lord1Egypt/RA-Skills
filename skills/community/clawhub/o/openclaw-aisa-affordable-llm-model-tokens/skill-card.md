## Description: <br>
Unified LLM Gateway - One API for 70+ AI models. Route to GPT, Claude, Gemini, Qwen, Deepseek, Grok and more with a single API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xjordansg-yolo](https://clawhub.ai/user/0xjordansg-yolo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to call an AIsa-hosted LLM routing API for chat, streaming, vision analysis, model comparison, and model listing through one API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, messages, image URLs or base64 image data, and related metadata are sent to AIsa and may be routed to downstream model providers. <br>
Mitigation: Avoid submitting secrets or regulated data unless approved, and use the skill only when the selected data is appropriate for third-party model routing. <br>
Risk: The skill depends on a bearer API key stored in AISA_API_KEY. <br>
Mitigation: Use a protected, limited API key where possible, rotate it if exposed, and avoid logging or sharing command examples that include the key value. <br>
Risk: Model routing and comparison can consume paid credits across providers. <br>
Mitigation: Set max token limits, monitor usage and costs, and choose lower-cost models for simple tasks when appropriate. <br>


## Reference(s): <br>
- [OpenClaw homepage](https://openclaw.ai) <br>
- [AIsa pricing and model availability](https://marketplace.aisa.one/pricing) <br>
- [AIsa API reference](https://aisa.mintlify.app/api-reference/introduction) <br>
- [ClawHub skill listing](https://clawhub.ai/0xjordansg-yolo/openclaw-aisa-affordable-llm-model-tokens) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; runtime responses may be JSON or streamed text from the AIsa API.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 or curl for examples and an AISA_API_KEY environment variable for authenticated API calls.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
