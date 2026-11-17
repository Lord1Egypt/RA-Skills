## Description:

Scan Polymarket prediction markets for book arbitrage opportunities in overbooked or underbooked multi-outcome markets, generate a formatted report, and deliver it via Telegram and email.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caoqi](https://clawhub.ai/user/caoqi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to scan active Polymarket multi-outcome markets, rank possible book-arbitrage opportunities, and schedule recurring reports for review before any trading decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The report sender can send email through the local Apple Mail account.

Mitigation: Review and restrict the .env recipient before scheduling or running the sender.

Risk: The sender uses shell execution around local scripts.

Mitigation: Install and run it only from a directory that is not writable or controlled by untrusted users.

Risk: Telegram delivery is described in the documentation but not implemented by the included sender script.

Mitigation: Treat Telegram instructions as inaccurate until the publisher updates the implementation.

## Reference(s):

- [Setup Guide](references/setup.md)
- [Polymarket Gamma API](https://gamma-api.polymarket.com)
- [ClawHub Skill Page](https://clawhub.ai/caoqi/skills/polymarket-opportunities-scanning)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JavaScript scripts, JSON scan output, and formatted report text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces opportunities.json and a formatted market-opportunity report for Telegram and email delivery.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
