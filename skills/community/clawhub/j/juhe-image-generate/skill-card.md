## Description:

Generates AI images from text prompts using Juhe's text-to-image API, supports common aspect ratios, and can save generated images locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juhemcp](https://clawhub.ai/user/juhemcp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn text prompts into images through Juhe's API, select aspect ratios, and choose whether to download generated images or return temporary image links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and the Juhe API key are sent to Juhe's image API.

Mitigation: Use a platform secret store or environment variable for JUHE_IMAGE_KEY, avoid passing keys with --key, and avoid committing scripts/.env.

Risk: The skill can download provider-returned image URLs to local storage.

Mitigation: Use --no-download or set a contained output directory when automatic downloads are not desired.

## Reference(s):

- [ClawHub skill release: juhe-image-generate](https://clawhub.ai/juhemcp/skills/juhe-image-generate)
- [Juhe AI Image Generation API documentation](https://www.juhe.cn/docs/api/id/824)
- [Juhe text-to-image API endpoint](https://gpt.juhe.cn/text2image/generate)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell commands, local file paths, and provider image URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and JUHE_IMAGE_KEY; provider image links are temporary and documented as valid for 24 hours.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
