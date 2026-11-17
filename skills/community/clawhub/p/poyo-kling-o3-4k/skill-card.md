## Description:

Helps agents prepare and submit PoYo Kling O3 4K video generation requests, including text-to-video, image-to-video, reference-to-video, multi-shot payloads, polling, and webhook guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare PoYo Kling O3 4K video generation payloads, submit trusted JSON requests, and guide status polling or webhook follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: POYO_API_KEY could be exposed through browser code, public repositories, logs, screenshots, or chat output.

Mitigation: Keep POYO_API_KEY in server-side environment variables or a backend secret manager, and avoid echoing it in generated commands or responses.

Risk: Private prompts, source media URLs, videos, or callback URLs may be shared with PoYo or a callback receiver during task submission.

Mitigation: Submit only content the user is comfortable sharing with PoYo and the callback receiver, and review payload JSON before live submission.

Risk: Prepared payloads can trigger live PoYo generation jobs when executed from a trusted shell.

Mitigation: Require explicit user intent before running the submit script or curl request, and report the returned task_id for follow-up polling.

## Reference(s):

- [PoYo Kling O3 API model page](https://poyo.ai/models/kling-o3-api)
- [PoYo Kling O3 4K API documentation](https://docs.poyo.ai/api-manual/video-series/kling-o3-4k)
- [PoYo API key page](https://poyo.ai/dashboard/api-key)
- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-kling-o3-4k)
- [Bundled API reference](references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON payloads and curl or bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit live PoYo API requests only after explicit user approval and with POYO_API_KEY set.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
