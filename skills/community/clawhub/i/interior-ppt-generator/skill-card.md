## Description:

Generates client-ready interior design PowerPoint decks from a folder of render images, adding sorted image slides, title sections, layout pages, material notes, and dark brand styling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[137984917-cyber](https://clawhub.ai/user/137984917-cyber)

### License/Terms of Use:

MIT-0

## Use Case:

Interior designers and design teams use this skill to turn project render folders into 16:9 client presentation decks with cover, review, concept, image showcase, material board, and closing slides.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated client-facing decks may include embedded publisher branding that is not appropriate for the user's organization or project.

Mitigation: Review each generated presentation before client delivery and remove or replace unwanted branding in the deck or source script.

Risk: The command-line interface does not expose an option to disable or customize the embedded branding.

Mitigation: Treat branding changes as a required manual review step before production use, especially for external client presentations.

## Reference(s):


## Skill Output:

**Output Type(s):** [code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with Python command examples; generated artifact is a PPTX file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, python-pptx, Pillow, an input image folder, and an output .pptx path.]

## Skill Version(s):

3.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
