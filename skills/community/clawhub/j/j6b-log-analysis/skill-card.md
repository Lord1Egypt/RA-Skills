## Description:

J6B泊车日志分析 helps agents locate and read J6B parking-system logs, identify common errors, collect diagnostics, and summarize QNX system-resource performance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coderchendq](https://clawhub.ai/user/coderchendq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, test engineers, and system engineers use this skill to inspect J6B parking-system logs, troubleshoot failures, collect diagnostic files, and produce system-resource analysis reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote log collection uses root-based access and the security scan reports a confirmed command-injection risk.

Mitigation: Review the shell scripts before use, prefer a least-privilege read-only account, and pass only trusted module names and connection values.

Risk: Downloaded logs and coredumps can contain sensitive diagnostic data.

Mitigation: Export only approved diagnostics, store downloads securely, and remove local or remote temporary files when analysis is complete.

Risk: Background CPU monitoring can run longer than intended and accumulate operational logs.

Mitigation: Run monitoring with a defined stop time, confirm cleanup behavior, and stop the background process after collection.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/coderchendq/skills/j6b-log-analysis)
- [User manual](用户使用手册.md)
- [Log locations](references/log-locations.md)
- [Error codes](references/error-codes.md)
- [Performance analysis](references/performance.md)
- [QNX commands](references/qnx-commands.md)
- [System resource report template](references/report-template-system-resource.md)
- [Troubleshooting cases](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and structured diagnostic report sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include command suggestions, log-analysis summaries, and system-resource report content for J6B/QNX diagnostics.]

## Skill Version(s):

1.1.0 (source: server release metadata; user manual v1.1, released 2026-03-30)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
