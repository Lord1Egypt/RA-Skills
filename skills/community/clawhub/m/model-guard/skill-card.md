## Description:

Monitors Anti-Gravity model quotas and automatically switches the default model to the highest-quota candidate, falling back to Gemini Flash when all tracked quotas are below the configured threshold.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sarielwang93](https://clawhub.ai/user/sarielwang93)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to keep OpenClaw model selection aligned with remaining Anti-Gravity quota during normal work. It can be run manually or scheduled when automatic default-model changes are desired.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically change the OpenClaw default model, including when run on a schedule.

Mitigation: Review guard.js to confirm the candidate models, threshold, and fallback model, then run it manually before enabling cron or heartbeat execution.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Command-line text output with configuration in JavaScript]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Updates the OpenClaw default model through the local openclaw CLI when quota conditions trigger a switch.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
