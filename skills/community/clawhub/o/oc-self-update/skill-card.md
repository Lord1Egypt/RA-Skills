## Description: <br>
Check for OpenClaw updates and self-update the installation when the user asks to update OpenClaw, check for updates, upgrade the bot, install a new version, or use a newly available release. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spideystreet](https://clawhub.ai/user/spideystreet) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External OpenClaw users and developers use this skill to check the globally installed OpenClaw package, compare it with npm's latest release, and apply a selected update channel after confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change the globally installed OpenClaw package. <br>
Mitigation: Confirm the user's intended update channel before installation and prefer the stable channel unless the user intentionally requests beta or dev. <br>
Risk: An update does not take effect until the OpenClaw gateway restarts. <br>
Mitigation: After a successful install, tell the user that a manual gateway restart is required and do not restart it automatically. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/spideystreet/oc-self-update) <br>
- [README](README.md) <br>
- [Changelog](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires npm and user confirmation before changing the global OpenClaw package; a manual gateway restart is required after update.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence and CHANGELOG.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
