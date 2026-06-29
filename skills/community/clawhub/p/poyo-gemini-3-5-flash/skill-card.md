## Description: <br>
Provides PoYo Gemini 3.5 Flash chat guidance for OpenAI-compatible chat payloads, Gemini Native Format payloads, streaming requests, generation settings, and server-side curl usage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to prepare PoYo Gemini 3.5 Flash chat requests, choose between OpenAI-compatible and Gemini Native formats, configure streaming or generation options, and avoid leaking API keys or private prompt data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PoYo API keys or authorization headers could be exposed if copied into client code, logs, screenshots, public repositories, or chat output. <br>
Mitigation: Keep POYO_API_KEY in a server-side environment or secret manager and avoid logging raw credentials. <br>
Risk: Private messages, system prompts, or media may be sent to PoYo when using the generated request payloads. <br>
Mitigation: Review payloads before sending and only forward private data when the user's policy allows it. <br>
Risk: The included shell helper makes a live network request to the PoYo chat completions endpoint. <br>
Mitigation: Run it only from a trusted shell with an intended payload and a properly scoped POYO_API_KEY. <br>


## Reference(s): <br>
- [PoYo Gemini Native Format Documentation](https://docs.poyo.ai/api-manual/chat-series/gemini-native-format) <br>
- [PoYo Chat Completions Documentation](https://docs.poyo.ai/api-manual/chat-series/chat-completions) <br>
- [PoYo Gemini 3.5 Flash Model Page](https://poyo.ai/models/gemini-3-5-flash) <br>
- [ClawHub Skill Page](https://clawhub.ai/coolhackboy/skills/poyo-gemini-3-5-flash) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON payload examples and bash curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include endpoint selection, model id, request payloads, streaming notes, generation configuration, safety settings, and response parsing notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
