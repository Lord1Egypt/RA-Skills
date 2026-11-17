## Description:

Visualize Hermes Agent work with bilingual summaries and reports for task progress, skill usage, tool calls, code changes, session statistics, and monitoring status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erich1566](https://clawhub.ai/user/erich1566)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Hermes Agent users use this skill to generate bilingual work summaries, reports, and monitoring views that make agent activity easier to inspect and share.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may present hard-coded sample analytics as current Hermes work metrics.

Mitigation: Treat generated reports as illustrative until the scripts are connected to real Hermes telemetry, and verify report contents before using or sharing them.

Risk: The monitor stop command can terminate unrelated processes that match its search pattern.

Mitigation: Patch monitoring control to record and stop only its own PID before enabling long-running monitoring.

Risk: Generated reports and monitor logs may contain workflow details that are not intended for external sharing.

Mitigation: Review generated report and log files before distributing them outside the intended audience.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/erich1566/skills/hermes-work-visualization)
- [Publisher profile](https://clawhub.ai/user/erich1566)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, HTML, Shell commands, Configuration]

**Output Format:** [Console text plus generated Markdown, JSON, and HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual Chinese/English output; report and monitor artifacts are written under the Hermes work-visualization skill directory.]

## Skill Version(s):

1.1.4 (source: SKILL.md frontmatter, _meta.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
