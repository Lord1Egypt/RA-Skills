## Description:

Enterprise AI security scanner using static analysis, runtime guards, and ClamAV to detect credential theft, data leaks, malware, and audit logging gaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pfaria32](https://clawhub.ai/user/pfaria32)

### License/Terms of Use:

MIT

## Use Case:

Security engineers and developers use this skill to scan AI agent code, detect suspicious credential access, data exfiltration patterns, malware indicators, and configure runtime protection with audit logging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill tells users to clone and run unaudited, unpinned code from an external repository.

Mitigation: Pin the repository to a specific commit or signed release and audit the source before running scanner or deployment commands.

Risk: Persistent scanning setup can expand access beyond the intended directories.

Mitigation: Run scans with read-only access limited to approved paths and review cron, alerting, and runtime guard configuration before enabling them.

## Reference(s):

- [OpenClaw Shield ClawHub page](https://clawhub.ai/pfaria32/skills/openclaw-shield)
- [OpenClaw Shield repository](https://github.com/pfaria32/OpenClaw-Shield-Security)
- [Responsible disclosure issues](https://github.com/pfaria32/OpenClaw-Shield-Security/issues)
- [Inspired by Resonant shield guide](https://github.com/ManoloRemiddi/resonantos-open-system-toolkit/blob/main/BUILD_YOUR_OWN_SHIELD.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash command examples and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to produce or review JSON security scan reports.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
