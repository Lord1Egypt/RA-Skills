## Description:

Trades Polymarket prediction markets on FDA drug approvals, biotech IPOs, clinical trial outcomes, pharma M&A, and precision medicine milestones using biotech event and market signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run or adapt an automated Polymarket trading agent for biotech and FDA event markets, with paper trading as the default and live trading only when explicitly enabled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place real-money prediction-market trades when configured for live execution.

Mitigation: Use paper mode first, keep live-capable credentials out of automated environments until reviewed, and require explicit --live use for real trading.

Risk: Advertised FDA/PDUFA/base-rate intelligence and some safeguards may not fully match the implementation.

Mitigation: Do not rely on those signals or volume/open-position controls unless the implementation is fixed or account-side limits independently constrain exposure.

Risk: The skill depends on simmer-sdk for market access and trade execution.

Mitigation: Pin and review the simmer-sdk dependency before using live-capable keys.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-biotech-trader)
- [FDA drug review process](https://www.fda.gov/patients/drug-development-process/step-4-fda-drug-review)
- [ClinicalTrials.gov API](https://clinicaltrials.gov/api/)
- [SEC EDGAR biotech search](https://efts.sec.gov/LATEST/search-index?q=%22biotech%22&dateRange=custom)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk source repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, API calls]

**Output Format:** [Console text logs and Simmer/Polymarket trade requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY; defaults to paper trading and only attempts live Polymarket trades when --live is passed.]

## Skill Version(s):

0.0.3 (source: server release evidence; artifact frontmatter reports 1.0 and clawhub.json reports 0.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
