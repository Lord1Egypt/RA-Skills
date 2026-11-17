## Description:

Generates gothic portrait images from text prompts with dark lighting, Victorian styling, and optional reference-image style inheritance through the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omactiengartelle](https://clawhub.ai/user/omactiengartelle)

### License/Terms of Use:

MIT-0

## Use Case:

External users, creators, and developers use this skill to generate gothic or dark fantasy portrait images from prompts, with optional size selection and reference-image style inheritance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, reference image IDs, and the Neta token are sent to an external image service.

Mitigation: Install only if that data sharing is acceptable for the intended use case, and avoid sending sensitive prompts or reference identifiers.

Risk: Passing a real token on the command line can expose it through shell history or logs.

Mitigation: Avoid placing real tokens in reusable command examples or logs, and rotate any token that may already have been exposed.

Risk: Install and execution instructions rely on broad shell execution.

Mitigation: Prefer a pinned or ClawHub-managed install path and review the skill before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/omactiengartelle/skills/gothic-portrait-generator)
- [Neta access page](https://www.neta.art/open/)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text image URL with CLI status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token; accepts optional image size and reference image UUID parameters.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
