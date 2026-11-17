## Description:

Expand concise music-style ideas on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `boost-music-style`, music prompt enhancement, genre and mood expansion, instrumentation direction, production descriptors, Generate Music preparation, callbacks, and music detail retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and music-generation workflow builders use this skill to expand concise genre, mood, instrument, tempo, or production cues through PoYo's boost-music-style API before passing reviewed results into a Generate Music workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PoYo API requests upload the reviewed payload data to api.poyo.ai.

Mitigation: Do not send confidential campaign, customer, or proprietary music direction unless sharing it with PoYo is acceptable.

Risk: Exposing POYO_API_KEY could allow unauthorized use of the PoYo API.

Mitigation: Keep POYO_API_KEY server-side and out of browser code, public repositories, logs, screenshots, and chat output.

Risk: Live API calls can submit unintended payloads when run in an untrusted or unreviewed environment.

Mitigation: Make live calls only when explicitly requested in a trusted environment and use a reviewed payload file.

Risk: The enhanced music-style description may drift from the user's intended genre, mood, or instrumentation.

Mitigation: Review the enhanced description before using it in Generate Music and keep only details that match the user's intent.

## Reference(s):

- [PoYo Boost Music Style API Reference](artifact/references/api.md)
- [PoYo Boost Music Style Model Page](https://poyo.ai/models/boost-music-style)
- [PoYo Boost Music Style API Docs](https://docs.poyo.ai/api-manual/music-series/boost-music-style)
- [PoYo Music Detail API Docs](https://docs.poyo.ai/api-manual/music-series/query-music-detail)
- [PoYo Music Webhook Docs](https://docs.poyo.ai/api-manual/music-series/music-webhook)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON payload summaries and bash snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, a reviewed payload file, and a server-side POYO_API_KEY; live submission returns a task_id for detail lookup or webhook handling.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
