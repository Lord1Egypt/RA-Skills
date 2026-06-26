## Description: <br>
Queries Jiimore Amazon niche market data and helps agents present market metrics, pricing, competition, reviews, inventory, and growth trends for a supplied niche ID. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, Amazon sellers, and ecommerce analysts use this skill to retrieve and summarize Jiimore niche-market intelligence for a known nicheId in the US, JP, or DE marketplaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can silently send broad feedback about user interactions to a separate LinkFox feedback API. <br>
Mitigation: Install only if that reporting is acceptable, review when feedback is sent, and use a scoped, revocable LINKFOXAGENT_API_KEY. <br>


## Reference(s): <br>
- [Jiimore API Reference](references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfox-jiimore-niche-info) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Markdown, Guidance] <br>
**Output Format:** [JSON API responses summarized as Markdown tables and sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY; queries one nicheId per request; supports US, JP, and DE marketplaces.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
