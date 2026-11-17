## Description:

Generates and edits images through Picnow's api.letmego.top service with 1K, 2K, and 4K quality options and square, landscape, or portrait aspect ratios.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeekchen](https://clawhub.ai/user/jeekchen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent to create product images, banners, posters, social visuals, thumbnails, and image-to-image edits through the Picnow API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reference-image generation can upload any readable local file passed through --ref to a third-party API.

Mitigation: Use only prompts and reference images that are appropriate to send to api.letmego.top, avoid arbitrary local paths, and confirm reference files before execution.

Risk: The skill requires an API token for the third-party Picnow service.

Mitigation: Store LETMEGO_API_KEY in a secret manager or temporary environment variable and avoid exposing it in command history, logs, or shared files.

## Reference(s):

- [Picnow install and usage documentation](https://picnow.letmego.top/skills)
- [Picnow API service](https://api.letmego.top)
- [ClawHub release page](https://clawhub.ai/jeekchen/skills/picnow)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON URL output from the generation script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generation script prints a single JSON object containing generated image URLs.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
