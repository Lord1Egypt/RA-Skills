## Description:

Mac Health Check reads live macOS telemetry through macmon and summarizes current temperature, load, memory, swap, and power usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruban-gt](https://clawhub.ai/user/ruban-gt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent for a practical snapshot of a Mac's thermal state, CPU/GPU activity, RAM, swap, and power usage. It is scoped to macOS hosts with macmon installed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs local macmon commands to read host telemetry.

Mitigation: Install it only where local Mac telemetry collection is intended, and review command execution before deployment.

Risk: The wrapper may invoke zsh as a login shell, so shell startup files and PATH can influence what runs.

Mitigation: Keep shell startup files and PATH trusted, and verify macmon resolves to the expected binary before use.

## Reference(s):

- [Mac Health Check ClawHub page](https://clawhub.ai/ruban-gt/skills/mac-health-check)
- [macmon project](https://github.com/vladkens/macmon)
- [Sample macmon JSON fields](references/sample-output.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text summary or raw JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One-shot local telemetry snapshot; raw JSON can be pretty-printed on request.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
