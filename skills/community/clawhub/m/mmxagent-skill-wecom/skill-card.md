## Description: <br>
Connects OpenClaw to WeCom by generating an authorization link, waiting for user confirmation, polling the authorization result, and writing the resulting bot credentials to OpenClaw configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oreoandyuumi](https://clawhub.ai/user/oreoandyuumi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and operators use this skill to bind a WeCom bot to OpenClaw when they need WeCom messaging integration. The skill guides the user through sharing an authorization link in WeCom, confirming completion, and applying the resulting bot configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores a WeCom bot secret in ~/.openclaw/openclaw.json. <br>
Mitigation: Keep the OpenClaw configuration file private and rotate the WeCom bot secret if the file is exposed. <br>
Risk: The skill restarts the OpenClaw gateway after successful authorization. <br>
Mitigation: Run the skill only when intentionally connecting OpenClaw to WeCom and expect a gateway restart after credentials are written. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oreoandyuumi/mmxagent-skill-wecom) <br>
- [WeCom authorization link generation endpoint](https://work.weixin.qq.com/ai/qc/generate?source=wecom-cli&plat=3) <br>
- [WeCom authorization result polling endpoint](https://work.weixin.qq.com/ai/qc/query_result?scode=<scode>) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell command examples and configuration key paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user confirmation before polling; stores WeCom bot credentials locally and restarts the OpenClaw gateway after authorization.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
