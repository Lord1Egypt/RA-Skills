## Description: <br>
Installs, deploys, and manages Hermes Agent and hermes-webui on Windows, including startup, background operation, updates, status checks, and troubleshooting guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwardwason](https://clawhub.ai/user/edwardwason) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Windows users and developers use this skill to install and manage the Hermes Agent and hermes-webui through PowerShell and WSL2 setup guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package describes privileged startup, background, update, and uninstall scripts that were not included in the reviewed artifact. <br>
Mitigation: Inspect and trust the PowerShell scripts from the claimed source before running them, and confirm scheduled task, persistence, and update behavior are acceptable. <br>
Risk: The workflow may store API keys in WSL and uses uninstall or reinstall commands that can affect local Hermes data. <br>
Mitigation: Review where secrets are stored, secure the Windows account and WSL environment, and back up Hermes data before reinstalling or uninstalling. <br>


## Reference(s): <br>
- [hermes-for-win reference documentation](references/README.md) <br>
- [ClawHub skill page](https://clawhub.ai/edwardwason/hermes-for-win) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with PowerShell commands and setup instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Targets Windows 10/11 with WSL2 and Ubuntu.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
