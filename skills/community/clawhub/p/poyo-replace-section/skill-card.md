## Description:

Replace a section of generated music on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `replace-section`, music section editing, infill_start_s, infill_end_s, task_id plus audio_id inputs, callbacks, and music detail retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare and submit PoYo Replace Section music-editing payloads, including source task identifiers, replacement time ranges, prompts, lyrics, callback configuration, and status retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials could be exposed if POYO_API_KEY or authorization headers are copied into client code, logs, repositories, screenshots, or chat output.

Mitigation: Keep POYO_API_KEY in server-side environment variables or a backend secret manager, and avoid logging raw authorization headers.

Risk: Private prompts, lyrics, task IDs, audio IDs, generated URLs, or callback URLs may contain sensitive project or user data.

Mitigation: Review payload JSON before submission and send private content to PoYo only when appropriate for the user's workflow and policy.

Risk: Submitting a malformed replacement range can edit the wrong section or fail the API request.

Mitigation: Confirm that infill_end_s is greater than infill_start_s and that the source task_id and audio_id match the intended completed track before live submission.

## Reference(s):

- [PoYo Replace Section API Reference](references/api.md)
- [PoYo Replace Section model page](https://poyo.ai/models/replace-section)
- [PoYo Replace Section API docs](https://docs.poyo.ai/api-manual/music-series/replace-section)
- [PoYo Replace Section OpenAPI JSON](https://docs.poyo.ai/api-manual/music-series/replace-section.json)
- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-replace-section)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON payload examples and bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include PoYo model id, source task and audio identifiers, replacement time range, payload summary, returned task id, and next-step status or webhook guidance.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
