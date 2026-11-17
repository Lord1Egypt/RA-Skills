## Description:

Retrieve timestamped lyrics on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `get-timestamped-lyrics`, synchronized lyrics, word timing, waveform data, task_id plus audio_id inputs, callbacks, and music detail retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to prepare and submit PoYo get-timestamped-lyrics requests for completed music tracks, then interpret synchronized word timing and waveform responses for subtitles, karaoke, or audio visualization workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill submits request payloads containing task IDs, audio IDs, callback URLs, and related music data to PoYo.

Mitigation: Review the JSON payload before submission and send only data that is intended for PoYo.

Risk: The PoYo API key is required for authenticated requests.

Mitigation: Store POYO_API_KEY as a server-side secret and avoid exposing it in browser code, public repositories, logs, screenshots, or chat output.

## Reference(s):

- [PoYo Get Timestamped Lyrics API Reference](references/api.md)
- [PoYo Get Timestamped Lyrics Model Page](https://poyo.ai/models/get-timestamped-lyrics)
- [PoYo Get Timestamped Lyrics API Documentation](https://docs.poyo.ai/api-manual/music-series/get-timestamped-lyrics)
- [PoYo Get Timestamped Lyrics OpenAPI JSON](https://docs.poyo.ai/api-manual/music-series/get-timestamped-lyrics.json)
- [ClawHub Skill Page](https://clawhub.ai/coolhackboy/skills/poyo-get-timestamped-lyrics)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with JSON payloads and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include request payloads, curl commands, returned task identifiers, timing response summaries, and next-step retrieval or webhook guidance.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
