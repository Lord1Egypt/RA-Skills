## Description:

Monitors local PC resource status, including CPU, memory, disk, network, and available temperature readings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1173910773](https://clawhub.ai/user/1173910773)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect local PC resource usage on demand or through OpenClaw automation. It is useful for quick health checks covering CPU, memory, disk space, network counters, and optional temperature data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The launcher can automatically install an unpinned Python dependency when psutil is missing.

Mitigation: Review the launcher before use, prefer a virtual environment or OS package manager, and install a pinned psutil version explicitly before running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1173910773/skills/pc-monitor-cn)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text monitoring report or JSON when invoked with --json]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports local host resource counters from psutil and disk usage from the filesystem.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
