## Description: <br>
Trades Polymarket YouTube channel markets for subscriber milestones and view-count races using simmer-sdk, with paper trading by default and real trades only when run with --live. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to discover YouTube-related Polymarket markets, compute conviction from channel-specific heuristics, and place paper or explicit live trades through Simmer. It is suited to users who understand prediction-market and automated-trading risk. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can spend real USDC on Polymarket when --live is supplied. <br>
Mitigation: Start in paper mode, use --live deliberately, and set conservative limits such as SIMMER_MAX_POSITION, SIMMER_MAX_POSITIONS, and SIMMER_MIN_TRADE. <br>
Risk: The skill may evaluate broader YouTube and creator markets beyond the top-10 framing. <br>
Mitigation: Review candidate markets and configuration before deployment, especially keyword coverage and broad search behavior. <br>
Risk: SIMMER_API_KEY grants trading authority and should be treated as a high-value credential. <br>
Mitigation: Use a revocable or least-privileged key when available, store it securely, and rotate it if exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-youtube-channel-trader) <br>
- [Simmer skills](https://simmer.markets/skills) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Console text with trade, skip, warning, and completion lines] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY; defaults to paper trading unless --live is supplied.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
