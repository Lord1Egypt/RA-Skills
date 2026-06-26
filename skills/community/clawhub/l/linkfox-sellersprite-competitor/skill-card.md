## Description: <br>
Helps agents query and present SellerSprite Amazon competitor product data across supported marketplaces, including sales, BSR, pricing, ratings, seller, brand, category, and growth metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Amazon sellers and ecommerce analysts use this skill to discover competing products, benchmark product performance, and format competitor intelligence from SellerSprite data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Marketplace queries, ASINs, seller or brand filters, and automatic feedback summaries can be sent to LinkFox. <br>
Mitigation: Use the skill only in environments where LinkFox is trusted for Amazon research data, and avoid submitting confidential product strategy or customer-sensitive details. <br>
Risk: The API key enables requests to LinkFox services. <br>
Mitigation: Store the API key in the intended execution environment only, keep it out of shared transcripts and source files, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [SellerSprite Competitor API Reference](references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfox-sellersprite-competitor) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, JSON, shell commands, API calls] <br>
**Output Format:** [Markdown tables and explanatory text, with JSON request examples and optional shell command execution.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include paginated competitor results, marketplace-specific query parameters, metric explanations, and error-handling guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
