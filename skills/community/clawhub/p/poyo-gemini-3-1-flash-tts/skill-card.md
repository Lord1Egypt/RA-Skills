## Description: <br>
Helps agents prepare and submit PoYo `gemini-3-1-flash-tts` text-to-speech jobs, including voice and style options, two-speaker dialogue, callbacks, and task status retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to build PoYo Gemini 3.1 Flash TTS requests, choose speech settings, submit trusted shell requests, and explain how to retrieve generated audio results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: POYO_API_KEY or generated audio workflow details could be exposed if copied into browser code, logs, screenshots, public repositories, or chat output. <br>
Mitigation: Keep the API key in server-side environment variables or a backend secret manager, and avoid logging private text, callback URLs, task ids, or generated audio URLs unless policy allows it. <br>
Risk: Private or regulated text may be sent to PoYo during text-to-speech generation. <br>
Mitigation: Use the skill only when PoYo is approved for the data involved, and do not make live API calls unless the user explicitly asks from a trusted server-side environment. <br>
Risk: Untrusted callback URLs could disclose task events or generated audio workflow metadata. <br>
Mitigation: Use callback_url values only for trusted HTTPS endpoints controlled by the deploying team. <br>


## Reference(s): <br>
- [PoYo Gemini 3.1 Flash TTS API Reference](references/api.md) <br>
- [PoYo Gemini 3.1 Flash TTS documentation](https://docs.poyo.ai/api-manual/music-series/gemini-3-1-flash-tts) <br>
- [PoYo Gemini 3.1 Flash TTS model page](https://poyo.ai/models/gemini-3-1-flash-tts) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with JSON payload examples and bash command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include model id, voice settings, style instructions, prepared request payloads, task ids, and next-step retrieval guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
