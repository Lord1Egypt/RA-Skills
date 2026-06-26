## Description: <br>
Diagnose OpenClaw "message sent but no assistant reply" issues, then safely switch active model references with primary + multi-fallback support, including heartbeat-triggered recovery to the highest available model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zxs1633079383](https://clawhub.ai/user/zxs1633079383) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to diagnose OpenClaw sessions that send a user message but return no assistant content, then validate model availability and apply a safe model fallback or rollback workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Applying the model-switching workflow can change active OpenClaw model routing. <br>
Mitigation: Run dry-runs first, perform the required pre- and post-switch model availability probes, and review changed files and backups before relying on the new routing. <br>
Risk: Provider probes use the configured provider endpoint and credentials. <br>
Mitigation: Verify the configured provider base URL before probing and run the workflow only in an environment where the OpenClaw configuration and logs are appropriate to inspect. <br>
Risk: Heartbeat or cron integration can keep reapplying fallback and recovery behavior. <br>
Mitigation: Enable heartbeat or cron only when ongoing automatic fallback and recovery is intended, and keep the priority list explicit. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zxs1633079383/openclaw-session-reply-debug) <br>
- [README.md](README.md) <br>
- [OpenClaw model connectivity test runbook](openclaw-model-connectivity-test.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and validation steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose dry-run and apply commands that inspect OpenClaw sessions, probe model providers, and update local model references after validation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
