## Description:

Generates 5-15 fixed-size HTML report pages from arbitrary input, decomposing each page into focused dimensions with concise Chinese-first narrative and supporting charts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[panhongwei](https://clawhub.ai/user/panhongwei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and report authors use this skill to convert source material into PPT-sized HTML report pages with structured sections, SVG charts, visual templates, and screenshot validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use web search for unfamiliar diagram types, which can create unwanted network exposure when working with confidential material.

Mitigation: Use the skill only with approved web access, remove sensitive details from diagram queries, or disable web-dependent behavior for confidential reports.

Risk: Some visual templates may load Google Fonts from a remote URL.

Mitigation: Use local or system fonts, or remove remote font imports before using generated HTML in restricted or offline environments.

Risk: The skill is Chinese-first, so generated narrative and labels may need localization for other audiences.

Mitigation: Review and localize report text, chart labels, and page metadata before publishing externally.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/panhongwei/skills/html-report-generator)
- [01 - Canvas and Structure Rules](artifact/references/01-canvas.md)
- [02 - Design System and Visual Templates](artifact/references/02-design-system.md)
- [03 - Layout System](artifact/references/03-layout.md)
- [04 - Color and Font System](artifact/references/04-color-font.md)
- [05 - Content Rules and Chart Library](artifact/references/05-content.md)
- [06 - Workflow and Quality Checks](artifact/references/06-workflow.md)
- [07 - Special Page Specifications](artifact/references/07-special-pages.md)
- [08 - Extended SVG Chart Library](artifact/references/08-svg-extended.md)
- [09 - Component Library](artifact/references/09-components.md)
- [10 - Business Diagram Library](artifact/references/10-diagram-types.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [HTML report pages with Markdown-style summaries, inline HTML/CSS/SVG code, and validation commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces multiple 1017x720 report pages and a concise validation summary covering page count, visual templates, layout variants, overflow checks, and color consistency.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
