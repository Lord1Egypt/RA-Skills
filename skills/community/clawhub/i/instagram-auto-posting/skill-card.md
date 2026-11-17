## Description:

Automates creation and direct publishing of promotional images to Instagram Business accounts using the Meta Graph API, Cloudinary uploads, and user-provided credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pawanshekhawat](https://clawhub.ai/user/pawanshekhawat)

### License/Terms of Use:

MIT-0

## Use Case:

External users, business owners, marketers, and developers use this skill to create promotional images, optionally extract public business details from a user-provided website, upload images to Cloudinary, and publish them to an Instagram Business account through the Meta Graph API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish content directly to an Instagram Business account using user-provided credentials.

Mitigation: Use least-privilege Meta tokens, start with a test account, and review generated images and captions before running the post command.

Risk: The optional scraping step makes outbound requests to user-provided URLs and may extract public contact details.

Mitigation: Only provide public website URLs and avoid internal or private URLs; the artifact documents DNS, private-IP, scheme, TLS, and redirect controls.

Risk: Uploaded images become publicly hosted through Cloudinary before Instagram publishing.

Mitigation: Use signed or restricted Cloudinary upload presets and avoid uploading private or sensitive creative assets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pawanshekhawat/skills/instagram-auto-posting)
- [Meta Graph API Explorer](https://developers.facebook.com/tools/explorer/)
- [Cloudinary](https://cloudinary.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; runtime outputs include PNG image files, Cloudinary URLs, and Instagram post URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided Meta Graph API and Cloudinary credentials; generated promotional images are 1080x1350 PNG files.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
