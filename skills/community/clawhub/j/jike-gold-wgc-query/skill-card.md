## Description: <br>
Queries current and historical World Gold Council gold prices through the Jike API, with filters for date, weight unit, and currency. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer current or historical international gold price questions by running a Python helper backed by Jike API data. It returns price dates, update times, weight units, currencies, and prices, with a reminder that market data is not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script sends the configured Jike AppKey as a query parameter to the selected API base URL. <br>
Mitigation: Use the default jikeapi.cn endpoint or set JIKE_API_BASE_URL only to a trusted endpoint that is intended to receive the AppKey. <br>
Risk: Local .env support can persist the AppKey near the script. <br>
Mitigation: Keep any script-local .env file limited to the intended Jike key and avoid committing or sharing it. <br>
Risk: Gold price data may be mistaken for financial advice. <br>
Mitigation: Present returned prices as informational market data and preserve the skill's investment-advice caveat. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/jike-gold-wgc-query) <br>
- [Publisher profile](https://clawhub.ai/user/jikeapi-cn) <br>
- [Jike API homepage](https://www.jikeapi.cn/) <br>
- [Jike WGC latest gold price endpoint](https://api.jikeapi.cn/v1/gold/wgc/latest) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown conversation responses with shell command examples, configuration notes, tabular text output, and optional JSON API payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a Jike AppKey supplied through JIKE_GOLD_WGC_QUERY_KEY, JIKE_APPKEY, --key, or a local script .env file.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
