## Description: <br>
Query Shopify sales, profitability, customers, and marketing data through Ned's API for ecommerce analytics questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[matt998759](https://clawhub.ai/user/matt998759) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Shopify merchants and their agents use this skill to answer profit, revenue, product performance, customer segment, churn risk, ad efficiency, and store health questions from Ned-connected business data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Ned API key that could expose Shopify analytics if shared or logged. <br>
Mitigation: Use a revocable or least-privileged Ned API key when available and avoid entering it in shared terminals, transcripts, or logs. <br>
Risk: Queries can return customer-level and churn-risk business data in agent conversations. <br>
Mitigation: Limit use to intended Ned-connected Shopify analytics workflows and avoid requesting sensitive customer details in shared chats. <br>


## Reference(s): <br>
- [Ned website](https://meetned.com) <br>
- [Ned API base](https://api.meetned.com/api/v1) <br>
- [ClawHub release page](https://clawhub.ai/matt998759/ned-analytics) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses NED_API_KEY for authenticated Ned API requests; API responses contain store analytics data.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
