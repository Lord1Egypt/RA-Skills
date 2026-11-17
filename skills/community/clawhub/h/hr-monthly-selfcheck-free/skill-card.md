## Description:

A Chinese-language local HR monthly self-check skill that reconciles payroll withholding, cumulative individual income tax withholding, and social insurance or housing fund contribution tables from segmented user-provided text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, payroll, and HR staff use this skill during monthly close or payroll reconciliation to check pasted payroll, tax, social-insurance, and housing-fund tables for arithmetic mismatches, duplicate or missing rows, and incomplete materials. It supports local reconciliation but does not replace legal, tax, audit, or compliance sign-off.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may paste payroll, tax, social-insurance, or housing-fund tables that contain sensitive employee data.

Mitigation: Run the packaged checker locally, avoid sharing input files externally, and handle source tables according to the organization's HR and payroll data policies.

Risk: The skill performs arithmetic reconciliation and may be mistaken for legal, tax, audit, or compliance approval.

Mitigation: Treat results as reproducible reconciliation findings only and have qualified HR, finance, tax, or compliance reviewers make final decisions.

Risk: The free version omits some checks and does not infer conclusions when required material is missing.

Mitigation: Review the reported checks-not-run and missing-material messages before relying on the output for a monthly close workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/hr-monthly-selfcheck-free)
- [chenqg618 publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Guidance, Shell commands]

**Output Format:** [Markdown guidance and optional JSON results from local Node.js execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source rows where available, list checks that were not run in the free version, and report insufficient input instead of fabricating conclusions.]

## Skill Version(s):

1.0.53 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
