## Description:

Converts structured single-slide or small-deck HTML designs into editable PPTX slides with native PowerPoint text boxes, shapes, chips, arrows, and panels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[textboy](https://clawhub.ai/user/textboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and presentation authors use this skill to convert supported fixed-layout HTML slide drafts into editable PowerPoint decks, and to add a new preset when the slide family is unsupported.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated decks may not preserve every source title, label, spacing detail, or layout nuance, especially for preset-specific templates.

Mitigation: Run the bundled preflight QA and visually inspect the PPTX before sharing; update or add presets when fidelity issues appear.

Risk: The skill runs local Node/npm code that reads input HTML and writes PPTX, model, and QA files.

Mitigation: Install dependencies through a reviewed lockfile process and run the converter only on HTML inputs and output paths you intend to process.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/textboy/skills/present-ppt)
- [README](README.md)
- [Setup and portability](references/setup.md)
- [Usage Principles](references/usage-principles.md)
- [Preset decision rules](references/preset-decision-rules.md)
- [Presets](references/presets.md)
- [New preset template checklist](references/preset-template.md)
- [HTML to Editable PPTX QA heuristics](references/qa-heuristics.md)
- [Roadmap](references/roadmap.md)

## Skill Output:

**Output Type(s):** [files, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, plus generated PPTX, JSON model, and QA report files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are local files; conversion quality depends on matching or implementing a suitable preset and reviewing QA results.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
