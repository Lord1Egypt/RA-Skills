## Description:

Jiuma AI image editing uses the Jiuma AI API to edit existing images from text prompts and supports fusion editing with up to three input images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dddcn1](https://clawhub.ai/user/dddcn1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit image-editing or multi-image fusion jobs to Jiuma AI, then check task status and retrieve the resulting image URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uploads input images and prompts to Jiuma's cloud service.

Mitigation: Use it only for images and prompts that are acceptable to send to a third party; avoid sensitive photos, confidential work, and regulated data.

Risk: The login flow saves a reusable Jiuma API key on the local filesystem.

Mitigation: Treat the saved key as a local secret and delete or permission-harden the .jiuma key file after use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dddcn1/skills/jiuma-free-image-edit)
- [Publisher Profile](https://clawhub.ai/user/dddcn1)
- [Login and API Key Documentation](artifact/LOGIN.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON responses and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces task IDs, task status messages, image result URLs, and login/API-key setup guidance.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
