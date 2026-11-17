## Description:

Macvital checks macOS hardware health including CPU usage, RAM pressure, disk space, temperatures, and top processes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wrentheai](https://clawhub.ai/user/wrentheai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and agents use Macvital to check whether a local Mac has enough CPU, memory, disk, and thermal headroom before heavy work or while diagnosing performance issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Temperature collection may attempt sudo and run local shell commands.

Mitigation: Use non-temperature status or check modes by default, and run temperature collection with elevated privileges only when the operator explicitly wants that data.

Risk: The skill reports local hardware and process information from the Mac where it runs.

Mitigation: Review output before sharing it outside the local environment, especially process names and resource usage details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wrentheai/skills/macvital)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text status summaries, JSON status output, process tables, and exit codes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The check command uses exit code 0 for ok, 1 for warning, and 2 for critical status.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
