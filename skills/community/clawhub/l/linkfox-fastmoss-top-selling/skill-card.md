## Description: <br>
Queries FastMoss data for TikTok Shop top-selling product rankings by market, category, and day, week, or month period. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and ecommerce operators use this skill to inspect TikTok Shop top-selling products across supported markets, categories, and time windows. It helps agents return ranking tables with sales, GMV, growth, shop, category, commission, and delisting fields. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs agents to automatically report feedback, user intent mismatches, and improvement notes to a separate LinkFox endpoint. <br>
Mitigation: Disable feedback reporting or require explicit user approval before sending feedback, and do not include private business plans, customer data, or sensitive commercial context in feedback payloads. <br>
Risk: The skill requires a LinkFox API key for FastMoss/TikTok ranking queries. <br>
Mitigation: Store LINKFOXAGENT_API_KEY in the runtime environment, avoid printing or committing it, and install only where use of that credential is approved. <br>


## Reference(s): <br>
- [FastMoss TikTok top selling API reference](artifact/references/api.md) <br>
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/linkfox-fastmoss-top-selling) <br>
- [LinkFox FastMoss product ranking endpoint](https://tool-gateway.linkfox.com/fastmoss/productRankTopSelling) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown tables and explanatory text, with optional JSON returned by the bundled Python script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY. pageSize is capped at 10 and ranking data has a T+1 statistical delay.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
