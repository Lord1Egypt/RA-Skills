## Description:

Helps agents identify a website's colors, fonts, and design tokens to build a matching interface.

This skill is ready for commercial/non-commercial use.

## Publisher:

[soraiabarroso](https://clawhub.ai/user/soraiabarroso)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and designers use this skill to extract a site's brand palette, typography, and design tokens for new interfaces or theme configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted website URLs are shared with MiroMiro, a third-party service.

Mitigation: Only submit URLs intended for external analysis; avoid private or internal sites.

Risk: The service requires an API key.

Mitigation: Use your own key and keep it out of project files.

Risk: Inferred palette colors may not be official brand colors.

Mitigation: Check source signals and label usage-derived colors as approximations.

Risk: A website's font files may require a separate commercial license.

Mitigation: Check font licensing before using the fonts in production.

## Reference(s):

- [MiroMiro website color palette API](https://miromiro.app/api/website-color-palette-api)
- [Match a website's brand and design tokens on ClawHub](https://clawhub.ai/soraiabarroso/skills/match-brand)

## Skill Output:

**Output Type(s):** [Guidance, Configuration instructions, Code]

**Output Format:** [Markdown guidance with optional CSS, JSON, or Tailwind configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Brand confidence and source signals can distinguish declared colors from inferred approximations.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
