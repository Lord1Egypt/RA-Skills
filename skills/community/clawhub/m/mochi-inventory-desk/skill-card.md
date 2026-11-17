## Description:

Track SKUs and warehouse movements, calculate stock and moving-average cost, and export reorder reports by currency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Warehouse and operations teams can maintain a workspace-local SKU and movement ledger, calculate stock and moving-average cost, and generate inventory and reorder reports by currency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stock-changing requests can alter the local inventory ledger.

Mitigation: Review stock-changing requests and back up the local inventory database before important updates.

Risk: Inventory reports may contain sensitive business data.

Mitigation: Share exported reports deliberately.

## Reference(s):

- [Action contract](references/input.md)
- [MochiLab homepage](https://mochilab.bz)
- [ClawHub release](https://clawhub.ai/hznetnewpower/skills/mochi-inventory-desk)

## Skill Output:

**Output Type(s):** [Guidance, JSON, Files]

**Output Format:** [JSON results and workspace-local inventory and reorder reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local ledger and reports; currency totals are kept separate without foreign-exchange conversion.]

## Skill Version(s):

1.0.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
