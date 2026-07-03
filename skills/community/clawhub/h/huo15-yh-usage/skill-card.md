## Description: <br>
Huo15 Yh Usage helps an agent use a customer-provided Huo15 Fireworks-style API key to retrieve token usage and billing summaries by provider, model, and day, with CNY and USD output options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaobod1](https://clawhub.ai/user/zhaobod1) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, support teams, and customer-facing teams use this skill to produce a concise usage and cost report for a single authorized Huo15 API key. It is suited for answering questions about total spend, expensive models or providers, and recent usage trends. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow sends a user-provided fsk API key to the Huo15 billing endpoint. <br>
Mitigation: Use only keys the user is authorized to inspect, keep the key out of shared chats and shell history where possible, and confirm the request targets the documented Huo15 usage endpoint. <br>
Risk: The report covers only the single API key supplied by the user. <br>
Mitigation: State that multi-key account totals require the account console or another authorized aggregation path. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaobod1/skills/huo15-yh-usage) <br>
- [Huo15 usage endpoint](https://fireworks-simulator-api.huo15.com/v1/usage?days=30) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown billing report with optional raw JSON output and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports can cover 1 to 90 days and can display costs in CNY or converted USD.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
