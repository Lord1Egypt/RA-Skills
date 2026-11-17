## Description:

Compares two or more job offers by calculating true total compensation, effective hourly rate, PTO value, and break-even base salary for negotiation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Employees and external users use this skill to compare job offers across salary, benefits, commute, cost of living, PTO, and equity assumptions. It helps produce a negotiation-ready base salary target while keeping tax, legal, and career-fit decisions out of scope.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Job offer details can contain sensitive compensation, location, and benefits information.

Mitigation: Keep offer documents and input JSON local, and remove unnecessary personal information before sharing results.

Risk: The model is gross of tax and is not financial, tax, or legal advice.

Mitigation: Verify outputs against the actual offer documents and consult qualified advisers for tax, legal, or investment decisions.

Risk: Results depend on user-supplied assumptions such as expected bonus, equity risk, commute, overtime, and cost of living.

Mitigation: Review assumptions before negotiating, run sensitivity checks, and rerun the comparison after any revised offer.

## Reference(s):

- [Compensation Model](references/compensation-model.md)
- [ClawHub Skill Page](https://clawhub.ai/voronindenis5/skills/job-offer-comparator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON output from the local comparison script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The comparison script can emit machine-readable JSON for compare and breakeven commands.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
