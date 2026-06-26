## Description: <br>
MacPowerTools provides local macOS maintenance, resource forecasting, backup, process monitoring, and LAN service discovery helpers for OpenClaw agents on Apple Silicon. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AadiPapp](https://clawhub.ai/user/AadiPapp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use MacPowerTools to run local macOS maintenance workflows, generate resource forecasts, simulate agent-swarm metrics, monitor processes, and prepare local backups on Darwin hosts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Safety claims may understate local persistence because the tool can leave logs and history under ~/.logs/macpowertools and ~/.config/macpowertools. <br>
Mitigation: Review storage behavior before installation and disclose cleanup or removal steps to users. <br>
Risk: The shipped power_tools.py is not a clean runnable Python file according to server security evidence. <br>
Mitigation: Validate and correct the script syntax before executing or distributing it. <br>
Risk: The fleet-scan command may browse local LAN service advertisements. <br>
Mitigation: Run LAN discovery only in environments where local network discovery is expected and permitted. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/AadiPapp/mac-power-tools) <br>
- [Publisher Profile](https://clawhub.ai/user/AadiPapp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with text and JSON-style command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Darwin-only; requires Python >=3.10 and numpy for simulation features.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
