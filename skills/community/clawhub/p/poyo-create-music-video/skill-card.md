## Description:

Create music videos on PoYo by preparing and optionally submitting create-music-video API payloads for an existing music task and audio track.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when a user has selected PoYo for a music-video workflow and needs a request payload, server-side curl command, callback setup, or status retrieval for a completed music task and audio track.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can submit jobs to PoYo and may expose sensitive workflow data if payloads, task IDs, callback URLs, media URLs, or authorization headers are logged or shared.

Mitigation: Use it only for intended PoYo submissions, keep POYO_API_KEY server-side, review the JSON payload before execution, and avoid placing private identifiers, URLs, or headers in logs or chat.

Risk: The submit script depends on a trusted shell environment with curl and POYO_API_KEY configured.

Mitigation: Run the script only from a trusted server-side environment after confirming curl is available and POYO_API_KEY is loaded from a secret manager or environment variable.

## Reference(s):

- [PoYo Create Music Video model page](https://poyo.ai/models/create-music-video)
- [PoYo Create Music Video API docs](https://docs.poyo.ai/api-manual/music-series/create-music-video)
- [PoYo Create Music Video OpenAPI JSON](https://docs.poyo.ai/api-manual/music-series/create-music-video.json)
- [PoYo API key page](https://poyo.ai/dashboard/api-key)
- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-create-music-video)
- [Publisher profile](https://clawhub.ai/user/coolhackboy)
- [Local API reference](references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON payloads and bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a returned task_id when the user explicitly asks to submit a request from a trusted server-side environment.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
