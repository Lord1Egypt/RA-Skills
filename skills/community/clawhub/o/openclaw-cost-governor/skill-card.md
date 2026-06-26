## Description: <br>
Pre-flight cost estimation for subagent spawns and approval gates. Prevents API overspend and surprise billing. Budget control for sessions_spawn calls. Daily spend tracking. Essential for multi-agent OpenClaw deployments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[donovanpankratz-del](https://clawhub.ai/user/donovanpankratz-del) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to estimate subagent costs before spawning, require approval for higher-cost tasks, and keep local daily or monthly spend summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cost-tracking logs can contain task details, model names, and spend history. <br>
Mitigation: Avoid writing sensitive task details or secrets into the local cost-tracking log and review log retention practices. <br>
Risk: The approval gate can be bypassed or misconfigured. <br>
Mitigation: Review the bypass phrase, approval threshold, and budget settings before enabling the skill in routine workflows. <br>
Risk: Cron-based summaries may run recurring local automation. <br>
Mitigation: Enable cron only when recurring summaries are desired and periodically verify the schedule and output location. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/donovanpankratz-del/openclaw-cost-governor) <br>
- [Publisher profile](https://clawhub.ai/user/donovanpankratz-del) <br>
- [ClawHub homepage](https://clawhub.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown guidance with shell commands and local cost-tracking files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces estimates, approval prompts, local cost log entries, and daily or monthly spend summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
