## Description: <br>
Conversational PolySports trading and OpenClaw automation through structured `/skills/v1` endpoints for market lookup, balance and authorization checks, real position trading, redemption, scheduled pregame scans, in-game monitoring, and postgame review workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dreamcoin1998](https://clawhub.ai/user/dreamcoin1998) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to inspect PolySports markets and account state, place or sell real positions after explicit sizing and confirmation, and configure scheduled trading-related workflows through OpenClaw. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access PolySports and potentially make real-money trades. <br>
Mitigation: Install only when live trading is intended; require explicit order sizes, plain-language summaries, and confirmation unless the user has delegated authority. <br>
Risk: The skill asks for live trading API keys in chat. <br>
Mitigation: Use a secure secret or connection mechanism instead of pasting API keys into ordinary chat. <br>
Risk: Persistent automation can continue trading or monitoring after the immediate session. <br>
Mitigation: Prefer single-order or timeboxed authorization, verify Telegram delivery targets, and regularly disable or delete automation that is no longer needed. <br>


## Reference(s): <br>
- [PolySports Skills API](artifact/references/skills-api.md) <br>
- [PolySports Trading Playbook](artifact/references/trading-playbook.md) <br>
- [PolySports Monitoring Rules](artifact/references/monitoring-rules.md) <br>
- [Monitor Launcher Prompt Template](artifact/assets/templates/monitor-launcher.prompt.md) <br>
- [OpenClaw Cron Job Template](artifact/assets/cron/jobs.template.json) <br>
- [ClawHub Skill Page](https://clawhub.ai/dreamcoin1998/polysports-trading-agent) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, markdown, API calls, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with structured API-call instructions, OpenClaw cron configuration, and plain-language trade summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit order size, confirmation unless delegated authority exists, API-key authentication, and idempotency keys for write requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
