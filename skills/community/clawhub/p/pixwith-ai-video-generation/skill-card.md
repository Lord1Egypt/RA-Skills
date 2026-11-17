## Description:

AI video, image generation. 40+ models - Sora, Veo 3, Kling, Seedance, GPT Image, Hailuo, WAN. Text-to-video, image-to-video, text-to-image,image-to-image.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tate-kt](https://clawhub.ai/user/tate-kt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect OpenClaw to Pixwith through MCP, discover available media models, generate or edit images, create text-to-video and image-to-video tasks, and check credits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and uploaded reference images are sent to Pixwith as part of the skill's expected media-generation workflow.

Mitigation: Use the skill only when that data transfer is intended, and avoid submitting sensitive prompts or private images unless Pixwith is approved for that data.

Risk: The skill requires a Pixwith API key in the MCP configuration.

Mitigation: Use a Pixwith API key that is approved for the deployment, keep it in the MCP configuration rather than public text, and rotate it if exposed.

Risk: Model availability, schemas, credit costs, and task timing can change dynamically.

Mitigation: Call list_models and get_model_schema before generation, check credits before expensive jobs, and rebuild failed requests from the current schema.

## Reference(s):

- [Pixwith](https://pixwith.ai)
- [Pixwith API Keys](https://pixwith.ai/api)
- [Pixwith Pricing](https://pixwith.ai/pricing)
- [Pixwith Service Contract](references/service-contract.md)
- [Current Model Snapshot](references/model-snapshot.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with JSON configuration examples and tool-call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Pixwith MCP setup instructions, model-selection guidance, generation request payloads, polling guidance, and links to generated media results returned by Pixwith.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
