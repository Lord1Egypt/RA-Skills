## Description: <br>
Automates QR-code login for the Kuaishou Creator Platform, returns a scannable QR screenshot, monitors login status, and reports success or timeout. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[action2227](https://clawhub.ai/user/action2227) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users who need an agent-assisted browser workflow can use this skill to initiate Kuaishou Creator Platform QR-code login, receive the QR code for scanning, and get a final login status with screenshot evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Returned QR-code images and post-login screenshots may expose sensitive login material or account information. <br>
Mitigation: Treat screenshots like temporary credentials, avoid sharing or recording them, and use the skill only in trusted workspaces. <br>
Risk: A login prompt may remain active if the workflow is abandoned or times out. <br>
Mitigation: Close or expire unused login prompts when finished and retry with a fresh QR code if the login times out. <br>


## Reference(s): <br>
- [Kuaishou Creator Platform](https://creator.kuaishou.com/) <br>
- [ClawHub skill page](https://clawhub.ai/action2227/kuaishou-login) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Screenshots, Guidance] <br>
**Output Format:** [Plain text status messages with browser screenshots] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns QR-code and post-login screenshots; waits up to about 120 seconds before reporting timeout.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
