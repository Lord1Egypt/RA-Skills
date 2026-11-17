## Description:

全闭环自动化管道 — Hunter→Skill Factory→Orchestrator→Dashboard→Profit。将Phase 1-3所有组件串联为自动运行的超级管道。核心能力：(1) 一键全流程 (2) 定时自动运行 (3) 异常自愈 (4) 利润报告

This skill is ready for commercial/non-commercial use.

## Publisher:

[freeman88-tch](https://clawhub.ai/user/freeman88-tch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run and inspect a local OpenClaw automation pipeline that chains market scanning, orchestration, dashboard refresh, profit reporting, and health checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill launches multiple local OpenClaw skill scripts through shell commands with weak scoping.

Mitigation: Use only in a trusted workspace, verify exact referenced script paths before execution, and prefer a revised version that uses argument-list subprocess calls.

Risk: The skill overstates some scheduling and self-healing automation capabilities.

Mitigation: Treat scheduling and self-healing behavior as unverified until the release documents and implements those features.

Risk: The skill depends on other local skills and their permissions.

Mitigation: Review and trust the referenced local skills before installing or running this pipeline.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freeman88-tch/skills/mega-pipeline)

## Skill Output:

**Output Type(s):** [shell commands, text, JSON]

**Output Format:** [Console text with JSON log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pipeline status output is derived from locally installed OpenClaw skills under ~/.openclaw/workspace/skills.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
