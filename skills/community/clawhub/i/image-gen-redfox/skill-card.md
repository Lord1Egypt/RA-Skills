## Description:

AI image generator based on gpt-image-2 that supports text-to-image and image-to-image generation with PNG, JPEG, and WebP outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

External users, designers, content marketers, and e-commerce operators use this skill to generate or edit image assets from natural-language prompts and optional reference images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The RedFox API key can be provided through an environment variable, command-line argument, or plaintext config file, which can expose paid or sensitive credentials more broadly than expected.

Mitigation: Prefer an environment variable or credential manager, avoid the plaintext config-file option, and rotate the key if exposure is suspected.

Risk: Prompts and reference images are sent to RedFox for generation or editing.

Mitigation: Do not submit private images, confidential prompts, or regulated data unless the user is comfortable sharing them with RedFox.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/image-gen-redfox)
- [RedFox API key settings](https://redfox.hk/settings/api-keys?source=clawhub)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [CLI text output, task IDs, and generated image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Downloads generated images to a local output directory unless submit-only mode is used; can return a task ID for later polling.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
