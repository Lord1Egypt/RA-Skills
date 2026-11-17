## Description:

Create movie posters, film posters, cinema artwork, event posters, fan-made film posters, and theatrical promotional art from text prompts via the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omactiengartelle](https://clawhub.ai/user/omactiengartelle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate movie-poster-style image outputs from text prompts, with optional size selection and reference-image style inheritance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Poster prompts, optional reference image identifiers, and the Neta API token are sent to Neta's service.

Mitigation: Use the skill only when that data sharing is acceptable, and avoid prompts or references containing confidential material.

Risk: Passing the API token directly on the command line can expose it through shared terminal history or recordings.

Mitigation: Avoid running token-bearing commands in shared shells or recorded sessions, and rotate the token if exposure is possible.

Risk: Generated poster imagery may be unsuitable for a specific brand, audience, or rights-sensitive use case.

Mitigation: Review generated images before publication and apply the user's content, branding, and rights policies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/omactiengartelle/skills/movie-poster-generator)
- [Neta API token setup](https://www.neta.art/open/)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text image URL with command-line status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token; supports square, portrait, landscape, and tall image size presets plus an optional reference image UUID.]

## Skill Version(s):

1.0.1 (source: evidence release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
