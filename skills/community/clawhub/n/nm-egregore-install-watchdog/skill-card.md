## Description: <br>
Installs an egregore watchdog daemon via launchd or systemd for autonomous relaunching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill after initializing an egregore project or setting up a new machine when they want OS-native background relaunching for egregore sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The watchdog runs in the background and can automatically relaunch egregore sessions every 5 minutes. <br>
Mitigation: Install it only when automatic relaunching is desired, inspect the scheduler logs after installation, and use the uninstall skill to return to manual control. <br>
Risk: The installation commands invoke egregore plugin scripts through launchd or systemd. <br>
Mitigation: Confirm the referenced plugin scripts come from a trusted source before installation. <br>


## Reference(s): <br>
- [Egregore plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/egregore) <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-egregore-install-watchdog) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline bash commands and installation checks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides installation of a background watchdog using launchd on macOS or systemd on Linux.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
