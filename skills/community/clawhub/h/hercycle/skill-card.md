## Description:

Women's cycle intelligence companion that reads Whoop biometric data and menstrual cycle phase to identify the user's hormonal season and provide phase-aware recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gloria-zhang1](https://clawhub.ai/user/gloria-zhang1)

### License/Terms of Use:


## Use Case:

External users use HerCycle to combine Whoop recovery, HRV, sleep, skin temperature, and cycle phase signals into recommendations for training, nutrition, scheduling, social energy, and phase-aware actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive biometric and menstrual-cycle data may be exposed to a local backend or connected services.

Mitigation: Use only a trusted WhoopClaw implementation, inspect its code and dependencies before use, and limit access to users who intentionally want cycle-aware analysis.

Risk: Whoop OAuth credentials can grant access to personal health and recovery data.

Mitigation: Keep credentials scoped, private, and revocable; rotate or revoke them when the backend is no longer needed.

Risk: Recommendations may be inaccurate if based on stale cached data or incomplete cycle logs.

Mitigation: Pull live Whoop and cycle data before making recommendations and clearly account for missing or inferred phase information.

## Reference(s):

- [Whoop API - HerCycle Reference](references/whoop-api.md)
- [Action Modules - HerCycle Reference](references/action-modules.md)
- [Whoop Developer Dashboard](https://developer-dashboard.whoop.com)
- [HerCycle ClawHub Skill Page](https://clawhub.ai/gloria-zhang1/skills/hercycle)
- [gloria-zhang1 ClawHub Publisher Profile](https://clawhub.ai/user/gloria-zhang1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, API Calls]

**Output Format:** [Markdown with concise recommendations, setup guidance, endpoint references, and occasional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live WhoopClaw and Whoop data when available; recommendations should not rely on stale cached values.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
