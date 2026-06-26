## Description: <br>
Automated prediction market scanner that finds mispriced Polymarket markets and can execute trades through the Simmer Markets API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wyzmf](https://clawhub.ai/user/wyzmf) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users can use this skill to scan Polymarket prediction markets, check Simmer account status and positions, and identify or execute trading opportunities through the Simmer API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The default scan mode can submit trades through the Simmer API. <br>
Mitigation: Review before installing or running; use only a virtual or tightly capped Simmer account unless real-money safeguards are independently verified. <br>
Risk: The security review states that promised real-money confirmation and several risk controls are not implemented. <br>
Mitigation: Do not provide a live trading key or schedule unattended runs until explicit opt-in, per-trade confirmation, daily limits, and stop-loss behavior are implemented and tested. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wyzmf/polymarket-scanner) <br>
- [Simmer Markets](https://simmer.markets) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API calls, Configuration, Files] <br>
**Output Format:** [Markdown guidance with bash commands, command-line text output, and JSONL trade logs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY. The default scan mode can submit trades through the Simmer API and writes trading_log.jsonl.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
