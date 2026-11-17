## Description:

Send a photo to Mixtiles for ordering wall tiles. Use when a user forwards/sends a photo and wants to order it as a Mixtile, add it to their Mixtiles cart, or says "mixtile this", "make this a tile", or similar. Also handles image URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[saharcarmel](https://clawhub.ai/user/saharcarmel)

### License/Terms of Use:


## Use Case:

External users use this skill to turn one or more photos or image URLs into a Mixtiles cart link for customization and ordering. Agents use it when a user explicitly asks to add a photo to a Mixtiles cart or uses similar intent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Photos are uploaded to Cloudinary and sent to Mixtiles, which can expose personal or sensitive images.

Mitigation: Use only images the user explicitly wants to upload; avoid sensitive images and confirm user intent before running the script.

Risk: The script can fetch arbitrary image URLs, creating privacy and network-fetch risks.

Mitigation: Avoid private or internal URLs and require stronger URL-fetch protections, image validation, and download size limits before deployment.

Risk: No license is provided in server evidence or artifact files.

Mitigation: Confirm license and terms before commercial distribution or installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/saharcarmel/skills/mixtiles-it)
- [Mixtiles photo order page](https://www.mixtiles.com/photos)
- [Cloudinary image upload endpoint](https://api.cloudinary.com/v1_1/{cloud}/image/upload)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text cart URL with optional Markdown and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use local file paths or public image URLs and optional size or batch arguments.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
