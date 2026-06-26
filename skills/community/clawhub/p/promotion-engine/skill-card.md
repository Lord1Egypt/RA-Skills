## Description: <br>
Promotion Engine helps digital retail employees look up active retail promotions and calculate final prices, savings, bundles, thresholds, and membership discounts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fangwei-frank](https://clawhub.ai/user/fangwei-frank) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Digital retail employees and customer-facing agents use this skill to answer promotion questions, compare stackable discounts, and show calculation steps for cart or item pricing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Customer-facing pricing can be incorrect if promotion or membership data is stale, or if SKU/category applicability and exclusions are not checked. <br>
Mitigation: Verify the knowledge-base data before relying on results, and check SKU/category applicability and exclusions separately for customer-facing pricing. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown responses with calculation steps; the helper script can emit JSON or human-readable text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses promotion and membership knowledge-base data; pricing examples are in CNY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
