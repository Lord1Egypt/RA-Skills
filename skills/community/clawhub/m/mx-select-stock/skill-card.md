## Description:

Screens A-share, Hong Kong, and U.S. stocks through the Meixiang smart stock-screening API using user-specified indicators, industries, or sectors, then returns current results as CSV with Chinese column descriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xpmars](https://clawhub.ai/user/xpmars)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to translate natural-language stock-screening requests into Meixiang API calls, retrieve current market screening results, and present or attach CSV data with column explanations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stock-screening keywords and the configured API key are sent to an external Meixiang endpoint.

Mitigation: Avoid including secrets, proprietary strategy text, or unrelated confidential information in screening keywords, and use an appropriately scoped API key.

Risk: Returned tables use Chinese column headers, which can be misunderstood by users who expect another language.

Mitigation: Ask the agent to translate or explain column names before relying on the results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xpmars/skills/mx-select-stock)
- [Meixiang stock-screening API endpoint](https://mkapi2.dfcfs.com/finskillshub/api/claw/stock-screen)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, CSV data, guidance]

**Output Format:** [Markdown guidance with curl commands, JSON parsing steps, and optional CSV and Markdown files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MX_APIKEY; stock-screening queries and the API key are sent to the Meixiang endpoint, and returned tables use Chinese column headers.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
