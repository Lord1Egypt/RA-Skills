## Description: <br>
Queries itick.org for real-time stock quotes, stock information, IPO events, split factors, market depth, trades, and K-line data across supported global markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChnMasterOG](https://clawhub.ai/user/ChnMasterOG) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to compose authenticated itick.org API requests for stock market data, including current quotes, company information, IPO data, split factors, trades, depth, and K-line history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release was flagged as suspicious because its documentation exposes a concrete API token in examples. <br>
Mitigation: Use a dedicated ITICK_API_TOKEN from the environment, do not copy example tokens, and rotate any token that may have been exposed. <br>
Risk: The skill sends market-data requests to itick.org using the configured token. <br>
Mitigation: Install only if you trust itick.org and are comfortable providing a scoped token for read-only stock quote queries. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ChnMasterOG/itick-stock-quote) <br>
- [itick.org stock API examples](https://api.itick.org) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with bash curl examples and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ITICK_API_TOKEN for authenticated market-data requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and claw.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
