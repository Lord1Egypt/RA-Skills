## Description:

Upload images to ImgBB through an OOMOL-connected account, using a public URL or Base64 content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users can upload an image to ImgBB through their connected OOMOL account. The skill returns hosted image metadata for the uploaded image.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: If the oo CLI is missing, setup guidance may invoke a remote installer without a separate approval step.

Mitigation: Review the setup instructions and install a verified CLI release yourself before using the skill.

Risk: Using the connected ImgBB integration entrusts OOMOL with the connection, and approved images pass through that service.

Mitigation: Connect only an account you trust and approve uploads only for the intended image.

## Reference(s):

- [ImgBB](https://imgbb.com)
- [ImgBB API documentation](https://api.imgbb.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Shell commands with JSON input and JSON response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uploads use a public image URL or Base64 content; the response includes hosted image metadata.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
