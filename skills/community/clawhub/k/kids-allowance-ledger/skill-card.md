## Description:

Helps families manage a child's allowance through jar splits, chore earnings, parent-funded growth, savings goals, and readable statements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Parents and caregivers use this skill to track a child's allowance, split income among spending, saving, and sharing, plan purchases, and teach how saving and matching work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the bundled script creates or updates a local ledger containing a child's allowance records.

Mitigation: Review before execution and use --store to select a controlled location for the ledger.

Risk: Illustrative parent-paid interest rates may be mistaken for real-world savings returns.

Mitigation: Explain that the example growth rate is a teaching aid, not a bank rate or return forecast.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/voronindenis5/skills/kids-allowance-ledger)
- [Kids Allowance Ledger design reference](references/design.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, JSON, Guidance]

**Output Format:** [Plain-text statements and projections, command examples, and a local JSON ledger]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Records child allowance data locally; ledger location can be set with --store.]

## Skill Version(s):

1.0.1 (source: ClawHub release; bundled skill frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
