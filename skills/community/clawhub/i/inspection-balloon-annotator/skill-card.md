## Description:

Annotates dimensions and tolerances on mechanical drawings with numbered balloons and produces a matching inspection workbook and coverage report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zl19851022-commits](https://clawhub.ai/user/zl19851022-commits)

### License/Terms of Use:

MIT-0

## Use Case:

Quality engineers and inspectors use this skill to create numbered inspection drawings and matching first-article or dimensional inspection records from mechanical PDFs or images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A supplied dims_table.py is executed as Python code during processing.

Mitigation: Use only trusted dimension files and run the workflow in a contained workspace.

Risk: Automatic dimension extraction or balloon placement may miss or mislabel drawing features.

Mitigation: Have an engineer review the annotations, inspection workbook, and coverage report before use.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zl19851022-commits/skills/inspection-balloon-annotator)
- [Tolerance and symbols reference](references/tolerance-and-symbols.md)
- [Workflow and output reference](references/io-and-flows.md)

## Skill Output:

**Output Type(s):** [Annotated drawing files, Inspection workbook, Coverage report]

**Output Format:** [PDF/PNG, XLSX, and JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Balloon numbers correspond to inspection rows; engineer review is required before operational use.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and bundled manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
