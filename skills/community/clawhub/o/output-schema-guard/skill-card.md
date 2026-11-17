## Description:

Validates model-generated JSON against required fields, types, and allowed values, then provides actionable repair hints for downstream integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers integrating model-generated JSON into APIs, databases, forms, or tool calls use this skill to check required fields, types, and allowed values and to produce repair guidance. For important downstream decisions, pair it with a more complete validator.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper supports a limited custom schema format and may fail on unexpected input shapes.

Mitigation: Use a more complete validator for important downstream operations and confirm the schema and input shapes it supports.

Risk: A successful process exit can occur even when validation fails.

Mitigation: Check the returned pass value and issue details before allowing downstream processing.

Risk: The artifact's no-filesystem permission description is inaccurate because the helper reads the supplied schema and input files.

Mitigation: Provide only schema and input file paths the helper should read, and restrict those paths to the required files.

## Reference(s):

- [LGD theory](https://github.com/zhaoxinghua09-cell/LGD)
- [LGD formal paper](https://doi.org/10.5281/zenodo.22456647)
- [UIBC core protocol and reference implementation](https://github.com/zhaoxinghua09-cell/uibc-core)
- [LGD ecosystem hub](https://zhaoxinghua09-cell.github.io/lgd-hub/)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured JSON validation results with field-level findings and repair hints]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results include a pass value and issue details; inspect pass directly because process exit status may not reflect validation success.]

## Skill Version(s):

1.0.12 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
