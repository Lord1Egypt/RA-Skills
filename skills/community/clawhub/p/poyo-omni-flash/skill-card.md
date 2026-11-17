## Description:

Poyo Omni Flash helps agents prepare and submit PoYo Omni Flash video generation jobs for text-to-video, image-to-video, three-image reference fusion, and video-input workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to prepare PoYo Omni Flash video generation payloads, submit reviewed asynchronous jobs, and explain polling or webhook follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: POYO_API_KEY could be exposed if placed in browser code, logs, public repositories, screenshots, or chat output.

Mitigation: Keep POYO_API_KEY in server-side environment variables or a backend secret manager, and avoid echoing it in generated examples or command output.

Risk: Private prompts, source media URLs, or callback URLs may be shared with PoYo or the callback receiver during submission.

Mitigation: Submit sensitive prompts, media, and callback URLs only when the user explicitly trusts PoYo and the receiver.

Risk: A live API call could submit an unintended job or incur cost if a payload is not reviewed first.

Mitigation: Make live calls only after the user explicitly requests submission from a trusted shell and the payload JSON has been reviewed.

Risk: Model-specific options can change over time, causing invalid or unexpected requests.

Mitigation: Verify current field support in the PoYo docs before relying on resolution, duration, aspect ratio, image, or video options.

## Reference(s):

- [PoYo Omni Flash API Reference](references/api.md)
- [PoYo Omni Flash model page](https://poyo.ai/models/omni-flash)
- [PoYo Omni Flash API docs](https://docs.poyo.ai/api-manual/video-series/omni-flash)
- [PoYo API key page](https://poyo.ai/dashboard/api-key)
- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-omni-flash)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON payloads and bash/curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a returned task_id and polling or webhook next steps after an explicit submission.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
