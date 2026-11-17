## Description:

Memory Maintenance 2.0.0 manages persistent agent memory, delegated task execution, progress reporting, retries, and error handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucklylin](https://clawhub.ai/user/lucklylin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external ClawHub users use this skill to maintain agent memory files, run delegated tasks, report execution progress, and record recoverable failures. It is intended for workspaces where persistent memory and task automation are explicitly desired.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory may retain sensitive user or workspace data.

Mitigation: Use only in workspaces where persistent memory is intended, avoid entering secrets or private data, and regularly inspect memory/failure.log and daily memory files.

Risk: Background or cron scheduling can keep automation active beyond the immediate interaction.

Mitigation: Do not enable the background scheduler or cron configuration unless the operator understands how to inspect, disable, and remove it.

Risk: Generic task execution and broad memory automation are flagged as suspicious without enough controls.

Mitigation: Review carefully before installing and use in a constrained workspace with operator oversight.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lucklylin/skills/memory-maintenance-2-0-0)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Console status text, Markdown memory entries, JSON-like task and failure records, and inline code or shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist daily memory entries and failure logs in the workspace; no fixed token cap is documented.]

## Skill Version(s):

2.0.0 (source: evidence release version and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
