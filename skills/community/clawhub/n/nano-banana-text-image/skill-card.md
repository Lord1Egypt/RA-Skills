## Description:

Generates images from text prompts using the AtlasCloud Nanobanana 2 model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guilherme-funchal](https://clawhub.ai/user/guilherme-funchal)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate images from text prompts through AtlasCloud's Nanobanana 2 text-to-image model. It helps an agent prepare generation parameters, run the Node.js helper, and return the current image URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The AtlasCloud API token may be stored in agent memory or appear in command logs.

Mitigation: Use a short-lived or low-privilege token, avoid persistent memory storage, and rotate the token if it may have been exposed.

Risk: Image prompts are sent to AtlasCloud and may include sensitive private content.

Mitigation: Do not include secrets, personal data, or confidential material in prompts.

Risk: A stale image URL from a prior run could be reported instead of the current generated image.

Mitigation: Use only the IMAGE_URL line emitted by the current execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guilherme-funchal/skills/nano-banana-text-image)
- [AtlasCloud API endpoint used by the helper](https://api.atlascloud.ai/api/v1)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with inline bash and JSON; generated result is an image URL plus local JSON and text result files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Node.js runtime and an AtlasCloud API token.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence; artifact package metadata lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
