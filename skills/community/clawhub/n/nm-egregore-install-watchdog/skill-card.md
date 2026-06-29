## Description: <br>
Installs an egregore watchdog daemon via launchd or systemd for autonomous relaunching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill after initializing or setting up an egregore project when they want a user-level watchdog to relaunch egregore sessions automatically. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs a persistent user-level watchdog that relaunches egregore in the background. <br>
Mitigation: Use it only when autonomous relaunching is intended, confirm the launchd or systemd user service path, and keep the documented uninstall command available. <br>
Risk: Installer scripts modify user scheduler configuration. <br>
Mitigation: Inspect the referenced installer script before execution and verify the installed scheduler entry and log location after installation. <br>


## Reference(s): <br>
- [Egregore plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/egregore) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and verification guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes OS-specific launchd or systemd installation, verification, logging, troubleshooting, and uninstall guidance.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata; artifact frontmatter says 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
