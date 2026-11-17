## Description:

Generates self-contained, keyboard-navigable HTML presentation decks with fixed 1280x720 slides, structured planning, reusable layout templates, and optional PPTX export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomm1399](https://clawhub.ai/user/tomm1399)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and presentation authors use this skill to turn a requested topic, mode, and section count into a planned slide outline, finalized slide content, HTML presentation files, and optional editable PPTX output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML may embed untrusted slide text as active HTML or JavaScript.

Mitigation: Review generated HTML before sharing, escape or sanitize slide text, and allowlist layout and icon identifiers before rendering.

Risk: Optional PPTX export depends on an unpinned python-pptx requirement.

Mitigation: Pin python-pptx to an approved version before using the exporter in controlled environments.

Risk: Generated HTML loads Google Fonts from an external service.

Mitigation: Use a local font bundle or modify the template when external network requests are not acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tomm1399/skills/kaifafuzhuskll01)
- [Skill definition](artifact/SKILL.md)
- [Design system](artifact/references/design-system.md)
- [Content rules](artifact/references/content-rules.md)
- [Base HTML template](artifact/assets/base-template.html)
- [PPTX export script](artifact/scripts/export_pptx.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown planning guidance with JSON slide data, generated HTML, and optional PPTX files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces self-contained HTML presentations with fixed-size slides and keyboard navigation; optional PPTX export depends on python-pptx.]

## Skill Version(s):

3.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
