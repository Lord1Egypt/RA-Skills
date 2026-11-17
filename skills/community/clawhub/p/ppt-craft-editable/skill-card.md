## Description:

PPT Craft Editable helps agents create polished image-based presentations, optional text-editable PPTX decks, and editable PPTX conversions from PDF slide decks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ilioner](https://clawhub.ai/user/ilioner)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and presentation creators use this skill to turn topics, source material, or PDF slide decks into presentation deliverables with review steps and editable text workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install or change Python packages during preflight setup.

Mitigation: Review setup steps before installation and prefer running the skill in an isolated virtual environment.

Risk: The skill can create a persistent local cache for optional retouch tooling.

Mitigation: Confirm local cache location, disk usage, and cleanup expectations before enabling retouch tooling.

Risk: Marker blocks pasted from untrusted content could cause workflow files to be overwritten or scripts to run on untrusted input.

Mitigation: Accept marker blocks only from trusted review and editor pages, and inspect the source before allowing file overwrite or script execution.

Risk: PDF asset paths and rendering steps can affect local files and generated outputs.

Mitigation: Confirm PDF asset paths, file overwrite targets, and final rendering commands before proceeding.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/ilioner/skills/ppt-craft-editable)
- [Server-Resolved GitHub Provenance](https://github.com/ilioner/ppt-craft-editable)
- [README](README.md)
- [Pipeline Reference](references/pipeline.md)
- [Phase A Workflow](references/phaseA/workflow.md)
- [Phase C Workflow](references/phaseC/workflow.md)
- [Phase D Workflow](references/phaseD/workflow.md)
- [Phase D Extraction Schema](references/phaseD/extraction-schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance, JSON deck data, HTML review and editor files, image assets, and PPTX files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local artifacts and run Python scripts; editable PPTX output uses image backgrounds with editable PowerPoint text boxes.]

## Skill Version(s):

0.1.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
