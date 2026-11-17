## Description:

Turn a local image file, or an image URL, into a public https link with one curl call. Use when you need a shareable URL for a screenshot, chart, generated image, or diagram, for example to send it in chat, embed it in a post, a PR, or an email. Works with no signup or API key (temporary link, 30 days); add PIXELVAULT_API_KEY for permanent links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[facundofarias](https://clawhub.ai/user/facundofarias)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agents use this skill to upload a local image or, with an API key, import an image from an HTTPS URL and share the resulting public link in messages, posts, or documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded images are public to anyone with the link and may expose secrets or personal information in screenshots.

Mitigation: Check images for secrets and personal information before uploading, and upload only images intended to be shared publicly.

Risk: The optional API key could be exposed or logged.

Mitigation: Protect PIXELVAULT_API_KEY and never print or log it.

Risk: Image retention terms may affect long-term link availability.

Mitigation: Verify current retention terms before relying on long-term availability.

## Reference(s):

- [PixelVault OpenClaw integration](https://pixelvault.dev/integrations/openclaw/)
- [PixelVault dashboard](https://pixelvault.dev/dashboard/)

## Skill Output:

**Output Type(s):** [Text, API calls, Shell commands, Guidance]

**Output Format:** [A public HTTPS image URL, with JSON response examples and inline curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Links may be temporary for 30 days or permanent with an API key; image resizing options depend on upload type and key.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
