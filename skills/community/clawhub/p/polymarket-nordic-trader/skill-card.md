## Description:

Trades Polymarket prediction markets focused on Scandinavian and Nordic events, including politics, regional business milestones, local weather extremes, and sports outcomes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading-agent operators use this skill to find Nordic and Scandinavian Polymarket markets, produce conviction-based trade decisions, and run paper trades by default or live trades when explicitly enabled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can submit real Polymarket orders when run with --live.

Mitigation: Use paper mode first, require an explicit operator decision before live mode, and use a dedicated least-privilege Simmer/Polymarket credential.

Risk: Server security evidence reports gaps in live-trading safeguards, including a missing volume gate and max-position sizing issue.

Mitigation: Fix or account for those controls before risking funds, and keep live-capable credentials out of unattended automation until reviewed.

Risk: The skill depends on simmer-sdk for market access and trade execution.

Mitigation: Pin and review simmer-sdk before providing live credentials or deploying the skill in an environment with trading authority.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-nordic-trader)
- [SMHI weather data](https://www.smhi.se/)
- [Riksdagen open data](https://data.riksdagen.se/)
- [Statistics Sweden](https://www.scb.se/)
- [SVT Nyheter](https://www.svt.se/nyheter/)
- [Di.se](https://www.di.se/)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk source repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples and Python execution output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY and produces paper trading behavior by default; live Polymarket orders require an explicit --live flag.]

## Skill Version(s):

0.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
