## Description: <br>
Searches eBay marketplaces for product listings, sold or completed listings, auctions, prices, seller details, and market-research filters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, e-commerce sellers, buyers, and agents use this skill to search eBay listings, compare prices, inspect sold listings, and browse regional eBay marketplaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries, filters, API key usage, and feedback content may be sent to LinkFox services. <br>
Mitigation: Use the skill only if LinkFox is trusted for those details, and avoid sensitive business or personal information in searches or feedback. <br>
Risk: The artifact asks agents to submit feedback and user-intent details through a separate LinkFox feedback endpoint. <br>
Mitigation: Submit feedback only with explicit user agreement, and keep feedback content limited to the issue needed for review. <br>
Risk: The skill returns current eBay listing data with documented limits, including no historical pricing data and a maximum of 200 results per page. <br>
Mitigation: Treat results as a current listing snapshot, paginate when needed, and avoid overusing fresh-cache bypass requests. <br>


## Reference(s): <br>
- [eBay Search API Reference](artifact/references/api.md) <br>
- [ClawHub Release Page](https://clawhub.ai/linkfox-ai/linkfox-ebay-search) <br>
- [LinkFox Skills](https://skill.linkfox.com/) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown tables, JSON API responses, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results may include product links, prices, seller information, shipping data, sold quantities, bids, and sponsored-listing markers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
