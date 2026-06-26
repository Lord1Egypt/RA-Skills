## Description: <br>
Automates Polymarket trades locally by placing orders when configured price thresholds are met, without external data sharing beyond Polymarket API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-yuming](https://clawhub.ai/user/ai-yuming) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and traders use this skill to monitor a configured Polymarket market locally and place buy or sell orders automatically when price thresholds are met. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real Polymarket trades with a live API key and no built-in order or spending limits. <br>
Mitigation: Use a minimal-permission key where available, start with paper or smallest-size settings, and add live-trading opt-in, max spend, max order count, cooldown, and automatic stop safeguards before unattended use. <br>
Risk: A Polymarket API key is stored in local YAML configuration. <br>
Mitigation: Keep config.yaml private, avoid committing secrets, and rotate the key if it may have been exposed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ai-yuming/polyguard-trader-martin-v1) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, Text, Configuration] <br>
**Output Format:** [Local Python process that reads YAML configuration, emits log text, and sends Polymarket API requests.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs continuously until stopped; uses user-provided API key and trading parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
