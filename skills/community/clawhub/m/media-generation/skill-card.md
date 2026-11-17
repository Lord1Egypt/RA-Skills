## Description:

Generates and edits images, creates short videos, supports inpainting, outpainting, reference-image workflows, batch jobs, and retrieval of returned media.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lijiazhen0623](https://clawhub.ai/user/lijiazhen0623)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to route AI media requests to configured providers, generate or edit images and short videos, and collect downloaded outputs under predictable media directories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Provider-directed video polling and media downloads may contact unintended hosts or expose API keys.

Mitigation: Use trusted media providers, restrict network access where possible, and validate polling and download URLs against approved HTTPS provider or CDN origins before execution.

Risk: Sensitive prompts or private images can be sent to external media providers and remain in local media, mask, or batch-summary files.

Mitigation: Use only approved providers for sensitive work and clean tmp/images, tmp/videos, masks, and batch summaries after sensitive jobs.

## Reference(s):

- [Model Capabilities](references/model-capabilities.md)
- [Reference-Image Workflow](references/reference-image-workflow.md)
- [Batch Workflows](references/batch-workflows.md)
- [ClawHub Skill Page](https://clawhub.ai/lijiazhen0623/skills/media-generation)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with shell commands and generated media file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated images are saved under tmp/images/ and videos under tmp/videos/; batch runs may emit JSON summaries.]

## Skill Version(s):

2.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
