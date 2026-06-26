## Description: <br>
Control Homey home automation hub via CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KrauseFx](https://clawhub.ai/user/KrauseFx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and home automation operators use this skill to inspect and control Homey smart home devices, zones, and flows from an agent-accessible CLI workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The reviewed artifact references CLI files that were not included, so the runnable implementation was not fully reviewed. <br>
Mitigation: Inspect the referenced run.sh and package files before installation or execution. <br>
Risk: Homey credentials and OAuth tokens can grant control over real smart-home devices. <br>
Mitigation: Protect .env and ~/.config/homey-cli files, avoid committing secrets, and limit credential access to trusted users. <br>
Risk: Device changes and flow triggers can affect physical home automation state. <br>
Mitigation: Require clear user confirmation before write operations or flow triggers, and prefer the documented allowlisted capabilities. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/KrauseFx/homey-cli) <br>
- [Homey Developer Tools](https://tools.developer.homey.app/tools/app) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, text, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may read or modify real Homey device and flow state when executed with valid credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
