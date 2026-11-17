## Description:

Generate polished slide decks as self-contained HTML and editable PowerPoint from notes, with theme selection, deck schema guidance, rendering workflows, and presentation craft checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[isatimur](https://clawhub.ai/user/isatimur)

### License/Terms of Use:

MIT

## Use Case:

Developers, creators, and business users use this skill to turn notes or briefs into polished slide decks for pitches, investor updates, keynotes, product launches, sales demos, and related presentation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional deployment commands can publish decks to an external Vercel URL.

Mitigation: Confirm publication intent before deployment, avoid deploying confidential decks unless explicitly intended, and use preview deployments unless production publication is required.

Risk: Optional install, render, and export commands can run internet-downloaded or changing packages.

Mitigation: Review commands before execution, pin or preinstall trusted package versions where practical, and run rendering or PDF export in a sandboxed environment.

Risk: Untrusted deck content may be processed during PDF export.

Mitigation: Run export in an environment without unrelated credentials and keep the PDF export route guard and JavaScript-disabled rendering posture intact.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/isatimur/skills/presentation-md)
- [Server-resolved GitHub Source](https://github.com/isatimur/presentation-md/tree/main/skills/presentation-generator)
- [Repository](https://github.com/isatimur/presentation-md)
- [Presentation MD Homepage](https://presentation-md.vercel.app)
- [Presentation MD Studio](https://presentation-md.vercel.app/studio)
- [Deck Schema](references/deck-schema.md)
- [Theme Guide](references/themes.md)
- [Layout Recipes](references/layout-recipes.md)
- [Markdown Import](references/markdown-import.md)
- [PowerPoint Import](references/pptx-import.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Deck JSON, HTML, PowerPoint/PDF export commands, and deployment commands when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce self-contained HTML decks, editable PowerPoint output through the presentation-md tooling, and PDF exports through Playwright/Chromium.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
