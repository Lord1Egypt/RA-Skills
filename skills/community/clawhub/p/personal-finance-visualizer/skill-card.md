## Description:

Turns authorized personal finance records into local interactive reports with spending, income, transfers, cash movement, and optional daily budget views in English or Chinese.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasonhmy](https://clawhub.ai/user/jasonhmy)

### License/Terms of Use:

MIT-0

## Use Case:

People reviewing their authorized financial records can reconcile statement data and explore spending, income, transfers, cash movement, and optional daily budgets in a local report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan flags that a configured network endpoint may sync budget settings beyond the local-report purpose.

Mitigation: Use local-only mode unless budget syncing is wanted, and configure it only with a trusted same-origin /api/budget endpoint.

Risk: The security scan was partial, so some file content was not fully inspected.

Mitigation: Review the relevant code and endpoint configuration before enabling budget syncing.

## Reference(s):

- [Input data schema](references/schema.md)
- [Statement processing workflow](references/workflow.md)
- [Source repository (metadata link)](https://github.com/JasonHMY/personal-finance-visualizer)

## Skill Output:

**Output Type(s):** [Analysis, Files, Guidance]

**Output Format:** [Local interactive HTML report with concise explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [English or Simplified Chinese; report periods and optional budget views depend on supplied records and user requests.]

## Skill Version(s):

1.6.0 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
