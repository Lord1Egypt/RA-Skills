## Description: <br>
Searches Walmart product listings by keyword, category, price range, sort order, store, and device view. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, marketplace researchers, and agents use this skill to find current Walmart listings, compare prices, check availability, and inspect seller or rating fields for product research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms, filters, store IDs, and the LinkFox API key are sent to LinkFox services. <br>
Mitigation: Avoid entering personal, confidential, credential, payment, or business-sensitive information in searches, filters, or store-specific queries. <br>
Risk: The skill documentation directs agents to report feedback to LinkFox without interrupting the user's flow, with unclear limits on what may be included. <br>
Mitigation: Disable, constrain, or review automatic feedback reporting before deployment, and ensure feedback content excludes sensitive user or business data. <br>


## Reference(s): <br>
- [Walmart API Reference](references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfox-walmart-search) <br>
- [Publisher Profile](https://clawhub.ai/user/linkfox-ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summaries and tables with optional JSON or shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Walmart product links, prices, ratings, review counts, stock status, sponsored labels, and pagination guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
