## Description: <br>
Queries LinkFox Jiimore data to help Amazon sellers analyze keyword-level niche markets, including demand, competition, brand concentration, advertising costs, launch success, and return-rate metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Amazon sellers and ecommerce analysts use this skill to research keyword-level market segments across supported Amazon marketplaces. It helps compare demand, sales, pricing, brand density, advertising saturation, and new-product opportunity signals. <br>

### Deployment Geography for Use: <br>
Global use; API data is limited to US, JP, and DE Amazon marketplaces. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send Amazon research keywords, filters, and a LinkFox API key to LinkFox services. <br>
Mitigation: Use only with data that is intended to be shared with LinkFox, and avoid proprietary keywords, business plans, personal details, or unredacted user comments unless that sharing is intentional. <br>
Risk: The skill text instructs agents to auto-report feedback and user-intent text to a separate LinkFox endpoint. <br>
Mitigation: Disable the feedback flow or require explicit user approval before sending feedback, dissatisfaction, praise, or improvement notes. <br>
Risk: The skill depends on live third-party API responses and supports only US, JP, and DE Amazon marketplaces. <br>
Mitigation: Confirm the target marketplace before use and present API errors or empty results as service or filter outcomes rather than definitive market conclusions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfox-jiimore-niche-by-keyword) <br>
- [Jiimore Niche Info API Reference](references/api.md) <br>
- [LinkFox Skills](https://skill.linkfox.com/) <br>
- [Jiimore Niche Info API Endpoint](https://tool-gateway.linkfox.com/jiimore/getNicheInfoByKeyword) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries and tables, JSON API responses, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY and a keyword; supports pagination, sorting, and filters for US, JP, and DE marketplace data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
