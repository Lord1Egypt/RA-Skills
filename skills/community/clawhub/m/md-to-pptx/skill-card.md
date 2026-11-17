## Description:

Converts Markdown files with slide separators into PowerPoint (PPTX) presentations and can save output to an active Obsidian vault by default.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhcanyu4](https://clawhub.ai/user/zhcanyu4)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill to convert Markdown slide decks into PPTX presentations, with optional custom output paths and a default Obsidian vault destination when configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The converter reads Obsidian configuration and may write PPTX output into the active vault by default.

Mitigation: Install only if this behavior is acceptable, or pass an explicit output path for each conversion.

Risk: The intermediate HTML file is written next to the input Markdown file and can overwrite an existing sibling HTML path.

Mitigation: Avoid running the converter on Markdown files in directories writable by other users, and check for an existing sibling HTML file before conversion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhcanyu4/skills/md-to-pptx)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [PPTX files with terminal status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output defaults to the active Obsidian vault when no explicit output path is provided.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
