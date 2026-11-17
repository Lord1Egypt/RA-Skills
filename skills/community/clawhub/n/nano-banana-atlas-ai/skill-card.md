## Description:

Edit or combine images by applying styles or visual elements from one image to another while preserving identity, pose, and lighting with the AtlasCloud Nanobanana image-editing model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guilherme-funchal](https://clawhub.ai/user/guilherme-funchal)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to submit source and reference image URLs with editing prompts to AtlasCloud, then return a generated image URL. Typical tasks include changing clothes, combining visual styles, or applying elements from one image to another.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AtlasCloud API tokens may be exposed through persistent memory storage, command-line arguments, or a packaged environment file.

Mitigation: Use only short-lived, least-privilege tokens; remove or revoke any packaged API key; and update the skill to avoid persistent token memory and command-line secret passing before trusted use.

Risk: Prompts, source image URLs, generated image URLs, and job metadata are sent to AtlasCloud and may remain in local result files or logs.

Mitigation: Use the skill only with image URLs and prompts that are acceptable to share with AtlasCloud, and delete runtime result files and logs after use when they contain sensitive data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guilherme-funchal/skills/nano-banana-atlas-ai)
- [Publisher profile](https://clawhub.ai/user/guilherme-funchal)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON parameters, shell commands, and a generated image URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Submits prompts and image URLs to AtlasCloud, polls for completion, and writes the latest image URL and job metadata to local result files.]

## Skill Version(s):

1.0.1 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
