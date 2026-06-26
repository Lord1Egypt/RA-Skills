## Description: <br>
Retrieves structured Amazon product details by ASIN through the LinkFox Keepa API, including pricing, images, listing dates, product specifications, FBA fees, sales rank, and monthly sales history when requested. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, analysts, and agents use this skill to look up one or more known Amazon ASINs and present product, pricing, specification, FBA fee, rank, and monthly sales information for marketplace analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send feedback, user intent, or conversation-derived details to a separate LinkFox feedback endpoint without an explicit user-facing consent step. <br>
Mitigation: Review or disable automatic feedback behavior before deployment, and only send feedback after users explicitly consent to sharing the relevant details with LinkFox. <br>
Risk: Amazon ASIN lookups require a LinkFox API key and send lookup parameters to LinkFox's tool gateway. <br>
Mitigation: Deploy only where LINKFOXAGENT_API_KEY use and LinkFox processing are approved, and avoid submitting sensitive or unrelated user data with ASIN lookup requests. <br>


## Reference(s): <br>
- [Keepa Amazon Product Detail API Reference](references/api.md) <br>
- [ClawHub Skill Listing](https://clawhub.ai/linkfox-ai/linkfox-keepa-product-detail) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, JSON, Shell commands] <br>
**Output Format:** [Markdown summaries and tables, JSON API responses, and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY; supports up to 100 comma-separated ASINs, numeric Amazon marketplace domain IDs, and an optional history flag.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
