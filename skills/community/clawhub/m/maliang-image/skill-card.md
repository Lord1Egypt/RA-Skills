## Description:

Maliang Image generates images from text prompts or edits user-provided images using Google Gemini through the Maliang API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xexojay](https://clawhub.ai/user/xexojay)

### License/Terms of Use:


## Use Case:

External users and developers use the skill to generate new images from text prompts or edit user-provided images through the Maliang API. The skill guides an agent through account provisioning, request submission, result polling, balance checks, and delivery of the generated image URL or saved file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, selected images, and billing or account metadata are sent to nano.djdog.ai.

Mitigation: Install only when this data sharing is acceptable, avoid private or sensitive inputs, and prefer explicitly selected local image attachments.

Risk: The skill uses network and shell-command workflows that require review before installation.

Mitigation: Review and scan the skill before deployment, and construct requests safely rather than relying on direct shell placeholder substitution.

Risk: The skill auto-provisions an API key and stores it in the local environment.

Mitigation: Confirm account provisioning, API-key storage, and revocation expectations before first use.

## Reference(s):

- [Maliang API Homepage](https://nano.djdog.ai)
- [ClawHub Skill Page](https://clawhub.ai/xexojay/skills/maliang-image)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, API Calls, Files, Guidance]

**Output Format:** [Markdown status text with an image URL or local file path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns only API-provided task IDs and image URLs; may save base64 image output to a local file when no URL is returned.]

## Skill Version(s):

1.1.1 (source: server release metadata; artifact frontmatter lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
