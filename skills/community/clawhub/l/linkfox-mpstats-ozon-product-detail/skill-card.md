## Description: <br>
Batch-fetches full MPSTATS product cards for up to 100 Ozon Russia SKUs, including price, discounts, Ozon Card price, ratings, reviews, stock, sales, revenue, revenue potential, lost sales, first listing date, and images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketplace operators, product-sourcing teams, and commerce analysts use this skill to retrieve per-SKU Ozon product details and period metrics from MPSTATS for price, stock, rating, sales, revenue, and fulfillment checks. It is best suited when the user already has Ozon SKU IDs and needs compact product-card data or batch comparison. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a LinkFox API key and sends Ozon SKU lists, date windows, and possible feedback text to LinkFox-operated endpoints. <br>
Mitigation: Use a scoped, revocable LINKFOXAGENT_API_KEY, avoid submitting sensitive business notes as feedback, and install only when LinkFox is trusted for these data flows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfox-mpstats-ozon-product-detail) <br>
- [MPSTATS Ozon Product Detail API Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON-oriented summaries of API results, with optional shell commands for direct script usage.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results may include partial-success batch details, Ozon SKU product-card fields, and API error information.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
