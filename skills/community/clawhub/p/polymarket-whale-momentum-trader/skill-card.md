## Description: <br>
Detects when multiple top-performing whale wallets independently enter the same Polymarket market in the same direction within a configurable time window and trades with conviction-boosted sizing when two or more whales agree. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and trading automation developers use this skill to monitor Polymarket whale-wallet momentum and place Simmer or Polymarket trades when configurable consensus, spread, timing, and position-size checks pass. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated live trading can create financial loss if enabled unintentionally or with aggressive limits. <br>
Mitigation: Start in paper mode, require explicit live-mode activation, and keep conservative position, spread, volume, and open-position limits. <br>
Risk: A long-lived process can weaken the paper-mode safety promise if a live-trading client is reused across runs. <br>
Mitigation: Avoid mixing live and paper runs in the same long-lived Python process; restart the process between modes until the client reuse issue is fixed. <br>
Risk: The skill requires a sensitive SIMMER_API_KEY for trading access. <br>
Mitigation: Use a scoped key, store it only in the intended runtime environment, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-whale-momentum-trader) <br>
- [predicting.top leaderboard API](https://predicting.top/api/leaderboard) <br>
- [Polymarket Data API](https://data-api.polymarket.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API calls, Shell commands, Configuration guidance] <br>
**Output Format:** [Console status text, Python execution commands, environment-variable configuration, and Simmer trade requests.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY and simmer-sdk; defaults to paper mode unless live trading is explicitly enabled.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
