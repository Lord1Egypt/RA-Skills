## Description:

Helps agents prepare PoYo Gemini 3.5 Flash chat requests using OpenAI-compatible chat completions or Gemini Native Format, including payloads, streaming options, generation config, and server-side integration notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare PoYo Gemini 3.5 Flash request payloads, curl commands, and integration notes for chat, streaming, and Gemini Native Format workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can help send prompts or payload files to PoYo's API when a user runs its curl examples or helper script.

Mitigation: Use it only for intended PoYo workflows, review payload files before submission, and run helper commands only from a trusted server-side shell.

Risk: POYO_API_KEY and private prompt data could be exposed if copied into browser code, logs, screenshots, public repositories, or chat output.

Mitigation: Store POYO_API_KEY in server-side environment variables or a backend secret manager, and avoid logging private messages, system prompts, inline media data, or authorization headers.

## Reference(s):

- [PoYo Gemini 3.5 Flash API Reference](references/api.md)
- [PoYo Gemini 3.5 Flash model page](https://poyo.ai/models/gemini-3-5-flash)
- [PoYo Gemini Native Format docs](https://docs.poyo.ai/api-manual/chat-series/gemini-native-format)
- [PoYo Chat Completions docs](https://docs.poyo.ai/api-manual/chat-series/chat-completions)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON payloads and bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include endpoint selection, model id, synchronous or streaming handling, generation configuration, safety settings, and response parsing notes.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
