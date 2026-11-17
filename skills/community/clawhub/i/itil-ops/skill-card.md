## Description:

ITIL-aligned incident, problem, and change management for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chefboyrdave21](https://clawhub.ai/user/chefboyrdave21)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to detect service crashes, cron failures, resource pressure, and data integrity issues, then classify incidents, identify recurring problems, and plan controlled changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The authoritative security evidence rates the release suspicious because the bundled review script has a local code-execution bug and broad access to agent operational data.

Mitigation: Review and fix the script before installation, especially Python filename handling, and run it only in a least-privileged environment with access limited to the operational data it must inspect.

Risk: Review output and automated cron or coordination workflows may expose sensitive agent state or trigger operational actions before an operator has approved them.

Mitigation: Redact report contents, make cron, task, and remediation actions explicit, and require operator approval before enabling scheduled execution or acting on generated findings.

## Reference(s):

- [ITIL 4 to Agent Operations Mapping](references/itil4-agent-mapping.md)
- [ClawHub skill page](https://clawhub.ai/chefboyrdave21/skills/itil-ops)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit ITIL_CLEAR when no issues are found or an incident/problem report when issues are detected.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
