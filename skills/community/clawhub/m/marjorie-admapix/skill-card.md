## Description: <br>
AdMapix helps agents search ad creatives, analyze apps, view rankings, track download and revenue estimates, and summarize market insights through the AdMapix API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marjoriebroad](https://clawhub.ai/user/marjoriebroad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing, growth, product, and competitive-intelligence users can use this skill to research ad creatives, app rankings, app performance estimates, advertising distribution, and market trends. The skill is also useful for agents that need bilingual English and Chinese reporting over AdMapix API results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-directed ad and app research queries and related query parameters to the AdMapix API. <br>
Mitigation: Use it only for queries appropriate to share with AdMapix and avoid submitting sensitive or confidential search terms. <br>
Risk: The skill requires an API key for the AdMapix service. <br>
Mitigation: Keep the key scoped to this skill, configure it through the environment, and do not paste it into chats, logs, or generated reports. <br>
Risk: Download and revenue outputs are third-party estimates rather than official figures. <br>
Mitigation: Label estimate-based results clearly and avoid presenting them as authoritative financial or store-reported data. <br>


## Reference(s): <br>
- [AdMapix website](https://www.admapix.com) <br>
- [Complete setup guide](https://skillboss.co/skill.md) <br>
- [Creative Search API](artifact/references/api-creative.md) <br>
- [Product & Company API](artifact/references/api-product.md) <br>
- [Ranking API](artifact/references/api-ranking.md) <br>
- [Download & Revenue API](artifact/references/api-download-revenue.md) <br>
- [App Distribution API](artifact/references/api-distribution.md) <br>
- [Market Analysis API](artifact/references/api-market.md) <br>
- [Parameter Mapping Reference](artifact/references/param-mappings.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summaries, tables, H5 result links, and inline shell commands for API-key checks and API calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responds in English or Chinese based on the user's language and labels download and revenue figures as third-party estimates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
