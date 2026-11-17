## Description:

Extends uploaded audio on PoYo by helping agents prepare, submit, and follow up on upload-and-extend-audio API jobs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare PoYo upload-and-extend-audio payloads, submit trusted server-side curl requests, and retrieve task status or webhook follow-up details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PoYo API keys or private media details could be exposed if payloads, headers, callback URLs, task ids, lyrics, or generated result URLs are logged or shared.

Mitigation: Keep POYO_API_KEY in server-side secrets, review the JSON payload before submission, and avoid logging private audio URLs, lyrics, customer data, callback URLs, generated result URLs, or authorization headers.

Risk: Submitting a payload sends uploaded audio URLs and request details to PoYo.

Mitigation: Install and use the skill only for intended PoYo uploaded-audio extension workflows, and submit requests only after the user explicitly asks to send a reviewed payload.

## Reference(s):

- [PoYo Upload and Extend Audio API Reference](references/api.md)
- [PoYo Upload and Extend Audio Model Page](https://poyo.ai/models/upload-and-extend-audio)
- [PoYo Upload and Extend Audio Docs](https://docs.poyo.ai/api-manual/music-series/upload-and-extend-audio)
- [PoYo Upload and Extend Audio OpenAPI JSON](https://docs.poyo.ai/api-manual/music-series/upload-and-extend-audio.json)
- [PoYo Query Music Detail Docs](https://docs.poyo.ai/api-manual/music-series/query-music-detail)
- [PoYo Music Webhook Docs](https://docs.poyo.ai/api-manual/music-series/music-webhook)
- [ClawHub Skill Page](https://clawhub.ai/coolhackboy/skills/poyo-upload-and-extend-audio)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON payloads and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include PoYo task identifiers, callback guidance, and music detail retrieval steps when a request is submitted.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
