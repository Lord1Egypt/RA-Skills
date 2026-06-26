## Description: <br>
Update OpenClaw to the latest version for npm-installed OpenClaw instances. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jchen0824](https://clawhub.ai/user/jchen0824) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to check for OpenClaw updates, upgrade npm-installed OpenClaw, restart the gateway, and verify the installed version. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can replace a global OpenClaw installation. <br>
Mitigation: Confirm the intended OpenClaw version and review the npm release source before running update commands. <br>
Risk: The skill restarts the OpenClaw gateway and may cause downtime. <br>
Mitigation: Run it during an acceptable maintenance window and verify gateway health after restart. <br>
Risk: Troubleshooting guidance mentions sudo for global npm installation. <br>
Mitigation: Avoid sudo unless the package, environment, and permission model are fully trusted. <br>


## Reference(s): <br>
- [OpenClaw Self-Update ClawHub listing](https://clawhub.ai/jchen0824/openclaw-self-update) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with bash commands and an optional shell script workflow] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute npm global installation and OpenClaw gateway restart commands when followed by an agent or operator.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
