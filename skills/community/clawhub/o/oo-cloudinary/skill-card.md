## Description:

Cloudinary (cloudinary.com). Use this skill for ANY Cloudinary request — reading, creating, and updating data. Whenever a task involves Cloudinary, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to read and manage assets in a connected Cloudinary account through the oo CLI. It guides them through checking action schemas, submitting requests, and handling setup or connection errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs the agent to run downloaded installer code without a separate approval step; the installer and runtime were not verified.

Mitigation: Review and approve the CLI installation separately, prefer a verified pinned release, and retain confirmation before asset changes.

## Reference(s):

- [Cloudinary](https://cloudinary.com)
- [Cloudinary Image Upload API documentation](https://cloudinary.com/documentation/image_upload_api_reference)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Cloudinary skill release](https://clawhub.ai/oomol/skills/oo-cloudinary)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance]

**Output Format:** [Markdown with oo CLI commands and JSON request or response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requests use the connected Cloudinary account and action-specific schemas.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
