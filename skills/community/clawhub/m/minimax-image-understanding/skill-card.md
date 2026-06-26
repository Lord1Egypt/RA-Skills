## Description: <br>
Uses multimodal vision models to describe the business meaning and data content of screenshots, charts, and document photos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aidescend](https://clawhub.ai/user/aidescend) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to send a local image to MiniMax VLM, OpenAI GPT-4o, or Claude Vision and receive a concise business-focused description. It is suited for interpreting screenshots, charts, and document photos when the selected provider is approved for the image content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images and prompts are sent to MiniMax, OpenAI, or Anthropic under the chosen provider's data policies. <br>
Mitigation: Use only provider-approved data, and avoid confidential screenshots, regulated documents, IDs, credentials, or other sensitive images unless policy permits that transfer. <br>
Risk: A custom MINIMAX_API_HOST can redirect image data and API credentials to an untrusted endpoint. <br>
Mitigation: Keep MINIMAX_API_HOST set to an approved MiniMax endpoint and do not use untrusted hosts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aidescend/minimax-image-understanding) <br>
- [MiniMax API endpoint](https://api.minimaxi.com) <br>
- [OpenAI Chat Completions endpoint](https://api.openai.com/v1/chat/completions) <br>
- [Anthropic Messages endpoint](https://api.anthropic.com/v1/messages) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration guidance] <br>
**Output Format:** [Plain text from a CLI command, with Markdown setup examples in the skill instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local image path and one configured provider API key; optional model and prompt arguments change the selected provider and description focus.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
