## Description:

Picrd Image Hosting helps agents upload PNG, JPEG, WebP, and GIF images to picrd.com and return permanent, embeddable URLs without an account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[setdemos](https://clawhub.ai/user/setdemos)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and agents use this skill to upload screenshots, generated images, and diagrams for embedding in markdown, issues, pull requests, chats, and documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded images are hosted externally and unlisted links are shareable rather than private.

Mitigation: Upload only non-sensitive images and treat every returned page or image URL as accessible to anyone who has the link.

Risk: The delete URL is a one-time secret that cannot be recovered later.

Mitigation: Store the delete URL immediately when removal may be needed.

## Reference(s):

- [Picrd documentation](https://picrd.com/docs)
- [Picrd service](https://picrd.com)
- [ClawHub skill page](https://clawhub.ai/setdemos/skills/picrd-image-hosting)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl; uploads user-selected images to an external hosting service and returns shareable image, page, album, and delete URLs.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
