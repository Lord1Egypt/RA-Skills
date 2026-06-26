## Description: <br>
Removes the egregore watchdog daemon and its associated files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when they intentionally want to remove an installed egregore watchdog daemon and disable automatic egregore session relaunching on macOS or Linux. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the uninstall steps disables automatic egregore session relaunching. <br>
Mitigation: Use the skill only when you intend to remove the watchdog and no longer rely on automatic relaunching. <br>
Risk: The commands delete watchdog service files, PID files, and logs. <br>
Mitigation: Review the listed paths and run only the platform-specific removal commands that match the target system. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-egregore-uninstall-watchdog) <br>
- [Egregore plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/egregore) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes macOS launchd and Linux systemd uninstall paths and verification commands.] <br>

## Skill Version(s): <br>
1.9.12 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
