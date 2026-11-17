## Description:

Systematically finds markets with huge asymmetric payoff -- markets priced at 2-10% where cross-category macro analysis suggests the REAL probability is 15-30%.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and operators use this skill to scan Polymarket prediction markets for low-probability macro longshots, score cross-category support signals, and place simulated or explicitly enabled live trades through Simmer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place real Polymarket trades and expose account funds to loss.

Mitigation: Run in the default paper mode unless live trading is intentionally enabled, keep live account funds limited, and require explicit review before using --live.

Risk: Security evidence says some advertised financial safeguards are not actually enforced in the code.

Mitigation: Do not rely on documented volume, concurrent-position, or longshot-size safeguards until enforcement is verified; review carefully before installing or enabling live mode.

Risk: The required Simmer API key grants trading authority.

Mitigation: Use a least-privilege key where possible, protect it as a high-value credential, and rotate it if exposure is suspected.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/diagnostikon/skills/polymarket-macro-asymmetric-longshot-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can perform Simmer API calls and place simulated trades by default; live Polymarket trading requires explicit live-mode execution.]

## Skill Version(s):

0.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
