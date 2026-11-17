## Description:

Checks inventory in/out and cost tables for row-level arithmetic, total-line reconciliation, duplicate items, blanks, and weighted-average cost consistency, with each finding tied to the provided source material.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, cashier, and cost-accounting users can run this skill during monthly close, reconciliation, or inventory checks to verify inventory quantity and amount flows. It is intended for monthly weighted-average costing inputs and reports missing material instead of producing unsupported conclusions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The free version does not run every inventory-cost validation listed by the artifact.

Mitigation: Review the withheld checks in the output before relying on the result, especially negative quantity, available-quantity, negative value, and zero-cost opening balance checks.

Risk: The check assumes monthly weighted-average costing and may not fit FIFO, moving-average, or specific-identification accounting methods.

Mitigation: Confirm the accounting method before using the cost conclusion; for other methods, treat the result only as a quantity and amount reconciliation aid.

Risk: Inventory tables can contain business-sensitive financial data.

Mitigation: Use only the inventory table intended for reconciliation and keep execution local as described by the security evidence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/inventory-cost-flow-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)
- [SKILL.md](artifact/SKILL.md)
- [Sample input](artifact/templates/sample.json)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Human-readable console text or structured JSON containing executed checks, withheld checks, findings, summary, and input guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs identify free-version scope, local execution status, whether network use occurred, and omitted or out-of-scope checks.]

## Skill Version(s):

1.0.58 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
