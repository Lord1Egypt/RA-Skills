## Description:

Generate speech on PoYo using the ElevenLabs V3 TTS model, including payload preparation, async task submission, and task status retrieval guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare PoYo ElevenLabs V3 TTS request payloads, choose voice and model options, submit trusted server-side text-to-speech jobs, and explain how to retrieve generated audio results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PoYo API keys can be exposed if placed in browser code, logs, screenshots, repositories, or chat output.

Mitigation: Keep POYO_API_KEY in a server-side environment variable or secret manager and avoid echoing the key in generated examples or command output.

Risk: Submitting confidential text, callback URLs, task IDs, timestamps, or generated audio can create data-handling concerns.

Mitigation: Review payload JSON before submission and send sensitive content only when the user's PoYo account and data policy allow it.

Risk: The skill can make a hosted text-to-speech request when explicitly invoked with a prepared payload.

Mitigation: Make live submissions only from a trusted shell with curl and POYO_API_KEY available, and report the returned task_id for controlled follow-up retrieval.

## Reference(s):

- [PoYo ElevenLabs V3 TTS model page](https://poyo.ai/models/elevenlabs-v3-tts)
- [PoYo ElevenLabs V3 TTS API documentation](https://docs.poyo.ai/api-manual/music-series/elevenlabs-v3-tts)
- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-elevenlabs-v3-tts)
- [Artifact API reference](references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON payloads and bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include curl examples, payload summaries, selected voice and language options, task IDs, and status-retrieval next steps.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
