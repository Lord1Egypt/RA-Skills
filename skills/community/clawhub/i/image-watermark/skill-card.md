## Description:

Adds text watermarks to one or more PNG or JPG images with tiled, centered, or lower-right placement options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andyrenxu7255](https://clawhub.ai/user/andyrenxu7255)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to add readable text watermarks to submitted images while controlling placement, opacity, and approximate font sizing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images may contain sensitive information and the workflow returns processed results through WeCom.

Mitigation: Use the skill only with images suitable for the configured WeCom environment and retention policies.

Risk: The skill depends on Pillow and a Chinese font package being installed in the runtime environment.

Mitigation: Install dependencies from trusted, preferably pinned sources before processing images.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andyrenxu7255/skills/image-watermark)

## Skill Output:

**Output Type(s):** [Files, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance with Python code and generated PNG/JPG image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can process multiple images, preserve practical image quality, and return results individually or as a package.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact metadata remains 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
