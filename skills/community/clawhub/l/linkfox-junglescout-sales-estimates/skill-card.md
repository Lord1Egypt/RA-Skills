## Description: <br>
This skill queries daily sales estimates and last known price for a specified Amazon ASIN over a date range across supported Amazon marketplaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External marketplace sellers, analysts, and e-commerce operators use this skill to estimate ASIN-level daily sales, compare sales trends, and review recent known prices for competitor or product research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a LinkFox API key and sends ASIN, marketplace, and date-range queries to LinkFox. <br>
Mitigation: Use a dedicated key with appropriate access, avoid submitting sensitive product research unless approved, and rotate or revoke the key when access is no longer needed. <br>
Risk: The release evidence reports automatic feedback behavior that may send interaction feedback to LinkFox without interrupting the user flow. <br>
Mitigation: Review or disable feedback submission before installation, and allow feedback only after the exact content has been reviewed and approved. <br>


## Reference(s): <br>
- [Jungle Scout ASIN Sales Estimates API Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown summaries and tables, JSON API responses, and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Queries require marketplace, ASIN, start date, and an end date before the current date.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
