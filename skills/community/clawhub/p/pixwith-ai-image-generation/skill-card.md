## Description:

Helps agents use Pixwith through MCP to generate or edit images and create videos from text or reference images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tate-kt](https://clawhub.ai/user/tate-kt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to connect OpenClaw to Pixwith, discover current image and video models, configure requests, upload reference images when needed, and poll asynchronous generation tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, generation settings, credit checks, and uploaded reference images may be sent to Pixwith or its storage provider.

Mitigation: Avoid sensitive prompts or images unless the user is comfortable with Pixwith handling them, and use only the documented Pixwith endpoint.

Risk: Pixwith API keys are required for every request and can grant access to paid generation capacity.

Mitigation: Keep the API key private, use the documented Api-Key header, and direct users to replace placeholders with their own key only in their local MCP configuration.

Risk: Static model examples can become stale because Pixwith model availability and schemas are dynamic.

Mitigation: Call list_models and get_model_schema before generation, and treat the current input schema as authoritative for images, options, enum values, timing, and credits.

Risk: Video and higher-resolution image jobs can consume more credits or take longer than a quick model listing suggests.

Mitigation: Check get_credits before expensive jobs and stop rather than retrying automatically when credits are insufficient.

Risk: Generation tasks are asynchronous and may fail or still be processing when first checked.

Mitigation: Poll get_task_result until a terminal status and only rely on result URLs when the task status is completed.

## Reference(s):

- [Pixwith homepage](https://pixwith.ai)
- [Pixwith Service Contract](references/service-contract.md)
- [Current Model Snapshot](references/model-snapshot.md)
- [Text to Image Example](examples/text-to-image.md)
- [Image to Video Example](examples/image-to-video.md)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, API Calls]

**Output Format:** [Markdown with inline JSON examples and MCP tool-call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Pixwith MCP configuration snippets and generation-task polling instructions.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
