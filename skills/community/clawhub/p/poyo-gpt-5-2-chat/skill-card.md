## Description: <br>
Helps agents prepare PoYo GPT-5.2 chat-completion requests with OpenAI-compatible payloads, streaming options, and server-side API key handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create PoYo GPT-5.2 chat completion payloads, curl requests, and integration guidance for synchronous or streaming chat workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Chat prompts and messages are sent to PoYo when a request is submitted. <br>
Mitigation: Review payloads before submission and avoid sending private user messages unless policy and consent allow it. <br>
Risk: The PoYo API key could be exposed if copied into frontend code, logs, repositories, screenshots, or chat output. <br>
Mitigation: Keep POYO_API_KEY in server-side environment variables or a backend secret manager and avoid logging authorization headers. <br>
Risk: The included shell script submits a local JSON payload file to the PoYo chat completions endpoint. <br>
Mitigation: Run the script only from a trusted shell with a payload file you control. <br>


## Reference(s): <br>
- [PoYo chat completions documentation](https://docs.poyo.ai/api-manual/chat-series/chat-completions) <br>
- [PoYo GPT-5.2 Chat Completions API Reference](artifact/references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON payloads, curl examples, and optional shell-command instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference POYO_API_KEY and a user-controlled JSON payload file; no live API call unless explicitly requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
