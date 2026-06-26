## Description: <br>
Production-grade model router for OpenClaw: prefix routing (@codex/@mini), timezone-aware schedule switching, verify-after-switch, rollback, lock protection, and JSONL audit logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[VulcanusALex](https://clawhub.ai/user/VulcanusALex) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to route OpenClaw work to configured models by explicit prefixes or time-based policy, then verify switches, roll back failures, and inspect audit logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A configured session-controller binary or downstream executor could run with the agent environment available to it. <br>
Mitigation: Use a trusted absolute OpenClaw binary path, keep unnecessary secrets out of the runtime environment, and review sessionController settings before enabling model switching. <br>
Risk: Automatic schedule-based switching can route work to an unintended model if prefix or schedule configuration is wrong. <br>
Mitigation: Validate router.config.json and router.schedule.json, inspect active rules with scheduler resolve/list commands, and keep verify-after-switch and rollback enabled. <br>


## Reference(s): <br>
- [OpenClaw Model Router Skill on ClawHub](https://clawhub.ai/VulcanusALex/openclaw-model-router-skill) <br>
- [Model Router Runbook](docs/runbook.md) <br>
- [Scheduler Integration Notes](docs/scheduler-notes.md) <br>
- [Router Configuration](router.config.json) <br>
- [Router Schedule](router.schedule.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON configuration, and Node.js code references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce JSON route or scheduler command output when invoked with CLI --json options.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
