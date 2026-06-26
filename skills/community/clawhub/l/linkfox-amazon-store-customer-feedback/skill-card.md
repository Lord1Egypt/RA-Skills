## Description: <br>
Helps agents call the Amazon SP-API Customer Feedback v2024-06-01 endpoints through LinkFox developer proxy scripts to inspect item and browse-node review topics, review trends, return topics, return trends, and item browse nodes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and Amazon selling-partner operators use this skill to retrieve customer feedback signals for ASINs and browse nodes, including review topics, review trends, return topics, return trends, and browse-node mapping. It is useful when comparing MENTIONS and STAR_RATING_IMPACT feedback dimensions or diagnosing category-level customer sentiment and returns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive credentials for LinkFox and Amazon SP-API access. <br>
Mitigation: Provide LINKFOXAGENT_API_KEY only in a trusted runtime, use least-privilege Amazon roles, and avoid sharing command histories or JSON outputs that may contain seller or token data. <br>
Risk: The security summary notes that adjudication was limited by missing target artifact availability during the supplied scan. <br>
Mitigation: Install only from the intended ClawHub listing and publisher handle, and compare release hashes with the server evidence before deployment. <br>
Risk: Customer Feedback endpoints can fail when Amazon roles, marketplace support, or gateway allowlists are incomplete. <br>
Mitigation: Confirm Brand Analytics or Selling Partner Insights access, supported marketplace IDs, and gateway allowance for customerFeedback/2024-06-01 before relying on the output. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/linkfox-ai/linkfox-amazon-store-customer-feedback) <br>
- [Local API reference](references/api.md) <br>
- [Amazon Customer Feedback API v2024-06-01 guide](https://developer-docs.amazon.com/sp-api/docs/customer-feedback-api-v2024-06-01-use-case-guide) <br>
- [getItemReviewTopics](https://developer-docs.amazon.com/sp-api/reference/getitemreviewtopics) <br>
- [getItemBrowseNode](https://developer-docs.amazon.com/sp-api/reference/getitembrowsenode) <br>
- [getBrowseNodeReviewTopics](https://developer-docs.amazon.com/sp-api/reference/getbrowsenodereviewtopics) <br>
- [getItemReviewTrends](https://developer-docs.amazon.com/sp-api/reference/getitemreviewtrends) <br>
- [getBrowseNodeReviewTrends](https://developer-docs.amazon.com/sp-api/reference/getbrowsenodereviewtrends) <br>
- [getBrowseNodeReturnTopics](https://developer-docs.amazon.com/sp-api/reference/getbrowsenodereturntopics) <br>
- [getBrowseNodeReturnTrends](https://developer-docs.amazon.com/sp-api/reference/getbrowsenodereturntrends) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with bash examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY and the companion linkfox-amazon-store-auth skill unless skipDepCheck is explicitly set.] <br>

## Skill Version(s): <br>
0.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
