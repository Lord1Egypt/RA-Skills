## Description: <br>
Unified LLM Gateway - One API for 70+ AI models. Route to GPT, Claude, Gemini, Grok and more with a single API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chaimengphp](https://clawhub.ai/user/chaimengphp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to route chat, streaming, vision, model comparison, and OpenAI-compatible requests through the AIsa LLM gateway with a single AISA_API_KEY. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, conversation content, image URLs, and request metadata are sent to AIsa and may be routed to downstream model providers. <br>
Mitigation: Use the skill only for approved data flows and avoid submitting secrets, regulated data, private documents, or sensitive image links. <br>
Risk: The helper script depends on a valid AISA_API_KEY and external AIsa API availability. <br>
Mitigation: Store the API key in the environment, restrict access to it, and handle API errors or unavailable models as operational failures. <br>
Risk: Model availability and pricing are documented as variable. <br>
Mitigation: Check the current AIsa model list and pricing before relying on a specific model or cost profile. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/chaimengphp/openclaw-aisa-llm-gateway-route) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/chaimengphp) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [AIsa Pricing and Model List](https://marketplace.aisa.one/pricing) <br>
- [AIsa API Reference](https://docs.aisa.one/reference/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell and Python examples; the helper script returns JSON for non-streaming requests and plain streamed text for streaming chat.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY for API calls and sends prompt, message, image URL, and request metadata to the external AIsa API.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
