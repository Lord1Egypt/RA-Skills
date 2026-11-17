## Description:

Converts Markdown presentation or report documents into editable PPTX slide decks that can be opened in PowerPoint, Keynote, or WPS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sopaco](https://clawhub.ai/user/sopaco)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and business users use this skill to turn structured Markdown presentations or reports into editable slide decks while preserving the source content. The agent scans the document structure, builds a presentation schema, runs the PPTX generator, and verifies generated text coverage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads a selected Markdown file and writes temporary schema and PPTX files.

Mitigation: Use explicit input and output paths, and avoid running it in sensitive directories when temporary files matter.

Risk: Dependency resolution may vary across installs without a reviewed lockfile or pinned dependency set.

Mitigation: Use a reviewed install with pinned dependencies or a lockfile for reproducible production use.

Risk: Some content may require manual handling if section parsing fails or Mermaid diagrams are converted into placeholders.

Mitigation: Review the pagination plan and generated text verification, then manually handle any flagged sections or diagram placeholders.

## Reference(s):

- [Analysis Prompt](references/analysis-prompt.md)
- [Presentation Schema](references/presentation-schema.md)

## Skill Output:

**Output Type(s):** [Guidance, JSON, Shell commands, Files]

**Output Format:** [Markdown status updates, PresentationSchema JSON, shell command invocation, and editable PPTX file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads an explicit Markdown input path, writes a temporary schema JSON file, and writes the requested PPTX output file.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
