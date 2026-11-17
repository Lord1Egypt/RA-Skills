## Description:

Helps agents prepare PoYo MiniMax Music 2.6 music-generation payloads, submit confirmed jobs, and explain status polling for vocal, lyrics-optimized, or instrumental tracks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when a user has chosen PoYo for MiniMax Music 2.6 music generation and needs request payloads, server-side curl commands, callback setup, or status polling guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local API-key exposure through command lines, shell tracing, logs, screenshots, or public files.

Mitigation: Keep POYO_API_KEY in a trusted server-side environment or secret manager, avoid shell tracing, and do not print authorization headers.

Risk: Payload files submitted through the skill are uploaded to PoYo and can contain private prompts, lyrics, callback URLs, task IDs, or generated audio URLs.

Mitigation: Review payloads before submission, avoid unnecessary sensitive content, and keep private prompts, lyrics, URLs, and task IDs out of logs unless policy allows it.

Risk: Unintended live API calls can send data to an external service.

Mitigation: Submit jobs only when the user explicitly asks, confirms the payload should be sent to PoYo, and provides a trusted server-side environment.

## Reference(s):

- [PoYo MiniMax Music 2.6 API Reference](references/api.md)
- [PoYo MiniMax Music 2.6 Model Page](https://poyo.ai/models/minimax-music-2-6)
- [PoYo MiniMax Music 2.6 API Docs](https://docs.poyo.ai/api-manual/music-series/minimax-music-2.6)
- [PoYo MiniMax Music 2.6 OpenAPI JSON](https://docs.poyo.ai/api-manual/music-series/minimax-music-2.6.json)
- [ClawHub Skill Page](https://clawhub.ai/coolhackboy/skills/poyo-minimax-music-2-6)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON payload examples and bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a PoYo task_id when the user explicitly confirms submission from a trusted shell.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
