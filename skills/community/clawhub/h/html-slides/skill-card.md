## Description:

Creates interactive, self-contained HTML slide decks with sidebar navigation, comments, zoom controls, inline editing, present mode, bilingual support, and configurable brand presets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edsml-yl10823](https://clawhub.ai/user/edsml-yl10823)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business users use this skill to create or enhance browser-based presentation decks for periodic updates, product reviews, roadmap discussions, retrospectives, quarterly business reviews, and training material.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated decks may include external font links.

Mitigation: Review the final HTML before sharing or deployment, and replace remote font links with approved local assets when required.

Risk: The skill may rely on prior presentation files for copied logos or JavaScript.

Mitigation: Confirm the source and permissions for any reused presentation, logo, or script before publishing generated slides.

Risk: Corporate or confidential material may be exposed through brand assets or deck content.

Mitigation: Prefer the Neutral preset or provide explicit trusted asset paths when handling confidential corporate material.

## Reference(s):

- [Reusable Components](artifact/references/components.md)
- [Design Tokens](artifact/references/design-tokens.md)
- [JS Controller - SlidePresentation Class](artifact/references/js-controller.md)
- [Slide Types](artifact/references/slide-types.md)
- [Viewport Fitting and Interactive Chrome](artifact/references/viewport-chrome.md)
- [ClawHub skill page](https://clawhub.ai/edsml-yl10823/skills/html-slides)

## Skill Output:

**Output Type(s):** [Code, Files, Markdown, Guidance]

**Output Format:** [Self-contained HTML files with inline CSS and JavaScript, plus concise Markdown delivery notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated decks may include bilingual English/Chinese text, embedded or referenced brand assets, browser-side interaction controls, and localStorage-backed comments.]

## Skill Version(s):

1.0.0 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
