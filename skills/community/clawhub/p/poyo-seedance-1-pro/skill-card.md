## Description:

Seedance 1.0 Pro video generation on PoYo via the PoYo generate-submit API for text-to-video, image-to-video, task submission, polling, and webhook guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare and submit reviewed PoYo Seedance 1.0 Pro video-generation payloads, then explain task polling or webhook follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reviewed payloads are sent to PoYo and can contain prompts, source image URLs, callback URLs, and generation settings.

Mitigation: Review payloads before submission and do not include confidential prompts, personal data, internal-only URLs, proprietary media, or private callback URLs unless the user accepts PoYo as the external processor.

Risk: The PoYo API key could be exposed if copied into browser code, logs, repositories, screenshots, or chat output.

Mitigation: Keep POYO_API_KEY in a server-side environment variable or backend secret manager and send it only as an Authorization header.

Risk: A live API request can create an external video-generation task.

Mitigation: Submit only user-reviewed payload JSON after an explicit user request from a trusted shell environment.

## Reference(s):

- [PoYo Seedance 1 Pro model page](https://poyo.ai/models/seedance-1-pro)
- [PoYo Seedance 1.0 Pro API docs](https://docs.poyo.ai/api-manual/video-series/seedance-1.0-pro)
- [Local PoYo Seedance API reference](references/api.md)
- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-seedance-1-pro)

## Skill Output:

**Output Type(s):** [Guidance, JSON payloads, Shell commands, API calls, Configuration]

**Output Format:** [Markdown guidance with JSON payloads and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a returned task_id after an explicit user-approved submission.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
