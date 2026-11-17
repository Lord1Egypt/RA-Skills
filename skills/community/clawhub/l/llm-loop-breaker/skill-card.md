## Description:

Two-layer defense for Openclaw gateway: kills hallucinating LLM streams via entropy analysis, and watchdogs host CPU/RAM/Disk to prevent resource exhaustion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hehkcaspar](https://clawhub.ai/user/hehkcaspar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Openclaw operators use this skill to deploy runtime safeguards that interrupt repetitive LLM streams and monitor host resource exhaustion around a gateway deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent gateway modification and global fetch patching can alter runtime behavior after installation.

Mitigation: Review the deploy script before installation, test in a staging environment, keep the generated backup, and maintain a clear rollback plan.

Risk: The watchdog starts a detached background process and can kill selected gateway child process trees.

Mitigation: Run under a dedicated unprivileged account, use explicit service management, and confirm process-kill thresholds before production deployment.

Risk: Local host diagnostics and incident snapshots may include operational details from system logs.

Mitigation: Restrict log and incident paths, control file permissions, and review captured diagnostics before sharing.

Risk: Dependency installation and shell/path handling should be reviewed before execution.

Mitigation: Pin dependencies where possible and install only after reviewing the shell script in the target environment.

## Reference(s):

- [Openclaw ClawHub](https://github.com/openclaw/clawhub)
- [LLM Loop Breaker on ClawHub](https://clawhub.ai/hehkcaspar/skills/llm-loop-breaker)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with bash commands and deployment file descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Linux-focused deployment guidance requiring node, python3, bash, psutil, and OPENCLAW_APP_DIR.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
