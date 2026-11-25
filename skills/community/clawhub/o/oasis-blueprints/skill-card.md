## Description:

Create or revise construction drawing sheets as self-contained HTML and scaled PDFs, with plans, sections, details, title blocks, and tracked open items. Use for HTML drawing sets and permit-sheet drafting; not for structural design calculations or native CAD/DWG editing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oasiseng](https://clawhub.ai/user/oasiseng)

### License/Terms of Use:

MIT-0

## Use Case:

Drafting teams and engineers use the skill to turn supplied project information into editable construction drawing sheets and scaled PDFs for review, while tracking unanswered design requirements as open items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact was only partly inspected, so some file-access and tool-scope behavior may not be represented in the scan summary.

Mitigation: Review the skill files before use and limit access to the project files needed for the drawing set.

Risk: Drawing sheets may be mistaken for structurally verified or approved designs.

Mitigation: Keep the set in draft or review status until the engineer of record resolves open items and approves it; treat layout checks as drawing checks only.

## Reference(s):

- [Oasis Engineering documentation](https://docs.oasisengineering.com)
- [Oasis Blueprints on ClawHub](https://clawhub.ai/oasiseng/skills/oasis-blueprints)
- [Project file reference](references/project-file.md)
- [Sheet standard](references/sheet-standard.md)
- [Writing custom views](references/writing-views.md)

## Skill Output:

**Output Type(s):** [HTML files, PDF files, JSON configuration, Drafting guidance]

**Output Format:** [Self-contained HTML drawing set, scaled PDF sheets, and editable JSON project file]

**Output Parameters:** [Project-specific; PDF sheets are 36 × 24 in landscape]

**Other Properties Related to Output:** [Drafts preserve open items; layout checks do not establish structural adequacy or approval. PDF export and automated layout checks require Playwright and Chromium.]

## Skill Version(s):

0.4.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
