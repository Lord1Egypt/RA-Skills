## Description:

Helps agents prepare and submit PoYo Add Vocals requests that generate vocals over uploaded instrumental audio, including lyrics or vocal prompts, style controls, callbacks, and result retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and music automation teams use this skill to build PoYo Add Vocals workflows for adding generated vocals to instrumental audio, preparing request payloads, submitting tasks, and retrieving results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow sends instrumental audio URLs, lyrics or vocal prompts, and optional callback URLs to PoYo.

Mitigation: Review payloads before submission and avoid private recordings, customer names, sensitive lyrics, or sensitive callback URLs unless PoYo handling is acceptable for the use case.

Risk: The skill requires a PoYo API key for live submissions.

Mitigation: Store POYO_API_KEY only in server-side environment variables or a secret manager, and do not expose it in browser code, logs, screenshots, repositories, or chat output.

Risk: Submitting a task makes an external API call and may start a long-running generation workflow.

Mitigation: Make live calls only after the user confirms the payload and intended submission, then save the returned task ID for status checks or webhook handling.

## Reference(s):

- [PoYo Add Vocals API Reference](references/api.md)
- [PoYo Add Vocals model page](https://poyo.ai/models/add-vocals)
- [PoYo Add Vocals API docs](https://docs.poyo.ai/api-manual/music-series/add-vocals)
- [PoYo Add Vocals OpenAPI JSON](https://docs.poyo.ai/api-manual/music-series/add-vocals.json)
- [PoYo music detail docs](https://docs.poyo.ai/api-manual/music-series/query-music-detail)
- [PoYo music webhook docs](https://docs.poyo.ai/api-manual/music-series/music-webhook)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON payloads and bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include PoYo model selection, request fields, payload summaries, task IDs, callback guidance, and result retrieval steps.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
