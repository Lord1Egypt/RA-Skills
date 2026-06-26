## Description: <br>
Oven tracks oven usage and cooking schedules for bake sessions, reminders, inventory, and usage statistics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain3](https://clawhub.ai/user/bytesagain3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and household maintainers use Oven to log oven activity, track inventory, schedule reminders, and review cooking or maintenance history from a local CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved oven notes and exports may contain sensitive household details because entries are stored locally in plaintext. <br>
Mitigation: Avoid entering sensitive schedules, personal details, or security-related household information, and review or delete files under ~/.local/share/oven/ as needed. <br>
Risk: Export commands can duplicate saved notes into JSON, CSV, or TXT files. <br>
Mitigation: Treat generated exports as copies of the local log data and manage, share, or remove them according to the sensitivity of the entries. <br>


## Reference(s): <br>
- [Oven on ClawHub](https://clawhub.ai/bytesagain3/oven) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files] <br>
**Output Format:** [Plain text CLI output with optional JSON, CSV, or TXT export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local logs and exports under ~/.local/share/oven/.] <br>

## Skill Version(s): <br>
2.0.1 (source: release evidence; artifact files report 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
