## Description:

Creates Instagram-ready portrait images by overlaying titles, gradient treatments, optional numbered lists, quotes, and watermark text on a source photo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyduckler](https://clawhub.ai/user/psyduckler)

### License/Terms of Use:


## Use Case:

Developers and content-producing agents use this skill to turn user-supplied photos and post copy into 4:5 Instagram carousel, list, cover, or quote images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated images include the default tabiji.ai watermark unless the agent disables or replaces it.

Mitigation: Review the watermark setting before publishing and pass an empty or approved --watermark value when required.

Risk: The documented Pillow install command is unpinned, which can affect reproducibility across environments.

Mitigation: Use a virtual environment and pin the Pillow version for controlled or repeatable deployments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/psyduckler/skills/instagram-photo-text-overlay)

## Skill Output:

**Output Type(s):** [shell commands, configuration, files, text]

**Output Format:** [JPEG image file with terminal status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates a cropped 4:5 portrait image; style options are list, clean, and quote.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
