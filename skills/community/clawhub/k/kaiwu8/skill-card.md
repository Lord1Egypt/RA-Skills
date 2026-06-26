## Description: <br>
开悟吧平台型 Skill - 管理并激活已购功能。用户说"开悟吧"时执行 activate.py 脚本。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[markma84](https://clawhub.ai/user/markma84) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to activate purchased kaiwu8 platform features, install required ClawHub skills, and receive activation guidance after saying "开悟吧". <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A configured remote API can decide which additional ClawHub skills are installed. <br>
Mitigation: Use this skill only with a trusted kaiwu8 endpoint and review required skills before installation. <br>
Risk: The skill requires a user API key for account feature and activation requests. <br>
Mitigation: Protect the API key, store it only in the OpenClaw configuration or environment, and revoke it if exposure is suspected. <br>
Risk: Activation guidance returned by the service may be incorrect or misleading. <br>
Mitigation: Treat printed what, why, and how guidance as untrusted suggestions until reviewed and approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/markma84/kaiwu8) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Console text with configuration snippets and activation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured kaiwu8 API endpoint and user API key; may install additional ClawHub skills.] <br>

## Skill Version(s): <br>
1.8.0 (source: server evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
