## Description:

Automation Master is an office automation suite for file conversion, batch renaming, Excel data merging, template-based document generation, invoice extraction, and tax reconciliation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mk1350](https://clawhub.ai/user/mk1350)

### License/Terms of Use:

MIT-0

## Use Case:

External business users, finance and accounting teams, HR teams, and data analysts use this skill to automate office file handling, extract structured invoice data, and reconcile tax or business datasets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has broad local execution and file-handling powers.

Mitigation: Review the skill before installation and run it only in an isolated, non-admin Windows environment with dedicated temporary and output directories.

Risk: Document conversion can depend on an external LibreOffice executable.

Mitigation: Restrict the LibreOffice executable path to a trusted administrator-managed binary.

Risk: Dependencies and optional printing behavior can expand the local system impact.

Mitigation: Pin and review dependencies, and disable or remove printing unless explicitly needed.

Risk: Invoice and identity documents may contain confidential information.

Mitigation: Avoid processing confidential invoices or identity documents until logging and cleanup are fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mk1350/skills/mk1350-automation-master)
- [Artifact README](artifact/README.md)
- [Artifact skill manifest](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Files, JSON, Text]

**Output Format:** [JSON status responses with links or paths to generated office files and spreadsheets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce converted documents, renamed files, generated Word or Excel documents, invoice spreadsheets, reconciliation spreadsheets, or print job status.]

## Skill Version(s):

1.0.2 (source: server release evidence and artifact/SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
