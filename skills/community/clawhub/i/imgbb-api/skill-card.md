## Description:

Upload images to ImgBB via local file, URL, or base64 and get shareable direct links, supporting batch uploads and optional expiration settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kexu9](https://clawhub.ai/user/kexu9)

### License/Terms of Use:


## Use Case:

Developers, engineers, and agent users use this skill to upload selected local images, image URLs, or base64 image data to ImgBB and return shareable links. It also supports batch uploads and optional image expiration settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be exposed if passed directly on the command line or stored without appropriate file permissions.

Mitigation: Prefer the IMGBB_API_KEY environment variable and restrict permissions on any ~/.imgbb_api_key file.

Risk: Uploaded files and remote URLs may become public or shareable through ImgBB links.

Mitigation: Upload only images intended for sharing and avoid sensitive or confidential content.

## Reference(s):

- [ClawHub ImgBB API skill page](https://clawhub.ai/kexu9/skills/imgbb-api)
- [ImgBB API documentation](https://api.imgbb.com/)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples, plain text status output, and optional JSON upload results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include public ImgBB direct image URLs, viewer URLs, thumbnail URLs, and per-file batch results.]

## Skill Version(s):

1.1.2 (source: server release metadata and target metadata; artifact frontmatter says 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
