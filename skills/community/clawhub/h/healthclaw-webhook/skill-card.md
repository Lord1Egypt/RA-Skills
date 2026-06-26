## Description: <br>
HealthClaw streams Apple Health data from iPhone and Apple Watch through a self-hosted webhook so an OpenClaw agent can analyze trends, calculate recovery scores, and detect anomalies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[crxiaobailiu-gif](https://clawhub.ai/user/crxiaobailiu-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and developers use this skill to connect Apple Health data to an OpenClaw agent for recovery scoring, health trend questions, scheduled anomaly checks, and proactive alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive Apple Health data may be exposed through a public webhook, tunnel, local data directory, or notification channel. <br>
Mitigation: Use a strong ADMIN_TOKEN, prefer VPN or private access where possible, protect or encrypt the health-data directory, and keep alert messages minimal and private. <br>
Risk: Health alerts and recovery scores can be misleading if baseline data is sparse, thresholds are poorly tuned, or agent analysis is treated as medical advice. <br>
Mitigation: Review outputs before acting on them, tune thresholds against personal baselines, and use the results as wellness signals rather than diagnosis. <br>
Risk: Background sync, tunnels, servers, and cron jobs can keep moving health data after the user no longer expects it. <br>
Mitigation: Know how to stop the tunnel, webhook server, iOS background sync, and OpenClaw cron jobs before enabling continuous syncing. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/crxiaobailiu-gif/healthclaw-webhook) <br>
- [HealthClaw source](https://github.com/sprausliu/healthclaw) <br>
- [HealthClaw TestFlight beta](https://testflight.apple.com/join/SXDjT6vC) <br>
- [Recovery score example](examples/recovery-score.md) <br>
- [Health alerts example](examples/health-alerts.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include OpenClaw cron and task configuration, curl commands, and health analysis guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
