## Description:

Generates mature (18+) creative images and image edits through Atlas Cloud models such as Wan 2.6, Seedream, and Wan 2.5 using an ATLASCLOUD_API_KEY.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xixihhhh](https://clawhub.ai/user/xixihhhh)

### License/Terms of Use:

MIT-0

## Use Case:

External adult users and creative professionals use this skill to generate or edit mature image assets for lawful 18+ artistic and professional projects such as figure drawing, fashion photography, fine art, and mature illustration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A broad paid Atlas Cloud API key can bill the user's account and is not scoped to this skill.

Mitigation: Use a dedicated low-balance key, monitor account usage, and revoke the key when it is no longer needed.

Risk: Prompts and edited source images are sent to Atlas Cloud for generation.

Mitigation: Avoid private, identifying, or sensitive images and prompts unless the user intentionally wants to upload them.

Risk: The script downloads provider-returned output URLs without validating the downloaded content.

Mitigation: Treat downloaded outputs as untrusted files and review or sandbox them until download validation is fixed.

Risk: The skill is intended for mature image generation.

Mitigation: Confirm the user is 18 or older and that the request is for lawful adult creative work before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xixihhhh/skills/nsfw-image)
- [Atlas Cloud](https://www.atlascloud.ai)
- [Atlas Cloud API endpoint](https://api.atlascloud.ai/api/v1)

## Skill Output:

**Output Type(s):** [Files, Shell commands, API Calls, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with shell commands and generated image file paths or provider URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ATLASCLOUD_API_KEY; prompts and optional source images are sent to Atlas Cloud and generated outputs are downloaded from provider-returned URLs.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
