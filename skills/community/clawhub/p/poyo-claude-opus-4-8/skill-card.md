## Description: <br>
Helps agents prepare Claude Opus 4.8 Messages API payloads and integration guidance for PoYo, including streaming, tool use, structured output, cache settings, vision content blocks, and server-side curl workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to build PoYo Claude Opus 4.8 Messages API requests, examples, and integration notes for Claude-compatible chat, tool use, structured output, streaming, and server-side workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PoYo API keys and private prompt data could be exposed if copied into browser code, logs, public repositories, screenshots, or chat output. <br>
Mitigation: Keep POYO_API_KEY in server-side environment variables or a backend secret manager, and avoid logging private messages, image content, tool inputs, or raw API-key headers. <br>
Risk: The helper script submits a user-provided payload to PoYo when run with a valid API key. <br>
Mitigation: Review payload files before execution and make live API calls only from a trusted shell after the user explicitly requests them. <br>
Risk: Optional Messages API fields and streaming behavior may vary by current PoYo support. <br>
Mitigation: Verify current PoYo documentation before relying on optional parameters, and use streaming only with a client that can consume streaming responses. <br>


## Reference(s): <br>
- [PoYo Claude Messages API documentation](https://docs.poyo.ai/api-manual/chat-series/claude-messages) <br>
- [PoYo Claude Opus 4.8 model page](https://poyo.ai/models/claude-opus-4-8) <br>
- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-claude-opus-4-8) <br>
- [Artifact API reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON payloads and inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include synchronous or streaming handling notes, model id, request fields, response parsing notes, and secret-handling guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
