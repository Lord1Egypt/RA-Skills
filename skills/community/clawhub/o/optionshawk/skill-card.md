## Description: <br>
OptionsHawk provides options flow analysis, unusual activity detection, and options strategy evaluation for equities and ETFs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OptionsHawk24](https://clawhub.ai/user/OptionsHawk24) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to analyze options-market flow, detect unusual activity, evaluate options strategies, and configure alert thresholds for equities and ETFs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OptionsHawk API key for market-data and alert access. <br>
Mitigation: Keep OPTIONSHAWK_API_KEY private and prefer a revocable or scoped key when available. <br>
Risk: Broad scans or frequent alerts may increase provider usage or billing. <br>
Mitigation: Monitor provider usage and billing, and tune OPTIONSHAWK_ALERT_THRESHOLD for the intended workflow. <br>
Risk: The skill produces options-market analysis and alerts, not trade execution authority. <br>
Mitigation: Review outputs before making financial decisions and do not treat the skill as authorization to place trades. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/OptionsHawk24/optionshawk) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/OptionsHawk24) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown text with market-analysis summaries and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OPTIONSHAWK_API_KEY; OPTIONSHAWK_ALERT_THRESHOLD can tune unusual-activity alerts.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
