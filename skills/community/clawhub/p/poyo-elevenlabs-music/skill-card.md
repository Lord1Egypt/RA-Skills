## Description:

Generate music on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `elevenlabs-music`, text-to-music, instrumental music, structured composition plans, section timing, audio output formats, async task submission, callbacks, and task status retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and engineers use this skill to prepare PoYo ElevenLabs Music generation payloads, submit trusted server-side requests, and track asynchronous music generation results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill submits user-prepared music prompts and optional callback URLs to the PoYo API when explicitly requested.

Mitigation: Review payload JSON before submission and avoid sending private prompts, lyrics, callback URLs, task ids, or generated-audio links unless that is acceptable for the workflow.

Risk: The workflow requires a PoYo API key.

Mitigation: Keep POYO_API_KEY server-side in environment variables or a backend secret manager, and never expose it in browser code, logs, screenshots, public repositories, or chat output.

## Reference(s):

- [PoYo ElevenLabs Music API Reference](references/api.md)
- [PoYo ElevenLabs Music model page](https://poyo.ai/models/elevenlabs-music)
- [PoYo ElevenLabs Music API docs](https://docs.poyo.ai/api-manual/music-series/elevenlabs-music)
- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-elevenlabs-music)
- [coolhackboy publisher profile](https://clawhub.ai/user/coolhackboy)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON payloads and inline bash or curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a PoYo task_id and status retrieval or webhook next steps when a task is submitted.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
