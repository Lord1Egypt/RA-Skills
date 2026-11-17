## Description:

Trades Polymarket prediction markets on celebrity events, viral social media moments, Elon Musk tweet counts, influencer milestones, and reality TV outcomes using keyword discovery, conviction sizing, and celebrity-market bias adjustments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to discover celebrity, influencer, and social-media prediction markets, size candidate trades, and optionally execute paper or live Polymarket orders through Simmer. It is intended for users who can review and harden financial trading automation before enabling live mode.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live trading can place real USDC orders, and evidence.security says live-trading safety boundaries and advertised risk controls are not reliably enforced.

Mitigation: Keep live mode disabled by default, use paper trading for validation, and fix client-mode and risk-limit enforcement issues before any real-money execution.

Risk: The required SIMMER_API_KEY grants trading authority and is a high-value credential.

Mitigation: Use a dedicated, limited Simmer credential, store it outside source files, rotate it if exposed, and restrict its permissions where the platform allows.

Risk: The skill depends on simmer-sdk for market discovery, context checks, and trade placement.

Mitigation: Pin and review the SDK dependency before deployment, then test behavior in paper mode after dependency updates.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/diagnostikon/skills/polymarket-celebrity-social-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk GitHub Repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [Text, API Calls, Shell commands, Configuration, Guidance]

**Output Format:** [Console logs and trading API calls, with Python configuration through environment variables and ClawHub tunables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY and simmer-sdk; defaults to paper trading unless live mode is explicitly enabled.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
