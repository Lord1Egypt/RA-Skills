## Description: <br>
Helps agents reverse-search US Amazon niches and keywords from historical opportunity metrics, including market size, growth, competition, price tiers, demographics, product features, and review themes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, ecommerce operators, and sourcing analysts use this skill to turn business criteria such as low competition, growth, price gaps, demographics, or review pain points into candidate US Amazon niches and keywords. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a LinkFox API key and sends screening queries to the LinkFox tool gateway. <br>
Mitigation: Use a scoped API key and avoid submitting secrets, sensitive customer data, or confidential business plans in queries. <br>
Risk: Server security guidance flags that the skill asks agents to send automatic free-form feedback without interrupting the user. <br>
Mitigation: Make feedback submission explicit and user-approved, or disable that behavior before deployment. <br>
Risk: Results are historical niche snapshots rather than real-time Amazon market data. <br>
Mitigation: Label outputs as collection-time snapshots and verify important business decisions against current market data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/linkfox-amazon-opportunity-screener) <br>
- [Publisher profile](https://clawhub.ai/user/linkfox-ai) <br>
- [API reference](references/api.md) <br>
- [LinkFox Skills](https://skill.linkfox.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, shell commands, guidance] <br>
**Output Format:** [Markdown tables and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns niche-level, time-snapshot Amazon opportunity data for the US marketplace.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
