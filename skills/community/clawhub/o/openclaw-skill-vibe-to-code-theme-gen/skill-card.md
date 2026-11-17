## Description:

Generates a color palette and CSS variables based on a descriptive atmosphere.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liverock](https://clawhub.ai/user/liverock)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and designers use this skill to turn an atmosphere prompt into theme snippets for CSS, Tailwind, or VS Code settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The vibe prompt is sent to OpenRouter, which can expose sensitive branding, client, or unreleased product details if users include them.

Mitigation: Do not enter secrets, client names, unreleased product details, or confidential branding prompts.

Risk: Model-generated CSS, Tailwind, or VS Code output may contain incorrect or unsuitable color and font values.

Mitigation: Review generated theme output before using it in a project or editor configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liverock/skills/openclaw-skill-vibe-to-code-theme-gen)
- [OpenRouter chat completions endpoint](https://openrouter.ai/api/v1/chat/completions)

## Skill Output:

**Output Type(s):** [Text, Code, Configuration]

**Output Format:** [CSS variables, Tailwind configuration JSON, or VS Code settings JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated from a required vibe string and optional css, tailwind, or vscode format.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
