## Description: <br>
Install the Mobazha native binary on Linux, macOS, or Windows. Use when the user wants to run a store without Docker. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fengzie](https://clawhub.ai/user/fengzie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and store operators use this skill to install and manage Mobazha as a native binary on Linux, macOS, or Windows when they want to run a store without Docker. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Linux and macOS flow asks the user to download and execute a remote installer that can create a background service. <br>
Mitigation: Install only if the user trusts Mobazha and get.mobazha.org, review the installer script before execution, and use --no-start when a background service should not be started immediately. <br>
Risk: Uninstall or purge commands can affect local store data. <br>
Mitigation: Back up store data before uninstalling or running purge commands. <br>


## Reference(s): <br>
- [Mobazha Self-Host Guide](https://mobazha.org/self-host) <br>
- [Mobazha Downloads](https://mobazha.org/download) <br>
- [Mobazha Installer](https://get.mobazha.org/install) <br>
- [ClawHub Skill Page](https://clawhub.ai/fengzie/mobazha-native-install) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and step-by-step installation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes platform-specific install, service management, backup, uninstall, and troubleshooting commands.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
