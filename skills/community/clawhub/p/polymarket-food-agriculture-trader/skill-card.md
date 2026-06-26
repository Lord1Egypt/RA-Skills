## Description: <br>
Trades Polymarket prediction markets on food commodity prices, crop yields, drought-driven supply shocks, alternative protein milestones, and agricultural policy events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and operators use this skill to discover food and agriculture prediction markets, size paper or live Polymarket trades, and apply agriculture-specific timing and commodity-confidence signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real Polymarket trades when run with --live. <br>
Mitigation: Keep paper mode enabled until live behavior, account funding, and trading limits are intentionally reviewed. <br>
Risk: Documented safeguards do not fully match the actual defaults, and the volume safeguard may not be enforced. <br>
Mitigation: Verify runtime tunables for thresholds, minimum days, max spread, max positions, and volume filtering before deployment. <br>
Risk: The skill requires a high-value SIMMER_API_KEY credential. <br>
Mitigation: Use a limited, revocable API key where available and avoid running automation with funds you are not prepared to risk. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-food-agriculture-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Console logs, command-line execution guidance, and configuration parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY and uses paper trading by default unless run with --live.] <br>

## Skill Version(s): <br>
0.0.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
