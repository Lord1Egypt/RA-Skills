## Description: <br>
Etsy product research helper that uses LinkFox/EHunt `_ehunt_productQuery` to filter listings by keyword or URL, price, sales, favorites, reviews, listing date, category, product type, and marketplace badges. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, ecommerce researchers, and agents use this skill to query Etsy listing data through LinkFox/EHunt for product sourcing and market screening. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Etsy keywords, listing URLs, filters, and API credentials are sent to the LinkFox/EHunt service for user-directed product research. <br>
Mitigation: Use an approved LinkFox API key and avoid including private or sensitive business information in queries unless sharing it with that provider is acceptable. <br>


## Reference(s): <br>
- [_ehunt_productQuery API Reference](references/api.md) <br>
- [ClawHub Skill Listing](https://clawhub.ai/linkfox-ai/linkfox-ehunt-etsy-product-query) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON responses and concise Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY; pageSize supports 1-100 with 50 or fewer recommended.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
