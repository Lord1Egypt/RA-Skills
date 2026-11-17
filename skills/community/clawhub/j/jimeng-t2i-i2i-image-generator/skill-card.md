## Description:

Use Jimeng AI 4.0 (Volcengine) to generate images from text or image references, and optionally send results to Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tangc](https://clawhub.ai/user/tangc)

### License/Terms of Use:


## Use Case:

Developers and automation users use this skill to generate PNG image URLs from text prompts or reference images with Jimeng AI 4.0, with optional Feishu delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user prompts and optional reference image URLs to an external image-generation service.

Mitigation: Avoid sensitive prompts or reference images and review applicable data-sharing requirements before use.

Risk: Volcengine access keys are used by the local script and may be exposed if the host process list or shell history is not protected.

Mitigation: Use least-privilege Volcengine keys, keep credentials in environment variables, and run the skill only in trusted local environments.

Risk: The optional Feishu delivery path posts generated content to a local service on localhost:18789.

Mitigation: Use the Feishu target option only when the local service is trusted and the destination user ID has been verified.

Risk: Prompt and URL values are interpolated into JSON request bodies by shell script logic.

Mitigation: Review inputs before execution; the publisher should replace manual JSON construction with a real JSON encoder.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tangc/skills/jimeng-t2i-i2i-image-generator)
- [Volcengine Visual API endpoint](https://visual.volcengineapi.com)
- [Default image-to-image reference image](https://cdn.jsdelivr.net/gh/SumeLabs/clawra@main/assets/clawra.png)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with bash examples; runtime output is plain text image URLs and API status text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Volcengine credentials; generated images are PNG resources returned as URLs, with optional Feishu delivery through a local service.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
