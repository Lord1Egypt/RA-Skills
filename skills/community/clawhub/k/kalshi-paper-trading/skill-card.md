## Description:

Kalshi-native paper trading ledger and CLI for binary prediction contracts. Use for paper opens, marks, reconciliation, valuation, and review without relying on the generic spot-style paper trader.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brs999](https://clawhub.ai/user/brs999)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to manage Kalshi-specific paper trading workflows, including account setup, paper opens and closes, quote marks, settlement reconciliation, valuation, and performance review. It is designed for binary prediction contracts that need cent-denominated accounting and Kalshi-native exposure rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live market lookup commands can be configured to request arbitrary base URLs.

Mitigation: Keep KALSHI_BASE_URL and --kalshi-base-url pointed at the official Kalshi API unless intentionally testing, and do not let untrusted prompts choose that URL.

Risk: The skill maintains a persistent local paper-trading database.

Mitigation: Install and run it only where local paper-trading records are acceptable, and review the configured database path before use.

## Reference(s):

- [Kalshi Documentation](https://docs.kalshi.com)
- [Kalshi Paper Ledger Proposal](references/kalshi-paper-ledger.md)
- [ClawHub Skill Page](https://clawhub.ai/brs999/skills/kalshi-paper-trading)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash command blocks and JSON-capable CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node and writes paper-trading state to a local SQLite database.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
