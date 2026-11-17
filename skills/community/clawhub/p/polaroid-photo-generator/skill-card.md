## Description:

Generates retro Polaroid-style images from text prompts using the Neta image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blammectrappora](https://clawhub.ai/user/blammectrappora)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create nostalgic instant-film images from scene or portrait descriptions. The skill can generate square, portrait, landscape, or tall outputs and optionally use a reference image UUID for style inheritance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and the Neta token are sent to the Neta/talesofai image generation service.

Mitigation: Use the skill only with data appropriate for that service, avoid sensitive personal or business details in prompts, and pass tokens from a protected environment variable where possible.

Risk: Installing an unpinned release can expose users to later changes they have not reviewed.

Mitigation: Pin the install source to a reviewed version or commit when using the skill in controlled environments.

## Reference(s):

- [Neta API token and service page](https://www.neta.art/open/)
- [Polaroid Photo Generator on ClawHub](https://clawhub.ai/blammectrappora/skills/polaroid-photo-generator)

## Skill Output:

**Output Type(s):** [Text, Shell commands]

**Output Format:** [Plain text image URL printed to stdout, with progress and errors on stderr]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta token supplied with --token; supports square, portrait, landscape, and tall sizes plus an optional reference image UUID.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
