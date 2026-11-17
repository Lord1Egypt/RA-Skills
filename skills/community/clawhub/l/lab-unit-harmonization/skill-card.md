## Description:

Lab Unit Harmonization standardizes clinical laboratory data from multiple sources by converting between US conventional and SI units, cleaning numeric formats, and addressing common data quality issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data engineers, and clinical analytics teams use this skill to prepare multi-source laboratory data for healthcare analytics, CKD research panels, ETL pipelines, and machine learning preprocessing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lab-cleaning guidance can silently drop records or alter clinical measurements.

Mitigation: Require explicit source units or trusted source mappings, preserve original values, and log every conversion or dropped record.

Risk: Range checks used as automatic conversion or clamping rules can produce misleading values.

Mitigation: Treat range checks as validation warnings and keep full-precision canonical numeric data for review.

## Reference(s):

- [CKD Lab Features Dictionary](reference/ckd_lab_features.md)
- [KDIGO Guidelines](https://kdigo.org/)
- [Unified Code for Units of Measure](https://ucum.org/)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown guidance with Python code snippets and reference tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose value parsing, unit conversion, row filtering, validation checks, and formatted lab outputs.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
