## Description: <br>
Connects to Preny AI Chatbot so an agent can summarize and analyze sales, customer, conversation, conversion, and tag data in near real time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nguyentdam](https://clawhub.ai/user/nguyentdam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Shop owners, sales teams, managers, and customer support teams use this skill to ask natural-language questions about Preny sales and CRM performance, including customer counts, conversations, conversions, revenue, and customer tags. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Preny token that can access business and customer data. <br>
Mitigation: Use a scoped official API credential where possible, keep the token out of shell startup files and repositories, rotate it if exposed, and install only when the publisher is trusted. <br>
Risk: Bundled conversation tools can read customer conversations and send customer-facing replies. <br>
Mitigation: Review conversation access before use and use the reply helper only when a human explicitly intends to send the message. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/nguyentdam/preny-analytics) <br>
- [Preny website](https://preny.ai) <br>
- [Preny app](https://app.preny.ai) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [How to get Preny Token](docs/how-to-get-token.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and terminal-oriented text with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and PRENY_TOKEN; some bundled scripts also reference PRENY_API_KEY and PRENY_WORKSPACE_ID.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release evidence and artifact/claw.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
