## Description:

帮助代理评估 Linux 磁盘 SMART 健康、监控 HDD/NVMe 风险指标，并排查备份韧性问题。

This skill is ready for commercial/non-commercial use.

## Publisher:

[peterliu-512](https://clawhub.ai/user/peterliu-512)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, DevOps engineers, and system administrators use this skill to inspect Linux disk health signals, set up SMART-based sentinel monitoring, and reason about backup placement and restore-drill findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Formatting or persistent mount guidance can destroy data or target the wrong partition if device identity is not independently verified.

Mitigation: Verify the exact device using stable identifiers, confirm current backups, check for existing or damaged filesystems, and accept the destructive impact before running any formatting or fstab commands.

Risk: SMART monitoring examples are tied to specific local device names and sudo smartctl behavior, which may produce incomplete or misleading results on different systems.

Mitigation: Adapt device paths, thresholds, baseline locations, and sudo permissions to the target host before relying on alerts or automated self-tests.

## Reference(s):

- [本机磁盘健康与备份韧性改造记录（2026-09-04）](references/diREDACTED-SECRET.md)
- [ClawHub skill page](https://clawhub.ai/peterliu-512/skills/linux-disk-health-monitoring)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash code blocks and shell script snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include disk-health summaries, risk matrices, SMART command examples, monitoring scripts, and backup resilience recommendations.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
