## Description: <br>
HerCycle reads Whoop biometrics and cycle phase data to identify the user's hormonal phase and provide phase-aware recommendations or actions for training, nutrition, scheduling, social energy, and music. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gloria-zhang1](https://clawhub.ai/user/gloria-zhang1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to connect Whoop biometrics and cycle phase information to phase-aware recommendations for daily planning, training intensity, nutrition, social energy, and optional action modules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive reproductive-health and biometric data. <br>
Mitigation: Review the skill carefully before installation and only connect Whoop or cycle data sources when the user is comfortable with that access. <br>
Risk: The activation and possible external actions are not scoped tightly enough for sensitive health-related data. <br>
Mitigation: Require explicit confirmation before connecting to live health services or performing external actions such as changing schedules, sending messages, or calling third-party tools. <br>
Risk: Recommendations can be misleading if based on stale or incomplete biometric data. <br>
Mitigation: Pull live data before recommendations and clearly treat inferred phase information as an estimate when no explicit cycle log is available. <br>


## Reference(s): <br>
- [Whoop API - HerCycle Reference](references/whoop-api.md) <br>
- [Action Modules - HerCycle Reference](references/action-modules.md) <br>
- [Whoop Developer Dashboard](https://developer-dashboard.whoop.com) <br>
- [HerCycle on ClawHub](https://clawhub.ai/gloria-zhang1/hercycle) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, configuration] <br>
**Output Format:** [Markdown or conversational text with optional API endpoint guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call configured WhoopClaw and action-module backends when the user authorizes live data access or external actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
