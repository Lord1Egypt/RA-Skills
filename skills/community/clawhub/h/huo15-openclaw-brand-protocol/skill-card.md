## Description:

Guides an agent through collecting official brand sources, extracting visual identity details, verifying them, and producing a structured brand-spec.md for downstream frontend design work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and design agents use this skill to research an existing brand from official sources and codify colors, typography, logo notes, tone, downloaded assets, and prompt-ready design guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill proposes shell commands with placeholders and an unpinned npx Playwright invocation, which can execute mutable third-party code or mishandle unsafe values.

Mitigation: Review commands before running them, use only official public brand sources, validate brand slugs to lowercase letters, numbers, and hyphens, quote paths and URLs, and pin or preinstall Playwright.

Risk: Brand specifications can be misleading if unofficial sources are used or extraction skips the stated verification checks.

Mitigation: Prefer official brand, press, Figma, GitHub design-system, and website sources, and require color and font evidence before codifying the brand spec.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaobod1/skills/huo15-openclaw-brand-protocol)
- [Publisher profile](https://clawhub.ai/user/zhaobod1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with structured tables and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a brand-spec.md template and guidance for locally downloaded brand assets.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
