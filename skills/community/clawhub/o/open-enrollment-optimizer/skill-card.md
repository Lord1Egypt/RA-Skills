## Description:

Use during fall benefits/open-enrollment window (or Medicare Oct 15-Dec 7) to choose health plans, FSA/HSA elections, and insurance elections. Models true annual cost of each plan across healthy/typical/high-use scenarios, computes FSA use-it-or-lose-it risk and optimal election, and prices HSA vs FSA vs taxable over a horizon.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Employees and people comparing Medicare options use this skill to compare health plan costs across care scenarios and estimate FSA and HSA choices before an enrollment deadline. It helps organize the comparison; users should confirm provider networks, drug coverage, and plan details against official documents.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Enrollment estimates or guidance may be inaccurate or out of date, including tax limits and plan coverage.

Mitigation: Use anonymized plan details and spending estimates. Verify calculations, current-year tax limits, and network and drug coverage against official plan documents before making elections.

Risk: Some documented command examples may not match the script's supported arguments.

Mitigation: Confirm command syntax against the script's current help before relying on documented examples.

## Reference(s):

- [FSA / HSA Decision Guide](references/fsa-hsa-guide.md)
- [Plan Comparison Method](references/plan-comparison-method.md)
- [Open-Enrollment Optimizer on ClawHub](https://clawhub.ai/voronindenis5/skills/open-enrollment-optimizer)

## Skill Output:

**Output Type(s):** [Analysis, Text, Guidance]

**Output Format:** [Terminal text with plan comparison tables and written guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scenario-based annual cost comparisons, FSA forfeiture estimates, and HSA projections based on the supplied plan and spending assumptions.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
