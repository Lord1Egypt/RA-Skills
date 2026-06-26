## Description: <br>
Analyzes low-star Amazon reviews to extract product pain points and produce a product opportunity report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zzhimin](https://clawhub.ai/user/zzhimin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External product managers, e-commerce operators, and developers use this skill to analyze 1-3 star Amazon reviews, identify recurring product defects, and convert customer pain points into product and listing recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Amazon product URLs and review requests are sent to Bright Data. <br>
Mitigation: Install only if that third-party data flow is acceptable for the intended products and review requests. <br>
Risk: Bright Data API keys can be exposed through shared shell history or process listings when passed to the helper script. <br>
Mitigation: Use scoped Bright Data API keys and avoid running the helper script in shared shells or environments where process arguments are visible. <br>
Risk: The helper script writes extracted_reviews.json in the current working directory. <br>
Mitigation: Run the script only from a directory where creating or overwriting extracted_reviews.json is intended. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zzhimin/product-opportunity-analyzer) <br>
- [Bright Data Amazon Product Reviews API](https://api.brightdata.com/datasets/v3/amazon_product_reviews) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with structured tables, with intermediate JSON arrays for extracted review pain points.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The local helper script can write extracted_reviews.json and requires a Bright Data API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
