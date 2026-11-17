## Description:

Seedance 2 video generation on PoYo via the PoYo generate-submit API for text-to-video, first/last-frame image-to-video, and multimodal reference-to-video workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative automation agents use this skill to prepare PoYo Seedance 2 video-generation requests, choose compatible model parameters, submit jobs, and track the returned task identifier for polling or callback workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shell helper can accept the PoYo API key as a command-line argument, which may expose credentials through shell history or process listings.

Mitigation: Set POYO_API_KEY in a protected environment variable and avoid passing the API key as a command-line argument.

Risk: Prompts, media URLs, callback URLs, and generation parameters are sent to PoYo for processing.

Mitigation: Use the skill only for content approved for PoYo processing, and avoid submitting sensitive or regulated data unless that processing is authorized.

## Reference(s):

- [PoYo Seedance 2 model page](https://poyo.ai/models/seedance-2)
- [PoYo Seedance 2 API docs](https://docs.poyo.ai/api-manual/video-series/seedance-2)
- [PoYo task status docs](https://docs.poyo.ai/api-manual/task-management/status)
- [PoYo Seedance 2 OpenAPI JSON](https://docs.poyo.ai/api-manual/video-series/seedance-2.json)
- [Local PoYo Seedance 2 API reference](artifact/references/api.md)
- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-seedance-2)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON payload examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include model choice, workflow type, payload summary, generated-audio and seed settings, returned task_id, and polling or callback next steps.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
