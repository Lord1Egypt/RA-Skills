## Description: <br>
Queries Keepa-powered Amazon product history for a single ASIN, including price, BSR, rating, seller count, and monthly sales trends across supported marketplaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Amazon sellers and ecommerce operators use this skill to inspect product-level historical price, sales-rank, rating, seller-count, and sales-volume trends for a specific ASIN. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ASIN lookup details and API-key-authenticated requests are sent to LinkFox infrastructure. <br>
Mitigation: Use the skill only for ASIN research that can be shared with LinkFox, and protect the LINKFOXAGENT_API_KEY as a credential. <br>
Risk: The artifact asks agents to send user-derived feedback summaries, including user intent or statements, to a separate LinkFox endpoint. <br>
Mitigation: Disable or make feedback submission opt-in before use with confidential competitive research or sensitive user statements. <br>


## Reference(s): <br>
- [Keepa API Reference](references/api.md) <br>
- [LinkFox Keepa Product Series API](https://tool-gateway.linkfox.com/keepa/productSeries) <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfox-keepa-product-history) <br>
- [LinkFox Publisher Profile](https://clawhub.ai/user/linkfox-ai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown guidance with JSON request examples and optional shell command execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Queries are limited to one ASIN per request and up to 365 days of historical data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
