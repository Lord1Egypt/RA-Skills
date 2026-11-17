## Description:

Happy Horse video generation on PoYo / poyo.ai via the PoYo async generation API for text-to-video, image-to-video, reference-driven short video, video edit planning, task submission, polling, and webhook integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare PoYo Happy Horse video-generation payloads, choose text-to-video or source-media workflows, submit asynchronous jobs, and explain polling or webhook follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script uses POYO_API_KEY to authenticate to an external paid API, which can expose the key through unsafe environments, logs, or shell history.

Mitigation: Store POYO_API_KEY only in a server-side environment or secret manager, avoid echoing commands that include secrets, and scrub logs and screenshots before sharing.

Risk: The helper script forwards arbitrary payload files to PoYo, which can submit private prompts, private media URLs, callback URLs, or unintended paid jobs.

Mitigation: Use only trusted payload files, review request content before submission, validate the model and request schema, and make live API calls only after the user explicitly requests them.

## Reference(s):

- [PoYo Happy Horse API Reference](references/api.md)
- [PoYo Happy Horse model page](https://poyo.ai/models/happy-horse)
- [PoYo Happy Horse API docs](https://docs.poyo.ai/api-manual/video-series/happy-horse)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON payloads and optional bash or curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a returned task_id after an explicitly requested live submission; requires POYO_API_KEY for API calls.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
