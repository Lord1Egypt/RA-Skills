## Description:

Trades Polymarket prediction markets on music streaming milestones, album chart performance, Grammy nominations, concert tour revenues, and music industry deals using entertainment-market signals and configurable risk controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to discover music and entertainment prediction markets, evaluate YES/NO trade signals, and place paper or explicitly enabled live Polymarket trades through Simmer. It is suited for entertainment-market experimentation where users can review and tune position sizing, volume, spread, and threshold settings before live use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live trading controls may be inaccurate or only partly enforced.

Mitigation: Use paper mode first, then verify volume, per-trade size, open-position, loss, spread, and threshold limits before enabling live trading.

Risk: A live-capable trading API key is passed to an unpinned dependency.

Mitigation: Pin and review simmer-sdk before live use, and use a narrowly scoped revocable key with no withdrawal authority.

Risk: Automated trades can create real USDC exposure when --live is explicitly used.

Mitigation: Keep the default paper mode for testing and set server-side trade and loss limits before supplying live credentials.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/diagnostikon/skills/polymarket-music-entertainment-trader)
- [Spotify Charts](https://charts.spotify.com/charts/overview/global)
- [Billboard Charts](https://www.billboard.com/charts/)
- [Chartmetric](https://chartmetric.com/)
- [RIAA Gold and Platinum Database](https://www.riaa.com/gold-platinum/)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk source repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and runtime log text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit paper or live trade logs; live trading requires an explicit --live flag and SIMMER_API_KEY.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
