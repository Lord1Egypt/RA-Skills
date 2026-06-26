## Description: <br>
Diagnoses, repairs, and documents OpenClaw gateway issues for main and vesper profiles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[siraustin](https://clawhub.ai/user/siraustin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to triage stuck, crash-looping, unresponsive, or unauthorized OpenClaw gateways, apply local fixes, and write an incident report after remediation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants broad local repair authority that can restart services, remove locks, edit configuration, or reset session state. <br>
Mitigation: Require confirmation of exact files, profiles, ports, and process IDs before deleting, killing, pruning, or rewriting anything, and back up config and session files first. <br>
Risk: Triage may inspect logs, environment variables, and auth profile files that can expose token or credential values. <br>
Mitigation: Mask secrets before displaying command output and avoid printing raw token, password, refresh token, or API key values. <br>
Risk: Incorrect profile or LaunchAgent changes can disrupt main and vesper gateways. <br>
Mitigation: Verify plist alignment, state directories, ports, and profile names before restarting gateways, then record the final changes in the incident report. <br>


## Reference(s): <br>
- [OpenClaw DX on ClawHub](https://clawhub.ai/siraustin/openclaw-dx) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown with shell commands and an incident report template] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include file paths, process IDs, config changes, restart steps, and incident report content.] <br>

## Skill Version(s): <br>
1.9.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
