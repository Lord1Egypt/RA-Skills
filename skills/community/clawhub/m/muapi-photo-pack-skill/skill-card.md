## Description:

Generate a pack of professional or aesthetic photos from a single reference image while preserving the exact identity of the person.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anil-matcha](https://clawhub.ai/user/anil-matcha)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate themed photo packs from a provided face image, such as professional headshots, dating profiles, and stylized portraits, while prompting the image model to preserve identity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Face photos may be uploaded to an external image service.

Mitigation: Use only images the user is authorized and comfortable uploading, and disclose the external upload before execution.

Risk: Unsafe shell option handling can execute unintended commands when untrusted values are passed to script options such as --num.

Mitigation: Do not pass untrusted option values to the bundled shell script; validate numeric inputs before execution.

Risk: The --view behavior can download generated images and write files locally.

Mitigation: Use --view only when local downloads are expected and acceptable.

## Reference(s):

- [Photo Pack Generator on ClawHub](https://clawhub.ai/anil-matcha/skills/muapi-photo-pack-skill)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Files, Guidance]

**Output Format:** [Markdown with generated image links, optional JSON output, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save generated images locally when view/download behavior is enabled.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
