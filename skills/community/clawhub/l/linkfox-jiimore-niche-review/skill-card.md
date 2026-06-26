## Description: <br>
Helps agents query and summarize Jiimore-powered Amazon niche market review data so sellers can understand consumer sentiment, pain points, review themes, and demand signals across supported marketplaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Amazon sellers and market researchers use this skill to inspect niche-level customer review topics, sentiment, and pain points for keywords in the US, Japan, or Germany marketplaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries and feedback may send Amazon market-research intent, satisfaction, or interaction details to LinkFox endpoints. <br>
Mitigation: Use only with approval for sharing this information with LinkFox, and prevent or explicitly approve feedback submissions that include user intent or interaction details. <br>
Risk: The security scan verdict is suspicious because the skill asks the agent to silently report feedback to a separate LinkFox endpoint. <br>
Mitigation: Review feedback behavior before installation and disable or gate feedback submissions where silent reporting is not acceptable. <br>


## Reference(s): <br>
- [Jiimore Niche Review API Reference](references/api.md) <br>
- [ClawHub release page](https://clawhub.ai/linkfox-ai/linkfox-jiimore-niche-review) <br>
- [LinkFox tool gateway endpoint](https://tool-gateway.linkfox.com/jiimore/getNicheReviewFromKeyword) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown tables and concise narrative guidance, with optional shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses keyword-based query parameters and marketplace filters; requires a LinkFox API key in LINKFOXAGENT_API_KEY for direct script execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
