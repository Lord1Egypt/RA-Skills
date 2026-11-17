## Description:

Generates e-commerce clothing imagery for single images or coordinated sets, including white-background, model, lifestyle, selling-point, A+ and size-chart images from clothing or model references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, marketing teams, and agents use this skill to turn apparel reference images and product intent into commercial e-commerce image-generation plans, prompts, and generated image deliverables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, image URLs, and account credentials are sent to LinkFox services.

Mitigation: Use the skill only when that third-party processing is acceptable, and disclose the data flow to users before generating commercial assets.

Risk: Credential setup may expose API access if keys are stored too broadly.

Mitigation: Use a scoped LINKFOX_AGENT_API_KEY for the session, avoid storing it in shell startup files, and avoid endpoint override environment variables during normal use.

Risk: Uploads can make local files publicly accessible.

Mitigation: Upload only files that are approved for public release and review local paths before invoking upload-dependent flows.

Risk: Pipeline jobs and state files can drive local script execution.

Mitigation: Run only job and state files created in the current trusted session, and inspect unexpected files before dispatch.

Risk: Unsafe or incorrect model-selection defaults can affect generated output quality and suitability.

Mitigation: Confirm provider, resolution, and quality choices before generation, then review outputs before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-expert-aigc-imagegen-cloth)
- [Skill definition](artifact/SKILL.md)
- [Runtime workflow index](artifact/references/runtime/00-index.md)
- [Delivery workflow](artifact/references/runtime/03-deliver.md)
- [Image generation API reference](artifact/skills/linkfox-aigc-imagegen/references/api.md)
- [Text generation API reference](artifact/skills/linkfox-aigc-textgen/references/api.md)
- [File upload API reference](artifact/skills/linkfox-file-upload/references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with JSON parameters, shell commands, and generated image file references.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local image files, public image URLs after upload, and markdown image links for completed tasks.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
