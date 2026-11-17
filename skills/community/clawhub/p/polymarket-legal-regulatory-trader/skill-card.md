## Description:

Trades Polymarket prediction markets on landmark court cases, antitrust rulings, SEC enforcement actions, EU regulatory decisions, and DOJ investigations using legal and regulatory market signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to identify and optionally execute paper or live Polymarket trades tied to legal and regulatory prediction markets. It is intended for users who can evaluate legal-market signals and manage trading risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live trading can place real Polymarket orders using a high-value Simmer API key.

Mitigation: Use paper mode by default, require an explicit live-mode review before execution, and use a narrowly scoped, low-balance credential.

Risk: Live-trading safeguards may not fully prevent trades outside the user's safety expectations.

Mitigation: Pin and review simmer-sdk, verify the effective venue before every order, and keep account-side limits aligned with the configured maximum position.

Risk: Market filters and position sizing depend on configurable thresholds that can materially change trading exposure.

Mitigation: Review minimum volume, maximum spread, maximum position, and maximum open-position settings before enabling live use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/diagnostikon/skills/polymarket-legal-regulatory-trader)
- [diagnostikon Publisher Profile](https://clawhub.ai/user/diagnostikon)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Console text and Markdown guidance with configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or place paper trades by default; live Polymarket trading requires an explicit live flag and a Simmer API key.]

## Skill Version(s):

0.0.3 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
