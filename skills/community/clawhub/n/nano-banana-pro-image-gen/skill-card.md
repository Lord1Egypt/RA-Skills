## Description:

Generates and edits images from text prompts or reference images through API易's NanoBananaPro image service using Node.js or Python helpers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuchubuzai2018](https://clawhub.ai/user/wuchubuzai2018)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create image assets, social media visuals, marketing images, wallpapers, and edited variants from prompts or up to 14 input images. It is suited for workflows where prompts and selected input images may be sent to API易 and its upstream image provider.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and input images may be sent to API易/api.apiyi.com and an upstream image provider.

Mitigation: Use the skill only with prompts and images approved for third-party processing, and avoid confidential documents, secrets, private keys, or unrelated local paths.

Risk: Command templates may be unsafe if prompt text, filenames, API keys, or image paths are interpolated into a shell command.

Mitigation: Prefer environment-variable API keys and shell-free argument passing; when a shell is unavoidable, carefully quote and escape all user-controlled values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wuchubuzai2018/skills/nano-banana-pro-image-gen)
- [Publisher profile](https://clawhub.ai/user/wuchubuzai2018)
- [API易 service](https://api.apiyi.com/)
- [Common usage scenarios](artifact/references/scene.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Code, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands that generate PNG image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs image files to a caller-selected or timestamped path; supports text-to-image and image-editing modes, 10 aspect ratios, and 1K, 2K, or 4K resolution settings.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
