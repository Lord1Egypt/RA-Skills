## Description: <br>
Auto-log trades with context, track outcomes, generate calibration reports to improve trading. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simmer](https://clawhub.ai/user/simmer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to sync Simmer prediction-market trades, inspect trade history, update outcomes, export CSV data, and generate daily, weekly, or monthly performance reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to Simmer trade history through SIMMER_API_KEY. <br>
Mitigation: Store SIMMER_API_KEY as a secret and install only when access to Simmer trade history is acceptable. <br>
Risk: Synced trade history and enriched trade context are stored locally and CSV exports may contain sensitive trading information. <br>
Mitigation: Keep the data directory private and review CSV exports before sharing them. <br>
Risk: Changing SIMMER_API_URL can send authenticated requests to a different endpoint. <br>
Mitigation: Do not override SIMMER_API_URL unless the endpoint is trusted. <br>


## Reference(s): <br>
- [Prediction Trade Journal on ClawHub](https://clawhub.ai/simmer/prediction-trade-journal) <br>
- [Simmer publisher profile](https://clawhub.ai/user/simmer) <br>
- [Simmer API base URL](https://api.simmer.markets) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code] <br>
**Output Format:** [CLI text output, Markdown setup guidance, local JSON storage, and optional CSV exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY and writes trade history under the skill's local data directory.] <br>

## Skill Version(s): <br>
1.1.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
