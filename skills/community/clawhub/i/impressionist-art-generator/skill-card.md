## Description:

Generate impressionist-style images from text prompts using the Neta AI image generation API, with size options and optional reference-image style inheritance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blammectrappora](https://clawhub.ai/user/blammectrappora)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn text prompts into impressionist-style image URLs through the Neta API for art, education, reference, or print workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API tokens can be exposed when pasted directly into commands that are saved in shell history or logs.

Mitigation: Use a shell variable or another secret-management workflow, and avoid committing or sharing tokens.

Risk: Prompts, reference-image IDs, and the API token are sent to an external image-generation service.

Mitigation: Avoid submitting sensitive prompts or private reference identifiers unless the service is approved for that data.

Risk: The documented npx install command is mutable and should be reviewed before installation.

Mitigation: Prefer the ClawHub install path or a pinned, verified package source, and review the skill before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/blammectrappora/skills/impressionist-art-generator)
- [Neta API Token Access](https://www.neta.art/open/)
- [README](README.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown guidance with bash commands; runtime output is a direct image URL.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token; supports size selection and optional reference-image UUID style inheritance.]

## Skill Version(s):

1.0.0 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
