## Description: <br>
Create macOS desktop app launchers for dev projects that open Terminal and run a local development server from a desktop icon. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to package local projects as clickable macOS .app launchers that start common dev-server commands. It is useful when a project should be opened from the Desktop instead of by manually running shell commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports under-disclosed network icon generation and a hardcoded third-party API key. <br>
Mitigation: Review the script before installation, avoid --auto-icon unless external icon generation is intended, and remove or rotate the embedded FAL key before use. <br>
Risk: The launcher can run an auto-detected or user-supplied command in Terminal. <br>
Mitigation: Verify the exact project path and command before creating or launching the .app bundle. <br>
Risk: An existing .app with the same name may be deleted and replaced. <br>
Mitigation: Confirm the output directory and app name first, and preserve any existing launcher that should not be overwritten. <br>


## Reference(s): <br>
- [Phy App Launcher on ClawHub](https://clawhub.ai/PHY041/phy-app-launcher) <br>
- [Publisher profile](https://clawhub.ai/user/PHY041) <br>
- [Canlah AI homepage](https://canlah.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated macOS launcher files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a macOS .app bundle containing a launcher script, Info.plist, and optional icon resources.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
