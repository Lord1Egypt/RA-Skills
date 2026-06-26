## Description: <br>
Trades Polymarket prediction markets on celebrity events, viral social media moments, Elon Musk tweet counts, influencer milestones, and reality TV outcomes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to discover celebrity and social-media Polymarket markets, size paper or live trades, and apply configurable safeguards for position size, spread, market volume, and resolution timing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real Polymarket trades when live mode is explicitly enabled. <br>
Mitigation: Start in paper mode, review candidate markets before using --live, and keep position limits low. <br>
Risk: SIMMER_API_KEY grants trading authority and is a high-value credential. <br>
Mitigation: Protect the key, avoid exposing it in logs or shared environments, and rotate it if it may have been disclosed. <br>
Risk: Keyword-based market discovery can include markets outside the user's intended celebrity or social-media scope. <br>
Mitigation: Review candidate markets and narrow the keyword list for tighter live-trading scope. <br>


## Reference(s): <br>
- [Polymarket Celebrity Social Trader on ClawHub](https://clawhub.ai/diagnostikon/polymarket-celebrity-social-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Console text with trade, skip, warning, and completion status lines] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY; defaults to paper trading and uses --live for real Polymarket trades.] <br>

## Skill Version(s): <br>
0.0.3 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
