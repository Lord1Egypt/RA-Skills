## Description: <br>
Controls Clash for Windows proxy state by starting or stopping proxy routing, checking status, and switching nodes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[IceNoodle](https://clawhub.ai/user/IceNoodle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users who run Clash for Windows use this skill to let an agent inspect and change local proxy routing state through the Clash external controller. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change local proxy routing from broad proxy-control commands without a separate confirmation step. <br>
Mitigation: Use explicit Clash-specific commands and review whether agent-driven proxy changes are appropriate before deployment. <br>
Risk: The artifact includes a hardcoded Clash external-controller secret. <br>
Mitigation: Replace the hardcoded secret with a private local configuration value before use. <br>
Risk: The documented Clash configuration includes allow-lan, which can expose proxy access beyond the local machine if enabled carelessly. <br>
Mitigation: Avoid enabling allow-lan unless the network exposure is intended and controlled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/IceNoodle/openclaw-clash-forwindows-controller) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Plain text status and action-result messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may report current Clash status, selected node, success, or failure after local proxy-control actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
