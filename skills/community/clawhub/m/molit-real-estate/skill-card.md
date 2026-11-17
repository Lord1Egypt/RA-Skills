## Description:

Retrieves MOLIT apartment sale transaction data from data.go.kr and helps summarize recent Korean real estate transactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sw326](https://clawhub.ai/user/sw326)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to look up Korean apartment sale transactions by district code and contract month, then summarize recent trades, price per pyeong, and related context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports that the bundled shell script can run unintended code if crafted arguments are passed to it.

Mitigation: Review and fix the script to validate inputs and pass arguments safely to Python before using it.

Risk: The skill requires a data.go.kr API key stored on disk.

Mitigation: Store the API key with restrictive file permissions or in a secret store, and avoid sharing generated outputs that expose credentials.

Risk: Government transaction data may lag actual real estate activity.

Mitigation: Treat summaries as point-in-time reference data and verify high-impact decisions against authoritative current sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sw326/skills/molit-real-estate)
- [Publisher profile](https://clawhub.ai/user/sw326)
- [MOLIT RTMS apartment trade API endpoint](https://apis.data.go.kr/1613000/RTMSDataSvcAptTrade)
- [data.go.kr](https://www.data.go.kr)
- [data.go.kr apartment trade OpenAPI listing](https://www.data.go.kr/data/15057511/openapi.do)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with transaction tables, setup instructions, shell commands, and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a data.go.kr API key and district/month query parameters; API responses may be delayed relative to transaction dates.]

## Skill Version(s):

2.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
