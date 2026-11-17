## Description:

Generate speech on PoYo using the elevenlabs-tts-turbo-2-5 text-to-speech model, with guidance for payload preparation, voice controls, async submission, callbacks, and result retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare PoYo text-to-speech requests, tune voice and delivery parameters, submit trusted server-side payloads, and explain how to retrieve task results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PoYo API keys could be exposed if copied into browser code, public repositories, logs, screenshots, or chat output.

Mitigation: Keep POYO_API_KEY server-side in environment variables or a backend secret manager and avoid printing it in generated examples.

Risk: Text payloads, callback URLs, task ids, and generated audio URLs may contain private or customer-sensitive information.

Mitigation: Submit only policy-approved content to PoYo and avoid logging private scripts, callback URLs, task ids, or generated audio URLs unless explicitly allowed.

## Reference(s):

- [PoYo ElevenLabs TTS Turbo 2.5 API Reference](references/api.md)
- [PoYo model page](https://poyo.ai/models/elevenlabs-tts-turbo-2-5)
- [PoYo API docs](https://docs.poyo.ai/api-manual/music-series/elevenlabs-tts-turbo-2-5)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON payload examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include model id, voice and language choices, delivery controls, final payload summary, returned task_id, and next retrieval step.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
