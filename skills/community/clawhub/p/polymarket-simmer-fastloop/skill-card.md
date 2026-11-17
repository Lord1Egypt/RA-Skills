## Description:

Trade Polymarket BTC/ETH/SOL 5/15-minute fast markets with momentum and order book filters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andrewbrownrd](https://clawhub.ai/user/andrewbrownrd)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading automation users use this skill to run or adapt a Polymarket fast-market strategy that evaluates crypto momentum, order book, timing, and budget signals before proposing or executing trades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run recurring live trades and may spend real funds when live mode and a Polymarket venue are enabled.

Mitigation: Start in paper mode, keep strict external spending limits, review cron settings before enabling live execution, and maintain a fast disable path.

Risk: The security evidence reports an embedded external API credential and an unpinned SDK dependency.

Mitigation: Use narrowly scoped and revocable credentials, rotate any exposed credential, and ask the publisher to remove embedded secrets and pin dependencies before live use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andrewbrownrd/skills/polymarket-simmer-fastloop)
- [ClawHub publisher profile](https://clawhub.ai/user/andrewbrownrd)
- [Simmer Markets](https://simmer.markets)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, Python execution guidance, configuration values, and trading run summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit JSON automaton summaries and local ledger, cache, and spend files during execution.]

## Skill Version(s):

1.0.10 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
