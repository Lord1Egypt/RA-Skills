## Description:

Use PoYo AI Flux 2 through the PoYo generate-submit endpoint to prepare payloads, submit media generation or editing jobs, and track task status for the Flux 2 model family.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to build PoYo-compatible Flux 2 requests, choose the right model variant, submit authenticated jobs, and report the returned task identifier for follow-up polling or callback handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The PoYo API key may be exposed through command-line or process arguments if passed directly to the helper script.

Mitigation: Use POYO_API_KEY from the environment, avoid passing secrets on the command line, and rotate any key that may already have been exposed.

Risk: Prompts, image URLs, callback URLs, and generated media requests are sent to PoYo and may contain confidential information.

Mitigation: Review payloads before submission, avoid sensitive content unless approved for PoYo processing, and use approved callback endpoints.

Risk: The helper script can expose the full request payload through process arguments while submitting jobs.

Mitigation: Prefer non-sensitive payloads, keep local execution environments controlled, and review requests before using the shell helper.

## Reference(s):

- [PoYo Flux 2 model page](https://poyo.ai/models/flux-2)
- [PoYo Flux 2 API docs](https://docs.poyo.ai/api-manual/image-series/flux-2)
- [PoYo Flux 2 OpenAPI JSON](https://docs.poyo.ai/api-manual/image-series/flux-2.json)
- [PoYo task status docs](https://docs.poyo.ai/api-manual/task-management/status)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON payloads and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include the selected model id, request parameters, reference-image usage, returned task_id, and next-step polling or webhook guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
