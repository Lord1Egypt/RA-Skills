## Description:

Generates a five-sheet Excel valuation workbook for China-focused foreclosure and distressed-asset screening, comparing auction prices with market estimates and modeling discount repairability and three-scenario IRR/MOIC.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lingyu9495-source](https://clawhub.ai/user/lingyu9495-source)

### License/Terms of Use:

MIT-0

## Use Case:

Investors and analysts assessing Chinese foreclosure properties or distressed assets use this skill to compare auction and estimated market prices, review discount repairability, and stress-test returns before bidding. Its model supports due diligence rather than replacing investment advice.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Unverified comparables or optimistic assumptions can make estimated returns misleading.

Mitigation: Verify market comparables and input assumptions independently; review conservative scenarios before relying on the workbook.

Risk: Taxes, occupancy or eviction delays, and unexpected costs can materially reduce returns.

Mitigation: Investigate tax obligations, title and occupancy, potential eviction costs, and disposal timing as part of due diligence.

Risk: Untrusted JSON inputs or spreadsheet calculations can produce misleading valuations.

Mitigation: Validate the JSON input source and inspect and recalculate the XLSX before using its figures.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/lingyu9495-source/skills/npa-fapai-valuation-lite)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Files]

**Output Format:** [Text instructions and five-sheet XLSX workbook]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Workbook includes input assumptions, scenario cash flows, sensitivity analysis, and a discount scorecard.]

## Skill Version(s):

1.1.1 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
