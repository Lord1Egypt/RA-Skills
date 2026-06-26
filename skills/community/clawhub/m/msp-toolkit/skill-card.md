## Description: <br>
Provides IT MSP tools for Azure/M365 audits, NPU monitoring, and firewall, SSH, update, and system health checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phibuc87](https://clawhub.ai/user/phibuc87) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, IT operators, and MSP teams use this skill for Azure/M365 status checks, endpoint health review, NPU monitoring, and firewall, SSH, update, and reboot-related workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence marks the release as suspicious because setup instructions publish a local skill path instead of installing or running the advertised MSP tools. <br>
Mitigation: Do not run the publish command unless intentionally publishing under your own ClawHub account; request a complete package with the referenced MSP scripts and clear run instructions. <br>
Risk: The artifact references a reboot script and MSP scripts that are not included in the package. <br>
Mitigation: Review the complete scripts before use, especially any reboot action, and run them only in an approved maintenance context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/phibuc87/msp-toolkit) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/phibuc87) <br>
- [Artifact skill file](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and file references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The artifact references external MSP scripts and a publish command, but the provided package contains only the skill description.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
