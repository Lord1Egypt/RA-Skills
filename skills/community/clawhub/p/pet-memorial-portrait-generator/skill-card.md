## Description:

Generates AI pet memorial portraits and remembrance keepsake imagery from written descriptions using the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blammectrappora](https://clawhub.ai/user/blammectrappora)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate pet memorial portrait images from text descriptions, with optional orientation and reference-style settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and tokens are sent to the Neta/Tales of AI external service.

Mitigation: Verify trust in the provider before use and avoid including sensitive personal details in prompts unless that sharing is acceptable.

Risk: The documented token flag can expose credentials through command history or process listings.

Mitigation: Use a safer token handling mechanism where available, such as an environment variable or a reviewed wrapper around the command.

Risk: Unversioned installation commands can pull code that differs from the reviewed release.

Mitigation: Prefer pinned or reviewed installation sources for deployments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/blammectrappora/skills/pet-memorial-portrait-generator)
- [Neta API token setup](https://www.neta.art/open/)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text image URL with command-line usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports portrait, landscape, square, and tall image sizes, plus an optional reference image UUID for style inheritance.]

## Skill Version(s):

1.0.0 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
