## Description:

A Chinese-language ToB SaaS PRD assistant for creating, reviewing, and optimizing product requirements documents across new product, new capability, and existing feature iteration scenarios.

This skill is ready for commercial/non-commercial use.

## Publisher:

[woai36d](https://clawhub.ai/user/woai36d)

### License/Terms of Use:

MIT-0

## Use Case:

Product managers, product operations teams, and SaaS builders use this skill to draft PRDs, review PRD quality, benchmark competitors, define SaaS metrics, and prepare role-adapted product documentation for engineering, sales, and executive audiences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PRD review or competitor screenshot analysis may expose sensitive customer data, credentials, confidential strategy, or unauthorized third-party material.

Mitigation: Use only authorized materials and redact secrets, customer data, credentials, and internal-only strategy before providing inputs to the skill.

Risk: Batch screenshot analysis can process a broader set of files than intended if the job scope is ambiguous.

Mitigation: Keep screenshot analysis jobs scoped to explicit file lists and clearly named output locations.

## Reference(s):

- [PRD Templates](references/prd-templates.md)
- [Competitor Analysis Framework](references/competitor-analysis-framework.md)
- [SaaS Metrics Guide](references/saas-metrics-guide.md)
- [Compliance Checklist](references/compliance-checklist.md)
- [PRD Best Practices Organization Module](references/prd-best-practices-organization-module.md)
- [API Reference](references/api_reference.md)
- [PRD Markdown Template](assets/templates/prd-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Markdown PRD documents, PRD review reports, competitor analysis matrices, structured JSON screenshot analysis, and role-adapted document views.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripted generation and format conversion are described as future work in this release; the current release is primarily instruction and reference driven.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
