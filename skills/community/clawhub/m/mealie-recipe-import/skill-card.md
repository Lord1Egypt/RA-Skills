## Description:

Import recipes into a self-hosted Mealie instance from a photo, text, or URL, with AI ingredient parsing and cover image upload.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maikimolto](https://clawhub.ai/user/maikimolto)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to convert recipe photos, pasted recipe text, or recipe URLs into structured recipes in a self-hosted Mealie instance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a long-lived Mealie API token that can create and modify recipe data, and documented HTTP examples could expose the token over plaintext transport.

Mitigation: Use HTTPS for MEALIE_URL, prefer a dedicated revocable token with the least permissions available, avoid exposing the token in shared logs or shell history, and rotate any token previously used over plaintext HTTP.

Risk: The helper can create or modify recipes, foods, units, metadata, and cover images in the target Mealie instance.

Mitigation: Review the job file and target MEALIE_URL before execution, then verify the created recipe and uploaded image after the run.

## Reference(s):

- [Mealie](https://mealie.io)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Mealie API requests and job-file guidance for creating, updating, uploading images to, and verifying recipes.]

## Skill Version(s):

1.0.0 (source: package.json and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
