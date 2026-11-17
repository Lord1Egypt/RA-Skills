## Description:

Track earnings, payouts, uptime, and fiat estimates across multiple passive crypto income apps with summaries, alerts, and export options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mariusfit](https://clawhub.ai/user/mariusfit)

### License/Terms of Use:

MIT

## Use Case:

Developers, homelab operators, and crypto node operators use this skill to monitor passive income services, summarize earnings, track payout thresholds, and export history for reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to handle sensitive account, session, API, or node credentials.

Mitigation: Use dedicated, revocable, read-only tokens where possible, avoid command-line exposure of session tokens or private node keys, and rotate credentials if they may have been exposed.

Risk: Earnings data may be sent to WhatsApp or Telegram alerts.

Mitigation: Confirm the destination accounts, message contents, and privacy expectations before enabling alerts.

Risk: The security review could not confirm that token storage encryption and outbound network restrictions are implemented as described.

Mitigation: Review the implementation before installation and verify encrypted local storage and expected outbound destinations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mariusfit/skills/passive-income-tracker)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and tabular status examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local configuration, encrypted token storage, messaging alerts, fiat conversion, and CSV or JSON export workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
