## Description: <br>
Checks current Mac temperature, load, memory, swap, and power usage with macmon. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ruban-gt](https://clawhub.ai/user/ruban-gt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Mac users and support-oriented agents use this skill to collect a short local health snapshot for temperature, CPU/GPU activity, memory, swap, and power usage. It is suited for quick troubleshooting and status checks on macOS hosts with macmon installed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local macmon commands and may use a zsh login-shell fallback, so local shell startup files and PATH configuration can affect execution. <br>
Mitigation: Use the skill only in a trusted local macOS environment and verify the intended Homebrew macmon package before running it. <br>
Risk: The summary reflects a single live telemetry snapshot and may not represent long-term thermal or performance behavior. <br>
Mitigation: Treat results as a point-in-time status check and avoid making sustained-health conclusions from one sample. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/ruban-gt/mac-health-check) <br>
- [Publisher profile](https://clawhub.ai/user/ruban-gt) <br>
- [macmon project](https://github.com/vladkens/macmon) <br>
- [Sample macmon JSON fields](references/sample-output.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text summary with optional JSON input/output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS and the local macmon command, commonly installed with Homebrew formula macmon.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
