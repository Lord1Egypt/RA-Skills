## Description:

Browse, trade, and manage positions on Polymarket prediction markets via the polymarket CLI, including market search, price checks, portfolio views, order management, and expiry arbitrage scanning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guzus](https://clawhub.ai/user/guzus)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to inspect Polymarket markets, retrieve JSON market data, check prices and order books, manage wallet-backed trades, and run helper scans for expiry-based pricing opportunities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer scripts fetch and execute remote artifacts and may build from source without pinned verification.

Mitigation: Review or replace the installer with pinned, verified Polymarket CLI artifacts before deployment.

Risk: Wallet-backed commands can place trades, approve contracts, bridge funds, import wallets, or otherwise affect assets.

Mitigation: Prefer read-only commands unless trading is intentional, and require explicit wallet setup and human review before asset-moving operations.

Risk: Command-line private key import can expose sensitive wallet material through shell history or process metadata.

Mitigation: Do not paste real private keys into command lines; use safer wallet setup procedures and secret handling.

Risk: The expiry arbitrage helper interpolates user query text into a shell command.

Mitigation: Avoid running scripts/expiry-arb.ts with untrusted query text until shell interpolation is fixed.

## Reference(s):

- [Polymarket Docs](https://docs.polymarket.com)
- [Polymarket CLI GitHub](https://github.com/Polymarket/polymarket-cli)
- [ClawHub Skill Page](https://clawhub.ai/guzus/skills/mgnlia-polymarket)
- [ClawHub Publisher Profile](https://clawhub.ai/user/guzus)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent-facing guidance emphasizes JSON output for scripted Polymarket CLI use.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter version is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
