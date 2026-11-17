## Description:

A 0-token jobs and monitoring framework for OpenClaw: run long-running read tasks via scripts, checkpoint/resume safely, and send periodic progress and immediate alerts to Telegram.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zjianru](https://clawhub.ai/user/zjianru)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to configure and monitor long-running OpenClaw jobs outside the model loop, including read-only scans, health checks, checkpoint/resume, status reporting, and alerting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured jobs can repeatedly run local commands, so a trusted-looking read workflow can still execute harmful commands if the job file or referenced scripts are unsafe.

Mitigation: Review ops-jobs.json and every referenced script before enabling jobs, keep autoResume off unless it is explicitly needed, and run the monitor under a low-privilege account.

Risk: Telegram status and alert messages can disclose secrets or sensitive operational details if job output includes them.

Mitigation: Avoid sending secrets in status output, use print-only mode during validation, and restrict permissions on OpenClaw configuration files that contain messaging credentials.

Risk: Stopping a job by PID can terminate the wrong process if the status command returns stale or incorrect process information.

Mitigation: Prefer explicit stop commands for long-running jobs and use PID-based stopping only after validating the status command's process data.

## Reference(s):

- [OPS_FRAMEWORK.md](OPS_FRAMEWORK.md)
- [README.md](README.md)
- [UPSTREAM.md](UPSTREAM.md)
- [ClawHub Skill Page](https://clawhub.ai/zjianru/skills/ops-framework)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown with inline shell commands and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local Python monitor commands, job configuration guidance, and status contract details.]

## Skill Version(s):

0.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
