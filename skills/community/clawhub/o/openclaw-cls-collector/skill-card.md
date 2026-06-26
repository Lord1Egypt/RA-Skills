## Description: <br>
Deploys OpenClaw observability data collection to Tencent Cloud CLS and returns a dashboard link. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[trumphuang](https://clawhub.ai/user/trumphuang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to set up OpenClaw observability collection with Tencent Cloud CLS, configure region and credentials, and obtain a dashboard link after deployment. <br>

### Deployment Geography for Use: <br>
Global, subject to Tencent Cloud CLS regional availability. <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to collect Tencent Cloud credentials for CLS setup. <br>
Mitigation: Use a dedicated least-privilege or temporary Tencent Cloud credential and avoid sharing broad account keys in chat. <br>
Risk: The deployment flow runs a downloaded Tencent-hosted installer without an integrity check in the artifact instructions. <br>
Mitigation: Verify the installer through a trusted Tencent source before running it. <br>
Risk: The deployment can create or modify CLS resources and install or configure collection components. <br>
Mitigation: Confirm how to stop the collector and delete or adjust created CLS resources before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/trumphuang/openclaw-cls-collector) <br>
- [Tencent Cloud CAM API key console](https://console.cloud.tencent.com/cam/capi) <br>
- [Tencent Cloud OpenClaw CLS installer](https://mirrors.tencent.com/install/cls/openclaw/setup.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline bash commands and a dashboard URL] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Collects SecretId, SecretKey, and region before deployment; returns a Tencent Cloud CLS dashboard link after setup.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
