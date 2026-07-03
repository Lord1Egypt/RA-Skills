## Description: <br>
Profile Model Manager helps agents inspect, switch, and batch-manage Hermes profile model settings for primary, auxiliary, and delegation models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[youbuwei](https://clawhub.ai/user/youbuwei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Hermes users use this skill to review current model and provider settings, plan or apply single-profile and batch model changes, and verify gateway restarts after configuration updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide persistent Hermes profile changes, including bulk provider and model updates. <br>
Mitigation: Review commands before running apply actions, preview changes when possible, and back up profile configuration before bulk changes. <br>
Risk: Troubleshooting may involve API key environment files, which can expose secrets if real values are printed into chat or logs. <br>
Mitigation: Avoid sharing real .env contents, redact key values during troubleshooting, and add API keys through a safer secret-management path. <br>
Risk: Model switches may not take effect until the affected Hermes gateway is restarted. <br>
Mitigation: Restart the relevant gateway and run the documented configuration, chat, and gateway-status verification checks after changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/youbuwei/hermes-profile-model-manager) <br>
- [Server-resolved source repository](https://github.com/youbuwei/hermes-profile-model-manager) <br>
- [BigModel model overview](https://docs.bigmodel.cn/cn/guide/start/model-overview) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash and YAML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes preview, apply, restart, troubleshooting, and verification workflows for Hermes profile model configuration.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata; artifact frontmatter version 2.1.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
