## Description: <br>
Openrouter Free lists free OpenRouter models and sends chat prompts to free OpenRouter chat models using a configured API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binsonhao](https://clawhub.ai/user/binsonhao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to list zero-priced OpenRouter models and run CLI chat requests against a free model after configuring their own OpenRouter API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Chat prompts are sent to OpenRouter for processing and may include sensitive user data. <br>
Mitigation: Avoid sending secrets, proprietary code, or private data unless the user accepts OpenRouter processing that content. <br>
Risk: The skill requires an OpenRouter API key for model listing and chat requests. <br>
Mitigation: Provide OPENROUTER_API_KEY explicitly in the runtime environment and prefer a dedicated limited key. <br>
Risk: Some models may be unavailable in certain regions or may return provider-specific errors. <br>
Mitigation: Handle OpenRouter errors during execution and use the automatic free-model route when a specific model is unavailable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/binsonhao/openrouter-free) <br>
- [OpenRouter API key settings](https://openrouter.ai/settings/keys) <br>
- [OpenRouter API endpoint](https://openrouter.ai/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown model lists, plain chat text, JSON model data, and CLI command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses OPENROUTER_API_KEY and sends prompts to OpenRouter; chat responses request up to 2048 tokens.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
