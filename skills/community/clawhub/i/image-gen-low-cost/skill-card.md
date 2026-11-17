## Description:

Image Gen Low Cost is a command-line skill for low-cost AI image generation and image editing through OpenAI-compatible API endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[enihsago](https://clawhub.ai/user/enihsago)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to generate images from text prompts, edit images from URLs, choose model aliases, configure an API token, and save or print generated image outputs from a CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, image URLs, and bearer tokens may be sent to arbitrary or unsafe API endpoints.

Mitigation: Use a dedicated IMGEN_TOKEN, configure only trusted HTTPS IMGEN_API_URL endpoints, and avoid sensitive prompts or private/internal image URLs.

Risk: The skill can fall back to OPENAI_API_KEY and can store API tokens locally for CLI use.

Mitigation: Prefer a scoped token dedicated to this skill and review local token storage before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/enihsago/skills/image-gen-low-cost)
- [Publisher profile](https://clawhub.ai/user/enihsago)
- [Default API registration page](https://api.laozhang.ai/register/?aff_code=lfa0)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files, guidance]

**Output Format:** [CLI text output, image URLs, data URLs, and PNG files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saves images to generated-images/ by default; --no-save prints URLs or data URLs instead.]

## Skill Version(s):

1.0.5 (source: server release evidence and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
