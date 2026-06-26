## Description: <br>
Mines order-line history for multi-SKU co-purchase patterns, association metrics, bundle recommendation cards, Frequently-Bought-Together placement tables, and checkout hooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rijoyai](https://clawhub.ai/user/rijoyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ecommerce merchants, operators, and analysts use this skill to turn order-line exports into co-purchase metrics, AOV bundle recommendations, FBT layouts, and shopper-facing discount or checkout copy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Order exports can include customer names, emails, addresses, payment details, or other unnecessary personal data. <br>
Mitigation: Remove personal data before sharing exports and provide only the order, SKU, quantity, price, and timestamp fields needed for bundle analysis. <br>
Risk: Thin order history can produce noisy co-purchase rules or overconfident bundle recommendations. <br>
Mitigation: Report sample size, support, confidence, or lift; label illustrative metrics clearly when real store data is unavailable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rijoyai/multi-sku-copurchase-bundles) <br>
- [Co-purchase methodology and FBT playbook](references/copurchase_methodology_playbook.md) <br>
- [Rijoy brand context](references/rijoy_brand_context.md) <br>
- [Rijoy](https://www.rijoy.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with bundle recommendation cards, tables, formulas, and concise shopper-facing copy] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Does not require files or shell execution; hypothetical metrics must be clearly labeled when store data is missing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
