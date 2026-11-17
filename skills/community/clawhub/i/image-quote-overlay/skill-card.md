## Description:

Creates social-media quote images by applying text and a gradient overlay to a random JPG from a configured local photo folder.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quoc-modoro](https://clawhub.ai/user/quoc-modoro)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content automation users use this skill to generate branded quote images for LinkedIn, X, Facebook, WordPress, or downstream posting workflows from local JPG photos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads JPG files from the configured local photo folder, which may include sensitive personal images.

Mitigation: Point PICS_DIR at a dedicated folder containing only images intended for generated quote overlays.

Risk: Generated images may be reused by social-media posting workflows before a human reviews the final visual.

Mitigation: Review each generated image before upload, scheduling, or publication by another skill.

Risk: Default and intermediate file paths may use shared temporary directories.

Mitigation: Choose a private output directory for generated images and avoid shared temporary paths for sensitive content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/quoc-modoro/skills/image-quote-overlay)
- [README](artifact/README.md)
- [Usage examples](artifact/examples/README.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell command examples; runtime output is plain text plus generated PNG image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ImageMagick, Bash, configured JPG input photos, and available local fonts.]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
