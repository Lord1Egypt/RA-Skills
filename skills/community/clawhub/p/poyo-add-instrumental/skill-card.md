## Description:

Add instrumental accompaniment to uploaded audio on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `add-instrumental`, backing tracks, style tags, negative tags, music model versions, callbacks, and music detail retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and music automation builders use this skill to prepare PoYo Add Instrumental payloads, submit trusted server-side requests, and retrieve or handle asynchronous music generation results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The request payload sends the audio URL, title, tags, negative tags, and optional callback URL to PoYo.

Mitigation: Review the payload before submission and avoid including private recordings, customer identifiers, callback secrets, or sensitive style notes unless the product policy allows it.

Risk: POYO_API_KEY exposure could allow unauthorized PoYo API usage.

Mitigation: Store POYO_API_KEY only in a server-side secret or environment variable, and do not place it in browser code, logs, screenshots, repositories, or chat output.

Risk: A live submission may start an asynchronous PoYo generation task.

Mitigation: Submit only after the user explicitly confirms the prepared payload should be sent from a trusted shell or server environment.

## Reference(s):

- [PoYo Add Instrumental API Reference](references/api.md)
- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-add-instrumental)
- [PoYo Add Instrumental model page](https://poyo.ai/models/add-instrumental)
- [PoYo Add Instrumental API docs](https://docs.poyo.ai/api-manual/music-series/add-instrumental)
- [PoYo Add Instrumental OpenAPI JSON](https://docs.poyo.ai/api-manual/music-series/add-instrumental.json)
- [PoYo music detail docs](https://docs.poyo.ai/api-manual/music-series/query-music-detail)
- [PoYo music webhook docs](https://docs.poyo.ai/api-manual/music-series/music-webhook)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON payload examples and bash curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a returned task_id when the user explicitly authorizes a live PoYo submission.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
