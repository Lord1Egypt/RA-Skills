## Description: <br>
根据用户的巡检需求推荐心跳场景，并生成可用的 HEARTBEAT.md 巡检清单和 Cron 定时配置。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jack-long-2022](https://clawhub.ai/user/jack-long-2022) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and operators use this skill to choose recurring heartbeat checks for email, calendar, market, code, backup, and similar monitoring needs, then generate concise HEARTBEAT.md snippets and cron schedules. It is most useful when a user wants proactive checks without activating too many recurring tasks at once. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated cron schedules may run at the wrong local time if timezone conversion is not checked. <br>
Mitigation: Verify the intended local timezone against the generated UTC cron expression before enabling any recurring job. <br>
Risk: Too many active heartbeat checks can create noisy monitoring and reduce attention to important alerts. <br>
Mitigation: Keep active heartbeat items at five or fewer and prioritize time-sensitive checks such as email and calendar. <br>
Risk: Heartbeat plans may involve sensitive accounts, financial data, passwords, backups, or account settings. <br>
Mitigation: Require explicit user confirmation before applying workflow changes, and avoid putting secrets or sensitive values in HEARTBEAT.md. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jack-long-2022/openclaw-heartbeat-designer) <br>
- [SCENARIOS.md](artifact/SCENARIOS.md) <br>
- [CRON.md](artifact/CRON.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with HEARTBEAT.md snippets, cron expressions, and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes scenario recommendations, timing rationale, timezone conversion notes, and overload warnings when more than five heartbeat checks are proposed.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
