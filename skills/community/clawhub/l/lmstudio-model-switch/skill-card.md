## Description: <br>
Switches AI models on the fly between local LM Studio and cloud Kimi API in OpenClaw with simple commands and automatic gateway restart. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Endihunn](https://clawhub.ai/user/Endihunn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers using OpenClaw use this skill to switch between local LM Studio models and the Kimi API for privacy, quality, reliability, or GPU usage tradeoffs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API mode routes work to a cloud provider. <br>
Mitigation: Use local mode for secrets, credentials, proprietary code, regulated data, or other sensitive work. <br>
Risk: Switching models changes OpenClaw configuration and restarts the gateway briefly. <br>
Mitigation: Expect openclaw.json to be backed up and modified, then verify the active model after the gateway restarts. <br>
Risk: The artifact text includes a placeholder repository URL. <br>
Mitigation: Install from the real ClawHub artifact or another trusted source. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Endihunn/lmstudio-model-switch) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style command guidance and status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may update openclaw.json and briefly restart the OpenClaw gateway.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
