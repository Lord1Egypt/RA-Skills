## Description:

Creates a presentation-ready copy of a NotebookLM-exported slide-deck PDF by masking the small visible NotebookLM footer badge at the bottom-right of each page.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fudanjx](https://clawhub.ai/user/fudanjx)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create a cleaned copy of a NotebookLM slide-deck PDF for sharing, presenting, or emailing while keeping the original PDF unchanged.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional metadata or annotation stripping can remove document provenance or review information from the cleaned copy.

Mitigation: Keep the original PDF and use --strip-metadata or --strip-annots only when that removal is intentional.

Risk: The default mask is narrowly tuned to NotebookLM slide-deck footer badges and may cover the wrong area on unusual page layouts.

Mitigation: Use --inspect and spot-check page 1 plus a later page; adjust mask values before sharing when needed.

## Reference(s):

- [NotebookLM PDF Cleaner on ClawHub](https://clawhub.ai/fudanjx/skills/notebooklm-pdf-cleaner)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown with inline shell commands and local PDF file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a new *-clean.pdf copy by default; optional inspection, mask tuning, metadata stripping, and annotation stripping are available.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
