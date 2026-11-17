## Description:

Connects directly with Preny AI Chatbot to summarize and analyze sales, customer, conversation, and tag data in real time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nguyentdam](https://clawhub.ai/user/nguyentdam)

### License/Terms of Use:

MIT-0

## Use Case:

Shop owners, sales teams, managers, and customer-support teams use this skill to ask natural-language questions about Preny sales performance, customer activity, message volume, conversion signals, and tag-based CRM status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live Preny tokens may expose business or customer data if copied from browser sessions or stored insecurely.

Mitigation: Use a read-only, scoped Preny API credential where available, rotate exposed tokens promptly, and avoid storing tokens in shell startup files such as ~/.bashrc.

Risk: The artifact includes customer conversation and reply capabilities in addition to analytics reporting.

Mitigation: Enable conversation or reply scripts only when explicitly needed and authorized for customer-support operations; review any outbound message before sending.

Risk: The skill makes authenticated requests to Preny API hosts.

Mitigation: Verify configured API hosts before use and run the skill in an environment where credentials and network access are scoped to the intended Preny workspace.

## Reference(s):

- [Preny Analytics README](artifact/README.md)
- [Preny token setup guide](artifact/docs/how-to-get-token.md)
- [Preny](https://preny.ai)
- [Preny app](https://app.preny.ai)
- [OpenClaw](https://openclaw.ai)
- [ClawHub skill page](https://clawhub.ai/nguyentdam/skills/preny-analytics)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or terminal-formatted text with shell command examples and Preny analytics summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, and PRENY_TOKEN; some scripts also expect Preny API or workspace credentials.]

## Skill Version(s):

1.5.0 (source: server release metadata and artifact/claw.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
