## Description:

Compare fresh grocery prices across Hema, Dingdong, Meituan Maicai and more to find the best deals on a shopping list.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to parse grocery lists, compare mock or supplied fresh-food prices across Chinese grocery platforms, normalize units, calculate totals, and produce a ready-to-shop procurement plan.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The documentation advertises live platform scraping, price alerts, and screenshot/OCR handling that the inspected script does not implement.

Mitigation: Treat generated comparisons as local mock-data output unless live data integration is reviewed and added; verify any price-sensitive recommendations against the grocery platforms before purchase.

Risk: The skill works with shopping lists and may reference city-level availability.

Mitigation: Avoid collecting precise location or account credentials, and keep use limited to public price data and user-provided shopping-list details.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/skills/grocery-price-comparer)
- [Platform reference data](artifact/references/platforms.json)
- [Product category mappings](artifact/references/categories.json)
- [Input schema](artifact/schemas/input.schema.json)
- [Output schema](artifact/schemas/output.schema.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands and optional JSON output from the bundled comparison script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces parsed items, a price comparison matrix, platform totals, strategy recommendations, and a procurement plan; current inspected behavior uses local mock data.]

## Skill Version(s):

1.0.0 (source: frontmatter, skill.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
