## Description:

Turn rental-unit move-out or turnover inspection findings (reports, photos, notes) into a priced, vendor-ready make-ready scope using the Tektolo property turnover engine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tektolo](https://clawhub.ai/user/tektolo)

### License/Terms of Use:

MIT-0

## Use Case:

Rental property managers and owners use this skill to turn move-out or turnover inspection reports, photos, and notes into priced make-ready task lists, vendor scopes, and owner approval estimates for US rental units.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Inspection reports or photos may contain tenant personal information.

Mitigation: Use the rental-property MCP endpoint and remove tenant names, addresses, faces, and other personal details before uploading reports.

Risk: Extracted findings and estimated prices may be incomplete or incorrect.

Mitigation: Review and confirm the extracted findings before relying on a cost estimate.

## Reference(s):

- [Tektolo Property Turnover capability](https://tektolo.com/capabilities/property-turnover?ref=clawhub)
- [Rental Property MCP endpoint](https://tektolo.com/mcp/rental-property)
- [Tektolo catalog](https://tektolo.com/catalog.json)
- [ClawHub skill release](https://clawhub.ai/tektolo/skills/property-turnover)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown task lists, cost ranges, assumptions, and vendor scopes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [US rental-unit estimates; includes priorities, trade groupings, assumptions, and refer-outs where applicable.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
