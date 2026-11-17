## Description:

Build, refine, and package sellable AI persona/prompt products such as companion personas, roleplay personas, prompt packs, and style bundles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaonizhou-crypto](https://clawhub.ai/user/xiaonizhou-crypto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and operators use this skill to turn rough persona ideas into structured prompt-pack products with system prompts, persona specs, examples, configuration, and buyer-facing documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The packaged helper script expects template files that are not present in the artifact, so it may fail if run as-is.

Mitigation: Supply the referenced templates before using the script, or generate the persona-pack files manually from the documented structure.

Risk: Persona products inspired by real people can create identity confusion or misleading clone claims.

Mitigation: Use public-trait abstractions, avoid names or identity claims, and review the generated pack against the safety-positioning guidance before release.

Risk: Generated prompt-pack files can contain incorrect or unsuitable positioning for a target platform or audience.

Mitigation: Review generated Markdown and JSON outputs before publication, and run the helper script in a fresh output directory.

## Reference(s):

- [Persona Product Blueprint](references/persona-product-blueprint.md)
- [Safety and Positioning](references/safety-positioning.md)
- [OpenClaw Skill Variant](references/openclaw-skill-variant.md)
- [Project homepage](https://github.com/xiaonizhou-crypto/persona-pack-builder)
- [ClawHub skill page](https://clawhub.ai/xiaonizhou-crypto/skills/persona-pack-builder)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown files, JSON configuration, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate a reusable persona-product folder containing prompts, examples, configuration, and packaging documentation.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
