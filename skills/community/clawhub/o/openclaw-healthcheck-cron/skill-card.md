## Description:

Create and run a reusable OpenClaw deep healthcheck automation using a cron job plus a script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plgonzalezrx8](https://clawhub.ai/user/plgonzalezrx8)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to set up scheduled OpenClaw health audits, standardize status checks, and package the cron-based workflow for reuse.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled health checks can run under an overly privileged account.

Mitigation: Run the cron job as a low-privilege user before enabling routine execution.

Risk: Healthcheck logs and summaries may be written to a shared temporary directory by default.

Mitigation: Set HEALTHCHECK_OUTPUT_DIR to a private per-user state directory.

Risk: Cron timing may be wrong if the default timezone is not appropriate for the deployment.

Mitigation: Set the scheduled job timezone explicitly before enabling the cron job.

## Reference(s):

- [Cron job example](artifact/references/cron-job-example.json)
- [ClawHub skill page](https://clawhub.ai/plgonzalezrx8/skills/openclaw-healthcheck-cron)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a concise verdict, pass/warn/fail counts, artifact path, and recommended next action.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
