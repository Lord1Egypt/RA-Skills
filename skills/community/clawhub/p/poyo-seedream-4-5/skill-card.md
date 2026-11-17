## Description:

Seedream 4.5 image generation and editing on PoYo via the PoYo generation API, covering standard generation, image editing, 2K or 4K output, multi-reference editing, and higher image counts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare and submit PoYo Seedream 4.5 image generation or image editing requests, including prompts, reference image URLs, output size, image count, and follow-up task polling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, reference image URLs, callback URLs, and related task metadata are sent to PoYo.

Mitigation: Use the skill only when sending that data to PoYo is acceptable, and avoid submitting sensitive prompts, private image URLs, or callback endpoints that should not leave the deployment environment.

Risk: The helper script can receive an API key as a command-line argument.

Mitigation: Set POYO_API_KEY through a protected environment or secret manager instead of passing the key on the command line; rotate any key that was previously exposed this way.

Risk: The security verdict is suspicious and requires review before installation.

Mitigation: Review the skill before deployment and confirm the data-sharing behavior, credential handling, and PoYo API usage match the intended environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/coolhackboy/skills/poyo-seedream-4-5)
- [PoYo Seedream 4.5 Model Page](https://poyo.ai/models/seedream-4-5-api)
- [PoYo Seedream 4.5 API Documentation](https://docs.poyo.ai/api-manual/image-series/seedream-4-5)
- [PoYo Seedream 4.5 OpenAPI JSON](https://docs.poyo.ai/api-manual/image-series/seedream-4-5.json)
- [PoYo Task Status Documentation](https://docs.poyo.ai/api-manual/task-management/status)
- [Local API Reference](artifact/references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON payload examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include selected model id, payload summary, reference-image usage, returned task_id, and polling or webhook next steps.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
