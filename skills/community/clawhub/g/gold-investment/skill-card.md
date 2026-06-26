## Description: <br>
A gold investment analysis skill that retrieves current gold-market information and helps agents produce price, technical, fundamental, and risk-analysis reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FMouseBoy](https://clawhub.ai/user/FMouseBoy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to research gold prices, market news, technical indicators, and fundamental factors before preparing an informational gold-market analysis report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User queries are sent to Tavily for live gold-market search. <br>
Mitigation: Avoid including private financial details in prompts or search queries. <br>
Risk: Gold-market analysis may be mistaken for personalized investment advice. <br>
Mitigation: Treat generated analysis as informational and review it before making financial decisions. <br>


## Reference(s): <br>
- [Gold Investment Skill Page](https://clawhub.ai/FMouseBoy/gold-investment) <br>
- [Technical Indicators Reference](references/technical-indicators.md) <br>
- [Tavily](https://tavily.com/) <br>
- [Tavily Search API](https://api.tavily.com/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with source links and optional shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TAVILY_API_KEY for live search.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
