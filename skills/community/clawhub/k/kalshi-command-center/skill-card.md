## Description:

Complete Kalshi trading command interface for portfolio P&L, live market scanning with edge scoring, trade execution, and risk management through an OpenClaw agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kingmadellc](https://clawhub.ai/user/kingmadellc)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and traders use this skill to connect an OpenClaw agent to Kalshi for portfolio review, market scanning, order lookup, and trade execution. It is suited for users who can independently review trading decisions and manage Kalshi API credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place live Kalshi orders, and release security evidence warns that live order authority is paired with incomplete risk controls.

Mitigation: Use manual review before every trade and independently confirm price, quantity, exposure, and daily loss before running execution commands.

Risk: Kalshi API credentials and trade logs can expose sensitive account and trading information.

Mitigation: Store private keys and logs with restrictive file permissions and avoid sharing command output that includes account or order details.

Risk: The security guidance warns against running execute unless local Kalshalyst code it may load is trusted.

Mitigation: Run execute only in a trusted local environment after reviewing installed local dependencies and related OpenClaw skills.

## Reference(s):

- [Kalshi Command Center Documentation](SKILL.md)
- [Risk Limits Framework](references/risk-limits.md)
- [Heuristic Edge Scoring Algorithm](references/scoring.md)
- [Market Blocklist](references/blocklist.md)
- [Kalshi](https://kalshi.com)
- [ClawHub Skill Page](https://clawhub.ai/kingmadellc/skills/kalshi-command-center)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call the Kalshi API and write local trade audit logs when execution commands are run.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
