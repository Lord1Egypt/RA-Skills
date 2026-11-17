## Description:

Powerpoint Generator guides an agent through requirements gathering, research, slide planning, HTML design, visual QA, and PPTX export for professional presentation decks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cerealaxis](https://clawhub.ai/user/cerealaxis)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and presentation creators use this skill to turn a topic, source material, or presentation requirements into structured slide decks with HTML previews and editable or pixel-fidelity PPTX exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup and post-processing workflow runs local Python and Node scripts and installs package dependencies.

Mitigation: Install and run the skill in an isolated workspace, review scripts before first use, and keep package dependencies pinned.

Risk: Generated HTML is rendered in Chromium and may expose local slide content or local file paths during rendering or QA.

Mitigation: Use a non-confidential working directory, constrain image and asset paths to the presentation asset folder, and review generated HTML before rendering.

Risk: Optional image sourcing and visual QA can involve external services and may send presentation content outside the local environment.

Mitigation: Disable remote visual QA and external image services for confidential decks, or use only locally provided assets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cerealaxis/skills/powerpoint-generator)
- [README.md](README.md)
- [Method](references/method.md)
- [Pipeline compatibility](references/pipeline-compat.md)
- [Bento grid layouts](references/bento-grid.md)
- [Style system](references/style-system.md)
- [Prompt templates](references/prompts.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with JSON planning artifacts, HTML slides, PNG/SVG assets, and PPTX files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are normally written under ppt-output/ as preview.html, slide HTML files, SVG and PNG exports, and presentation-svg.pptx or presentation-png.pptx when dependencies are available.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
