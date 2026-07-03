## Description: <br>
Helps agents prepare Claude Opus 4.7 Messages API payloads and server-side PoYo calls for messages, system prompts, multi-turn conversations, tools, structured output, prompt caching, vision content blocks, and streaming. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when a workflow has explicitly chosen PoYo for Claude Opus 4.7 and needs request payloads, curl commands, streaming setup, tool-use payloads, structured-output payloads, or response parsing guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PoYo API keys or private prompt data could be exposed through frontend code, logs, screenshots, repositories, or chat output. <br>
Mitigation: Keep POYO_API_KEY in server-side environment variables or a backend secret manager, avoid logging sensitive payloads or headers, and review payloads before sending. <br>
Risk: The bundled shell helper can submit live requests to PoYo when run with a prepared payload and POYO_API_KEY. <br>
Mitigation: Run live calls only from a trusted shell after the user explicitly confirms the payload should be sent to PoYo. <br>
Risk: Prompts, image content, tool inputs, or user data may leave the local environment when sent to PoYo. <br>
Mitigation: Send private or regulated data only when the user's policy allows PoYo processing for that information. <br>


## Reference(s): <br>
- [PoYo Claude Opus 4.7 Messages API Reference](references/api.md) <br>
- [PoYo Claude Messages API documentation](https://docs.poyo.ai/api-manual/chat-series/claude-messages) <br>
- [PoYo Claude Opus 4.7 model page](https://poyo.ai/models/claude-opus-4-7) <br>
- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-claude-opus-4-7) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with JSON payloads and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include model id, request payloads, curl examples, streaming notes, tool and structured-output settings, cache settings, and response parsing guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
