## Description:

Helps agents prepare, submit, and follow up on PoYo Wan Animate video generation jobs for character animation and character replacement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to build PoYo Wan Animate requests, choose the character replacement or character animation workflow, prepare payloads, submit trusted async jobs, and explain polling or webhook follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send source video URLs, target image URLs, prompt-related data, and optional callback URLs to PoYo.

Mitigation: Use it only for intended PoYo Wan Animate workflows, avoid private likenesses or private media unless PoYo and the callback receiver are trusted, and keep sensitive URLs out of logs and screenshots.

Risk: The workflow requires a PoYo API key.

Mitigation: Store POYO_API_KEY in a server-side environment variable or secret manager and never expose it in browser code, public repositories, logs, screenshots, or chat output.

Risk: Submitting a payload starts an external asynchronous generation job.

Mitigation: Make live API calls only after explicit user request from a trusted shell, save the returned task_id, and use polling or a trusted webhook for follow-up.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-wan-animate)
- [PoYo Wan Animate model page](https://poyo.ai/models/wan-animate)
- [PoYo Wan Animate API docs](https://docs.poyo.ai/api-manual/video-series/wan-animate)
- [Local API reference](references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON payload examples and bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can submit prepared JSON payloads to PoYo when the user requests execution and provides a trusted server-side POYO_API_KEY environment.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
