## Description: <br>
Intelligent product recommendation engine for retail digital employees that recommends products from a knowledge base based on customer needs, budget, recipient, occasion, preferences, and purchase history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fangwei-frank](https://clawhub.ai/user/fangwei-frank) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Retail digital employees use this skill to handle customer product-selection requests, including gift recommendations, comparisons, outfit pairing, cross-sell, upsell, and help-me-decide flows. It is intended for catalog-backed recommendations where product data is available in a products[] knowledge base. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may be triggered for generic decision-making questions outside retail product selection. <br>
Mitigation: Install it only for retail product-selection workflows and configure routing so unrelated decision-making requests do not invoke it. <br>
Risk: Purchase history or customer preference data can expose unnecessary personal information if passed into the recommendation flow. <br>
Mitigation: Disclose purchase-history use and pass only the minimum customer data needed to make the recommendation. <br>
Risk: Fallback behavior can surface products over budget or outside stated constraints when no exact match is available. <br>
Mitigation: Clearly label products that exceed budget or constraints, or show them only after the customer consents to broader results. <br>


## Reference(s): <br>
- [Product Recommender on ClawHub](https://clawhub.ai/fangwei-frank/product-recommender) <br>
- [Intent Extraction Guide](references/intent-extraction.md) <br>
- [Product Filtering & Scoring Logic](references/filtering-logic.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Markdown guidance and JSON recommendation data from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a ranked shortlist, reasons, optional upsell candidate, budget-relaxation flag, and intent used when the helper script is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
