## Description: <br>
OpenClaw plugin that applies guardrails and auto-fixes reversible failures such as rate limits, disconnects, and stuck session pins. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[homeofe](https://clawhub.ai/user/homeofe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this OpenClaw plugin to monitor common reversible failures and apply guarded recovery actions for model failover, session pin repair, WhatsApp gateway reconnects, failing cron jobs, and plugin crashes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically change OpenClaw session and gateway state. <br>
Mitigation: Use dryRun first, review proposed recovery actions, and keep disruptive autoFix options disabled unless automatic repair is explicitly accepted. <br>
Risk: Cron and plugin repair options can disable services and create GitHub issues. <br>
Mitigation: Keep disableFailingCrons and disableFailingPlugins off by default, set issueRepo to a trusted private repository when needed, and review generated issue content. <br>
Risk: Error details sent to issues or logs may contain sensitive paths, tokens, or business details. <br>
Mitigation: Treat failure text as sensitive until redaction and approval controls are verified. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/homeofe/openclaw-self-healing-elvatis) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [OpenClaw plugin manifest](artifact/openclaw.plugin.json) <br>
- [Security policy](artifact/SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands, JSON, text] <br>
**Output Format:** [OpenClaw plugin actions, configuration changes, JSON status snapshots, JSONL metrics, logs, and optional GitHub issue text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can patch session model pins, restart gateways, disable failing cron jobs or plugins, and create GitHub issues when configured; dry-run mode is available.] <br>

## Skill Version(s): <br>
0.2.16 (source: server release, README, package.json, openclaw.plugin.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
