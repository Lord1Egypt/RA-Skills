## Description: <br>
Compare fresh grocery prices across Hema, Dingdong, Meituan Maicai & more - find the best deals on your shopping list. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and shopping assistants use this skill to compare grocery items across supported fresh-food delivery platforms, normalize units, estimate total costs, and produce a ready-to-shop procurement plan. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The current CLI price data may be mock or stale, which can mislead purchase decisions. <br>
Mitigation: Treat generated prices as estimates unless real platform lookups are configured, and verify final prices in the grocery platform before purchasing. <br>
Risk: Future alerting or scraping behavior could poll platforms or collect platform data without clear user intent. <br>
Mitigation: Enable alerts or platform lookups only with explicit user consent, avoid platform credentials, and use only public price and product data. <br>
Risk: Shopping lists, screenshots, or location details may contain personal information. <br>
Mitigation: Strip screenshot metadata, avoid storing precise coordinates, and use city-level location only when coverage checks are needed. <br>


## Reference(s): <br>
- [Platform reference data](references/platforms.json) <br>
- [Product category mappings](references/categories.json) <br>
- [Input schema](schemas/input.schema.json) <br>
- [Output schema](schemas/output.schema.json) <br>
- [ClawHub release page](https://clawhub.ai/harrylabsj/grocery-price-comparer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance, Shell commands] <br>
**Output Format:** [Markdown tables or JSON objects with parsed items, price matrix, totals, recommendations, procurement plan, warnings, and optional alert status] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are based on the selected grocery platforms and may include mock or estimated prices unless real platform lookups are added.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, skill.json, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
