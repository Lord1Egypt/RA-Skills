## Description:

Trades Polymarket prediction markets on stock index milestones, major IPOs, earnings surprises, analyst upgrades, and company-specific financial events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to discover equity-related Polymarket markets and size simulated or live trades based on configured thresholds, market filters, and equity-market bias logic.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place real Polymarket trades when run with live authority, and server security evidence says its live-trading safeguards are not reliable enough for the requested financial authority.

Mitigation: Keep live mode disabled until reviewed, use paper trading by default, and only test with tightly scoped credentials and strict spending limits.

Risk: The SIMMER_API_KEY credential grants trading authority and is treated by the security evidence as high value.

Mitigation: Store the credential in an isolated environment, rotate it if exposed, and avoid sharing it across unrelated automations.

Risk: Volume filters, account-wide position limits, and live-versus-paper client separation require review before live deployment.

Mitigation: Verify those controls against a small account or sandbox workflow before enabling live trading.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-equity-markets-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, Python code, JSON configuration, and command-line output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY and defaults to paper trading unless live mode is explicitly enabled.]

## Skill Version(s):

0.0.3 (source: server release metadata; artifact frontmatter version 1.0 and artifact clawhub.json version 0.0.2 differ)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
