## Description:

Meitu Beauty helps an agent run Meitu's CLI to apply AI portrait beautification, including skin smoothing, whitening, and facial refinement, for single-person photos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meitu](https://clawhub.ai/user/meitu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to validate a single-person portrait photo, choose a natural or enhanced beautification strength, run the Meitu CLI, and deliver the processed image file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Portrait photos may be sent to Meitu for beautification.

Mitigation: Use the skill only when the user is comfortable sending the selected portrait photo to Meitu.

Risk: The skill requires Meitu API credentials and may read ~/.meitu/credentials.json.

Mitigation: Prefer environment variables or managed secrets, and grant credential-file access only when necessary.

Risk: CLI install and execution steps can be unsafe when filenames, paths, or URLs are untrusted.

Mitigation: Pin and verify the Meitu CLI version, and pass user-provided paths or URLs as safely escaped or structured arguments.

## Reference(s):


## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and a generated image file path or image URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces one beautified portrait image, preserving the original image format when supported.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and changelog mention 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
