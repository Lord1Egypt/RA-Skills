## Description: <br>
ValueScan Skill Beta helps agents analyze cryptocurrency fund flows, whale activity, sector rotation, opportunity and risk tokens, and major-holder cost trends using ValueScan API data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[majincheng](https://clawhub.ai/user/majincheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query ValueScan cryptocurrency analytics for market signals, fund-flow monitoring, whale transaction analysis, sector rotation, and address-level position trends. The skill is useful when an agent needs structured crypto market context, but its outputs should not be treated as financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a ValueScan API key and secret stored locally for signed requests. <br>
Mitigation: Store credentials only in the documented local credentials file, restrict file access, and rotate keys if the local environment is shared or suspected to be exposed. <br>
Risk: Vague market questions can trigger API calls that consume ValueScan credits. <br>
Mitigation: Ask clarifying questions before making fund-flow, sentiment, or token-screening requests when the user's intent or scope is ambiguous. <br>
Risk: Crypto analytics outputs may be mistaken for investment advice. <br>
Mitigation: Present results as market-data analysis only and tell users to make independent financial decisions. <br>


## Reference(s): <br>
- [ValueScan homepage](https://beta.valuescan.io) <br>
- [ValueScan API documentation](https://beta-claw.valuescan.io/zh-CN/) <br>
- [ValueScan developer portal](https://beta.valuescan.io/dev-portal/home/) <br>
- [ValueScan SDK README](artifact/script/sdk/README.md) <br>
- [ValueScan endpoint references](artifact/references/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with optional JSON, JavaScript, and shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ValueScan API query guidance, credential configuration steps, signed request examples, endpoint selection, and market-analysis summaries.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
