## Description: <br>
Restores Universal Control and AirDrop settings on a managed Mac by resetting the relevant managed preference files and setting AirDrop discoverability to Contacts Only. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinntrance](https://clawhub.ai/user/jinntrance) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, IT administrators, and support agents use this skill to restore Universal Control and AirDrop preference settings on managed Macs and optionally keep those settings restored after reboot or login. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional startup installation creates persistent root-level execution for restoring macOS managed preference settings. <br>
Mitigation: Use the one-time restore scripts when possible; require explicit administrator approval, review the LaunchDaemon and LaunchAgent before installation, and maintain a clear uninstall plan before enabling reboot persistence. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS administrative authorization for root-level managed preference changes and startup item installation.] <br>

## Skill Version(s): <br>
0.1.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
