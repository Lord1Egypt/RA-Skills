## Description:

This skill helps an agent work with HoneyBook client-portal data for vendor contracts, invoices, proposals, payment links, and signing links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

External HoneyBook client-portal users can ask an agent to inspect vendor sessions, list shared files, summarize contract or invoice status, and return portal deep links for confirmed signing or payment workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HoneyBook magic links and returned portal links may provide sensitive session access.

Mitigation: Treat pasted and returned links as sensitive, avoid sharing them broadly, and refresh sessions only from trusted vendor emails.

Risk: Signing or payment links could be used for the wrong vendor, contract, invoice, or amount.

Mitigation: Confirm the intended HoneyBook vendor and request details before using any returned signing or payment link.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chrischall/skills/honeybook-mcp)
- [Publisher Profile](https://clawhub.ai/user/chrischall)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown or plain text with HoneyBook portal status summaries and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sensitive session, signing, or payment links that should be reviewed before use.]

## Skill Version(s):

0.4.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
