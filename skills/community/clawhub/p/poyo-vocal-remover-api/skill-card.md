## Description:

Helps agents prepare and submit PoYo Vocal Remover API requests for vocal separation, stem splitting, callbacks, and music detail retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to build PoYo vocal-removal workflows, choose the correct model id, prepare request payloads, submit trusted server-side API calls, and retrieve or receive separated audio results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: POYO_API_KEY could be exposed through client code, logs, screenshots, repositories, or chat output.

Mitigation: Keep the key in a server-side environment variable or secret manager, and redact authorization headers from all outputs.

Risk: Private audio URLs, callback URLs, task ids, audio ids, or generated stem URLs could be shared beyond the intended workflow.

Mitigation: Review payloads before submission and avoid logging or sending sensitive URLs and identifiers unless the workflow permits sharing them with PoYo.

Risk: The bundled submit script can make a live external API request.

Mitigation: Run it only from a trusted shell after the user explicitly confirms the payload should be sent to PoYo.

Risk: PoYo API fields and model-specific options may change.

Mitigation: Verify current PoYo documentation before relying on model options in production workflows.

## Reference(s):

- [PoYo Vocal Remover API Reference](references/api.md)
- [PoYo Vocal Remover API Model Page](https://poyo.ai/models/vocal-remover-api)
- [PoYo Separate Vocals API Docs](https://docs.poyo.ai/api-manual/music-series/vocal-remover/separate-vocals)
- [PoYo Stem Split API Docs](https://docs.poyo.ai/api-manual/music-series/vocal-remover/stem-split)
- [PoYo Upload and Separate Vocals API Docs](https://docs.poyo.ai/api-manual/music-series/vocal-remover/upload-and-separate-vocals)
- [PoYo Query Music Detail API Docs](https://docs.poyo.ai/api-manual/music-series/query-music-detail)
- [PoYo Music Webhook API Docs](https://docs.poyo.ai/api-manual/music-series/music-webhook)
- [ClawHub Skill Page](https://clawhub.ai/coolhackboy/skills/poyo-vocal-remover-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON payloads and bash curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include returned PoYo task ids only after an explicitly requested API submission.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
