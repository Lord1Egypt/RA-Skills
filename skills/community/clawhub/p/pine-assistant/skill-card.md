## Description:

Handle customer service, bills, reservations, and more via Pine AI: negotiate, cancel, dispute, book, and resolve from the terminal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bojieli](https://clawhub.ai/user/bojieli)

### License/Terms of Use:


## Use Case:

External users and agents use Pine Assistant to create, monitor, and follow up on Pine AI sessions for customer service calls, bill negotiation, cancellations, disputes, reservations, appointments, outreach, and web-based account tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can delegate real-world actions through calls, emails, browser automation, and account workflows.

Mitigation: Confirm the intended task, session, payment state, and sensitive account details with the user before creating sessions, starting tasks, or sending information to Pine.

Risk: The required pine CLI and local credential file can affect user accounts and task data.

Mitigation: Install only from a trusted source, consider pinning or verifying pineai-cli, and protect ~/.pine/config.json.

Risk: The security evidence marks the release as suspicious because it grants broad authority to inspect task history and start user-impacting actions.

Mitigation: Review the skill before deployment and use it only for tasks where the user is comfortable sharing details with Pine and allowing delegated follow-up.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bojieli/skills/pine-assistant)
- [Pine Assistant homepage](https://pineclaw.com)
- [Pine AI](https://19pine.ai)
- [Pine privacy policy](https://www.19pine.ai/page/privacy-policy)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Pine session links, JSON CLI commands, and prompts for user-provided account, payment, OTP, PIN, or scheduling information.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
