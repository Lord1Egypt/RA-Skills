## Description: <br>
Persistent cloud memory plugin for OpenClaw. This document routes setup, troubleshooting, and uninstall flows and defines config boundaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[c4pt0r](https://clawhub.ai/user/c4pt0r) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users and developers use this skill to install, reconnect, troubleshoot, or uninstall the mem9 cloud memory plugin while keeping credential handling and OpenClaw configuration within documented boundaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles MEM9_API_KEY, a sensitive credential for cloud-backed memory. <br>
Mitigation: Treat MEM9_API_KEY as a secret, paste it only in trusted chat environments, and store it in a password manager or secure vault. <br>
Risk: Using mem9 sends OpenClaw memory activity to the mem9 cloud service. <br>
Mitigation: Review the dry-run configuration changes before approval and do not use this skill if cloud-backed memory is not intended. <br>
Risk: Local uninstall removes local mem9 wiring but does not delete remote mem9 data or revoke the API key. <br>
Mitigation: Use the mem9 dashboard or another reviewed account-management workflow for remote data deletion or key revocation. <br>


## Reference(s): <br>
- [mem9 OpenClaw memory homepage](https://mem9.ai/openclaw-memory) <br>
- [ClawHub skill page](https://clawhub.ai/c4pt0r/mem9-ai) <br>
- [mem9 memory dashboard](https://mem9.ai/your-memory/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup, reconnect, troubleshooting, and uninstall guidance for OpenClaw mem9 configuration.] <br>

## Skill Version(s): <br>
1.0.48 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
