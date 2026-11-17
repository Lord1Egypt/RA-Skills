## Description:

Tracks US stock with reorder points, dated count adjustments and the tax and shipping rules that apply to each item.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

US warehouse leads, operations coordinators, and small-business owners use the skill to track stock counts, dated adjustments, reorder points, and tax or shipping checks for inventory items.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The inventory calculator silently loses item identifiers and omits calculations, making results unreliable for business decisions.

Mitigation: Use copies of records, independently check identifiers and reorder quantities, and do not rely on the calculator for operational decisions until it is corrected.

Risk: The skill's tax guidance includes a LIFO-repeal claim that the security assessment says conflicts with IRS Form 970 guidance.

Mitigation: Verify tax guidance against current IRS sources and consult a qualified tax professional before relying on it.

Risk: An optional unsigned Windows application presents a separate trust risk and is not needed for the Python workflow.

Mitigation: Avoid the optional application unless independently assessed; use the Python workflow instead.

## Reference(s):

- [Inventory US rules](references/inventory-us-rules.md)
- [IRS Form 970](https://www.irs.gov/forms-pubs/about-form-970)

## Skill Output:

**Output Type(s):** [CSV files, Markdown, Inventory guidance]

**Output Format:** [CSV inventory worksheets and Markdown reports]

**Output Parameters:** [SKU-level stock, count, demand, lead-time, and safety-stock data]

**Other Properties Related to Output:** [Proposed reorder points are not purchase orders. The calculator needs correction before operational use; independently verify item identifiers, quantities, and tax guidance.]

## Skill Version(s):

1.0.6 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
