## Description: <br>
Diagnose and prevent OpenClaw agent failures including session bloat, lane deadlocks, bootstrap truncation, auth errors, compaction timeouts, gateway errors, and operational health check failures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zurbrick](https://clawhub.ai/user/zurbrick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to troubleshoot OpenClaw agents that stop responding, run slowly, fail authentication, hit rate limits, deadlock on cron lanes, or approach session and bootstrap limits. It provides triage guidance, shell commands, configuration checks, and optional watchdog scripts for ongoing operational monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled diagnostics read local OpenClaw logs, session metadata, cron configuration, and AGENTS.md size, which may expose operational details. <br>
Mitigation: Run the diagnostics only in trusted environments and keep watchdog output in trusted channels. <br>
Risk: Registering the watchdog as a cron job creates recurring checks and recurring alert output. <br>
Mitigation: Register the cron watchdog only when recurring monitoring is desired, and use an isolated cron session lane. <br>
Risk: Break-glass recovery may require manual edits to OpenClaw JSON state. <br>
Mitigation: Use manual state edits only as last-resort recovery, make timestamped backups first, and validate JSON before restarting OpenClaw services. <br>
Risk: Running bundled bash scripts executes local shell commands against OpenClaw configuration and log paths. <br>
Mitigation: Review the scripts before running them and confirm the paths match the intended OpenClaw installation. <br>


## Reference(s): <br>
- [OpenClaw Operator release page](https://clawhub.ai/zurbrick/openclaw-operator) <br>
- [Design Patterns](references/design-patterns.md) <br>
- [Failure Patterns](references/failure-patterns.md) <br>
- [Auth Profile Eval](evals/auth-profile.md) <br>
- [Bootstrap Budget Eval](evals/bootstrap-budget.md) <br>
- [Lane Deadlock Eval](evals/lane-deadlock.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend running bundled bash scripts and reviewing local OpenClaw logs, cron configuration, session metadata, and AGENTS.md size.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
