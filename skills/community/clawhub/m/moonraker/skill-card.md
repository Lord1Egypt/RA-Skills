## Description: <br>
Control and monitor a Klipper 3D printer via the Moonraker API, including print status, temperatures, pause, resume, cancel, and emergency stop. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rogueecho](https://clawhub.ai/user/rogueecho) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, makers, and printer operators use this skill to let an agent query and control a Klipper 3D printer through Moonraker. It supports status checks, temperature monitoring, file listing, pause, resume, cancel, and emergency stop operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control a configured Moonraker/Klipper 3D printer, including pause, cancel, emergency stop, and firmware restart actions that can stop a print or require recovery. <br>
Mitigation: Keep MOONRAKER_HOST pointed at a trusted local printer and require explicit confirmation before any disruptive printer-control action. <br>
Risk: A misconfigured MOONRAKER_HOST could direct commands to the wrong printer or an untrusted Moonraker endpoint. <br>
Mitigation: Verify the target host before use and avoid exposing the Moonraker service beyond trusted local networks. <br>


## Reference(s): <br>
- [Moonraker ClawHub release](https://clawhub.ai/rogueecho/moonraker) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and Moonraker REST API endpoint guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MOONRAKER_HOST and curl; jq is optional for formatted JSON output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
