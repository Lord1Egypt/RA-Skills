## Description:

Generates Pixar-style 3D animated character portraits from text prompts using the Neta AI image generation API and returns a direct image URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omactiengartelle](https://clawhub.ai/user/omactiengartelle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request stylized avatar or character portrait images from text prompts. It supports size selection and an optional reference image UUID for style inheritance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, reference identifiers, and the Neta API token are sent to an external image-generation API.

Mitigation: Install only when that external service use is acceptable, and avoid sending sensitive prompts or identifiers.

Risk: Passing the token directly on the command line can expose it through shell history or process listings.

Mitigation: Prefer a short-lived token or a wrapper that supplies the token without recording it in command history.

Risk: The security review notes that the advertised portrait-transform behavior is not tightly aligned with the implementation.

Mitigation: Treat the skill as text-prompt image generation unless a reference-image workflow has been separately verified.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/omactiengartelle/skills/pixar-portrait-generator)
- [Neta AI token setup](https://www.neta.art/open/)

## Skill Output:

**Output Type(s):** [text, shell commands]

**Output Format:** [Plain text image URL on stdout, with progress and errors on stderr.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token; optional size and reference image UUID inputs control the image request.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
