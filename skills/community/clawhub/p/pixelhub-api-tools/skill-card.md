## Description:

Use for Pixelhub API direct calls when users need image generation/editing, video generation/post-processing, or audio/music generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leik1000](https://clawhub.ai/user/leik1000)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to discover Pixelle/Pixelhub workflow tools, submit image, video, and audio generation tasks, and poll for task results through the bundled Python runner.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be exposed if users paste them into chat or write them into the runner source file.

Mitigation: Use the Pixelhub_API_KEY environment variable or another secret store, and do not commit or paste API keys into chat.

Risk: Prompts, media URLs, and task data are sent to the external Pixelle/Pixelhub service.

Mitigation: Use the skill only with data that is acceptable to send to Pixelle/Pixelhub.

Risk: Changing Pixelhub_BASE_URL or --base-url can redirect requests and credentials away from the intended service.

Mitigation: Keep the base URL set to the intended Pixelle HTTPS service unless the user has explicitly verified another endpoint.

## Reference(s):

- [Pixelle website](https://www.pixellelabs.com/)
- [Pixelle API keys](https://www.pixellelabs.com/user/api-keys)
- [ClawHub skill page](https://clawhub.ai/leik1000/skills/pixelhub-api-tools)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON runner output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The runner returns tool lists, task status, or completed task result payloads from the Pixelle/Pixelhub service.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
