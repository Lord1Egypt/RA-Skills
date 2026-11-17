## Description:

Manual Qztc is a QZTC-internal workflow for generating teaching work manual DOCX files from Excel course records and reviewing the generated documents for expected placeholders and table structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alukardo](https://clawhub.ai/user/alukardo)

### License/Terms of Use:

MIT-0

## Use Case:

QZTC instructors or administrative staff use this skill to create teaching work manual documents from Excel spreadsheets containing student, homework, and grade data. The workflow can also run a reviewer that checks whether placeholders were replaced and homework and grade tables are present.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Input spreadsheets and generated Word documents may contain student records and grades.

Mitigation: Run the workflow only on trusted local files and store generated outputs in protected locations appropriate for student data.

Risk: Generated documents depend on the expected QZTC spreadsheet columns and Word template structure.

Mitigation: Use the bundled review step and inspect any failed checks before distributing generated manuals.

## Reference(s):

- [Teaching Manual Generation Rules](references/grading-formula.md)
- [Manual Qztc ClawHub Skill Page](https://clawhub.ai/alukardo/skills/manual-qztc)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Analysis, Configuration instructions]

**Output Format:** [DOCX files plus terminal review reports and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated documents are written locally from user-provided Excel and Word template files.]

## Skill Version(s):

5.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
