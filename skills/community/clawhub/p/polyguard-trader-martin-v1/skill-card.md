## Description:

Automates Polymarket trades locally by placing orders when configured price thresholds are met, with no external data sharing beyond Polymarket API calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-yuming](https://clawhub.ai/user/ai-yuming)

### License/Terms of Use:


## Use Case:

Developers and traders use this skill to run local Polymarket trading automation from a flat YAML configuration. It monitors a configured market and places buy or sell orders when the configured price threshold is met.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can repeatedly place live Polymarket orders using stored credentials.

Mitigation: Use narrowly scoped, revocable Polymarket credentials and run it only with funds you are prepared to risk.

Risk: A populated config.yaml can expose a real API key if committed or shared.

Mitigation: Keep placeholder values in versioned files, store real credentials outside source control, and rotate credentials if exposure is suspected.

Risk: The artifact behaves as continuous trading automation rather than a one-time alert or single confirmed order.

Mitigation: Review the configuration, order size, threshold, and polling interval before execution, then monitor the process and stop it when the intended trading window ends.

## Reference(s):

- [PolyGuard Martin Pro ClawHub page](https://clawhub.ai/ai-yuming/skills/polyguard-trader-martin-v1)
- [ai-yuming publisher profile](https://clawhub.ai/user/ai-yuming)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Runtime logs, Polymarket API requests, and YAML configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs as repeated trading automation using flat config.yaml values until stopped.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
