## Description:

Tracks the user's stated to-dos and purchases, asks for confirmation before they count, and answers questions about open tasks and spending.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samuel-wei](https://clawhub.ai/user/samuel-wei)

### License/Terms of Use:

MIT-0

## Use Case:

HiJavis users use it to capture their own to-dos and spending from spoken or typed inputs, review pending entries, and ask for confirmed list or monthly spending totals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Personal details and short quotes are sent to the HiJavis server before confirmation, including possible content from shared conversations.

Mitigation: Review pending cards carefully before confirming them, especially when recordings may include other people.

Risk: An exposed gateway token or untrusted server connection could put ledger data at risk.

Mitigation: Keep the gateway token private and use a trusted HTTPS server address outside the internal container network.

Risk: The server's isolation, retention, and app controls were not verified.

Mitigation: Confirm the provider's data handling and controls before relying on the skill for sensitive records.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/samuel-wei/skills/javis-todo-spend-tracker)
- [HiJavis iPhone app](https://apps.apple.com/us/app/hijavis/id6745134765)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [Short chat responses and structured ledger entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Entries remain pending until user confirmation; spending totals keep currencies separate.]

## Skill Version(s):

0.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
