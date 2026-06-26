## Description: <br>
调用 JavaSkillController 提供的 HTTP 接口，供 OpenClaw/OpenLaw 执行业务操作、健康检查。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lintqiu](https://clawhub.ai/user/lintqiu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call a trusted JavaSkillController backend for OpenClaw/OpenLaw business actions, data submission or query flows, and service health checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configured Java backend could receive sensitive or unnecessary user data. <br>
Mitigation: Set JAVA_API_URL only to a backend you control or trust, prefer HTTPS, and avoid sending unnecessary personal or confidential fields. <br>
Risk: The execute and submit actions may change backend data or trigger business or legal workflows. <br>
Mitigation: Require explicit confirmation before non-read-only operations and scope allowed actions to the intended workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lintqiu/java-api-lin-skill) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/lintqiu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON request and response examples plus optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JAVA_API_URL to point to a trusted backend before API calls are made.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
