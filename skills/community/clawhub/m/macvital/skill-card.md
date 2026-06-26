## Description: <br>
Check macOS hardware health: CPU usage, RAM pressure, disk space, temperatures, and top processes, returning a quick status summary or full breakdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wrentheai](https://clawhub.ai/user/wrentheai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agents use Macvital to check whether a macOS machine has enough CPU, memory, disk, and thermal headroom before heavier work or while diagnosing local performance issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Temperature checks can request sudo for more accurate Apple Silicon die temperature data. <br>
Mitigation: Use non-sudo status, check, detail, and top commands for routine checks; approve sudo only when temperature data was specifically requested. <br>
Risk: Detailed output may reveal process names and local system details. <br>
Mitigation: Review output before sharing it and omit sensitive process or system information when reporting results. <br>
Risk: Watch mode continuously reports local system status until stopped. <br>
Mitigation: Stop watch mode when monitoring is complete. <br>


## Reference(s): <br>
- [Macvital on ClawHub](https://clawhub.ai/wrentheai/macvital) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text summaries, optional JSON status output, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exit codes indicate health state for scripting: 0 ok, 1 warn, 2 critical.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
