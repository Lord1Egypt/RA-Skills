## Description: <br>
Build autonomous AI features using the Polsia Agent API only; never call model providers directly for product AI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentlevier](https://clawhub.ai/user/agentlevier) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to build autonomous AI features through the Polsia Agent API, including agent runs, chat flows, and connected Gmail, GitHub, Slack, Calendar, or Sheets tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Polsia API key and connected Gmail, GitHub, Slack, Calendar, or Sheets permissions may expose sensitive account data. <br>
Mitigation: Trust the Polsia API proxy before use and limit POLSIA_API_KEY and connected service permissions to the minimum needed. <br>
Risk: The send_email and save_data tools can send messages or store sensitive user data. <br>
Mitigation: Require user approval in workflows that send email or store sensitive user data. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/agentlevier/polsia-agent-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, configuration] <br>
**Output Format:** [Markdown guidance with API usage constraints and tool references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires POLSIA_API_URL and POLSIA_API_KEY; connected tool permissions may enable email sending and data storage.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
