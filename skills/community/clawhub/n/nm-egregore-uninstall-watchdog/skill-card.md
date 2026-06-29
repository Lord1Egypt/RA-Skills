## Description: <br>
Removes the egregore watchdog daemon and its associated files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to stop automatic egregore session relaunching and remove the watchdog service when retiring or switching away from daemon mode. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The uninstall guidance removes launchd or systemd units and local watchdog files, so running commands against the wrong paths could remove unintended files or leave automation partially configured. <br>
Mitigation: Review the listed paths before execution and run the included verification commands for the local operating system after removal. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-egregore-uninstall-watchdog) <br>
- [Egregore homepage](https://github.com/athola/claude-night-market/tree/master/plugins/egregore) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes OS-specific macOS launchd and Linux systemd removal and verification commands.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata; artifact frontmatter reports 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
