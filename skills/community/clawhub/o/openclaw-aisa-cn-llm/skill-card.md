## Description: <br>
China LLM Gateway - Unified interface for Chinese LLMs including Qwen, DeepSeek, GLM, Baichuan. OpenAI compatible, one API Key for all models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chaimengphp](https://clawhub.ai/user/chaimengphp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to route chat, coding, reasoning, vision, translation, streaming, and model-comparison requests to Chinese LLMs through the AIsa OpenAI-compatible gateway. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends prompts, message content, and optional image URLs to the AIsa third-party gateway. <br>
Mitigation: Use it only when the provider's data-handling terms are acceptable, and avoid sending secrets, regulated data, proprietary code, or private image URLs. <br>
Risk: The AISA_API_KEY can authorize paid model usage if exposed or reused broadly. <br>
Mitigation: Use a dedicated API key, keep it in the environment rather than chats or logs, and monitor cost and quota. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chaimengphp/openclaw-aisa-cn-llm) <br>
- [OpenClaw homepage](https://openclaw.ai) <br>
- [AIsa API reference](https://docs.aisa.one/reference/) <br>
- [AIsa model pricing](https://marketplace.aisa.one/pricing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON API examples, Python code snippets, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY for chat and compare commands; the models command can run without an API key.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
