## Description:

Helps agents prepare and submit Kling 3.0 motion-control video generation jobs through the PoYo API using one reference image and one reference video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to build PoYo Kling 3.0 motion-control payloads, submit prepared JSON jobs, and guide polling or webhook follow-up for generated videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PoYo API keys could be exposed through browser code, public repositories, logs, screenshots, or chat output.

Mitigation: Keep POYO_API_KEY in a server-side environment variable or secret manager, and do not print or embed it in generated examples.

Risk: Private media URLs, prompts, or callback URLs may be sent to PoYo or a webhook receiver during a video-generation request.

Mitigation: Submit only inputs the user has reviewed and is willing to share with PoYo and the callback receiver.

Risk: A live submission can trigger an external async generation job from the prepared JSON payload.

Mitigation: Make live API calls only when the user explicitly asks to submit and has provided a trusted shell environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-kling-3-0-motion-control)
- [PoYo Kling 3.0 Motion Control model page](https://poyo.ai/models/kling-3-0-motion-control)
- [PoYo Kling 3.0 Motion Control API docs](https://docs.poyo.ai/api-manual/video-series/kling-3-0-motion-control)
- [Artifact API reference](references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON payloads and bash/curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include the model id, payload summary, API task_id, and polling or webhook next steps.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
