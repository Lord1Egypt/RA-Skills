## Description:

Generates ecommerce model images from mannequin or dress-form clothing photos, with optional model and background references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and ecommerce operators use this skill to turn mannequin clothing photos into product display images showing a real model wearing the garment. It supports optional reference images for model identity and background style.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner verdict is suspicious because job JSON can supply Python script paths for execution.

Mitigation: Use only trusted job files and review script paths before running the workflow.

Risk: Local file inputs may become public once uploaded for downstream image or text generation.

Mitigation: Upload only files that are approved for public access and avoid private or sensitive images.

Risk: The skill handles API keys, SMS codes, and billing-related onboarding flows.

Mitigation: Run the skill in a trusted environment and avoid exposing credentials in shared logs or persisted documentation.

Risk: Custom LINKFOX gateway URLs could redirect requests, credentials, or media to an untrusted endpoint.

Mitigation: Do not set custom LINKFOX_* gateway URLs unless the endpoint is fully trusted.

## Reference(s):

- [Skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-expert-aigc-imagegen-mannequin-to-model)
- [Workflow reference](references/workflow.md)
- [Data fields reference](references/data-fields.md)
- [Image generation API reference](skills/linkfox-aigc-imagegen/references/api.md)
- [Text generation API reference](skills/linkfox-aigc-textgen/references/api.md)
- [File upload API reference](skills/linkfox-file-upload/references/api.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with JSON parameters and shell commands; successful runs produce local image file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces one mannequin-to-model image per run; image generation is mediated by text prompt generation and reference image URLs.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
