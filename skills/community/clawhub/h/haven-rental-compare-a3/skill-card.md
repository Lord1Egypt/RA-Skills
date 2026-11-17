## Description:

Compare rental listings against a monthly budget, separate refundable deposits, and flag unknown fees and source gaps. Use for rental cost comparisons; it does not discover listings or contact landlords.

This skill is ready for commercial/non-commercial use.

## Publisher:

[akankshasm](https://clawhub.ai/user/akankshasm)

### License/Terms of Use:

MIT-0

## Use Case:

Renters and housing researchers can compare supplied rental listings against a monthly budget, separate refundable deposits from recurring costs, and identify missing fees or source details. Use the comparison to review trade-offs while checking the underlying listing sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stale source dates, mixed currencies or billing periods, and unknown mandatory fees can make totals or budget fit unreliable.

Mitigation: Check source dates and use one currency and monthly period; leave unknown fees unknown so the comparison keeps the total and budget fit indeterminate.

Risk: Supplied listing fields are preserved in the output and may contain information the user did not intend to include.

Mitigation: Include only listing data intended for the output.

## Reference(s):

- [Input schema and interpretation](references/schema.md)
- [Synthetic example listings](assets/example-listings.json)
- [Haven Rental Compare on ClawHub](https://clawhub.ai/akankshasm/skills/haven-rental-compare-a3)
- [Publisher profile](https://clawhub.ai/user/akankshasm)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Guidance]

**Output Format:** [JSON comparison results with a concise explanation of monthly totals, budget fit, missing information, and preference trade-offs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Compares supplied listings only; unknown mandatory fees keep monthly totals and budget fit unknown. Refundable deposits are reported separately from recurring costs.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
