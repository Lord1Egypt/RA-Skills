## Description: <br>
Looks up MOLIT apartment real transaction price data and helps summarize Korean apartment sales by district and contract month. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sw326](https://clawhub.ai/user/sw326) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents use this skill to fetch and summarize South Korean apartment transaction records from the MOLIT data.go.kr API for market checks, trend review, and district comparisons. <br>

### Deployment Geography for Use: <br>
South Korea <br>

## Known Risks and Mitigations: <br>
Risk: The helper script has a code-execution risk when shell parameters are interpolated into inline Python. <br>
Mitigation: Review or fix the script before installation; pass inputs to Python as argv or environment variables and validate district code, YYYYMM, and row count. <br>
Risk: Credential handling is confusing and may expose or misplace the data.go.kr API key. <br>
Mitigation: Use a documented user-owned credential path or environment variable and store the API key with restrictive file permissions such as chmod 600. <br>
Risk: The skill contacts external data services and may optionally route related requests to search, law, weather, or finance tools. <br>
Mitigation: Confirm network access and downstream tool use are acceptable for the deployment environment before enabling the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sw326/molit-real-estate) <br>
- [data.go.kr](https://www.data.go.kr) <br>
- [MOLIT apartment sale transaction OpenAPI](https://www.data.go.kr/data/15057511/openapi.do) <br>
- [MOLIT apartment transaction endpoint](https://apis.data.go.kr/1613000/RTMSDataSvcAptTrade/getRTMSDataSvcAptTrade) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with JSON transaction data from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include apartment name, area, floor, price, price per pyeong, transaction date, and related legal or trend notes.] <br>

## Skill Version(s): <br>
2.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
