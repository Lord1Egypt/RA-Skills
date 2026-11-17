## Description:

World Cup Groups skill that simulates or automates market-dynamics trades on group-winner markets by buying pre-tournament favorites, trimming after market repricing, and trading confirmed incoherent group market sets back toward consistency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bridgeaisocial](https://clawhub.ai/user/bridgeaisocial)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading-automation users use this skill to discover 2026 World Cup group-winner markets, review active and importable candidates, and run sim-first or live guarded trading passes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated prediction-market trading can lose money when live mode is enabled.

Mitigation: Run dry-run or sim mode first, review all settings, and avoid funded credentials until exit and position reconciliation behavior has been reviewed.

Risk: The trading SDK dependency is unpinned in the artifact.

Mitigation: Use a pinned, audited simmer-sdk version before production use.

Risk: Live credentials could permit unintended account activity.

Mitigation: Use narrowly scoped API credentials and account-side spending limits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bridgeaisocial/skills/polymarket-worldcup-group-repricer)
- [Publisher profile](https://clawhub.ai/user/bridgeaisocial)
- [Disclaimer](artifact/DISCLAIMER.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration details, and text status reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY and simmer-sdk; the managed entrypoint is scripts/group_repricer.py.]

## Skill Version(s):

0.2.0 (source: server release metadata, artifact metadata, and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
