## Description: <br>
OpenClaw飞书问题排查 helps users troubleshoot Feishu plugin issues with an FAQ and /feishu doctor diagnostic guidance for app permissions, API connectivity, and user authorization state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenfa188](https://clawhub.ai/user/chenfa188) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and administrators who manage an OpenClaw Feishu app use this skill to resolve card callback and permission or authorization problems and to decide when to run /feishu doctor for deeper diagnostics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diagnostic reports may reveal Feishu app configuration, bot identity, permission gaps, and authorization state, even when secrets are masked. <br>
Mitigation: Use the diagnostic guidance only when administering or helping troubleshoot the relevant Feishu app, and handle generated reports as sensitive operational information. <br>


## Reference(s): <br>
- [Feishu Open Platform App Console](https://open.feishu.cn/app) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration] <br>
**Output Format:** [Markdown troubleshooting guidance with Feishu configuration steps and slash command instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Diagnostic reports should be treated as sensitive because they can expose app configuration, bot identity, permission gaps, and authorization state.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
