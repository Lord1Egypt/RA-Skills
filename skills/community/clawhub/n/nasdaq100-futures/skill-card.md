## Description: <br>
Fetch the latest Nasdaq-100 futures quote (default NQ=F) via Yahoo Finance chart API using Node.js and return price, change, percent change, and timestamp. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lbl581581](https://clawhub.ai/user/lbl581581) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to retrieve the latest Nasdaq-100 futures quote, or another Yahoo Finance symbol, and return price, change, percent change, timestamp, and a concise summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts Yahoo Finance with the requested ticker symbol. <br>
Mitigation: Install only when outbound access to Yahoo Finance is acceptable for the deployment environment. <br>
Risk: Returned quotes are market data and may depend on market hours, provider availability, or delayed upstream data. <br>
Mitigation: Treat the output as informational market data for display or analysis, not as financial advice. <br>
Risk: The default summary message is in Chinese. <br>
Mitigation: Confirm that Chinese output is appropriate for the agent's users or adjust the skill before deployment. <br>


## Reference(s): <br>
- [OpenClaw runtime notes](references/openclaw.md) <br>
- [ClawHub skill page](https://clawhub.ai/lbl581581/nasdaq100-futures) <br>
- [Yahoo Finance chart API endpoint](https://query1.finance.yahoo.com/v8/finance/chart/) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, api calls] <br>
**Output Format:** [JSON object with string-formatted market values and a human-readable Chinese summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts an optional Yahoo Finance symbol parameter and defaults to NQ=F.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
