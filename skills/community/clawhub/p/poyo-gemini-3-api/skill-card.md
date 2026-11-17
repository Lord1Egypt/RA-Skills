## Description:

Helps agents prepare PoYo Gemini 3 API chat and Gemini Native Format requests, including payloads, curl commands, streaming settings, and integration guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build server-side PoYo Gemini 3 chat integrations, choose an endpoint style, prepare request payloads, and handle streaming or response parsing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PoYo API keys could be exposed if copied into browser code, public files, logs, screenshots, or chat output.

Mitigation: Keep POYO_API_KEY server-side in environment variables or a backend secret manager and avoid echoing authorization headers.

Risk: Prompts, inline media, secrets, or other private payload data may be shared with PoYo during API calls.

Mitigation: Review payload files before submission and send private data only when organizational policy allows sharing it with PoYo.

Risk: A live curl request can submit unreviewed data to the external PoYo API.

Mitigation: Run the submit script only from a trusted shell after an explicit request and payload review.

## Reference(s):

- [PoYo Gemini 3 model page](https://poyo.ai/models/gemini-3-api)
- [PoYo chat completions docs](https://docs.poyo.ai/api-manual/chat-series/chat-completions)
- [PoYo Gemini Native Format docs](https://docs.poyo.ai/api-manual/chat-series/gemini-native-format)
- [PoYo Gemini 3 Series API Reference](references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON payload examples and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include model IDs, endpoint style, synchronous or streaming handling, generation configuration, safety settings, and response parsing notes.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
