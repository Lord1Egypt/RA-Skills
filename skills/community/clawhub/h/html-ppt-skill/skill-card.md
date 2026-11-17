## Description:

Generates HTML-based slide decks as a modern alternative to PPT/PPTX, using 16:9 CSS scroll-snap slides with keyboard, scroll, on-screen navigation, and browser print-to-PDF export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[boboy-j](https://clawhub.ai/user/boboy-j)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and presentation authors use this skill to create responsive HTML slide decks for technical talks, academic reports, product pitches, brand presentations, and organization history or culture presentations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill strongly defaults presentation requests to HTML output instead of PPTX.

Mitigation: Ask the agent explicitly for PPTX when that format is required.

Risk: Generated decks may save files as part of the slide creation workflow.

Mitigation: Review generated file paths and contents before sharing or deploying the deck.

Risk: Generated HTML decks may load fonts from Google when opened in a browser.

Mitigation: Request local fonts or approved font sources when external font loading is not acceptable.

## Reference(s):

- [HTML PPT Design System](artifact/references/design-system.md)
- [Blank Starter Template](artifact/assets/blank-starter.html)

## Skill Output:

**Output Type(s):** [code, markdown, configuration, guidance]

**Output Format:** [HTML, CSS, JavaScript, and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces 16:9 browser-rendered slide decks that can be exported to PDF through browser print.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
