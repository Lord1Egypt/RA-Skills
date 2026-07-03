## Description: <br>
Helps agents prepare PoYo Gemini 3 chat requests, including OpenAI-compatible chat payloads, Gemini Native Format payloads, streaming calls, and server-side curl examples. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to build PoYo Gemini 3 chat integrations, choose an endpoint style, draft request payloads, and understand response handling for synchronous or streaming workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PoYo API keys and private prompt data could be exposed through client-side code, logs, repositories, screenshots, or chat output. <br>
Mitigation: Keep POYO_API_KEY in server-side environment variables or a backend secret manager, and avoid logging API keys, private prompts, inline media data, or authorization headers. <br>
Risk: Live API calls can submit user content to the PoYo endpoint and may incur external service effects. <br>
Mitigation: Run calls only when the user explicitly requests execution in a trusted server-side environment, and review payloads before submission. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/coolhackboy/skills/poyo-gemini-3-api) <br>
- [PoYo Gemini Native Format docs](https://docs.poyo.ai/api-manual/chat-series/gemini-native-format) <br>
- [PoYo Chat Completions docs](https://docs.poyo.ai/api-manual/chat-series/chat-completions) <br>
- [PoYo Gemini 3 API model page](https://poyo.ai/models/gemini-3-api) <br>
- [PoYo Gemini 3 Series API reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON payload examples and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include endpoint choice, model id, generation settings, streaming notes, and response parsing guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
