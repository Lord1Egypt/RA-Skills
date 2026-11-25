## Description:

Tracks US stock with reorder points, dated count adjustments and the tax and shipping rules that apply to each item. Use when the user asks for inventory tracker template, stock count sheet, reorder point calculator. For US warehouse leads, operations coordinators and small business owners counting stock and ordering replacements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

US warehouse leads, operations coordinators, and small business owners use this skill to organize stock counts, record dated quantity adjustments, review reorder points, and identify inventory details that need checking.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The security review rates this release suspicious and warns that advertised inventory functions may be missing or produce misleading results; its analysis is incomplete.

Mitigation: Review the reported behavior and verify the calculations and input handling before relying on results for purchasing or inventory decisions.

Risk: The supplied script reads simple key-value input and defaults missing or nonnumeric values to zero, while the documented starting template is CSV; this can produce incomplete or misleading reports.

Mitigation: Check that each input field is read as intended and independently verify calculations before using a report.

## Reference(s):

- [Inventory US Rules](references/inventory-us-rules.md)
- [ClawHub inventory-tracker listing](https://clawhub.ai/rapidworker1/skills/inventory-tracker)

## Skill Output:

**Output Type(s):** [Markdown, Inventory guidance]

**Output Format:** [Markdown calculation report and inventory guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A CSV template is provided as input; validate results before operational use.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
