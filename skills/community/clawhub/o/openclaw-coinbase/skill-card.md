## Description:

Accesses the Coinbase API so agents can fetch balances, inspect EUR trading products, create market or limit crypto orders, and review order history and fills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mtrab](https://clawhub.ai/user/mtrab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to integrate Coinbase account, product, order, and fill operations into crypto trading workflows. It is intended for controlled use with human confirmation and least-privilege Coinbase API credentials before any trade is placed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place real crypto trades using stored Coinbase credentials without built-in confirmation or safety limits.

Mitigation: Require a manual confirmation step before create_order, enforce order-size limits and product allowlists, and use a separate least-privilege Coinbase API key.

Risk: Private key material is loaded from files near the script and could be exposed through source control, backups, or broad filesystem permissions.

Mitigation: Store credentials outside the skill directory when possible, keep credential files out of source control and backups, and restrict file permissions to the owning user.

Risk: Unpinned dependencies can change behavior or introduce supply-chain risk at install time.

Mitigation: Pin and review the cryptography and PyJWT dependencies before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mtrab/skills/openclaw-coinbase)
- [Publisher profile](https://clawhub.ai/user/mtrab)
- [Coinbase Developer Platform](https://portal.cdp.coinbase.com)

## Skill Output:

**Output Type(s):** [code, configuration, guidance]

**Output Format:** [Python module and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Coinbase API credentials from local key files and returns JSON-like Python data structures from API responses.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
