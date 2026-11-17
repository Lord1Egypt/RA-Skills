## Description:

Classic image manipulation with Python Pillow for resize, crop, composite, format conversion, watermarks, brightness and contrast adjustments, and web optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galbria](https://clawhub.ai/user/galbria)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to perform deterministic image processing tasks such as resizing, cropping, compositing, watermarking, format conversion, and web optimization. It is intended for transforming existing pixels, including post-processing AI-generated images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: URL loading and optional Bria API examples can perform network requests.

Mitigation: Use URL loading only with trusted public image sources, and avoid attacker-controlled, localhost, private-network, or cloud-metadata URLs.

Risk: The skill can be used alongside the separate bria-ai skill and examples rely on a Bria API key.

Mitigation: Review the bria-ai skill separately, pin or approve its version where supported, and keep API credentials out of prompts and generated outputs.

## Reference(s):

- [Image Utils code example](references/code-examples/image_utils.py)
- [Image Utils on ClawHub](https://clawhub.ai/galbria/skills/image-utils)
- [Bria AI companion skill](https://clawhub.ai/galbria/bria-ai)

## Skill Output:

**Output Type(s):** [code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.3.1 (source: ClawHub release metadata; artifact frontmatter reports 1.3.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
