## Description: <br>
End-to-end stablecoin payments for links, invoices, receipts, and dashboards across Telegram, WhatsApp, and Discord. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OFUZORCHUKWUEMEKE](https://clawhub.ai/user/OFUZORCHUKWUEMEKE) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, merchants, fundraisers, and service providers use this skill to let an agent create and check USDC payment links, invoices, fundraising campaigns, dashboards, and payment history from chat or OpenClaw workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent receives API-key access that can create and inspect payment workflows in the user's Obverse account. <br>
Mitigation: Use a separate restricted API key where available and require explicit human confirmation before creating invoices, payment links, or fundraising campaigns. <br>
Risk: Dashboard credentials and customer payment data may appear in normal agent outputs. <br>
Mitigation: Avoid sharing dashboard passwords in shared chats or logs, and limit dashboard access to trusted users for the shortest practical time. <br>
Risk: Payment links can collect customer contact details and other custom fields. <br>
Mitigation: Collect or export customer data only with consent, document the purpose, and apply a clear retention policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/OFUZORCHUKWUEMEKE/obverse-payments) <br>
- [Obverse homepage](https://www.obverse.cc) <br>
- [Obverse API docs](https://obverse.onrender.com/api-docs) <br>
- [README](artifact/README.md) <br>
- [Deployment guide](artifact/DEPLOYMENT.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown or plain text with payment links, dashboard links, JSON command results, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OBVERSE_API_KEY; outputs can include payment identifiers, customer data, and temporary dashboard credentials.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact package.json and clawhub.json state 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
